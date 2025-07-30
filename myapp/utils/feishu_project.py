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
from collections import defaultdict

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
        "work_item_type_key": "story"
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
    """
    :param date: 开始时间
    :param uid: 指定用户
    :param finished_time: 完成时间
    :return: 返回阶段时间内所有已完成的测试数据
    """
    headers = feishu_project_head
    project_key = '62a6fce5ed2541be7bf5c2d3'
    url = f"{fei.feishu_project_url}{project_key}/work_item/story/search/params"
    search_params = [
        {
            "param_key": "all_states",
            "value": ["测试阶段"],
            "operator": "HAS ANY OF"
        }
    ]
    if date:
        search_params.append(
            {
                "param_key": "feature_state_time",
                "value": {
                    "state_name": "测试阶段",
                    "state_timestamp": get_zero_timestamp_ms_from_int(date),
                    "state_condition": 1},
                "operator": ">="
            })
    else:
        search_params.append(
            {
                "param_key": "feature_state_time",
                "value": {
                    "state_name": "测试阶段",
                    "state_timestamp": 1735660800000,
                    "state_condition": 1},
                "operator": ">="
            })
    if uid:
        search_params.append({
            "param_key": "role_owners",
            "value": [{"role": "qa", "owners": [f'{uid}']}],
            "operator": "HAS ANY OF"
        })
    if finished_time:
        search_params.append(
            {
                "param_key": "feature_state_time",
                "value": {
                    "state_name": "测试阶段",
                    "state_timestamp": get_zero_timestamp_ms_from_int(finished_time),
                    "state_condition": 1},
                "operator": "<="
            })
    return _paged_post(url, headers, search_params)


def get_demand_progress_list(uid=None):
    """
    :param uid: 可传指定用户指定用户
    :return: 返回测试阶段内所有已完成的测试数据
    """
    headers = feishu_project_head
    project_key = '62a6fce5ed2541be7bf5c2d3'
    url = f"{fei.feishu_project_url}{project_key}/work_item/story/search/params"
    search_params = [
        {"param_key": "work_item_status", "value": ["end"], "operator": "!="},
        {"param_key": "created_at", "value": 1735660800000, "operator": ">="},
        {
            "param_key": "all_states",
            "value": ["测试阶段"],
            "operator": "HAS ANY OF"
        }
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
        # node_list = filter_data_list2(node_list, str(date))
    else:
        node_list = get_demand_progress_list(uid)
        # node_list = filter_data_list(node_list)
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
    """
    :param data_list:
    :param cutoff_str:
    :return:
    """
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
    """
    :param data_list:
    :param types:
    :param date: 测试开始时间
    :param finished_time: 需求结束节点时间
    :return: 处理所有测试研发比十五
    """
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
                f"负责人{get_user_name(stages.get('qa', ''), 1)},需求名称: {item['需求名称name']} 测试时间为0，请注意填写！！！"
                f"https://project.feishu.cn/wangmao12345678/story/detail/{item['需求id']}?"
                f"parentUrl=%2Fwangmao12345678%2Fstory%2Fhomepage&openScene=4"
            )
        else:
            ratio = round(develop / (test + test_case), 3)
            if ratio < 3:
                if test_case == 0:
                    case_issues_result = ""
                else:
                    case_issues = test_case / test
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
        f"{rec['需求名称']}。{get_user_name(rec['负责人'], 1)}。测试: {rec['测试']}, " \
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


def get_user_name(uid_list, nums):
    """
    :param nums: 选择情况
    :param uid_list:
    :return: 获取用户列表
    """
    u_list = []
    for uid in uid_list:
        if nums == 1:
            uname = fei.qa_list[int(uid)][0]
            u_list.append(uname)

        elif nums == 2:
            uname = fei.qa_list[int(uid)][1]
            u_list.append(uname)
    return u_list


def get_check(date, uid, date_type, finished_time):
    return analyze_workload_by_version(get_items_node(date, uid, date_type, finished_time), date_type, date,
                                       finished_time)


def send_feishu_card(datas):
    """
    :param datas:
    :return: 发送飞书卡片
    """
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


