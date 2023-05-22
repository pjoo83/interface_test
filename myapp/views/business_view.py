import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.forms import ModelForm
from myapp import models
import datetime


class BusinessModel(ModelForm):
    class Meta:
        model = models.interface_businessCategories
        fields = ["businessName"]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for item in self.fields.items():
                item.widget.attrs = {"class": "form=control", "placeholder": item.label}


# 业务列表
def business_list(request):
    queryset = models.interface_businessCategories.objects.all()
    forms = BusinessModel()
    context = {
        "forms": forms,
        "queryset": queryset
    }
    return render(request, 'business_list.html', context)


# 业务增加
def business_add(request):
    forms = BusinessModel(data=request.POST)
    # print(forms)
    if forms.is_valid():
        forms.instance.createUser = request.session['info']["name"]
        forms.save()
        return JsonResponse({"status": 200, 'message': "success"})
    return JsonResponse({"status": 300, "message": forms.errors})


# 删除业务
def business_del(request):
    business_id = request.GET.get('bid')
    print(business_id)
    exists = models.interface_businessCategories.objects.filter(id=business_id).exists()
    if not exists:
        return JsonResponse({"status": False, "message": "数据异常，删除失败"})
    models.interface_businessCategories.objects.filter(id=business_id).delete()
    return JsonResponse({"status": True, "message": "数据删除成功"})


# 业务修改
def business_edit(request):
    business_id = request.GET.get("bid")
    forms = BusinessModel(data=request.POST)
    exists = models.interface_businessCategories.objects.filter(id=business_id).exists()
    if not exists:
        return JsonResponse({"status": False, 'message': "数据异常编辑失败"})
    else:
        bname = request.GET.get("bname")
        models.interface_businessCategories.objects.filter(id=business_id).update(businessName=bname)
        models.interface_businessCategories.objects.filter(id=business_id).update(
            updateUser=request.session['info']['name'])
        return JsonResponse({"status": True, "message": "修改成功"})
