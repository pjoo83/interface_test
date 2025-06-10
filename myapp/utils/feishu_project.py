import requests
import json
from myapp.utils.feishu_data import Feishu_data
from myapp.utils.feishu_get_token import get_plugin_access_token
from datetime import datetime
import time
import json

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


def get_demand_list(year, month, day, uid):
    """
    :return: 复杂传参获取需求列表，按照时间戳取时间段的需求
    state_ket:doing 产品内审、end：需求结束
    """
    headers = feishu_project_head
    project_key = get_business_key()
    url = f"{fei.feishu_project_url}{project_key}/work_item/story/search/params"
    payload = json.dumps({
        "page_size": 50,
        "page_num": 1,
        "search_group": {
            "conjunction": "AND",
            "search_params": [
                {
                    "param_key": "finish_time",
                    "value": get_zero_timestamp_ms(year, month, day),
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

        },
        "expand": {
            "need_workflow": True,
            # "need_multi_text": True,
            # "relation_fields_detail": True
        }
    })
    response = requests.post(url=url, headers=headers, data=payload)
    testing_list = response.json()['data']
    # print(testing_list)
    return testing_list


# get_demand_list()


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
    # print(response.json()['data'])


# get_workflow(6156738065)

def calculate_points_if_has_test_stage(data):
    target_names = [
        "Android端开发",
        "iOS端开发",
        "流媒体开发",
        "测试阶段",
        "Web前端开发",
        "Web后端开发",
        "主服务端开发"
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
    # print(points_result)
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
def get_items_node(year, month, day, uid):
    """
    :return:工作的所有需求的节点工作时间
    """
    node_list = get_demand_list(year, month, day, uid)
    node_id_list = []
    for story_id in node_list:
        data_detail = calculate_points_if_has_test_stage(get_workflow(story_id['id']))
        if data_detail is False:
            continue
        else:
            node_id_list.append({"需求id": story_id['id'], '需求名称name': story_id['name'],
                                 "单个需求数据data": data_detail})
    return node_id_list


def analyze_workload_by_version(data_list):
    """
    :param data_list: 传入测试研发数据
    :return: 返回测试研发比
    """
    version_keys = {"Android端开发", "iOS端开发", "流媒体开发"}
    test_key = "测试阶段"

    # 分类存储
    version_demands = []
    non_version_demands = []

    # 分类
    for item in data_list:
        stages = item["单个需求数据data"]
        if any(k in stages for k in version_keys):
            version_demands.append(item)
        else:
            non_version_demands.append(item)

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
        ratio = round(dev_total/test_total, 3) if dev_total != 0 else "N/A"
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


def get_check(year, month, day, uid):
    result = analyze_workload_by_version(get_items_node(year, month, day, uid))
    return result


if __name__ == '__main__':
    print(get_check(2025, 5, 1, 7117238460611624964))
