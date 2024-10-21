from ..utils.feishu_get_token import get_tenant_access_token
import requests
from ..utils.feishu_data import Feishu_data
import json

fei = Feishu_data()


def get_chat_id():
    """
    :return:获取机器人所在群id
    """
    chat_id_url = fei.get_chats_id_url
    fei.content_type1['Authorization'] = "Bearer " + f"{get_tenant_access_token()}"
    headers = fei.content_type1
    response = requests.get(url=chat_id_url, headers=headers)
    item_list = response.json()['data']['items']
    for i in item_list:
        if i['name'] == '测试调用':
            print(i['chat_id'])
            return i['chat_id']
    print(response.json())


def send_msg(chat_id, translate_url):
    """
    :param chat_id: 群信息id
    :param translate_url: 上传的文件地址
    :return:
    """
    send_url = fei.send_msg_url
    fei.content_type1['Authorization'] = "Bearer " + f"{get_tenant_access_token()}"
    headers = fei.content_type1
    data = json.dumps({
        "receive_id": f"{chat_id}",
        "msg_type": "text",
        "content": "{\"text\":" + "\" " + f"{translate_url}" + "\"}",
    })
    response = requests.post(url=send_url, headers=headers, data=data)
    print(response.json())


def start_send(translate_url):
    """
    :return: 进行发送
    """
    cid = get_chat_id()
    send_msg(cid, translate_url)

# start_send("sssssss")
