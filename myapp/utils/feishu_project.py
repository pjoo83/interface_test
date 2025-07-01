import requests
from myapp.utils.feishu_data import Feishu_data
from myapp.utils.feishu_get_token import get_plugin_access_token
from datetime import datetime, timezone
import json
from dateutil.parser import parse

fei = Feishu_data()


def get_zero_timestamp_ms(year: int, month: int, day: int) -> int:
    """
    :param year:
    :param month:
    :param day:
    :return: 转化指定时间的时间戳
    """
    dt = datetime(year, month, day, 0, 0, 0)
    timestamp_ms = int(dt.timestamp() * 1000)
    return timestamp_ms


def get_zero_timestamp_ms_from_int(date_int: int) -> int:
    """
    将形如 20250601 的整数日期转换为该日期零点的时间戳（毫秒）。

    :param date_int: 日期，如 20250601
    :return: 该日期零点的时间戳（毫秒）
    """
    date_str = str(date_int)
    dt = datetime.strptime(date_str, "%Y%m%d")
    timestamp_ms = int(dt.timestamp() * 1000)
    return timestamp_ms


# 示例

feishu_project_head = {
    "X-PLUGIN-TOKEN": f"{get_plugin_access_token()}",
    'Content-Type': 'application/json',
    'X-USER-KEY': '7117238460611624964',
    "plugin_token": f"{get_plugin_access_token()}"}


