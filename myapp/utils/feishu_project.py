import ast

import requests
import json
import time
from datetime import datetime, timezone
from dateutil.parser import parse
from concurrent.futures import ThreadPoolExecutor, as_completed
from myapp.utils.feishu_data import Feishu_data
from myapp.utils.feishu_get_token import get_plugin_access_token, get_tenant_access_token
from myapp.utils.feishu_send_message import start_send

fei = Feishu_data()

feishu_project_head = {
    "X-PLUGIN-TOKEN": f"{get_plugin_access_token()}",
    'Content-Type': 'application/json',
    'X-USER-KEY': '7117238460611624964',
    "plugin_token": f"{get_plugin_access_token()}"
}

feishu_backend_head = fei.content_type1
feishu_backend_head['Authorization'] = f"Bearer {get_tenant_access_token()}"

THREADS = 3  # 控制并发线程数
MAX_RETRIES = 5  # 最大重试次数


def get_field_all():
    """
    :return: 获取指定空间或工作项类型（推荐）下所有“字段”的基础信息
    """
    project_key = '62a6fce5ed2541be7bf5c2d3'
    url = f'{fei.feishu_project_url}{project_key}/field/all'
    payload = json.dumps({
        "work_item_type_key": "version"
    })
    response = requests.post(url=url, headers=feishu_project_head, data=payload)
    print(response.json()['data'])


def get_zero_timestamp_ms_from_int(date_int: int) -> int:
    dt = datetime.strptime(str(date_int), "%Y%m%d")
    return int(dt.timestamp() * 1000)


def get_business_key():
    url = f"{fei.feishu_project_url}projects"
    payload = json.dumps({
        "user_key": "7117238460611624964",
        "tenant_group_id": 0,
        "asset_key": "",
        "order": [""]
    })
    business = requests.post(url, headers=feishu_project_head, data=payload)
    return business.json()['data'][0]


def get_demand_finished_list(date, uid=None, finished_time=None):
    headers = feishu_project_head
    project_key = '62a6fce5ed2541be7bf5c2d3'
    url = f"{fei.feishu_project_url}{project_key}/work_item/story/search/params"
    search_params = [
        {"param_key": "work_item_status", "value": ["end"], "operator": "="}
    ]
    if date:
        search_params.append(
            {"param_key": "finish_time", "value": get_zero_timestamp_ms_from_int(date), "operator": ">="})
    if uid:
        search_params.append({
            "param_key": "role_owners",
            "value": [{"role": "qa", "owners": [f'{uid}']}],
            "operator": "HAS ANY OF"
        })
    if finished_time:
        search_params.append(
            {"param_key": "finish_time", "value": get_zero_timestamp_ms_from_int(finished_time), "operator": "<="})
    return _paged_post(url, headers, search_params)


def get_demand_progress_list(uid=None):
    headers = feishu_project_head
    project_key = '62a6fce5ed2541be7bf5c2d3'
    url = f"{fei.feishu_project_url}{project_key}/work_item/story/search/params"
    search_params = [
        {"param_key": "work_item_status", "value": ["end"], "operator": "!="},
        {"param_key": "created_at", "value": 1735660800000, "operator": ">"}
    ]
    if uid:
        search_params.insert(1, {
            "param_key": "role_owners",
            "value": [{"role": "qa", "owners": [f'{uid}']}],
            "operator": "HAS ANY OF"
        })
    return _paged_post(url, headers, search_params)


def _paged_post(url, headers, search_params):
    all_items = []
    page_num, page_size = 1, 50
    while True:
        payload = json.dumps({
            "page_size": page_size,
            "page_num": page_num,
            "search_group": {
                "conjunction": "AND",
                "search_params": search_params
            },
            "expand": {"need_workflow": True}
        })
        resp = requests.post(url, headers=headers, data=payload)
        if resp.status_code != 200:
            print(f"请求失败: {resp.status_code}, {resp.text}")
            break
        data_list = resp.json().get('data', [])
        if not data_list:
            break
        all_items.extend(data_list)
        if len(data_list) < page_size:
            break
        page_num += 1
    return all_items


def get_workflow_with_retry(story_id, project_key, headers):
    url = f"https://project.feishu.cn/open_api/62a6fce5ed2541be7bf5c2d3/work_item/story/{story_id}/workflow/query"
    payload = json.dumps({"flow_type": 0})
    retries, backoff = 0, 1
    while retries < MAX_RETRIES:
        try:
            resp = requests.post(url, headers=headers, data=payload, timeout=10)
            if resp.status_code == 200:
                return resp.json()['data']
            elif resp.status_code == 429:
                print(f"限流 story_id={story_id}，等待 {backoff}s 重试...")
                time.sleep(backoff)
                retries += 1
                backoff *= 2
            else:
                print(f"失败 {story_id}: {resp.status_code}, {resp.text}")
                return None
        except requests.RequestException as e:
            print(f"异常 {story_id}: {e}, 重试中...")
            time.sleep(backoff)
            retries += 1
            backoff *= 2
    print(f"{story_id} 重试失败，跳过")
    return None


