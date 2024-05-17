from django.http import JsonResponse
from django.shortcuts import render

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
