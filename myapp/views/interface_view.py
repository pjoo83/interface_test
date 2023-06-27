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


# 接口列表
@login_required
@csrf_exempt
def interface_list(request):
    if request.method == 'GET':
        form = Interface_listModel()
        queryset = models.interface_base.objects.all()
        page_object = Pagination(request, queryset)
        context = {
            "form": form,
            "queryset": page_object.page_queryset,
            "page_string": page_object.html()
        }

        return render(request, 'interface_manage/interface_list.html', context)


@csrf_exempt
@login_required
def interface_creat(request):
    """
    内容: 新建接口
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
            format=format)
        ApiParameters.save()
        return redirect("/autotest/inter/list/")
