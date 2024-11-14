from myapp.utils.feishu_get_token import get_tenant_access_token
import requests
from myapp.utils.feishu_data import Feishu_data
import json
from myapp.utils.data import sql_data
import datetime

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
        # elif i['name'] == '机器人测试啊' and function == 'pendant':
        #     print(i['chat_id'])
        #     return i['chat_id']
        # elif i['name'] == '机器人测试啊' and function == 'debris':
        #     print(i['chat_id'])
        #     return i['chat_id']


def send_msg(function, chat_id, horse_count, horse_id, horse_png, horse_pag, horse_name):
    """
    :param function: 消息类别
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
    if function == 'horse':
        data = json.dumps({
            "receive_id": f"{chat_id}",
            "content": "{\"zh_cn\":"
                       "{\"title\":\"注意注意注意,坐骑更新了！！！\",\"content\":"
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
                       "[{\"tag\":\"a\",\"href\":\"https://prod.ushow.media/internal/horse/index\","
                       "\"text\":\"点击后台查看\"},"
                       "{\"tag\":\"at\",\"user_id\":\"ou_aedb7a9856743c147d5e1d2bb27fe486\",\"user_name\":\"tom\"}],"
                       "[{\"tag\":\"img\",\"image_key\":\"img_v3_02gd_9f1569d4-680e-46e8-8d4c-5b958dc0773g\"}]]}}",
            "msg_type": "post"
        })
        response = requests.post(url=send_url, headers=headers, data=data)
        # print(response.json())
    elif function == 'pendant':
        data = json.dumps({
            "receive_id": f"{chat_id}",
            "content": "{\"zh_cn\":"
                       "{\"title\":\"注意注意注意！！！头像框更新了！！！\",\"content\":"
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
                       "[{\"tag\":\"a\"," "\"href\":\"https://prod.ushow.media/internal/money/pendant/index\",\"text\":\"点击后台查看\"}],"
                       "[{\"tag\":\"img\",\"image_key\":\"img_v3_02gd_8b46a8eb-d38d-4bda-8b3b-3a5f5047509g\"}]]}}",
            "msg_type": "post"
        })
        response = requests.post(url=send_url, headers=headers, data=data)
    elif function == 'debris':
        data = json.dumps({
            "receive_id": f"{chat_id}",
            "content": "{\"zh_cn\":"
                       "{\"title\":\"注意注意注意！！！有新的碎片更新了！！！\",\"content\":"
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
                       "{\"tag\":\"text\",\"text\":\"道具表校验结果:\"},"
                       "{\"tag\":\"text\",\"text\":" + "\" " + f"{horse_pag}" + "\"}],"
                       "[{\"tag\":\"a\"," "\"href\":\"https://prod.ushow.media/internal/money/pendant/index\",\"text\":\"点击后台查看\"}],"
                       "[{\"tag\":\"img\",\"image_key\":\"img_v3_02gd_c7873905-0ae5-49e1-bff8-0a374819b3dg\"}]]}}",
            "msg_type": "post"
        })
        response = requests.post(url=send_url, headers=headers, data=data)
    elif function == 'ab-test':
        data = json.dumps({
            "receive_id": f"{chat_id}",
            "content": "{\"zh_cn\":"
                       "{\"title\":\"注意注意注意！！！有新ab实验！！！\",\"content\":"
                       "["
                       "[{\"tag\":\"text\",\"text\":\"新增实验条数:\"},"
                       "{\"tag\":\"text\",\"text\":" + "\" " + f"{horse_count}" + "\"}],"
                       "["
                       "{\"tag\":\"text\",\"text\":\"实验id: \"},"
                       "{\"tag\":\"text\",\"text\":" + "\" " + f"{horse_id}    " + "\"},"
                       "{\"tag\":\"text\",\"text\":\"实验名称: \"},"
                       "{\"tag\":\"text\",\"text\":" + "\" " + f"{horse_name}   " + "\"}," 
                       "{\"tag\":\"text\",\"text\":\"实验作者:  \"},"
                       "{\"tag\":\"text\",\"text\":" + "\" " + f"{horse_pag[0]}" + "\"}],"                                                                                  
                       "["
                       "{\"tag\":\"text\",\"text\":\"实验时间:\"},"
                       "{\"tag\":\"text\",\"text\":" + "\" " + f"{horse_png[0]}" + "\"},"
                       "{\"tag\":\"text\",\"text\":\"至\"},"
                       "{\"tag\":\"text\",\"text\":" + "\" " + f"{horse_png[1]}" + "\"}],"
                       "["
                       "{\"tag\":\"text\",\"text\":\"实验状态  :\"},"
                       "{\"tag\":\"text\",\"text\":" + "\" " + f"{horse_pag[1]}  " + "\"},"
                       "{\"tag\":\"text\",\"text\":\"实验关联需求  :\"},"                                                                       
                       "{\"tag\":\"text\",\"text\":" + "\" " + f"{horse_pag[2]}" + "\"}],"
                       "["
                       "{\"tag\":\"text\",\"text\":\"实验分组占比:\"},"
                       "{\"tag\":\"text\",\"text\":" + "\" " + f"{horse_pag[4]}" + "\"}],"
                       "[{\"tag\":\"a\"," "\"href\":\"https://ab.ushow.media/experiments\",\"text\":\"点击后台查看\"}],"
                       "[{\"tag\":\"img\",\"image_key\":\"img_v3_02gk_af511a4a-e825-48f4-83d0-29be1e56ea2g\"}]]}}",
            "msg_type": "post"
        })
        response = requests.post(url=send_url, headers=headers, data=data)

def start_send(function, datas):
    """
    :return: 进行发送
    """
    cid = get_chat_id()
    if function == 'horse':
        for i in range(len(datas)):
            if datas[i][12]:
                send_msg(function, cid, 1, datas[i][0],
                         f'https://static.starmakerstudios.com/production/statics/horse/{datas[i][2]}',
                         f'https://static.starmakerstudios.com/production/statics/horse/{datas[i][12]}',
                         datas[i][1])
            elif datas[i][31]:
                send_msg(function, cid, 1, datas[i][0],
                         f'https://static.starmakerstudios.com/production/statics/horse/{datas[i][2]}',
                         f'https://static.starmakerstudios.com/production/statics/horse/{datas[i][31]}',
                         datas[i][1])
    elif function == 'pendant':
        for i in range(len(datas)):
            if datas[i][4]:
                send_msg(function, cid, 1, datas[i][0],
                         f'https://gift-resource.starmakerstudios.com/pendant/{datas[i][4]}',
                         'wu',
                         datas[i][1])
            elif datas[i][2]:
                send_msg(function, cid, 1, datas[i][0],
                         f'https://gift-resource.starmakerstudios.com/pendant/{datas[i][2]}',
                         'wu',
                         datas[i][1])
    elif function == 'debris':
        for i in range(len(datas)):
            props_id = datas[i][7].split(',')[0].split(':')[1]
            url = sql_data()[0]
            headers = sql_data()[1]
            payload = "instance_name=cdb-sg-prod-starmaker-live-r2&db_name=fb_live&schema_name=&tb_name=&sql_content" \
                      f"=select+*+from++static_props+where+props_id+%3D\'{props_id}\'"
            data = requests.post(url=url, headers=headers, data=payload)
            props_result = data.json()['data']['affected_rows']
            if props_result == 1:
                send_msg(function, cid, 1, datas[i][0],
                         f'https://static.starmakerstudios.com/production/gift/debris/{datas[i][3]}',
                         '道具表中有此配置的id',
                         datas[i][1])
            elif props_result == 0:
                send_msg(function, cid, 1, datas[i][0],
                         f'https://static.starmakerstudios.com/production/gift/debris/{datas[i][3]}',
                         '注意注意！！！！！碎片表中配错道具id',
                         datas[i][1])
    elif function == 'ab-test':
        test_group = []
        for i in range(len(datas)):
            url = sql_data()[0]
            headers = sql_data()[1]
            payload = 'instance_name=cdb-sg-prod-abookserver-abtest&db_name=abtest&schema_name=&tb_name=&sql_content' \
                      '=select+a.id++%2Ca.name+%2Ca.start_ts+%2Ca.end_ts+%2Ca.create_man+%2Ca.status+%2Ca' \
                      '.description+%2Cc.description++%2Cd.name+%2Cd.probability++from+experiment+a+inner+join+audien' \
                      'ce_experiment+b+inner+join+audience+c++inner+join+variant+d+on+a.id+%3D+b.experiment_id+and+b.' \
                      f'audience_id+%3D+c.id+and+a.id+%3Dd.experiment_id+where+a.id+%3D+{datas[i][0]}'
            data = requests.post(url=url, headers=headers, data=payload)
            test_date = data.json()['data']['rows']
            for z in range(len(test_date)):
                test_group.append(f"实验分组：{test_date[z][8]}，放量占比：{test_date[z][9]}")
            if test_date[0][5] == 0:
                test_date[0][5] = "实验中"
                print("实验开始中")
            elif test_date[0][5] == 3:
                test_date[0][5] = "实验未开始"
            send_msg(function=function, chat_id=cid, horse_count=1,
                     horse_id=test_date[0][0],
                     horse_name=test_date[0][1],
                     horse_png=(stamp_to_time(test_date[0][2]), stamp_to_time(test_date[0][3])),
                     horse_pag=(test_date[0][4], test_date[0][5],
                                test_date[0][6], test_date[0][7], test_group)
                     )


def stamp_to_time(time):
    dt = datetime.datetime.fromtimestamp(time)
    date_str = dt.strftime('%Y-%m-%d %H:%M:%S')
    return date_str