from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.forms import ModelForm
from django.views.decorators.csrf import csrf_exempt

from .. import models


# 接口管理
def interface_manage(request):
    return render(request, "interface_manage/interface_manage.html")


# 接口列表
def interface_list(request):
    if request.method == 'GET':
        return render(request, 'interface_manage/interface_list.html')


class BusinessCategories(ModelForm):
    class Meta:
        models = models.interface_base
        fields = '__all__'


# 接口新增
@csrf_exempt
@login_required
def interface_creat(request):
    if request.method == "GET":
        interface_BusinessCategories = models.interface_businessCategories.objects.all()
        return render(request, 'interface_manage/interface_create.html',
                      {"interface_BusinessCategories": interface_BusinessCategories})
    else:
        # forms = BusinessCategories(data=request.POST)
        forms = request.POST   
        print(forms)
        return
