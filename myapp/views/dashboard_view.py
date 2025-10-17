from django.http import JsonResponse
from django.shortcuts import render
import ast
from myapp.models import test_record_result, resource_date_record
from myapp.utils.database_tools import execute_sql, package_execute


def dashboard_index(request):
    return render(request, 'dashboard.html')


def dashboard_translate_bar(request):
    android_new_list = []
    package_execute(android_new_list, 1, 1, 'newly_quantity')
    android_modify_list = []
    package_execute(android_modify_list, 1, 1, 'modify_quantity')
    ios_new_list = []
    package_execute(ios_new_list, 1, 2, 'newly_quantity')
    ios_modify_list = []
    package_execute(ios_modify_list, 1, 2, 'modify_quantity')
    server_new_list = []
    package_execute(server_new_list, 1, 3, 'newly_quantity')
    flutter_new_list = []
    package_execute(flutter_new_list, 1, 5, 'newly_quantity')
    print(ios_new_list)
    series = [
        {
            'name': 'android新增',
            'type': 'bar',
            'stack': 'Aa',
            'emphasis': {
                'focus': 'series'
            },
            'data': android_new_list[:6]
        }, {
            'name': 'android修改',
            'type': 'bar',
            'stack': 'Aa',
            'emphasis': {
                'focus': 'series'
            },
            'data': android_modify_list[:6]
        },
        {
            'name': 'ios新增',
            'type': 'bar',
            'stack': 'Ab',
            'emphasis': {
                'focus': 'series'
            },
            'data': ios_new_list[:6]
        },
        {
            'name': 'ios修改',
            'type': 'bar',
            'stack': 'Ab',
            'emphasis': {
                'focus': 'series'
            },
            'data': ios_modify_list[:6]
        },
        {
            'name': 'server新增',
            'type': 'bar',
            'stack': 'Ac',
            'emphasis': {
                'focus': 'series'
            },
            'data': server_new_list[:6]
        },
        {
            'name': 'flutter新增',
            'type': 'bar',
            'stack': 'Ad',
            'emphasis': {
                'focus': 'series'
            },
            'data': flutter_new_list[:6]
        },
    ]
    date_list = []
    package_execute(date_list, 2, 2, 'quantity')
    result = {
        "status": True,
        "data": {
            # "legend": legend,
            "data_list": series,
            "date_list": date_list
        }
    }
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
    flutter_count = execute_sql(1, 5, "quantity")[0][0]
    data = {
        'android': android_count,
        'ios': ios_count,
        'server': server_count,
        # 'unity_count': unity_count
        'flutter': flutter_count
    }
    result = {
        "status": True,
        'data': data
    }
    return JsonResponse(result)


def dashboard_executions_translate_total(request):
    """
    :param request:
    :return: 返回脚本执行次数
    """
    total = len(execute_sql(1, 2, 'newly_quantity'))
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
    flutter = execute_sql(1, 5, "quantity")[0][0]
    data = [
        {'value': android, 'name': '安卓'},
        {'value': ios, 'name': 'ios'},
        {'value': server, 'name': 'server'},
        # {'value': 484, 'name': 'unity'},
        {'value': flutter, 'name': 'flutter'}
    ]
    result = {
        "status": True,
        "data": {
            "data_list": data}
    }
    return JsonResponse(result)


def dashboard_qa_data(request):
    """
    :param request: 测试数据
    :return:
    """
    query_time = test_record_result.objects.filter(type='测试数据').order_by('-id').first()
    data_record = query_time.data_record
    user_data = ast.literal_eval(data_record)
    qa_datas = []
    for i in user_data:
        qa_datas.append({'name': i['user'], 'num': i['已承接的需求数量']})
    clean_data = [item for item in qa_datas if isinstance(item, dict)]
    # 按 num 从大到小排序
    sorted_data = sorted(clean_data, key=lambda x: x['num'], reverse=True)

    names = [item['name'] for item in sorted_data]
    nums = [item['num'] for item in sorted_data]
    return JsonResponse({
        'xAxis': names,
        'series': nums,
    })


def dashboard_resource_show(request):
    """
    :return: 返回当前资源id
    """
    resource = resource_date_record.objects.filter(resource_name='resource').order_by('-id')[:10]
    pendent = resource_date_record.objects.filter(resource_name='pendent').order_by('-id')[:10]
    debris = resource_date_record.objects.filter(resource_name='debris').order_by('-id')[:10]
    ab = resource_date_record.objects.filter(resource_name='ab').order_by('-id')[:10]
    bubble = resource_date_record.objects.filter(resource_name='bubble').order_by('-id')[:10]
    numbers_resource = [r.resource_sum for r in resource]
    numbers_pendent = [p.resource_sum for p in pendent]
    numbers_debris = [d.resource_sum for d in debris]
    numbers_ab = [a.resource_sum for a in ab]
    numbers_bubble = [b.resource_sum for b in bubble]

    print(numbers_bubble, numbers_ab, numbers_debris, numbers_pendent, numbers_resource)
    date = {'numbers_resource': numbers_resource,
            'numbers_pendent': numbers_pendent,
            'numbers_debris': numbers_debris,
            'numbers_ab': numbers_ab,
            'numbers_bubble': numbers_bubble,
            }
    return JsonResponse({"code": 200, 'date': date})
