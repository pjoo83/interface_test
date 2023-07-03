import datetime
import json
from django.forms import ModelForm

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.forms import ModelForm
from django.views.decorators.csrf import csrf_exempt
from .. import models
from ..utils.pagination import Pagination


# 接口管理
def interface_manage(request):
    return render(request, "interface_manage/interface_manage.html")


# 实例化列表
class Interface_listModel(ModelForm):
    class Meta:
        model = models.interface_base
        fields = '__all__'


@login_required
@csrf_exempt
def interface_list(request):
    """
    :param request: 全部接口显示
    """
    if request.method == 'GET':
        form = Interface_listModel()
        queryset = models.interface_base.objects.all()
        if len(queryset) > 0:
            page_object = Pagination(request, queryset)
            context = {
                "form": form,
                "queryset": page_object.page_queryset,
                "page_string": page_object.html()
            }
            return render(request, 'interface_manage/interface_list.html', context)
        else:
            return render(request, 'interface_manage/interface_list.html')


@csrf_exempt
@login_required
def interface_creat(request):
    """
     :param request: 新建接口
    """
    if request.method == "GET":

        interface_BusinessCategories = models.interface_businessCategories.objects.all()
        return render(request, 'interface_manage/interface_create.html',
                      {"interface_BusinessCategories": interface_BusinessCategories})
    else:
        interface_name = request.POST.get("interfaceName")
        businessCategories = request.POST.getlist("businessCategories")
        requestType = request.POST.get("requestType")
        interfaceAddress = request.POST.get("interfaceAddress")
        expected_result = request.POST.get("expected_result")
        status = request.POST.get("status")
        format = request.POST.get("format")
        transfer = request.POST.get("transfer")
        if transfer == "0" or requestType == "1":
            # 代表post的无参请求
            format = "3"
        head = json.loads(request.POST.get("head"))
        print(head)
        raw = request.POST.get("raw")
        type_list = []
        descriptions_list = []
        # 请求头中取出参数类型
        for i in head:
            type_list.append(i.pop("type"))
            descriptions_list.append(i.pop("description"))
        interfaces = models.interface_base(
            interfaceName=interface_name,
            requestType=requestType,
            interfaceAddress=interfaceAddress,
            status=status,
            yn=1,
            executeNumber=0,
            createUser=request.session['info']["name"],
            updateUser=request.session['info']["name"],
            createTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            updateTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        )
        interfaces.save()
        # 对业务进行遍历
        for interface_base_nu in businessCategories:
            interface_base_nu = models.interface_businessCategories.objects.get(id=interface_base_nu)
            interfaces.businessCategories.add(interface_base_nu)
            interfaces.save()
        api_id = models.interface_base.objects.filter().order_by("-id")[0].id
        heads = json.dumps(head).encode('utf-8').decode('unicode_escape')
        req = json.loads(request.POST.get("request"))
        requests = json.dumps(req).encode("utf-8").decode('unicode_escape')
        ApiParameters = models.ApiParameter(
            ApiHead=heads,
            request_value=requests,
            description=descriptions_list,
            raw_data=raw,
            expected_result=expected_result,
            format=format, api_id=api_id)
        ApiParameters.save()
        return redirect("/autotest/inter/list/")


def interface_edit(request):
    """
    :param request: 接口内容编辑
    :return:
    """
    if request.method == "GET":
        Iid = request.GET.get("id")
        exists = models.interface_base.objects.filter(id=Iid).exists()
        if not exists:
            return JsonResponse({"status": 200, "message": "数据未查到"})
        else:
            inter_head = models.interface_base.objects.get(id=Iid)
            ApiParameters = models.ApiParameter.objects.filter(api_id=Iid).values()
            interface_BusinessCategories = models.interface_businessCategories.objects.all()
            busResult = inter_head.businessCategories.all()
            for i in busResult:
                businessCategories = i.businessName
            ApiHead = ApiParameters[0]["ApiHead"]
            # print(ApiHead)
            types = ApiParameters[0]["_type"]
            description = ApiParameters[0]["description"]
            expected_result = ApiParameters[0]["expected_result"]
            request_value = ApiParameters[0]["request_value"]
            raw_data = ApiParameters[0]["raw_data"]
            format = ApiParameters[0]["format"]
            # 定义一个空的字符串，命名为format
            format_nu = ''
            # 当format等于0时，format_nu = "abc"【因为前端的0和2存到库中用的字段是一样的，因此需要做一下判断来进行回显】
            if format == '0':
                format_nu = "abc"
            elif format == '2':
                format_nu = "abc1"
            context = {
                "interfaces": inter_head,
                "interface_businessCategories": interface_BusinessCategories,
                # "ApiParameters": ApiHead,
                "expected_result": expected_result,
                format_nu: request_value,
                "format": format, "raw_data": raw_data,
                # "businessCategories": businessCategories
            }
        return render(request, 'interface_manage/interface_edit.html', context)
    else:
        Iid = request.GET.get("id")
        update_inter = models.interface_base.objects.get(id=Iid)
        # 通过POST.get的方法进行获取前端的值，与数据库中的值进行替换
        update_inter.interfaceName = request.POST.get("interfaceName")
        update_inter.requestType = request.POST.get("requestType")
        update_inter.interfaceAddress = request.POST.get("interfaceAddress")
        update_inter.status = request.POST.get("status")
        businessCategories = request.POST.get('businessCategories')
        update_inter.save()

        obj = update_inter.businessCategories.all()
        update_inter.businessCategories.remove(*obj)
        bus_obj = models.interface_businessCategories.objects.get(businessName=businessCategories)
        update_inter.businessCategories.add(bus_obj)
        bus_obj.businessName = businessCategories
        bus_obj.save()

        # 获取是否传参的状态
        transfer = request.POST.get("transfer")
        if transfer == '0':
            update_result = models.ApiParameter.objects.get(api_id=Iid)
            update_result.expected_result = request.POST.get("expected_result")
            update_result.save()
        else:
            # 修改请求头
            update_api = models.ApiParameter.objects.get(api_id=Iid)
            update_api.ApiHead = request.POST.get("head")
            # 修改请求请求体从参数
            update_api.request_value = request.POST.get("request_value")
            update_api.expected_result = request.POST.get("expected_result")
            update_api.save()
            print("+++++++++++++++++++++++++++修改成功++++++++++++++++++++++++++++++++++++++++++++++")


def interface_run(request):
    """

    :param request: 单个接口运行
    :return:
    """
    pass
