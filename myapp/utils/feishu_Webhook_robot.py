import requests
import json
from myapp.utils.feishu_data import Feishu_data

fei = Feishu_data()


def feishu_card_rot(data_list):
    """
    :return:
    """
    url = "https://open.feishu.cn/open-apis/bot/v2/hook/102f3e05-d3c1-49b3-863b-379b7601427c"
    pro_url ='https://open.feishu.cn/open-apis/bot/v2/hook/dfa244c7-40c6-4ecf-b82e-7f2b603017c7'
    if data_list[5] == 'all':
        if data_list[1] is None:
            uid = '本次检测所有测试同学'
        else:
            uid = f'本次检测用户{fei.qa_list[data_list[1]][1]}'
        if data_list[2] == 'person_incomplete_data':
            date_type = '还未完成的需求汇总数据'
            date_url = 'https://rg975ojk5z.feishu.cn/base/Xl3EbBH6daKFdYsL5Eac6l8rnDc?table=tble4vqz6RqVWndL&view' \
                       '=vewaGgEfMy'
        elif data_list[2] == 'person_finished_data':
            date_type = '已完成的需求汇总数据'
            date_url = 'https://rg975ojk5z.feishu.cn/base/Xl3EbBH6daKFdYsL5Eac6l8rnDc?table=tblub91U25WmQaaN&view' \
                       '=vewD2HVVxN'
        if data_list[4] is None:
            time = '本次检测20250101至今'
        elif data_list[4] is not None:
            if data_list[3] is None:
                time = f'本次检测{data_list[4]}至今'
            else:
                time = f'本次检测{data_list[4]}至{data_list[3]}'

    else:
        if data_list[-1] is None:
            uid = '本次检测所有测试同学'
        else:
            print(data_list[-1])
            uid = f'本次检测用户{fei.qa_list[data_list[-1]][1]}'
        if data_list[-3] == 'person_incomplete_data':
            date_type = '还未完成的需求据详细数据'
            date_url = 'https://rg975ojk5z.feishu.cn/base/Xl3EbBH6daKFdYsL5Eac6l8rnDc?table=tble4vqz6RqVWndL&view' \
                       '=vewaGgEfMy'
        elif data_list[-3] == 'person_finished_data':
            date_type = '已完成的需求详细数据'
            date_url = 'https://rg975ojk5z.feishu.cn/base/Xl3EbBH6daKFdYsL5Eac6l8rnDc?table=tblub91U25WmQaaN&view' \
                       '=vewD2HVVxN'
        if data_list[-5] is None:
            time = '本次检测20250101至今'
        elif data_list[-5] is not None:
            if data_list[-4] is None:
                time = f'本次检测{data_list[-5]}至今'
            else:
                time = f'本次检测{data_list[-5]}至{data_list[-4]}'

    elements = [
        {
            "tag": "markdown",
            "content": f"检查对象：{uid}",
            "text_align": "right",
            "text_size": "normal_v2",
            "margin": "0px 0px 0px 0px"
        },
        {
            "tag": "markdown",
            "content": f"本次检测时间：{time}",
            "text_align": "right",
            "text_size": "normal_v2",
            "margin": "0px 0px 0px 0px"
        },
        {
            "tag": "button",
            "text": {
                "tag": "plain_text",
                "content": "点击进入详情页"
            },
            "type": "default",
            "width": "default",
            "size": "medium",
            "behaviors": [
                {
                    "type": "open_url",
                    "default_url": f"{date_url}",
                    "pc_url": "",
                    "ios_url": "",
                    "android_url": ""
                }
            ],
            "margin": "0px 0px 0px 0px"
        }]
    if data_list[-1] == "all":
        elements.insert(0, {
            "tag": "markdown",
            "content": f"版本需求：{data_list[0]['版本需求']}",
            "text_align": "left",
            "text_size": "normal_v2",
            "margin": "0px 0px 0px 0px"
        })
        elements.insert(1, {
            "tag": "markdown",
            "content": f"非版本需求：{data_list[0]['非版本需求']}",
            "text_align": "left",
            "text_size": "normal_v2",
            "margin": "0px 0px 0px 0px"
        },
                        )
        elements.insert(2, {
            "tag": "markdown",
            "content": f"总需求：{data_list[0]['总需求数']}",
            "text_align": "left",
            "text_size": "normal_v2",
            "margin": "0px 0px 0px 0px"
        })
    else:
        elements.insert(0, {
            "tag": "markdown",
            "content": f"本次检测的问题数据数量：{len(data_list) - 4}",
            "text_align": "left",
            "text_size": "normal_v2",
            "margin": "0px 0px 0px 0px"
        })
    payload = json.dumps({
        "msg_type": "interactive",
        "card": {
            "schema": "2.0",
            "config": {
                "update_multi": True,
                "style": {
                    "text_size": {
                        "normal_v2": {
                            "default": "normal",
                            "pc": "normal",
                            "mobile": "heading"
                        }
                    }
                }
            },
            "body": {
                "direction": "vertical",
                "padding": "12px 12px 12px 12px",
                "elements": elements
            },
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": f"本次检测:{date_type}"
                },
                "subtitle": {
                    "tag": "plain_text",
                    "content": ""
                },
                "template": "blue",
                "padding": "12px 12px 12px 12px"
            }
        }
    })

    # headers = {
    #     'Content-Type': 'application/json'
    # }
    headers = fei.content_type1
    requests.request("POST", url, headers=headers, data=payload)

# feishu_card_rot()
if __name__ == '__main__':
    feishu_card_rot(["直播间带玩游戏。['ou_baf2770fc108d7429e4fe97f324a9517']。测试: 5, 研发: 13,"
                     "测试用例：0。2.6。https://project.feishu.cn/wangmao12345678/story/detail/6169909600?parentUrl"
                     "=%2Fwangmao12345678%2Fstory%2Fhomepage&openScene=4。", 20250701, None, 'person_finished_data',
                     'detail', '7117238460611624964'])