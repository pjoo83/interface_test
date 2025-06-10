from django.http import JsonResponse
from myapp.utils.data import sql_data
import requests
from myapp.utils.database_tools import execute_sql
from myapp.utils.feishu_send_message import start_send
from myapp.utils.feishu_project import get_check
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def td_testing_calculations(request):
    """
    研发测试比
    """
    if request.method == "GET":
        uid = request.GET.get("uid")
        year = request.GET.get("year")
        day = request.GET.get("day")
        month = request.GET.get("month")
        print(uid, year, day, month)
        data = get_check(uid=int(uid), year=int(year), day=int(day), month=int(month))

        return JsonResponse({"status": 0, "msg": data})
