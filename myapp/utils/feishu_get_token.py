from myapp.utils.feishu_data import Feishu_data
import requests
import json

fei = Feishu_data()


def get_tenant_access_token():
    """
    :return: 自建应用获取tenant_access_token
    """
    body = json.dumps(fei.req_token_body)
    headers = fei.content_type1
    response = requests.post(url=fei.tenant_access_token_url, data=body, headers=headers)
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


def get_plugin_access_token():
    """
    :return: 返回访问plugin_access_token
    """
    url = "https://project.feishu.cn/open_api/authen/plugin_token"

    payload = json.dumps({
        "plugin_id": "MII_6784DC70B348001C",
        "plugin_secret": "25443C13FA76DD659237D60164AD4869",
        "type": 0
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()['data']['token']