from django.http import JsonResponse
import requests
from ..utils.database_tools import execute_sql
from ..utils.feishu_send_message import start_send


def resource_mount_increase(request):
    url = 'https://sql.ushow.media/query/'
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': 'csrftoken=yPmniuAZeEdZnlrT7OekdcQPHkft3Hd78Q0c2hmF9bBAYHCuGILkvoFt7X4NOAVB; '
                  'sessionid=wpp9w8ipqmgarsl0up49kr52vj2pmnhr; _ga_Y5QLWEHNZ4=GS1.1.1729134537.7.0.1729134537.60.0.0; '
                  '_ga=GA1.1.1792866753.1713751715; sessionid=wpp9w8ipqmgarsl0up49kr52vj2pmnhr; '
                  'tgw_l7_route=7a3b5e35664bcb9b34e8b8e8ba155169',
        'origin': 'https://sql.ushow.media',
        'priority': 'u=1, i',
        'referer': 'https://sql.ushow.media/sqlquery/',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'x-csrftoken': 'yPmniuAZeEdZnlrT7OekdcQPHkft3Hd78Q0c2hmF9bBAYHCuGILkvoFt7X4NOAVB',
        'x-requested-with': 'XMLHttpRequest'
    }
    payload = "instance_name=cdb-sg-prod-starmaker-live-r2&db_name=fb_live&schema_name=&tb_name=horse&sql_content" \
              "=select+*+from++horse+order+by+horse_id+desc%3B&limit_num=2"
    data = requests.post(url=url, data=payload, headers=headers)
    Mount_data = resource_check(3, 1)[0][2]
    new_data = data.json()['data']['rows'][0]
    if Mount_data == new_data[0]:
        return JsonResponse({"code": "200",
                             "msg": '数据相同，没有新增'})
    else:
        # start_send('注意！！注意！！！有新增坐骑，请注意测试！！！,'
        #            f'新增id：{new_data[0]},'
        #            f'新增资源名：{new_data[1]},'
        #            f'请前往{https://prod.ushow.media/internal/horse/index?page=1}查看')
        content = [new_data[0], new_data[1]]
        execute_sql(sid=4, channel_id=1, content=content[0], name=content[1])
        return JsonResponse({"code": "200",
                             "msg": '注意！！注意！！！有新增坐骑，请注意测试！！！,'
                                    f'新增id：{content[0]},'
                                    f'新增资源名：{content[1]}'})


def resource_check(sid, record_id):
    data = execute_sql(sid=sid, channel_id=record_id)
    return data
