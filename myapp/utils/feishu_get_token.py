from myapp.utils.feishu_data import Feishu_data
import requests
import json

fei = Feishu_data()
import datetime


def get_tenant_access_token():
    """
    :return: 自建应用获取tenant_access_token
    """
    current_timestamp = datetime.datetime.now().timestamp()

    body = json.dumps(fei.req_token_body)
    headers = fei.content_type1
    url1 = fei.tenant_access_token_url
    url2 = url1 + f"?timestamp={int(current_timestamp)}"
    response = requests.post(url=url2, data=body, headers=headers)
    if response.json()['code'] == 0:
        tenant_token = response.json()['tenant_access_token']
        return tenant_token
    else:
        get_tenant_access_token()


def get_app_access_token():
    """
    :return: 获取自建应用app_access_token
    """
    headers = fei.content_type1
    body = fei.req_token_body
    response = requests.post(url=fei.app_access_token_url, json=body, headers=headers)
    app_access_token = response.json()['app_access_token']
    return app_access_token


def get_user_access_token():
    """
    :return: 获取网页应用token
    """
    fei.content_type1['Authorization'] = "Bearer " + f"{get_app_access_token()}"
    headers = fei.content_type1
    payload = json.dumps({
        "code": "xMSldislSkdK",
        "grant_type": "authorization_code"
    })
    response = requests.post(url=fei.user_access_token, headers=headers, data=payload)
    body = response.text
    return response.json()


# def get_plugin_access_token():
#     """
#     :return: 返回访问plugin_access_token
#     """
#     current_timestamp = datetime.datetime.now().timestamp()
#     url = "https://project.feishu.cn/open_api/authen/plugin_token"+f"?timestamp={int(current_timestamp)}"
# 
#     payload = json.dumps({
#         "plugin_id": "MII_6784DC70B348001C",
#         "plugin_secret": "25443C13FA76DD659237D60164AD4869",
#         "type": 0
#     })
#     headers = {
#         'Content-Type': 'application/json'
#     }
# 
#     response = requests.request("POST", url, headers=headers, data=payload)
#     return response.json()['data']['token']
# 
# 


# ✅ 初始化缓存字典（避免 None 报错）
_plugin_token_cache = {
    "token": None,
    "expire_time": None
}


def get_plugin_access_token():
    """
    请求 Feishu 插件 token
    """
    url = "https://project.feishu.cn/open_api/authen/plugin_token"
    payload = json.dumps({
        "plugin_id": "MII_6784DC70B348001C",
        "plugin_secret": "25443C13FA76DD659237D60164AD4869",
        "type": 0
    })
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, headers=headers, data=payload)
    data = response.json()["data"]

    token = data["token"]
    expire_timestamp = data["expire_time"]
    expire_time = datetime.datetime.fromtimestamp(expire_timestamp)

    # ✅ 更新缓存
    _plugin_token_cache["token"] = token
    _plugin_token_cache["expire_time"] = expire_time

    print(f"[INFO] ✅ Plugin token refreshed, valid until {expire_time}")

    # ❌ 不要返回元组
    # ✅ 只返回 token
    return token


def get_valid_plugin_token():
    """
    检查缓存的 plugin_token 是否过期，若过期则自动刷新
    """
    now = datetime.datetime.now()

    if (
            _plugin_token_cache["token"]
            and _plugin_token_cache["expire_time"]
            and _plugin_token_cache["expire_time"] > now
    ):
        return _plugin_token_cache["token"]

    # ✅ 如果过期，直接获取新 token（get_plugin_access_token 现在只返回字符串）
    return get_plugin_access_token()