def batch_get_workflows(story_ids, project_key, headers):
    results = []
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = {executor.submit(get_workflow_with_retry, sid, project_key, headers): sid for sid in story_ids}
        for future in as_completed(futures):
            sid = futures[future]
            data = future.result()
            if data:
                results.append((sid, data))
    return results


def calculate_points_if_has_test_stage(data):
    target_names = [
        "Android端开发", "iOS端开发", "流媒体开发", "测试阶段", "Web前端开发",
        "Web后端开发", "主服务端开发", "互娱端开发", "游戏后端", "游戏前端", "曲库开发", "音视频开发", "大数据端开发",
        "算法端开发", "运维端开发", "用例设计"
    ]
    points_result = {}

    for node in data.get("workflow_nodes", []):
        name = node.get("name", "")
        if name in target_names:
            total_points = sum(s.get("points", 0) for s in node.get("schedules", []))
            points_result[name] = total_points

            if name == "测试阶段":
                # 插入测试阶段的 owners 到 qa 字段
                points_result["qa"] = node.get("owners", [])

    return points_result


def get_items_node(date, uid, date_type, finished_time):
    project_key = '62a6fce5ed2541be7bf5c2d3'
    if date_type == "person_finished_data":
        node_list = get_demand_finished_list(date, uid, finished_time)
        node_list = filter_data_list2(node_list, str(date))
    else:
        node_list = get_demand_progress_list(uid)
        node_list = filter_data_list(node_list)
    story_ids = [item['id'] for item in node_list]
    workflow_data_list = batch_get_workflows(story_ids, project_key, feishu_project_head)
    result = []
    for sid, data in workflow_data_list:
        points = calculate_points_if_has_test_stage(data)
        # if points:
        #     name = next((item['name'] for item in node_list if item['id'] == sid), "")
        #     result.append({"需求id": sid, "需求名称name": name, "单个需求数据data": points})

        if points:
            name = next((item['name'] for item in node_list if item['id'] == sid), "")
            result.append({
                "需求id": sid,
                "需求名称name": name,
                "单个需求数据data": points,
            })
    return result


def filter_data_list(data_list):
    """
    遍历数据列表，保留那些 '测试阶段' 节点 actual_finish_time 为空的数据。
    :param data_list: work item 数据的列表
    :return: 过滤后的列表
    """
    filtered_list = []
    for item in data_list:
        nodes = item.get("workflow_infos", {}).get("workflow_nodes", [])
        # 找到名字是“测试阶段”的节点
        test_stage_node = next((node for node in nodes if node.get("name") == "测试阶段"), None)
        # 如果没有该节点，或该节点 actual_finish_time 为空，保留
        if test_stage_node is None or not test_stage_node.get("actual_finish_time"):
            filtered_list.append(item)
    return filtered_list


def filter_data_list2(data_list, cutoff_str):
    cutoff = datetime.strptime(cutoff_str, "%Y%m%d").replace(tzinfo=timezone.utc)
    filtered_list = []

    for item in data_list:
        nodes = item.get("workflow_infos", {}).get("workflow_nodes", [])
        test_stage_node = next((node for node in nodes if node.get("name") == "测试阶段"), None)

        if test_stage_node:
            actual_finish_time = test_stage_node.get("actual_finish_time")
            if actual_finish_time:
                try:
                    finish_dt = parse(actual_finish_time)
                    if finish_dt >= cutoff:
                        filtered_list.append(item)
                except Exception as e:
                    print(f"解析时间失败: {actual_finish_time}, 错误: {e}")
                    # 可选择忽略或保留
            else:
                filtered_list.append(item)
        else:
            filtered_list.append(item)

    return filtered_list


