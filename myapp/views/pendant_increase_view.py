from django.http import JsonResponse
from myapp.utils.data import sql_data
import requests
from myapp.utils.database_tools import execute_sql
from myapp.utils.feishu_send_message import start_send


def pendant_mount_increase(request):
    url = sql_data()[0]
    headers = sql_data()[1]
    payload = "instance_name=cdb-sg-prod-starmaker-live-r2&db_name=fb_live&schema_name=&tb_name=&sql_content" \
              "=select+*+from+static_pendant+order+by+pendant_id+desc+limit+20"
    data = requests.post(url=url, headers=headers, data=payload)
    new_data = data.json()['data']['rows'][0]
    Mount_data = resource_check(3, 2)[0][2]
    if new_data[0] == Mount_data:
        print('挂件数据相同，没有新增')
        return JsonResponse({'code': 200,
                             'msg': '数据相同，没有更新'})
    else:
        datas = data.json()['data']['rows']
        pag_url = f'https://gift-resource.starmakerstudios.com/pendant/{new_data[2]}'
        datas_num = new_data[0] - Mount_data
        start_send(function='pendant', datas=datas[0:datas_num])
        content = [new_data[0], new_data[1], pag_url]
        execute_sql(sid=4, channel_id=2, content=content[0], name=content[1], record_pag_url='',
                    record_png_url=content[2])
        return JsonResponse({
            'code': 200,
            'msg': '有更新，有更新'
        })


def resource_check(sid, record_id):
    data = execute_sql(sid=sid, channel_id=record_id)
    return data
