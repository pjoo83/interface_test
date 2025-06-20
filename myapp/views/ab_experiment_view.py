from django.http import JsonResponse
import requests
from myapp.utils.database_tools import execute_sql
from myapp.utils.feishu_send_message import start_send
from myapp.utils.data import sql_data


def ab_experiment_increase(request):
    url = sql_data()[0]
    headers = sql_data()[1]
    payload = "instance_name=cdb-sg-prod-abookserver-abtest&db_name=abtest&schema_name" \
              "=&tb_name=&sql_content=select+distinct+id+from+experiment++order+by+id+desc+limit+5%3B%0A&limit_num=0"

    data = requests.post(url=url, headers=headers, data=payload, cookies=sql_data()[2])
    new_data = data.json()['data']['rows'][0]
    Mount_data = resource_check(3, 4)[0][2]
    if Mount_data == new_data[0]:
        print('ab实验没有新增')
        return JsonResponse({"code": 200,
                             "msg": 'ab实验没有新增'})
    else:
        datas = data.json()['data']['rows']
        datas_num = new_data[0] - Mount_data
        start_send(function='ab-test', datas=datas[0:datas_num])
        execute_sql(sid=4, channel_id=4, content=new_data[0], name='', record_pag_url='',
                    record_png_url='')
        return JsonResponse({
            'code': 200,
            'msg': '有更新，有更新'
        })


def resource_check(sid, record_id):
    data = execute_sql(sid=sid, channel_id=record_id)
    return data