def analyze_workload_by_version(data_list, types, date, finished_time):
    test_key = "测试阶段"
    version_keys = {
        "Android端开发", "iOS端开发", "流媒体开发", "主服务端开发", "互娱端开发", "曲库开发", "音视频开发",
        "大数据端开发", "算法端开发",
    }

    Lack_of_time = []
    attention_records = []
    version_demands = []
    non_version_demands = []
    for item in data_list:
        test_case = 0
        stages = item["单个需求数据data"]
        if test_key not in stages:
            continue

        test = stages.get(test_key, 0)
        if stages.get("用例设计", 0):
            test_case = stages.get("用例设计", 0)

        # 提取开发阶段字段（除“测试阶段”和“qa”）
        dev_stages = {k: v for k, v in stages.items() if k not in (test_key, 'qa', "用例设计")}

        # ✅ 如果有任意一个开发阶段没填（是 0、None、''），就跳过
        if any(v in (0, None, '', [], {}) for v in dev_stages.values()):
            continue

        develop = sum(dev_stages.values())

        # 分类版本需求
        if any(k in stages for k in version_keys):
            version_demands.append(item)
        else:
            non_version_demands.append(item)

        # 测试时间为 0 时提醒
        if develop == 0:
            continue
        elif test == 0:
            Lack_of_time.append(
                f"负责人{get_user_name(stages.get('qa', ''))},需求名称: {item['需求名称name']} 测试时间为0，请注意填写！！！"
                f"https://project.feishu.cn/wangmao12345678/story/detail/{item['需求id']}?"
                f"parentUrl=%2Fwangmao12345678%2Fstory%2Fhomepage&openScene=4"
            )
        else:
            ratio = round(develop / (test + test_case), 3)
            if ratio < 3:
                if test_case ==0:
                    case_issues_result= "用例不占排期"
                else:
                    case_issues = test / test_case
                    if case_issues > 0.25:
                        case_issues_result = "测试用例估期较高请注意"
                    else:
                        case_issues_result = "测试用例估期正常"
                attention_records.append({
                    '负责人': stages.get('qa', ''),
                    "需求id": item['需求id'],
                    "需求名称": item['需求名称name'],
                    "测试": test,
                    "研发": develop,
                    "测试用例": test_case,
                    "比": ratio,
                    "需求链接": f"https://project.feishu.cn/wangmao12345678/story/detail/{item['需求id']}?"
                                f"parentUrl=%2Fwangmao12345678%2Fstory%2Fhomepage&openScene=4",
                    "用例设计": case_issues_result
                })

    # 排序 attention_records 按比值从小到大
    sorted_attention = sorted(attention_records, key=lambda x: x['比'])

    # 构造传给接口的消息列表
    attention_messages = [
        f"{rec['需求名称']}。{get_user_name(rec['负责人'])}。测试: {rec['测试']}, " \
        f"研发: {rec['研发']},测试用例：{rec['测试用例']}。{rec['比']}。{rec['需求链接']}。{rec['用例设计']}"
        for rec in sorted_attention
    ]
    # 调用接口发送提醒
    if Lack_of_time:
        start_send(function='Testing_and_Development1', datas=Lack_of_time)
    if attention_messages:
        for data in attention_messages:
            start_record(data, types)
        attention_messages.append(date)
        attention_messages.append(finished_time)
        attention_messages.append(types)
        start_send(function='Testing_and_Development', datas=attention_messages)

    # 聚合统计函数
    def compute_totals(demands):
        test_total = sum(item["单个需求数据data"].get(test_key, 0) for item in demands)
        dev_total = sum(
            sum(v for k, v in item["单个需求数据data"].items() if k != test_key and k != 'qa') for item in demands
        )
        ratio = round(dev_total / test_total, 3) if test_total else "0"
        return test_total, dev_total, ratio

    v_test, v_dev, v_ratio = compute_totals(version_demands)
    nv_test, nv_dev, nv_ratio = compute_totals(non_version_demands)

    return {
        "版本需求": {"数量": len(version_demands), "测试总时间": v_test, "研发总时间": v_dev, "研发/测试比值": v_ratio},
        "非版本需求": {"数量": len(non_version_demands), "测试总时间": nv_test, "研发总时间": nv_dev,
                       "研发/测试比值": nv_ratio},
        "总需求数": {
            "数量": len(version_demands) + len(non_version_demands),
            "测试总时间": v_test + nv_test,
            "研发总时间": v_dev + nv_dev,
            "研发/测试比值": round((v_dev + nv_dev) / (v_test + nv_test), 3) if (v_test + nv_test) else "0"
        }
    }


def get_user_name(uid_list):
    """
    :param uid_list:
    :return: 获取用户列表
    """
    u_list = []
    for uid in uid_list:
        uname = fei.qa_list[0][int(uid)]
        u_list.append(uname)
    return u_list


def get_check(date, uid, date_type, finished_time):
    return analyze_workload_by_version(get_items_node(date, uid, date_type, finished_time), date_type, date,
                                       finished_time)


def send_feishu_card(datas):
    url = fei.feishu_card_url
    headers = feishu_backend_head
    payload = fei.feishu_card
    for i in range(len(datas)):
        payload['receive_id'] = datas[i]
        requests.request("POST", url, headers=headers, data=json.dumps(payload))


def start_record(data, types):
    """
    启动记录
    :return:
    """
    url = ""
    headers = feishu_backend_head
    if types == 'person_incomplete_data':
        url = fei.feishu_record_cloud_document
    elif types == 'person_finished_data':
        url = fei.feishu_record_finished_cloud_document
    datas = data.split("。")
    user_list = ast.literal_eval(datas[1])

    payload = json.dumps({
        "fields": {
            "测试研发数据": datas[2],
            "负责人": [
                {"id": str(open_id)} for open_id in user_list
            ],
            "需求": datas[0],
            "用例结论": datas[5],
            "测试研发比结果": datas[3],
            "需求链接": {
                "text": datas[0],
                "link": datas[4]
            },
        }
    })
    requests.request("POST", url, headers=headers, data=payload)
    # send_feishu_card(user_list)


if __name__ == '__main__':
    # get_user_name([7205168573025697794, 7212971331053240348])

    # result = get_check(20250601, uid=None, date_type='person_incomplete_data', finished_time=20250630)
    # print(get_check(20250601, uid=None, date_type='person_finished_data'))
    print(get_check(20250601, 7117238460611624964, 'person_finished_data', finished_time=None))
    # print(get_check(None, uid=None, date_type='person_incomplete_data', finished_time=None))
    # print(json.dumps(result, indent=2, ensure_ascii=False))
