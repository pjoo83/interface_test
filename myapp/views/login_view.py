from hashlib import md5

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth import authenticate, login, logout


# Create your views here.
class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True, min_length=3)


def user_login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        login_form = LoginForm(request.POST)
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        if login_form.is_valid():
            # cd = login_form.cleaned_data
            user = authenticate(username=username, password=password)
            if user:
                if user.is_staff:
                    login(request, user)
                    request.session['info'] = {'id': request.POST.get("id"), 'name': username}
                    request.session.set_expiry(60 * 60 * 24)
                    return redirect("/autotest/dashboard/")
                else:
                    return render(request, 'login.html',
                                  {"username": username, "password": password, "msg": "请联系管理员激活账号"})
            else:
                return render(request, 'login.html', {"username": username, "msg": "用户名或密码错误"})
        elif username == '':
            return render(request, 'login.html', {"username": "", "password": "", "msg": "请输入用户名"})
        elif password == '':
            return render(request, 'login.html', {"username": username, "password": "", "msg": "请输入密码"})
        else:
            return render(request, 'login.html', {"msg": "该用户还未注册"})


def user_logout(request):
    request.session.clear()
    return redirect('/autotest/login/')
