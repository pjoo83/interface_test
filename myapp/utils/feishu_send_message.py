from myapp.utils.feishu_get_token import get_tenant_access_token
import requests
from myapp.utils.feishu_data import Feishu_data
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
        if i['name'] == '机器人测试啊':
            print(i['chat_id'])
            return i['chat_id']


def send_msg(chat_id, horse_count, horse_id, horse_png, horse_pag, horse_name):
    """
    :param horse_pag: 坐骑pag
    :param horse_png: 坐骑图片
    :param horse_id: 坐骑id
    :param horse_count: 坐新增数量
    :param chat_id: 群信息id
    :param horse_name: 坐骑图片
    :return:
    """
    send_url = fei.send_msg_url
    fei.content_type1['Authorization'] = "Bearer " + f"{get_tenant_access_token()}"
    headers = fei.content_type1
    # data = json.dumps({
    #     "receive_id": f"{chat_id}",
    #     "msg_type": "text",
    #     # "content": "{\"text\":" + "\" " + f"{translate_url}" + "\"}",
    #     "content": "{\"text\":\"<at user_id=\\\"ou_aedb7a9856743c147d5e1d2bb27fe486\\\">Tom</at> text  content\"}",
    #
    # })
    data = json.dumps({
        "receive_id": f"{chat_id}",
        "content": "{\"zh_cn\":"
                   "{\"title\":\"注意注意注意！！！\",\"content\":"
                   "["
                   "[{\"tag\":\"text\",\"text\":\"新增条数:\"},"
                   "{\"tag\":\"text\",\"text\":" + "\" " + f"{horse_count}" + "\"}],"
                   "["
                   "{\"tag\":\"text\",\"text\":\"最新资源id:\"},"
                   "{\"tag\":\"text\",\"text\":" + "\" " + f"{horse_id}" + "\"}]," 
                   "["
                   "{\"tag\":\"text\",\"text\":\"最新资源名:\"},"
                   "{\"tag\":\"text\",\"text\":" + "\" " + f"{horse_name}" + "\"}]," 
                   "["
                   "{\"tag\":\"text\",\"text\":\"新增资源图片:\"},"
                   "{\"tag\":\"text\",\"text\":" + "\" " + f"{horse_png}" + "\"}],"     
                   "["
                   "{\"tag\":\"text\",\"text\":\"新增资源视频:\"},"
                   "{\"tag\":\"text\",\"text\":" + "\" " + f"{horse_pag}" + "\"}],"                                                              
                   "[{\"tag\":\"a\",\"href\":\"https://prod.ushow.media/internal/horse/index\",\"text\":\"点击后台查看\"},"
                   "{\"tag\":\"at\",\"user_id\":\"ou_aedb7a9856743c147d5e1d2bb27fe486\",\"user_name\":\"tom\"}],"
                   "[{\"tag\":\"img\",\"image_key\":\"img_v3_02g6_fe03870a-7f01-4d30-9a0c-88b6e9e893cg\"}]]}}",
        "msg_type": "post"
    })
    response = requests.post(url=send_url, headers=headers, data=data)
    print(response.json())


def start_send(horse_count, horse_id, horse_png, horse_pag, horse_name):
    """
    :return: 进行发送
    """
    cid = get_chat_id()
    send_msg(cid, horse_count, horse_id, horse_png, horse_pag, horse_name)


# start_send(2,1450,"https://static.starmakerstudios.com/production/statics/horse/horse_client_side_pag_source_20241030080041.pag",
#            'https://static.starmakerstudios.com/production/statics/horse/horse_img_20241028094922.png','魔法灵兽')
