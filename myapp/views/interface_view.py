from django.http import JsonResponse
from myapp.models import interface_result


def interface_insert_data(request):
    """
    :param request: 插入接口数据
    :return:
    """
    if request.method == "GET":
        data = {"code": 206, "msg": "请用post请求"}
        return JsonResponse(data)
    elif request.method == 'POST':
        if request.POST.get("token") != 'api_qa_inter':
            data = {"code": 403, "msg": "缺少认证内容"}
            return JsonResponse(data)
        else:
            total_interface = request.POST.get("total_interface")
            total_pass = request.POST.get('total_pass')
            total_fail = request.POST.get('total_fail')
            total_unexpected = request.POST.get('total_unexpected')
            passing_rate = request.POST.get('passing_rate')
            execution_time = request.POST.get('execution_time')
            if total_interface == 'null' or total_pass == 'null' or total_fail == 'null' or \
                    total_unexpected == 'null' or passing_rate == 'null' or execution_time == 'null':
                data = {"code": 204, "msg": "参数缺少，请检查上传的参数是否正常"}
            else:
                insert_data = interface_result(
                    total_interface=total_interface,
                    total_pass=total_pass,
                    total_fail=total_fail,
                    total_unexpected=total_unexpected,
                    passing_rate=passing_rate,
                    execution_time=execution_time
                )
                insert_data.save()
                data = {"code": 200, "msg": "数据插入成功"}
            return JsonResponse(data)


def dashboard_executions_interface_total(request):
    """
    :param request:
    :return: 返回执行次数
    """
    count = interface_result.objects.count()
    data = {
        'status': True,
        'count': count
    }
    return JsonResponse(data)


def dashboard_executions_interface_detail(request):
    """
    :param request:
    :return: 返回接口测试的执行的数据
    """
    book = interface_result.objects.values_list('total_interface', 'total_pass', 'total_fail', 'passing_rate',
                                                'datatime')
    total_interface = [int(item[0]) for item in book]
    total_pass = [int(item[1]) for item in book]
    total_fail = [int(item[2]) for item in book]
    passing_rate = [float(item[3]) for item in book]
    datatime = [item[4] for item in book]
    date_list = []
    for day in datatime:
        date_list.append(f"{day.year}-{day.month}-{day.day}")
    data = {
        "data": {'total_interface': total_interface,
                 'total_pass': total_pass,
                 'total_fail': total_fail,
                 'passing_rate': passing_rate,
                 'date_list': date_list
                 },
        "status": True,
    }

    return JsonResponse(data)
