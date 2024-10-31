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
        'cookie': 'csrftoken=q26vhXy7GQz0ikCy1D5xsBzGKBMQnfwQ7YHZETOgNlCNqjCzk7h7i8lbjAPR6e1N; sessionid=z91tcdxx1pdyj3iovo3j3k6mzmbzgye6; sessionid=z91tcdxx1pdyj3iovo3j3k6mzmbzgye6; tgw_l7_route=7a3b5e35664bcb9b34e8b8e8ba155169',
        'origin': 'https://sql.ushow.media',
        'priority': 'u=1, i',
        'referer': 'https://sql.ushow.media/sqlquery/',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'x-csrftoken': 'q26vhXy7GQz0ikCy1D5xsBzGKBMQnfwQ7YHZETOgNlCNqjCzk7h7i8lbjAPR6e1N',
        'x-requested-with': 'XMLHttpRequest'
    }
    payload = "instance_name=cdb-sg-prod-starmaker-live-r2&db_name=fb_live&schema_name=&tb_name=horse&sql_content" \
              "=select+*+from++horse+order+by+horse_id+desc%3B&limit_num=2"
    data = requests.post(url=url, data=payload, headers=headers)
    Mount_data = resource_check(3, 1)[0][2]
    new_data = data.json()['data']['rows'][0]
    if Mount_data == new_data[0]:
        print('数据相同，没有新增')
        return JsonResponse({"code": "200",
                             "msg": '数据相同，没有新增111'})
    else:
        start_send(horse_count=new_data[0] - Mount_data,
                   horse_id=new_data[0],
                   horse_name=new_data[1],
                   horse_png =f"https://static.starmakerstudios.com/production/statics/horse/{new_data[2]}",
                   horse_pag= f"https://static.starmakerstudios.com/production/statics/horse/{new_data[12]}")
        pag_url = f'https://static.starmakerstudios.com/production/statics/horse/{new_data[12]}'
        png_url = f'https://static.starmakerstudios.com/production/statics/horse/{new_data[2]}'
        content = [new_data[0], new_data[1],
                   pag_url,
                   png_url]
        execute_sql(sid=4, channel_id=1, content=content[0], name=content[1], record_pag_url=content[3],
                    record_png_url=content[2])
        return JsonResponse({"code": "200",
                             "msg": f'新增id：{content[0]},'
                                    f'新增资源名：{content[1]}'})


def resource_check(sid, record_id):
    data = execute_sql(sid=sid, channel_id=record_id)
    return data
