from django.http import JsonResponse
from django.shortcuts import render
from myapp.utils.database_tools import execute_sql, package_execute


def dashboard_index(request):
    return render(request, 'dashboard.html')


def dashboard_translate_bar(request):
    android_new_list = []
    package_execute(android_new_list, 1, 1, 'newly_quantity')
    android_modify_list = []
    package_execute(android_modify_list, 1, 1, 'modify_quantity')
    ios_new_list =[]
    package_execute(ios_new_list, 1, 2, 'newly_quantity')
    ios_modify_list=[]
    package_execute(ios_modify_list, 1, 2, 'modify_quantity')
    server_new_list = []
    package_execute(server_new_list, 1, 3, 'newly_quantity')
    series = [
        {
            'name': 'android新增',
            'type': 'bar',
            'stack': 'Aa',
            'emphasis': {
                'focus': 'series'
            },
            'data': android_new_list[::-1]
        }, {
            'name': 'android修改',
            'type': 'bar',
            'stack': 'Aa',
            'emphasis': {
                'focus': 'series'
            },
            'data': android_modify_list[::-1]
        },
        {
            'name': 'ios新增',
            'type': 'bar',
            'stack': 'Ab',
            'emphasis': {
                'focus': 'series'
            },
            'data': ios_new_list[::-1]
        },
        {
            'name': 'ios修改',
            'type': 'bar',
            'stack': 'Ab',
            'emphasis': {
                'focus': 'series'
            },
            'data': ios_modify_list[::-1]
        },
        {
            'name': 'server新增',
            'type': 'bar',
            'stack': 'Ac',
            'emphasis': {
                'focus': 'series'
            },
            'data': server_new_list[::-1]
        },
    ]
    date_list = []
    package_execute(date_list, 2, 2, 'quantity')
    result = {
        "status": True,
        "data": {
            # "legend": legend,
            "data_list": series,
            "date_list": date_list[::-1]
        }
    }
    print(series)
    return JsonResponse(result)


def dashboard_language_count(request):
    """
    :param request: 请求表头总多语言数量
    :return: 返回值
    """
    android_count = execute_sql(1, 1, 'quantity')[0]
    ios_count = execute_sql(1, 2, 'quantity')[0]
    server_count = execute_sql(1, 3, 'quantity')[0]
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
    total = len(execute_sql(1, 2, 'quantity'))
    data = {
        "status": True,
        'data': total
    }
    return JsonResponse(data)


def dashboard_translate_pie(request):
    """
    :param request: 饼图数据
    :return: 返回各项总数
    """
    android = execute_sql(1, 1, "quantity")[0][0]
    ios = execute_sql(1, 2, "quantity")[0][0]
    server = execute_sql(1, 3, "quantity")[0][0]
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
    return JsonResponse(result)
