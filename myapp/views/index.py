from django.http import JsonResponse
from django.shortcuts import render
from ..utils.database_tools import execute_sql


def index(request):
    return render(request, 'index.html')


def translate_bar(request):
    legend = ['新增', '修改']
    new_list = []
    new = execute_sql(2, 'newly_quantity')
    for i in new:
        new_list.append(i[0])
    modify_list = []
    modify = execute_sql(2, 'modify_quantity')
    for i in modify:
        modify_list.append(i[0])
    data_list = [
        {
            "name": 'fuck',
            "type": 'bar',
            "data": new_list
        },
        {
            "name": 'curry',
            "type": 'bar',
            "data": modify_list
        }
    ]
    date_list = ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '一月', '二月', '三月', '四月', '五月', '六月',
                 '七月', '五月', '六月',
                 '七月', '五月', '六月',
                 '七月']

    result = {
        "status": True,
        "data": {
            "legend": legend,
            "data_list": data_list,
            "date_list": date_list
        }
    }
    return JsonResponse(result)


def translate_pie(request):
    android = execute_sql(1, "quantity")[0][0]
    ios = execute_sql(2, "quantity")[0][0]
    server= execute_sql(3,"quantity")[0][0]
    data = [
        {'value': android, 'name': '安卓'},
        {'value': ios, 'name': 'ios'},
        {'value': server, 'name': 'server'},
        {'value': 484, 'name': 'unity'},
        {'value': 300, 'name': 'flutter'}
    ]
    result = {
        "status": True,
        "data": {
            "data_list": data}
    }
    print(result)
    return JsonResponse(result)
