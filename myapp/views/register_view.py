import json
from django.forms import ModelForm

from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from myapp import models


@csrf_exempt
def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("pwd")
        email = request.POST.get("email")
        count_user = User.objects.filter(username=username).count()
        if count_user > 0:
            code = 204
            message = "用户已存在，请重新注册"
        else:
            user_profile = User()  # 实例化用户表
            user_profile.username = username
            user_profile.password = make_password(password)
            user_profile.email = email
            user_profile.is_active = 1
            user_profile.save()
            code = 200
            message = "注册成功,请联系管理员激活账户"
        msg = {'message': message,
               'code': code}
        return JsonResponse(json.dumps(msg))
