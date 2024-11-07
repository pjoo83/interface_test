from django.http import JsonResponse
from myapp.utils.data import sql_data
import requests
from myapp.utils.database_tools import execute_sql
from myapp.utils.feishu_send_message import start_send


def debris_mount_increase(request):
    url = sql_data()[0]
    headers = sql_data()[1]
    payload = "instance_name=cdb-sg-prod-starmaker-live-r2&db_name=fb_live&schema_name=&tb_name=&sql_content=select" \
              "+*+from++static_debris+where+debris_type+%3D2+order+by+debris_id+desc+limit+10"
    data = requests.post(url=url, headers=headers, data=payload)
    new_data = data.json()['data']['rows'][0]
    Mount_data = resource_check(3, 3)[0][2]
    if new_data[0] == Mount_data:
        print('碎片数据相同，没有新增')
        return JsonResponse({'code': 200,
                             'msg': '数据相同，没有更新'})
    else:
        datas = data.json()['data']['rows']
        pag_url = f'https://static.starmakerstudios.com/production/gift/debris/{new_data[3]}'
        # 取出道具ID，再去id库中查
        datas_num = new_data[0] - Mount_data
        start_send(function='debris', datas=datas[0:datas_num])
        content = [new_data[0], new_data[1], pag_url]
        execute_sql(sid=4, channel_id=3, content=content[0], name=content[1], record_pag_url=new_data[7],
                    record_png_url=content[2])
        return JsonResponse({
            'code': 200,
            'msg': '有更新，有更新'
        })


def resource_check(sid, record_id):
    data = execute_sql(sid=sid, channel_id=record_id)
    return data
