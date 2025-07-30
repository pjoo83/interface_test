from django.http import JsonResponse
from django.shortcuts import render
import json
from myapp.models import test_record_result
from datetime import date
import ast
from myapp.utils import feishu_project


def user_statistics_view(request):
    # 示例数据：你可以从数据库或其他接口获取并替换这里
    query_time = test_record_result.objects.all().order_by('-id').first()
    if query_time:
        data_record = query_time.data_record
        datatime = str(query_time.datatime)
        today = str(date.today().strftime("%Y-%m-%d"))

        if datatime == today:
            user_data = ast.literal_eval(data_record)
            return render(request, "test_completion_rate_record.html", {"user_data": json.dumps(user_data, ensure_ascii=False)})
        else:
            print('数据未更新,请等待更新')
            new_date= feishu_project.get_all_user_finished_demand(create_date=20250101, uid=None, finished_time=None)
            if new_date:
                insert_data = test_record_result(
                    data_record=new_date[0],
                    all_record_num=new_date[1]
                )
                insert_data.save()
                print('数据已更新')
                return JsonResponse({"status": False, "message": "正在更新进入数据"})
            else:
                return JsonResponse({"status": False, "message": "没有数据"})
