from django.http import JsonResponse
from django.shortcuts import render
from ..utils.database_tools import execute_sql


def dashboard_index(request):
    return render(request, 'dashboard.html')


def dashboard_translate_bar(request):
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
    date_list = ['一月', '二月', '三月', '四月', '五月', '六月']

    result = {
        "status": True,
        "data": {
            "legend": legend,
            "data_list": data_list,
            "date_list": date_list
        }
    }
    return JsonResponse(result)


def dashboard_language_count(request):
    """
    :param request:
    :return: 返回值
    """
    android_count = execute_sql(1, 'quantity')[0]
    ios_count = execute_sql(2, 'quantity')[0]
    server_count = execute_sql(3, 'quantity')[0]
    # unity_count = execute_sql(4, 'quantity')[0]
    data = {
        'android': android_count,
        'ios': ios_count,
        'server': server_count,
        # 'unity_count': unity_count
    }
    result = {
        "status": True,
        'data': data
    }

    return JsonResponse(result)


def dashboard_executions_total(request):
    """
    :param request:
    :return: 返回脚本执行次数
    """
    total = len(execute_sql(2, 'quantity'))
    data = {
        "status": True,
        'data': total
    }
    return JsonResponse(data)


def dashboard_translate_pie(request):
    """
    :param request:
    :return: 返回各项总数
    """
    android = execute_sql(1, "quantity")[0][0]
    ios = execute_sql(2, "quantity")[0][0]
    server = execute_sql(3, "quantity")[0][0]
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
