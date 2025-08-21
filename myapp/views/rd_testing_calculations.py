from django.http import JsonResponse
from myapp.utils.data import sql_data
import requests
from myapp.utils.database_tools import execute_sql
from myapp.utils.feishu_send_message import start_send
from myapp.utils.feishu_project import get_check,get_check2
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def td_testing_calculations(request):
    """
    研发测试比
    """
    if request.method == "GET":
        date = request.GET.get("date", None)
        date_type = request.GET.get("date_type")
        uid = request.GET.get("uid", None)  # 默认 None
        finished_time = request.GET.get('finished_time', None)

        # 判断参数是否有效
        if not date_type:
            return JsonResponse({"code": 200,
                                 "msg": "缺少必要参数"}, json_dumps_params={'ensure_ascii': False})
        # 如果传了 uid，转为 int，否则为 None
        uid = int(uid) if uid else None

        if date_type in ['person_finished_data', 'person_incomplete_data']:
            data = get_check(date=date, uid=uid, date_type=date_type, finished_time=finished_time)
        else:
            return JsonResponse({"error": "不支持的 date_type 类型"}, status=400,
                                json_dumps_params={'ensure_ascii': False})

        start_send("All_testing_and_Development", data)
        return JsonResponse({"code": 200,
                             "msg": data}, json_dumps_params={'ensure_ascii': False})


def no_test_time(request):
    if request.method == "GET":
        date= request.GET.get("date", None)
        finished_time = request.GET.get('finished_time', None)
        get_check2(date=date, uid=None, date_type="person_incomplete_data", finished_time=finished_time)
        return JsonResponse({"code": 200,
                             "msg": "查询完毕"}, json_dumps_params={'ensure_ascii': False})

