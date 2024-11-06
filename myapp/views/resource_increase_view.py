from django.http import JsonResponse
import requests
from myapp.utils.database_tools import execute_sql
from myapp.utils.feishu_send_message import start_send
from myapp.utils.data import sql_data


def resource_mount_increase(request):
    url = sql_data()[0]
    headers = sql_data()[1]
    payload = "instance_name=cdb-sg-prod-starmaker-live-r2&db_name=fb_live&schema_name=&tb_name=horse&sql_content" \
              "=select+*+from++horse+order+by+horse_id+desc%3B&limit_num=10"
    data = requests.post(url=url, data=payload, headers=headers)
    Mount_data = resource_check(3, 1)[0][2]
    new_data = data.json()['data']['rows'][0]
    if Mount_data == new_data[0]:
        print('数据相同，没有新增')
        return JsonResponse({"code": "200",
                             "msg": '数据相同，没有新增111'})
    else:
        datas = data.json()['data']['rows']
        datas_num = new_data[0] - Mount_data
        start_send(function='horse', datas=datas[0:datas_num])
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
