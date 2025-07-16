import time
from myapp.utils.feishu_get_token import get_tenant_access_token
import requests
from myapp.utils.feishu_data import Feishu_data
import json
from myapp.utils.data import sql_data
import datetime
from myapp.utils.feishu_picture_upload import download_img
from myapp.utils.feishu_picture_upload import check_webp, check_image, check_png_transparency, \
    check_webp_animation_alpha

fei = Feishu_data()


def get_chat_id(function):
    """
    :return:获取机器人所在群id
    """
    chat_id_url = fei.get_chats_id_url
    fei.content_type1['Authorization'] = "Bearer " + f"{get_tenant_access_token()}"
    headers = fei.content_type1
    response = requests.get(url=chat_id_url, headers=headers)
    item_list = response.json()['data']['items']
    for i in item_list:
        if i['name'] == '机器人测试啊' and function != 'ab-test' and function != 'crazy_monster':
            print(i['chat_id'])
            return i['chat_id']
        elif i['name'] == '机器人测试啊' and function == 'ab-test':
            print(i['chat_id'])
            return i['chat_id']
        elif i['name'] == '机器人测试啊' and function == 'crazy_monster':
            print(i['chat_id'])
            return i['chat_id']


def atest_send(chat_id):
    image_key = download_img(
        'https://static.starmakerstudios.com/production/statics/horse/horse_client_side_pag_source_20250214105432.pag')
    content = {
        "zh_cn": {
            "title": f"注意注意注意,坐骑更新了！！！",
            "content": [
                [
                    {
                        "tag": "text",
                        "text": "下面是图片:",
                        "style": ["bold", "underline"]
                    },
                ],
                [{"tag": "img", "image_key": image_key}],
            ]
        },
    }

    data = {
        "receive_id": chat_id,
        "msg_type": "post",
        "content": json.dumps(content)  # ✅ 这里必须转换成字符串
    }
    fei.content_type1['Authorization'] = "Bearer " + f"{get_tenant_access_token()}"
    headers = fei.content_type1
    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
    response = requests.post(url, headers=headers, json=data)

    print(response.json())  # 确保返回成功