def get_all_user_demand(create_date, uid, finished_time, no_testing=None):
    """
    :return:返回查询数据，根据开始时间和结束时间
    """
    headers = feishu_project_head
    project_key = '62a6fce5ed2541be7bf5c2d3'
    url = f"{fei.feishu_project_url}{project_key}/work_item/story/search/params"

    search_params = [{
        "param_key": "all_states",
        "value": ["测试阶段"],
        "operator": "HAS ANY OF"
        # 用于查询测试用
        # "param_key": "work_item_status",
        # "value": [
        #     "linshihong_3331583830269491"//linshihong_3331583827552071   开发中
        # ],
        # "operator": "HAS ANY OF"
    },
    ]
    if create_date:
        search_params.append({
            "param_key": "feature_state_time",
            "value": {
                "state_name": "测试阶段",
                "state_timestamp": get_zero_timestamp_ms_from_int(create_date),
                "state_condition": 0},
            "operator": ">="
        })
    if uid:
        search_params.append({
            "param_key": "role_owners",
            "value": [{"role": "qa", "owners": [f'{uid}']}],
            "operator": "HAS ANY OF"
        })
    if finished_time:
        search_params.append({
            "param_key": "feature_state_time",
            "value": {
                "state_name": "测试阶段",
                "state_timestamp": get_zero_timestamp_ms_from_int(finished_time),
                "state_condition": 1
            },
            "operator": "<="
        }
        )
    if no_testing:
        search_params.append({
            "param_key": "work_item_status",
            "value": ['sub_stage_1658482927664',
                      'linshihong_3331583830269491',
                      '20avolygh', 'sub_stage_1657610860899', 'end', 'closed'],
            "operator": "HAS NONE OF"
        })
    return _paged_post(url, headers, search_params)


def get_all_user_finished_demand(create_date, uid, finished_time):
    """
    :param create_date: 需求开始时间
    :param uid:
    :param finished_time:
    :return: 返回阶段时间内，用户所有已完成的测试数据，需求承接数
    """
    all_datas = get_all_user_demand(create_date, uid, finished_time)
    all_datas_num = len(all_datas)
    user_test_list = []
    for i in range(len(all_datas)):
        test_list = all_datas[i]['workflow_infos']['workflow_nodes']
        test_name = all_datas[i]['name']
        test_id = all_datas[i]['id']

        test_user = get_test_user(test_list)
        try:
            user_test_list.append({"用户": get_user_name(test_user, 2), "用户id": test_user,
                                   "需求名称": test_name, '需求id': test_id})
        except Exception as e:
            print(f"Error processing item {i}: {e}")
            continue
        # url = f"https://project.feishu.cn/wangmao12345678/story/detail/{test_id}?parentUrl=%2Fwangmao12345678%2Fstory%2Fhomepage&openScene=4"
        # print(url)
    user_data = user_classification_data(user_test_list, all_datas_num)
    return user_data, all_datas_num
    # print(f"本次查询到总需求数量：{all_datas_num}条数据")


def user_classification_data(data, all_datas_num):
    """
    :param all_datas_num: 总需求数量
    :param data: 传入需求数据，每项包含 '用户', '用户id', '需求名称'
    :return: 返回每个用户的需求列表和数量等信息
    """
    user_map = defaultdict(lambda: {"需求列表": [], "user_id": None, "需求id": []})

    for item in data:
        users = item.get('用户', [])
        ids = item.get("用户id", [])
        name = item.get('需求名称', '')
        project_id = item.get('需求id', '')
        if not users:
            # 用户为空则归为“暂无”
            user_map["暂无"]["需求列表"].append(name)
            user_map["暂无"]["user_id"] = "0"
        else:
            for i, user in enumerate(users):
                user_map[user]["需求列表"].append(name)
                user_map[user]["需求id"].append(project_id)
                # 绑定用户id（如果有）
                if i < len(ids):
                    user_map[user]["user_id"] = ids[i]

    user_list = []
    for user, info in user_map.items():
        user_list.append({
            "user": user,
            "user_id": info["user_id"],
            "已承接的需求数量": len(info["需求列表"]),
            "完成需求占比": f"{len(info['需求列表']) / all_datas_num:.2%}" if all_datas_num else "0%",
            "需求列表": info["需求列表"],
            '需求id': info['需求id']
        })
    return user_list


def get_test_user(data):
    """
    :param data:
    :return: 获取测试id
    """
    owners_set = set()
    for item in data:
        if item.get('name') == '测试阶段':
            # 顶层 owners
            if 'owners' in item:
                owners_set.update(item['owners'])

            # node_schedule 内的 owners
            if 'node_schedule' in item and isinstance(item['node_schedule'], dict):
                owners_set.update(item['node_schedule'].get('owners', []))

            # role_assignee 中的 owners
            if 'role_assignee' in item and isinstance(item['role_assignee'], list):
                for ra in item['role_assignee']:
                    owners_set.update(ra.get('owners', []))

            # schedules 中的 owners
            if 'schedules' in item and isinstance(item['schedules'], list):
                for sched in item['schedules']:
                    owners_set.update(sched.get('owners', []))
    return list(owners_set)