def get_code():
    """
    :return: 用插件相关/获取code接口
    """
    url = f"{fei.feishu_project_url}authen/auth_code"
    payload = json.dumps({
        "plugin_id": "MII_6784DC70B348001C",
        "state": "111"
    })
    headers = {
        'cookie': f'{fei.feishu_cookie}',
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


def get_business_key():
    """
    :return: 获取空间key
    """
    url = f"{fei.feishu_project_url}projects"
    payload = json.dumps({
        "user_key": "7117238460611624964",
        "tenant_group_id": 0,
        "asset_key": "",
        "order": [
            ""
        ]
    })
    business = requests.request("POST", url, headers=feishu_project_head, data=payload)
    sm_zone_id = '62a6fce5ed2541be7bf5c2d3'
    work_item_type_key = business.json()['data'][0]
    return work_item_type_key


def get_field_all():
    """
    :return: 获取指定空间或工作项类型（推荐）下所有“字段”的基础信息
    """
    url = f'{fei.feishu_project_url}{get_business_key()}/field/all'
    payload = json.dumps({
        "work_item_type_key": "version"
    })
    response = requests.post(url=url, headers=feishu_project_head, data=payload)
    print(response.json()['data'])


def get_work_item_detail():
    """
    :return: 获取飞书空间详情
    """
    url = f"{fei.feishu_project_url}projects/detail"
    payload = json.dumps({
        "project_key": get_business_key(),
        "user_key": "7117238460611624964",
    })
    response = requests.post(url=url, headers=feishu_project_head, data=payload)
    print(response.text)


def get_work_item():
    """
    :return: 获取空间下工作项类型
    """
    url = f"{fei.feishu_project_url}{get_business_key()}/work_item/all-types"
    response = requests.get(url=url, headers=feishu_project_head)
    print(response.json())


def get_business_all():
    """
    :return: 获取业务线详情
    """
    url = f"{fei.feishu_project_url}{get_business_key()}/business/all"
    response = requests.get(url=url, headers=feishu_project_head)
    print(response.json())


def get_working_version_list():
    """
    :return: 获取在测中版本列表
    """
    headers = feishu_project_head
    project_key = get_business_key()
    url = f"{fei.feishu_project_url}{project_key}/work_item/filter"
    payload = json.dumps({
        "work_item_type_keys": ["story"],
        "work_item_status": [{
            "state_key": "ZPQ0hlfMX"
        }],
        # "expand": {
        #     "need_workflow": True,
        #     "need_multi_text": True,
        #     "relation_fields_detail": True
        # }
    })
    response = requests.post(url=url, headers=headers, data=payload)
    testing_list = response.json()['data']
    return testing_list


def get_demand_finished_list(date, uid=None):
    """
    :return: 复杂传参获取需求列表，按照时间戳取时间段的需求
    state_ket:doing 产品内审、end：需求结束
    """
    headers = feishu_project_head
    project_key = get_business_key()
    url = f"{fei.feishu_project_url}{project_key}/work_item/story/search/params"
    if uid is None:
        search_params = [
            {
                "param_key": "finish_time",
                "value": get_zero_timestamp_ms_from_int(date),
                "operator": ">="
            },
            {
                "param_key": "work_item_status",
                "value": ["end"],
                "operator": "="
            }
        ]
    else:
        search_params = [
            {
                "param_key": "finish_time",
                "value": get_zero_timestamp_ms_from_int(date),
                "operator": ">="
            },
            {
                "param_key": "work_item_status",
                "value": ["end"],
                "operator": "="
            },
            {
                "param_key": "role_owners",
                "value": [{"role": "qa",
                           "owners": [f'{uid}']}],
                "operator": "HAS ANY OF"
            }
        ]
    page_num = 1
    page_size = 50
    all_items = []
    while True:
        payload = json.dumps({
            "page_size": page_size,
            "page_num": page_num,
            "search_group": {
                "conjunction": "AND",
                "search_params": search_params
            },
            "expand": {
                "need_workflow": True,
                # "need_multi_text": True,
                # "relation_fields_detail": True
            }
        })

        response = requests.post(url=url, headers=headers, data=payload)
        if response.status_code != 200:
            print(f"请求失败: {response.status_code}, {response.text}")
            break

        resp_data = response.json()
        data_list = resp_data.get('data', [])

        if not data_list:
            break

        all_items.extend(data_list)

        if len(data_list) < page_size:
            # 当前页返回不足page_size，说明已到最后一页
            break
        page_num += 1
    return all_items


def get_demand_progress_list(uid=None):
    """
    :return: 复杂传参获取需求列表，查询没有结束的需求
    state_ket:doing 产品内审、end：需求结束
    """
    headers = feishu_project_head
    project_key = get_business_key()
    url = f"{fei.feishu_project_url}{project_key}/work_item/story/search/params"
    if uid is None:
        search_params = [
            {
                "param_key": "work_item_status",
                "value": ["end"],
                "operator": "!="
            },
            {
                "param_key": "work_item_status",
                "value": ["end"],
                "operator": "!="
            },
            {
                "param_key": "created_at",
                "value": 1735660800000,
                "operator": ">"
            },
        ]
    else:
        search_params = [
            {
                "param_key": "work_item_status",
                "value": ["end"],
                "operator": "!="
            },
            {
                "param_key": "role_owners",
                "value": [{"role": "qa",
                           "owners": [f'{uid}']}],
                "operator": "HAS ANY OF"
            },
            {
                "param_key": "created_at",
                "value": 1735660800000,
                "operator": ">"
            },
        ]
    page_num = 1
    page_size = 50
    all_items = []

    while True:
        payload = json.dumps({
            "page_size": page_size,
            "page_num": page_num,
            "search_group": {
                "conjunction": "AND",
                "search_params": search_params
            },
            "expand": {
                "need_workflow": True,
                # "need_multi_text": True,
                # "relation_fields_detail": True
            }
        })

        response = requests.post(url=url, headers=headers, data=payload)
        if response.status_code != 200:
            print(f"请求失败: {response.status_code}, {response.text}")
            break

        resp_data = response.json()
        data_list = resp_data.get('data', [])

        if not data_list:
            break

        all_items.extend(data_list)

        if len(data_list) < page_size:
            # 当前页不足page_size，说明最后一页
            break

        page_num += 1

    return all_items


def get_demand_story_list():
    """
    :return: 单空间获取在测列表
    state_ket:doing 产品内审
    """
    headers = feishu_project_head
    project_key = get_business_key()
    url = f"{fei.feishu_project_url}{project_key}/work_item/filter"
    payload = json.dumps({
        "work_item_type_keys": ["story"],
        "created_at": {
            "start": 1746445555000
        },
        "work_item_status": [
            {
                "state_key": "doing",
            }
        ],
        "page_size": 50
        # "expand": {
        #     "need_workflow": True,
        #     "need_multi_text": True,
        #     "relation_fields_detail": True
        # }
    })
    response = requests.post(url=url, headers=headers, data=payload)
    testing_list = response.json()
    return testing_list


# print(get_demand_story_list())


def get_working_query():
    """
    :return: 获取工作项详情
    """
    project_key = get_business_key()
    url = f"{fei.feishu_project_url}{project_key}/work_item/version/query"
    headers = feishu_project_head
    payload = json.dumps({
        "work_item_ids": [5383498496, 5383244487, 5376179886],
        "expand": {
            "need_workflow": True,
            "need_multi_text": True,
            "relation_fields_detail": True,
        }

    })
    response = requests.post(url=url, headers=headers, data=payload)
    print(response.text)


# get_working_query()
def get_workflow(story_id):
    """
    :return: 通过结点流获取到项目的时间结点
    """
    project_key = get_business_key()
    url = f"{fei.feishu_project_url}{project_key}/work_item/story/{story_id}/workflow/query"
    headers = feishu_project_head
    payload = json.dumps({
        "flow_type": 0,

    })
    response = requests.post(url=url, headers=headers, data=payload)
    return response.json()['data']


# get_workflow(6156738065)

def calculate_points_if_has_test_stage(data):
    target_names = [
        "Android端开发",
        "iOS端开发",
        "流媒体开发",
        "测试阶段",
        "Web前端开发",
        "Web后端开发",
        "主服务端开发",
        "互娱端开发",
        "游戏后端",
        "游戏前端",
        "曲库开发",
        "音视频开发"
    ]

    workflow_nodes = data.get("workflow_nodes", [])
    # 根据人查，不回涉及这个功能
    # if not any(node.get("name") == "测试阶段" for node in workflow_nodes):
    #     return {}  # 直接返回空结果
    points_result = {}
    for node in workflow_nodes:
        name = node.get("name", "")
        if name in target_names:
            total_points = sum(schedule.get("points", 0) for schedule in node.get("schedules", []))
            points_result[name] = total_points
    return points_result


# get_project_time(datas)

# 废弃，无法取时间
# def get_version_time():
#     """
#     :return: 获取版本时间,无法使用“所属工作项尚未开启工时登记，无法进行实际工时登记”
#     """
#     project_key = get_business_key()
#     url = f"{fei.feishu_project_url}/work_item/man_hour/records"
#     headers = feishu_project_head
#     payload = json.dumps({
#         "project_key": get_business_key(),
#         "work_item_type_key": "story",
#         "work_item_id": 6156738065,
#     })
#     response = requests.post(url=url, headers=headers, data=payload)
#     print(response.json())

# get_version_time()
# 获取每个项目的节点
def get_items_node(date, uid, date_type):
    """
    :return:工作的所有需求的节点工作时间
    """
    node_list = []
    if date_type == "person_finished_data":
        node_list = get_demand_finished_list(date, uid)
        node_list = filter_data_list2(node_list, str(date))
    elif date_type == "person_incomplete_data":
        date_list = get_demand_progress_list(uid)
        node_list = filter_data_list(date_list)
    node_id_list = []
    for story_id in node_list:
        data_detail = calculate_points_if_has_test_stage(get_workflow(story_id['id']))
        if data_detail is False:
            continue
        else:
            node_id_list.append({"需求id": story_id['id'], '需求名称name': story_id['name'],
                                 "单个需求数据data": data_detail})

    return node_id_list


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


def analyze_workload_by_version(data_list):
    """
    :param data_list: 传入测试研发数据
    :return: 返回测试研发比
    """
    version_keys = {
        "Android端开发", "iOS端开发", "流媒体开发", "测试阶段",
        "Web前端开发", "Web后端开发", "主服务端开发",
        "互娱端开发", "游戏后端", "游戏前端", '曲库开发', '音视频开发'
    }
    test_key = "测试阶段"

    # 分类存储
    version_demands = []
    non_version_demands = []

    # 分类
    for item in data_list:
        stages = item["单个需求数据data"]

        # 判断是否包含“测试阶段”，如果没有则跳过
        if test_key not in stages:
            continue

        test = 0
        develop = 0

        if any(k in stages for k in version_keys):
            version_demands.append(item)
        else:
            non_version_demands.append(item)

        for k, v in stages.items():
            if k == test_key:
                test += v
            else:
                develop += v

        if develop == 0:
            continue
        elif test == 0:
            print(f"需求ID: {item['需求id']}，需求名称: {item['需求名称name']} 的测试时间为0，请注意填写！！！")
        elif round(develop / test, 3) < 3:
            print(
                f"需求ID: {item['需求id']} 的测试/研发比过高，可能需要优化！",
                f"需求名称: {item['需求名称name']}, 测试时间: {stages.get(test_key, 0)}, "
                f"研发时间: {develop}, 测试/研发比: {round(develop / test, 3)}"
            )

    # 定义统计函数
    def compute_totals(demands):
        test_total = 0
        dev_total = 0
        for item in demands:
            for key, value in item["单个需求数据data"].items():
                if key == test_key:
                    test_total += value
                else:
                    dev_total += value
        ratio = round(dev_total / test_total, 3) if dev_total != 0 else "N/A"
        return test_total, dev_total, ratio

    # 计算数据
    v_test, v_dev, v_ratio = compute_totals(version_demands)
    nv_test, nv_dev, nv_ratio = compute_totals(non_version_demands)

    # 返回结果
    return {
        "版本需求": {
            "数量": len(version_demands),
            "测试总时间": v_test,
            "研发总时间": v_dev,
            "研发/测试比值": v_ratio,
        },
        "非版本需求": {
            "数量": len(non_version_demands),
            "测试总时间": nv_test,
            "研发总时间": nv_dev,
            "研发/测试比值": nv_ratio,
        },

        "总需求数": {
            "数量": len(version_demands) + len(non_version_demands),
            "测试总时间": v_test + nv_test,
            "研发总时间": v_dev + nv_dev,
            "研发/测试比值": round((v_dev + nv_dev) / (v_test + nv_test), 3) if (v_dev + nv_dev) != 0 else "N/A"
        }

    }


def get_check(date, uid, date_type):
    result = analyze_workload_by_version(get_items_node(date, uid, date_type))
    return result


if __name__ == '__main__':
    # print(get_check(20250501, uid=None, date_type='person_finished_data'))
    # print(get_check(20250601, 7117238460611624964, 'person_finished_data'))
    # print(get_check(20250601, 7117238460611624964, 'person_incomplete_data'))
    print(get_check(20250601, uid=None, date_type='person_incomplete_data'))