def send_msg(function, chat_id, horse_count, horse_id, horse_png, horse_pag, horse_name, data):
    """
    :param data: 总数据列
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
    if function == 'horse':
        content = {
            "zh_cn": {
                "title": f"注意注意注意！！！坐骑更新了！！！",
                "content": [
                    [
                        {
                            "tag": "text",
                            "text": f"资源名称 : {horse_name}",
                            "style": ["bold", "underline"]
                        },
                    ],
                    [
                        {
                            "tag": "text",
                            "text": f"资源id : {horse_id}",
                            "style": ["bold", "underline"]
                        },
                    ],
                    [
                        {
                            "tag": "text",
                            "text": f"资源链接 : {horse_png}",
                            "style": ["bold", "underline"]
                        },
                    ],
                    [
                        {
                            "tag": "text",
                            "text": f"资源链接 : {horse_pag[0]}",
                            "style": ["bold", "underline"]
                        },
                    ],
                    [
                        {
                            "tag": "text",
                            "text": f"操作人 : {horse_pag[1]}",
                            "style": ["bold", "underline"]
                        },
                    ],
                    [
                        {
                            "tag": "text",
                            "text": f"资源详情 : ",
                            "style": ["bold", "underline"]
                        },
                    ],
                    [{"tag": "img", "image_key": f'{download_img(horse_png)}'}],
                ]
            },
        }

        data1 = {
            "receive_id": chat_id,
            "msg_type": "post",
            "content": json.dumps(content)  # ✅ 这里必须转换成字符串
        }
        response = requests.post(url=send_url, headers=headers, json=data1, verify=True)
    elif function == 'pendant':
        if data[4]:
            data_resources1 = f"https://gift-resource.starmakerstudios.com/pendant/{data[4]}"
            if ".webp" not in data_resources1:
                data_resources = f"文件格式存在问题{data_resources1}"
            else:
                data_resources = f"文件格式正常:{data_resources1}"
                check_result = check_webp_animation_alpha('image.webp')
                file_checks = check_webp('image.webp')

        else:
            data_resources1 = f"https://gift-resource.starmakerstudios.com/pendant/{data[2]}"
            if ".png" not in data_resources1:
                data_resources = f"文件格式存在问题{data_resources1}"
            else:
                data_resources = f"文件格式正常:{data_resources1}"
                check_result = check_png_transparency('image.png')
                file_checks = check_image('image.png')
        content = {
            "zh_cn": {
                "title": f"注意注意注意！！！头像框更新了！！！",
                "content": [
                    [
                        {
                            "tag": "text",
                            "text": f"资源名称 : {data[1]}",
                            "style": ["bold", "underline"]
                        },
                    ],
                    [
                        {
                            "tag": "text",
                            "text": f"资源id : {data[0]}",
                            "style": ["bold", "underline"]
                        },
                    ],
                    [
                        {
                            "tag": "text",
                            "text": f"操作人 : {data[13]}",
                            "style": ["bold", "underline"]
                        },
                    ],
                    [
                        {
                            "tag": "text",
                            "text": data_resources,
                            "style": ["bold", "underline"]
                        },
                    ],
                    [
                        {
                            "tag": "text",
                            "text": f"文件检查结果 : {file_checks}",
                            "style": ["bold", "underline"]
                        },
                    ],
                    [
                        {
                            "tag": "text",
                            "text": f"透明度检测 : {check_result}",
                            "style": ["bold", "underline"]
                        },
                    ],
                    [
                        {
                            "tag": "text",
                            "text": f"资源详情 : ",
                            "style": ["bold", "underline"]
                        },
                    ],
                    [{"tag": "img", "image_key": f'{download_img(data_resources1)}'}],
                ]
            },
        }
        data1 = {
            "receive_id": chat_id,
            "msg_type": "post",
            "content": json.dumps(content)  # ✅ 这里必须转换成字符串
        }
        response = requests.post(url=send_url, headers=headers, json=data1, verify=True)
    elif function == 'debris':
        content = {
            "zh_cn": {
                "title": f"注意注意注意！！！有新的碎片更新了！！！",
                "content": [
                    [
                        {
                            "tag": "text",
                            "text": f"资源名称 : {horse_name}",
                            "style": ["bold", "underline"]
                        },
                    ],

                    [
                        {
                            "tag": "text",
                            "text": f"资源id : {horse_id}",
                            "style": ["bold", "underline"]
                        },
                    ],
                    [
                        {
                            "tag": "text",
                            "text": f"资源链接 : {horse_png}",
                            "style": ["bold", "underline"]
                        },
                    ],
                    [
                        {
                            "tag": "text",
                            "text": f"图片检查结果 : {check_image('image.png')}",
                            "style": ["bold", "underline"]
                        },
                    ],
                    [
                        {
                            "tag": "text",
                            "text": f"道具表检测结果 : {horse_pag}",
                            "style": ["bold", "underline"]
                        },
                    ],
                    [
                        {
                            "tag": "text",
                            "text": f"资源详情 : ",
                            "style": ["bold", "underline"]
                        },
                    ],
                    [{"tag": "img", "image_key": f'{download_img(horse_png)}'}],
                ]
            },
        }

        data1 = {
            "receive_id": chat_id,
            "msg_type": "post",
            "content": json.dumps(content)  # ✅ 这里必须转换成字符串
        }
        response = requests.post(url=send_url, headers=headers, json=data1, verify=True)
    elif function == 'ab-test':
        content = {
            "zh_cn": {
                "title": f"注意注意注意！！！有新ab实验！！！",
                "content": [
                    [
                        {
                            "tag": "text",
                            "text": f"实验名称 : {horse_name}",
                            "style": ["bold", "underline"]
                        },
                    ],
                    [
                        {
                            "tag": "text",
                            "text": f"实验id : {horse_id},  实验作者 : {horse_pag[0]}",
                            "style": ["bold", "underline"]
                        },
                    ],
                    [
                        {
                            "tag": "text",
                            "text": f"实验时间 : {horse_png[0]} 至 {horse_png[1]}",
                            "style": ["bold", "underline"]
                        },
                    ],
                    [
                        {
                            "tag": "text",
                            "text": f"实验状态 : {horse_pag[1]}",
                            "style": ["bold", "underline"]
                        },
                    ],
                    [
                        {
                            "tag": "text",
                            "text": f"实验关联需求 : {horse_pag[2]}",
                            "style": ["bold", "underline"]
                        },
                    ],
                    [
                        {
                            "tag": "text",
                            "text": f"实验版本控制 : {horse_pag[3]} ",
                            "style": ["bold", "underline"]
                        },
                    ],
                    [
                        {
                            "tag": "text",
                            "text": f"实验分组占比 : {horse_pag[4]} ",
                            # "style": ["bold", "underline"]
                        },
                    ],
                    [{"tag": "img", "image_key": 'img_v3_02gk_af511a4a-e825-48f4-83d0-29be1e56ea2g'}],
                ]
            },
        }
        data1 = {
            "receive_id": chat_id,
            "msg_type": "post",
            "content": json.dumps(content)  # ✅ 这里必须转换成字符串
        }
        response = requests.post(url=send_url, headers=headers, json=data1, verify=True)
    elif function == 'bubble':
        content = {
            "zh_cn": {
                "title": f"注意注意注意！！！有新的特权资源更新了！！！",
                "content": [
                    [
                        {
                            "tag": "text",
                            "text": f'{horse_name}',
                            "style": ["bold", "underline"]
                        },
                    ],
                    [
                        {
                            "tag": "text",
                            "text": f"资源id : {horse_id}",
                            "style": ["bold", "underline"]
                        },
                    ],
                    [
                        {
                            "tag": "text",
                            "text": f"资源链接 : {horse_png}",
                            "style": ["bold", "underline"]
                        },
                    ],
                    [
                        {
                            "tag": "text",
                            "text": f"资源链接 :{horse_pag} ",
                            "style": ["bold", "underline"]
                        },
                    ],
                    [
                        {
                            "tag": "text",
                            "text": f"文件检查结果 :{check_image('image.png')} ",
                            "style": ["bold", "underline"]
                        },
                    ],
                    [{"tag": "img", "image_key": f'{download_img(horse_png)}'}],
                ]
            },
        }

        data1 = {
            "receive_id": chat_id,
            "msg_type": "post",
            "content": json.dumps(content)  # ✅ 这里必须转换成字符串
        }
        response = requests.post(url=send_url, headers=headers, json=data1, verify=True)

    elif function == 'crazy_monster':
        if len(data) >= 17:
            content = {
                "zh_cn": {
                    "title": f"注意注意注意！！！热血怪兽有新的装备资源更新了！！！",
                    "content": [
                        [
                            {
                                "tag": "text",
                                "text": f'装备名称:{data[3]}',
                                "style": ["bold", "underline"]
                            },
                        ],
                        [
                            {
                                "tag": "text",
                                "text": f"装备自增id : {data[0]}，装备装备唯一key：{data[1]}，装备id：{data[2]}",
                                "style": ["bold", "underline"]
                            },
                        ],
                        [
                            {
                                "tag": "text",
                                "text": f"0级提供经验：{data[5]}  装备等级：{data[6]}  装备最高/低经验：{data[7], data[8]}  "
                                        f"品质：{data[9]}   星级：{data[10]}  ",
                                "style": ["bold", "underline"]
                            },
                        ],
                        [
                            {
                                "tag": "text",
                                "text": f"属性加成类型:{data[11]}  属性值：{data[12]} "
                                        f"装备类别：{data[13]}  装备元素：{data[14]}  装备战力：{data[15]}",
                                "style": ["bold", "underline"]
                            },
                        ],
                        [{"tag": "img", "image_key": f'{download_img(data[4])}'}],
                    ]
                },
            }

            data1 = {
                "receive_id": chat_id,
                "msg_type": "post",
                "content": json.dumps(content)  # ✅ 这里必须转换成字符串
            }
            response = requests.post(url=send_url, headers=headers, json=data1, verify=True)
        else:
            zb = ''
            url = sql_data()[0]
            equip_key = data[2]
            headers1 = sql_data()[1]
            payload = "instance_name=cdb-sg-prod-starmaker-live-2-r2&db_name=monster&schema_name=&tb_name=&sql_content" \
                      f"=select+*+from++equip+where+equip_key+%3D\'{equip_key}\'"
            datas1 = requests.post(url=url, headers=headers1, data=payload, cookies=sql_data()[2])
            props_result = datas1.json()['data']['affected_rows']
            if props_result == 1:
                zb = f"装备表有对应合成的装备key：{data[2]}"
                time.sleep(3)
            else:
                zb = f"注意注意！！！装备表没有对应合成的装备key：{data[2]}"
                time.sleep(3)
            content = {
                "zh_cn": {
                    "title": f"注意注意注意！！！热血怪兽有新的碎片更新了！！！",
                    "content": [
                        [
                            {
                                "tag": "text",
                                "text": f'碎片名称:{data[1]}，碎片id:{data[0]}',
                                "style": ["bold", "underline"]
                            },
                        ],
                        [
                            {
                                "tag": "text",
                                "text": f"合成装备的key : {zb}，",
                                "style": ["bold", "underline"]
                            },
                        ],
                        [
                            {
                                "tag": "text",
                                "text": f"0级提供经验 : {data[4]}，品质：{data[5]}，合成整件需要数量'：{data[6]}，合成消耗元宝数"
                                        f"：{data[7]}",
                                "style": ["bold", "underline"]
                            },
                        ],
                        [
                            {
                                "tag": "text",
                                "text": f"碎片说明1：{data[8]} 碎片说明2：{data[9]}  碎片说明3：{data[10]}",
                                "style": ["bold", "underline"]
                            },
                        ],
                        [{"tag": "img", "image_key": f'{download_img(data[3])}'}],
                    ]
                },
            }

            data1 = {
                "receive_id": chat_id,
                "msg_type": "post",
                "content": json.dumps(content)  # ✅ 这里必须转换成字符串
            }
            response = requests.post(url=send_url, headers=headers, json=data1, verify=True)

    elif function == 'Testing_and_Development':
        name = ''
        if data[-1] == 'person_finished_data':
            name = '未完成需求'
        elif data[-1] == "person_incomplete_data":
            name = '已经完成需求'
        content = {
            "zh_cn": {
                "title": "注意注意注意！！！！",
                "content": [
                    [
                        {
                            "tag": "text",
                            "text": f"本次检测{name}的需求",
                            "style": ["bold"]
                        }
                    ],
                    [
                        {
                            "tag": "text",
                            "text": f"本次共出现{len(data) - 1}条问题数据",
                            "style": ["bold"]
                        },
                        {
                            "tag": "a",
                            "href": f"https://rg975ojk5z.feishu.cn/base/Xl3EbBH6daKFdYsL5Eac6l8rnDc?table=tble4vqz6RqVWndL&view=vewaGgEfMy",
                            "text": "详情链接点这里",
                            "style": ["bold", "italic"]
                        },
                    ]
                ]
            }
        }

        data1 = {
            "receive_id": chat_id,
            "msg_type": "post",
            "content": json.dumps(content)  # ✅ 这里必须转换成字符串
        }
        response = requests.post(url=send_url, headers=headers, json=data1, verify=True)

    elif function == 'Testing_and_Development1':
        content = {
            "zh_cn": {
                "title": "注意注意注意！！！！",
                "content": [
                    [
                        {
                            "tag": "text",
                            "text": f"测试数据：{line}",
                            "style": ["bold"]
                        }
                    ] for line in data
                ]
            }
        }

        data1 = {
            "receive_id": chat_id,
            "msg_type": "post",
            "content": json.dumps(content)  # ✅ 这里必须转换成字符串
        }
        response = requests.post(url=send_url, headers=headers, json=data1, verify=True)

    elif function == 'All_testing_and_Development':
        content = {
            "zh_cn": {
                "title": "本次执行总数据",
                "content": [
                    [
                        {
                            "tag": "text",
                            "text": f"版本需求：{data['版本需求']}",
                            "style": ["bold"]
                        },
                        {
                            "tag": "text",
                            "text": f"非版本需求：{data['非版本需求']}",
                            "style": ["bold"]
                        }
                    ]
                ]
            }
        }

        data1 = {
            "receive_id": chat_id,
            "msg_type": "post",
            "content": json.dumps(content)  # ✅ 这里必须转换成字符串
        }
        response = requests.post(url=send_url, headers=headers, json=data1, verify=True)


def start_send(function, datas):
    """
    :return: 进行发送
    """
    cid = get_chat_id(function)
    if function == 'horse':
        for i in range(len(datas)):
            print(datas[i][24])
            if datas[i][12]:
                send_msg(function, cid, 1, datas[i][0],
                         f'https://static.starmakerstudios.com/production/statics/horse/{datas[i][2]}',
                         [f'https://static.starmakerstudios.com/production/statics/horse/{datas[i][12]}', datas[i][24]],
                         datas[i][1], '')

            elif datas[i][31]:
                send_msg(function, cid, 1, datas[i][0],
                         f'https://static.starmakerstudios.com/production/statics/horse/{datas[i][2]}',
                         [f'https://static.starmakerstudios.com/production/statics/horse/{datas[i][31]}', datas[i][24]],
                         datas[i][1], '')

    elif function == 'pendant':
        for i in range(len(datas)):
            send_msg(function, cid, 1, datas[i][0],
                     f'https://gift-resource.starmakerstudios.com/pendant/{datas[i][4]}',
                     datas[i][13],
                     datas[i][1], datas[i])
    elif function == 'debris':
        for i in range(len(datas)):
            data_type = datas[i][4]
            if data_type == 2:
                props_id = datas[i][7].split(',')[0].split(':')[1]
                url = sql_data()[0]
                headers = sql_data()[1]
                payload = "instance_name=cdb-sg-prod-starmaker-live-r2&db_name=fb_live&schema_name=&tb_name=&sql_content" \
                          f"=select+*+from++static_props+where+props_id+%3D\'{props_id}\'"
                data = requests.post(url=url, headers=headers, data=payload, cookies=sql_data()[2])
                props_result = data.json()['data']['affected_rows']
                if props_result == 1:
                    send_msg(function, cid, 1, datas[i][0],
                             f'https://static.starmakerstudios.com/production/gift/debris/{datas[i][3]}',
                             '道具表中有此配置的id',
                             datas[i][1], '')
                elif props_result == 0:
                    send_msg(function, cid, 1, datas[i][0],
                             f'https://static.starmakerstudios.com/production/gift/debris/{datas[i][3]}',
                             '注意注意！！！！！碎片表中配错道具id',
                             datas[i][1], '')
            elif data_type == 1:
                props_id = datas[i][7].split(',')[0].split(':')[1]
                url = sql_data()[0]
                headers = sql_data()[1]
                payload = "instance_name=cdb-sg-prod-starmaker-live-r2&db_name=fb_live&schema_name=&tb_name=&sql_content" \
                          f"=select+*+from++gift+where+gift_id+%3D\'{props_id}\'"
                data = requests.post(url=url, headers=headers, data=payload, cookies=sql_data()[2])
                props_result = data.json()['data']['affected_rows']
                if props_result == 1:
                    send_msg(function, cid, 1, datas[i][0],
                             f'https://static.starmakerstudios.com/production/gift/debris/{datas[i][3]}',
                             '礼物表中有此配置的id',
                             datas[i][1], '')
                elif props_result == 0:
                    send_msg(function, cid, 1, datas[i][0],
                             f'https://static.starmakerstudios.com/production/gift/debris/{datas[i][3]}',
                             '注意注意！！！！！碎片表中配错礼物表id',
                             datas[i][1], '')
    elif function == 'ab-test':
        for i in range(len(datas)):
            test_group = []
            url = sql_data()[0]
            headers = sql_data()[1]
            payload = 'instance_name=cdb-sg-prod-abookserver-abtest&db_name=abtest&schema_name=&tb_name=&sql_content' \
                      '=select+a.id++%2Ca.name+%2Ca.start_ts+%2Ca.end_ts+%2Ca.create_man+%2Ca.status+%2Ca' \
                      '.description+%2Cc.description++%2Cd.name+%2Cd.probability++from+experiment+a+inner+join+audien' \
                      'ce_experiment+b+inner+join+audience+c++inner+join+variant+d+on+a.id+%3D+b.experiment_id+and+b.' \
                      f'audience_id+%3D+c.id+and+a.id+%3Dd.experiment_id+where+a.id+%3D+{datas[i][0]}'
            data = requests.post(url=url, headers=headers, data=payload, cookies=sql_data()[2])
            test_date = data.json()['data']['rows']
            for z in test_date:
                test_group.append(f"实验分组：{z[8]}，放量占比：{z[9]}")
            if test_date[0][5] == 0:
                test_date[0][5] = "实验中"
            elif test_date[0][5] == 3:
                test_date[0][5] = "实验未开始"
            if "=" in test_date[0][7] and ">" not in test_date[0][7]:
                test_date[0][7] = f"控制仅为当前版本{test_date[0][7]}，需注意！！！！！！！！"
            send_msg(function=function, chat_id=cid, horse_count=1,
                     horse_id=test_date[0][0],
                     horse_name=test_date[0][1],
                     horse_png=(stamp_to_time(test_date[0][2]), stamp_to_time(test_date[0][3])),
                     horse_pag=(test_date[0][4], test_date[0][5],
                                test_date[0][6], test_date[0][7], test_group),
                     data=''
                     )

    elif function == 'bubble':
        for i in range(len(datas)):
            if datas[i][2] == 3:
                datas[i][1] = f'类型：专属勋章       名称：{datas[i][1]}'
            elif datas[i][2] == 5:
                datas[i][1] = f'类型：个人卡片     名称：{datas[i][1]}'
            elif datas[i][2] == 7:
                datas[i][1] = f'类型：弹幕特效     名称：{datas[i][1]}'
            elif datas[i][2] == 6:
                datas[i][1] = f'类型：发言气泡      名称：{datas[i][1]}'
            # print(datas[i][1])
            if 'png' in datas[i][4]:
                send_msg(function, cid, 1, datas[i][0],
                         f'https://gift-resource.starmakerstudios.com/privilege/{datas[i][4]}',
                         'png格式无zip包',
                         datas[i][1], '')
                # print(datas[i][1])

            elif 'zip' in datas[i][4]:
                send_msg(function, cid, 1, datas[i][0],
                         f'https://gift-resource.starmakerstudios.com/privilege/{datas[i][11]}',
                         f'https://gift-resource.starmakerstudios.com/privilege/{datas[i][4]}',
                         datas[i][1], '')
    elif function == 'crazy_monster':
        for i in range(len(datas)):
            send_msg('crazy_monster', cid, 1, datas[i][0], datas[i][2], datas[i][3], datas[i][4], datas[i])

    elif function == 'Testing_and_Development':
        send_msg('Testing_and_Development', cid, 1, datas, datas, datas, datas, datas)

    elif function == 'Testing_and_Development1':
        send_msg('Testing_and_Development1', cid, 1, datas, datas, datas, datas, datas)
    elif function == 'All_testing_and_Development':
        send_msg('All_testing_and_Development', cid, 1, datas, datas, datas, datas, datas)


def stamp_to_time(times):
    dt = datetime.datetime.fromtimestamp(times)
    date_str = dt.strftime('%Y-%m-%d %H:%M:%S')
    return date_str
