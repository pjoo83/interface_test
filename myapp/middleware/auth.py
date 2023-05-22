from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class AuthMiddleWare(MiddlewareMixin):
    """中间件坚持登录"""

    def process_request(self, request):
        # 读取session信息
        # 排除不需登录的界面
        if request.path_info in ['/autotest/login/', '/autotest/register/']:
            return
        info_dict = request.session.get("info")
        # print(info_dict)
        if info_dict:
            return
        # 没有提示未登录
        return redirect('/autotest/login/')
