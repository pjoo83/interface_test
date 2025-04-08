from django.http import JsonResponse
from myapp.utils.data import sql_data
import requests
from myapp.utils.database_tools import execute_sql
from myapp.utils.feishu_send_message import start_send


def check_crazy_monster_all(request):
    check_equip(equip_data, 6)
    check_equip(fragments, 7)
    return JsonResponse({
        "code": 200
    })


def check_equip(equip_datas, ids):
    url = sql_data()[0]
    headers = sql_data()[1]
    payload = equip_datas[0]
    data = requests.post(url=url, headers=headers, data=payload)
    new_data = data.json()['data']['rows'][0]
    Mount_data = resource_check(3, equip_datas[2])[0][2]
    if new_data[0] == Mount_data:
        print(equip_datas[1])
        return JsonResponse({'code': 200,
                             'msg': '数据相同，没有更新'})
    else:
        datas = data.json()['data']['rows']
        pag_url = new_data[4]
        # 取出道具ID，再去id库中查
        datas_num = new_data[0] - Mount_data
        start_send(function='crazy_monster', datas=datas[0:datas_num])
        content = [new_data[0], new_data[1], pag_url]
        execute_sql(sid=4, channel_id=ids, content=content[0], name=content[1], record_pag_url=new_data[7],
                    record_png_url=content[2])
        return JsonResponse({
            'code': 200,
            'msg': '有更新，有更新'
        })


def resource_check(sid, record_id):
    data = execute_sql(sid=sid, channel_id=record_id)
    return data


equip_data = ["instance_name=cdb-sg-prod-starmaker-live-2-r2&db_name=monster&schema_name=&tb_"
              "name=&sql_content=select""+*+from++equip+order+by+id+desc+limit+100",
              '热血怪兽装备数据相同，没有新增', 6]

fragments = ["instance_name=cdb-sg-prod-starmaker-live-2-r2&db_name=monster&schema_name=&tb_"
             "name=&sql_content=select""+*+from++fragments+order+by+fragments_id+desc+limit+100",
             '热血怪兽碎片数据相同，没有新增', 7]
