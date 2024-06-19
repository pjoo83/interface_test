from django.http import JsonResponse
from myapp.models import interface_result
import base64


def interface_insert_data(request):
    """
    :param request: 插入接口数据
    :return:
    """
    if request.method == "GET":
        data = {"code": 206, "msg": "请用post请求"}
        return JsonResponse(data)
    elif request.method == 'POST':
        token = request.POST.get("token")
        decoded_string = base64.urlsafe_b64decode(token).decode('utf-8')
        if decoded_string != 'api_qa_insert_interface_result':
            data = {"code": 403, "msg": "缺少认证内容"}
            return JsonResponse(data)
        else:
            total_interface = request.POST.get("total_interface")
            total_pass = request.POST.get('total_pass')
            total_fail = request.POST.get('total_fail')
            total_unexpected = request.POST.get('total_unexpected')
            passing_rate = request.POST.get('passing_rate')
            execution_time = request.POST.get('execution_time')
            if total_interface == '' or total_pass == '' or total_fail == '' or \
                    total_unexpected == '' or passing_rate == '' or execution_time == '':
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
    ordered_queryset = interface_result.objects.order_by('-id')
    book = ordered_queryset.values_list('total_interface', 'total_pass', 'total_fail', 'passing_rate',
                                        'datatime')[:6]
    total_interface = [int(item[0]) for item in book][::-1]
    total_pass = [int(item[1]) for item in book][::-1]
    total_fail = [int(item[2]) for item in book][::-1]
    passing_rate = [float(item[3]) for item in book][::-1]
    datatime = [item[4] for item in book][::-1]
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
