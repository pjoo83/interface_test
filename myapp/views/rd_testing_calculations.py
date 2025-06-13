from django.http import JsonResponse
from myapp.utils.data import sql_data
import requests
from myapp.utils.database_tools import execute_sql
from myapp.utils.feishu_send_message import start_send
from myapp.utils.feishu_project import get_check
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def td_testing_calculations(request):
    """
    研发测试比
    """
    if request.method == "GET":
        date = request.GET.get("date")
        date_type = request.GET.get("date_type")
        data = ""
        if request.GET.get("uid"):
            uid = request.GET.get("uid")
            if date_type == 'person_finished_data':
                data = get_check(date=date, uid=int(uid), date_type=date_type)
            elif date_type == 'person_incomplete_data':
                data = get_check(date=date, uid=int(uid), date_type=date_type)
        else:
            if date_type == 'person_finished_data':
                data = get_check(date=date, uid=None, date_type=date_type)
            elif date_type == 'person_incomplete_data':
                data = get_check(date=date, uid=None, date_type=date_type)
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False})
