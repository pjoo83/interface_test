from django.http import JsonResponse
from myapp.models import ui_result, channel_ui
import base64


def ui_android_insert_data(request):
    """
    :param request: 插入安卓ui测试结果数据
    :return:
    """
    if request.method == "GET":
        data = {"code": 206, "msg": "请用post请求"}
        return JsonResponse(data)
    elif request.method == "POST":
        token = request.POST.get('token')
        decoded_string = base64.urlsafe_b64decode(token).decode('utf-8')
        if decoded_string != 'api_qa_insert_ui_android_result' or token == '':
            data = {"code": 403, "msg": "认证错误，请检查token"}
            return JsonResponse(data)
        else:
            channel_id = request.POST.get("channel_id")
            total_case = request.POST.get("total_case")
            total_pass = request.POST.get("total_pass")
            total_fail = request.POST.get("total_fail")
            total_unexpected = request.POST.get("total_unexpected")
            live_fail = request.POST.get("live_fail")
            room_fail = request.POST.get("room_fail")
            chat_fail = request.POST.get("chat_fail")
            me_fail = request.POST.get("me_fail")
            moment_fail = request.POST.get("moment_fail")
            sing_fail = request.POST.get("sing_fail")
            report_url = request.POST.get("report_url")
            if channel_id == '' or total_case == '' or total_pass == '' or total_fail == '' or \
                    total_unexpected == '' or live_fail == '' or room_fail == '' or chat_fail == '' or \
                    me_fail == '' or moment_fail == '' or sing_fail == '' or report_url == '':
                data = {'code': 204, 'msg': '参数缺少，请检查上传的参数是否正常'}
            elif channel_id != '2':
                data = {'code': 204, 'msg': '客户端填写错误，请检查'}
            else:
                channel_instance = channel_ui.objects.get(id='2')
                insert_data = ui_result(channel_id=channel_instance,
                                        total_case=total_case,
                                        total_pass=total_pass,
                                        total_fail=total_fail,
                                        total_unexpected=total_unexpected,
                                        live_fail=live_fail,
                                        room_fail=room_fail,
                                        chat_fail=chat_fail,
                                        me_fail=me_fail,
                                        moment_fail=moment_fail,
                                        sing_fail=sing_fail,
                                        report_url=report_url)
                insert_data.save()
                data = {"code": 200, "msg": "数据插入成功"}
            return JsonResponse(data)


def ui_ios_insert_data(request):
    """
    :param request: 插入ios测试结果数据
    :return:
    """
    if request.method == "GET":
        data = {"code": 206, "msg": "请用post请求"}
        return JsonResponse(data)
    elif request.method == "POST":
        token = request.POST.get('token')
        decoded_string = base64.urlsafe_b64decode(token).decode('utf-8')
        if decoded_string != 'api_qa_insert_ui_ios_result' or token == '':
            data = {"code": 403, "msg": "认证错误，请检查token"}
            return JsonResponse(data)
        else:
            channel_id = request.POST.get("channel_id")
            total_case = request.POST.get("total_case")
            total_pass = request.POST.get("total_pass")
            total_fail = request.POST.get("total_fail")
            total_unexpected = request.POST.get("total_unexpected")
            live_fail = request.POST.get("live_fail")
            room_fail = request.POST.get("room_fail")
            chat_fail = request.POST.get("chat_fail")
            me_fail = request.POST.get("me_fail")
            moment_fail = request.POST.get("moment_fail")
            sing_fail = request.POST.get("sing_fail")
            report_url = request.POST.get("report_url")
            if channel_id == '' or total_case == '' or total_pass == '' or total_fail == '' or \
                    total_unexpected == '' or live_fail == '' or room_fail == '' or chat_fail == '' or \
                    me_fail == '' or moment_fail == '' or sing_fail == '' or report_url == '':
                data = {'code': 204, 'msg': '参数缺少，请检查上传的参数是否正常'}
            elif channel_id != '1':
                data = {'code': 204, 'msg': '客户端填写错误，请检查'}
            else:
                channel_instance = channel_ui.objects.get(id='1')
                insert_data = ui_result(channel_id=channel_instance,
                                        total_case=total_case,
                                        total_pass=total_pass,
                                        total_fail=total_fail,
                                        total_unexpected=total_unexpected,
                                        live_fail=live_fail,
                                        room_fail=room_fail,
                                        chat_fail=chat_fail,
                                        me_fail=me_fail,
                                        moment_fail=moment_fail,
                                        sing_fail=sing_fail,
                                        report_url=report_url)
                insert_data.save()
                data = {"code": 200, "msg": "数据插入成功"}
            return JsonResponse(data)


def ui_results(request):
    if request.method == 'GET':
        ordered_queryset = ui_result.objects.filter(channel_id=1).order_by('-id')
        android_book = ordered_queryset.values_list('live_fail', 'room_fail', 'chat_fail', 'me_fail',
                                                    'moment_fail', 'sing_fail')[:1][0]
        android_data = [{"value": android_book[0], "name": '直播错误'},
                        {"value": android_book[1], "name": '语音房错误'},
                        {"value": android_book[2], "name": '聊天错误'},
                        {"value": android_book[3], "name": '跟人页错误'},
                        {"value": android_book[4], "name": '广场页错误'},
                        {"value": android_book[5], "name": 'sing错误'}]
        ordered_queryset = ui_result.objects.filter(channel_id=2).order_by('-id')
        ios_book = ordered_queryset.values_list('live_fail', 'room_fail', 'chat_fail', 'me_fail',
                                                'moment_fail', 'sing_fail')[:1][0]
        ios_data = [{"value": ios_book[0], "name": '直播错误'},
                    {"value": ios_book[1], "name": '语音房错误'},
                    {"value": ios_book[2], "name": '聊天错误'},
                    {"value": ios_book[3], "name": '跟人页错误'},
                    {"value": ios_book[4], "name": '广场页错误'},
                    {"value": ios_book[5], "name": 'sing错误'}]

        result = {'status': True,
                  'android_data': android_data,
                  'ios_data': ios_data}
        return JsonResponse(result)