def completion_rate(create_date=None, date=None, uid=None, finished_time=None):
    """
    :return: 返回完成率
    """
    finished_demand_data = get_demand_finished_list(date=date, uid=uid, finished_time=finished_time)
    all_demand = get_all_user_demand(uid=uid, finished_time=finished_time, create_date=create_date)
    print(f"查询到总创建需求数量：{len(all_demand)}条数据")
    print(f"查询到已完成需求数量：{len(finished_demand_data)}条数据")
    proportion = len(finished_demand_data) / len(all_demand) if all_demand else 0
    print(f"完成率：{proportion:.2%}")


def get_no_testing_requirements():
    """
    :return: 返回没有安排测试的需求
    """
    all_datas = get_all_user_demand(create_date=None, uid=None, finished_time=None, no_testing=1)
    no_testing_list = []
    for i in range(len(all_datas)):
        test_list = all_datas[i]['workflow_infos']['workflow_nodes']
        test_user = get_test_user(test_list)
        if len(test_user) == 0:
            test_name = all_datas[i]['name']
            test_id = all_datas[i]['id']
            no_testing_list.append(f'{test_name, int(test_id)}')
    # print(no_testing_list)
    # no_testing_list =["('Happyday后台自定义开启优化', 6239798650)", "('巅峰对决-金牌房间', 6238889653)", "('小游戏-slots-埃及宾果', 6237192539)", "('BD直播/语音房账号', 6237187668)", "('使用模板的作品展示改动', 6237043245)", "('周周挑战赛-任务迭代', 6236985358)", "('BD小游戏账号优化3', 6236962343)", "('机审人脸识别需求', 6231928985)", "('OM后台作品信息增加', 6231484534)", "('亲密列表置顶关系新增信物图鉴入口', 6230725039)", "('通用卡片支持显示webp', 6225821388)", "('upay越南地区大额充值渠道接入', 6218367414)", "('抢唱房间恢复-部分大区', 6212061601)", "('房间玩法-数字炸弹', 6212013100)", "('模板展示排序优化', 6211879719)", "('活动循环配置', 6209892226)", "('个人主页 小 Banner 更改设计规范', 6195692927)", "('亲密回忆录', 6195522457)", "('直播活动-美食狂欢吸底逻辑优化', 6195519582)", "('币商协议优化', 6195446729)", "('家族任务荣耀之路资源投放优化', 6192618630)", "('随从增加主属性', 6178279743)", "('溢出碎片转化', 6178271039)", "('审核池排序优化二期（20250611）', 6169911619)", "('宠物支持针对性的配置某些宠物的词条随机范围', 6116020489)", "('全屏订阅页新增策略-新设备免费试用', 6093112024)", "('认证 H5 UI 优化', 5982284390)", "('扭蛋增加秒杀礼物', 5975038090)", "('PRO-同账号重复订阅问题', 5911127745)", "('IN跨区打赏优化2', 5910600657)", "('社群招募版主活动', 5828520298)", "('FB数据删除回调链接', 5825178756)", "('ef后台-直播间转盘小工具', 5691628086)", "('单社群精选主题活动', 5574540717)", "('新手送宠物', 5571298431)", "('新手礼包页签', 5549731201)", "('新手礼包弹窗弹出(前端)', 5549419840)", "('新手礼包支持经验值', 5524361128)", "('风控策略：异常设备登录拦截', 5508506301)", "('7.5期需求第二批', 5475903304)", "('BD体验账号 客户端需求', 5383385863)", "('系统消息-游戏消息频率A/B Testing', 5347589316)", "('老消息页面遗留问题优化 2期', 5344665117)", "('荣耀之路7.5期的留存弹窗', 5337757507)", "('OM后台新增未成年模型特征', 5305651229)", "('捕鱼数值放大', 5246984514)", "('[iOS] 应用内支付流程优化', 5114303450)", "('未成年历史逻辑更改', 5046986958)", "('荣耀之路拉新活动', 5046438498)", "('EVA发布动态需求', 5046351859)", "('CAP审核池内容写入SMP审核池需求', 5046349107)", "('拉黑场景屏蔽需求', 5046144192)", "('[Android] 客户端已全量AB实验代码和资源移除', 5045401775)", "('幸运奖励等你拿', 5043852701)", "('私信系统消息页面通知开关引导', 5010445960)", "('新增性别选项', 4975096956)", "('勋章-分享', 4974833038)", "('黑名单设置优化需求', 4974022995)", "('增加单麦房合唱pk进度实时通知', 4960018543)", "('个人账户权限设置', 4959127462)", "('iOS 房间公屏消息Cell高度自适应重构', 4947495558)", "('iOS IM消息Cell高度自适应重构', 4947495554)", "('直播&KTV房间长链接同步GIF消息', 4939201684)", "('入场动画资源增加md5校验', 4892850601)", "('APP登录和注册拆分', 4873230798)", "('Feed流实验全量', 4638241064)", "('H5页面用户特权显示规范', 4635639873)", "('Figma转h5页面模板', 4517236873)", "('礼物贴纸后台', 4500752419)", "('大区宝箱&宝箱奖励解耦', 4426354643)", "('特权奖励、碎片逻辑&原背包页面优化', 4425181007)", "('Sing页面迭代-全量', 4420537185)", "('Prod后台直播监控增加历史直播录像', 4346266087)", "('小视频支持多码率', 4323405952)", "('直播间任务宝箱逻辑优化', 4195455792)", "('搜索改版需求', 4086823438)", "('主播端新增开播测试能力', 4083427469)", "('“一起看”房间视频鉴黄', 3987636580)", "('公告支持多条件跳转', 3902098754)", "('搜索改版需求', 3614629245)", "('Android语音房坐席性能优化', 3508984823)", "('目前的作品滚动效果具有卡顿的感觉，需要优化一下，使得滚动效果更加平缓。', 3019649743)", "('耳返场景上线无延迟的limiter', 3016903647)", "('高等级小号广告任务限制', 3005009494)", "('用户自定义敏感词与评论设置第二期(已内审待排期)', 3002751166)", "('AI导唱V1.0', 3002456046)", "('iOS-运营弹窗接口统一和自研弹窗组件接入', 3001366987)", "('删除首页歌曲推荐卡片相关代码', 3001141371)", "('通知打开引导优化', 25336636)", "('退出房间交互优化', 21805997)", "('OCR头像识别', 21431973)", "('家族唱歌投稿活跃玩法', 20625564)", "('盲盒礼物动效&聊聊展示优化', 20552966)", "('抢唱新星周', 19727182)", "('每日福利活动设计', 18476108)", "('家族群里增加通用卡片推送', 16856276)", "('全平台优化头像框比例（二期）', 16182050)", "('订阅引导', 15090216)", "('头像挂件在多人场景露出', 15088023)", "('登录注册优化-手机号绑定&验证', 15074030)", "('公聊区气泡规范统一', 15047249)", "('菠菜房包装和导流方案', 12816699)", "('IOS注册流程实验及注册渠道新增', 12816371)", "('系统消息新增邮件发奖模块', 12796609)", "('用户家乡和居住地选择', 12778412)", "('空播问题治理', 12778211)", "('KTV推荐弹窗优化', 12741943)", "('语音房feed样式优化', 12741599)", "('私信举报详情页优化', 12175944)", "('KTV房间重构：统一麦位管理及相关视图', 9342093)", "('梳理长连接底层逻辑，排查隐藏的风险', 9277548)", "('家族列车、家族大乱斗redis层存储逻辑优化', 6540056)", "('录制默认音频导致的无法自动分享同步问题处理', 5531396)", "('转盘及活动通用发奖日志表拆分迁移', 4067641)"]
    return no_testing_list


if __name__ == '__main__':
    get_no_testing_requirements()
    # get_all_user_finished_demand(create_date=20250715, uid=7117238460611624964, finished_time=None)
    # get_user_name([7205168573025697794, 7212971331053240348])
    # get_all_user_finished_demand(create_date=20250101, uid=None, finished_time=20250108)
    # completion_rate(create_date=20250701, date=20250701, uid=7117238460611624964, finished_time=None)
    # result = get_check(20250601, uid=None, date_type='person_incomplete_data', finished_time=20250630)
    # print(get_check(20250601, uid=None, date_type='person_finished_data'))
    # print(get_check(20250601, 7117238460611624964, 'person_finished_data', finished_time=None))
    # print(get_check(None, uid=None, date_type='person_incomplete_data', finished_time=None))
    # print(json.dumps(result, indent=2, ensure_ascii=False))
