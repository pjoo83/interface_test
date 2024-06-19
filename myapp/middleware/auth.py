from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


# class AuthMiddleWare(MiddlewareMixin):
#     """中间件坚持登录"""
#
#     def process_request(self, request):
#         # 读取session信息
#         # 排除不需登录的界面
#         if request.path_info in ['/autotest/login/', '/autotest/register/']:
#             return
#         info_dict = request.session.get("info")
#         # print(info_dict)
#         if info_dict:
#             return
#         # 没有提示未登录
#         return redirect('/autotest/login/')

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # 读取session信息
        # 排除不需登录的界面
        exclude_urls = ['/autotest/login/', '/autotest/register/',
                        '/autotest/dashboard/interface/insert_api/', '/autotest/dashboard/android/insert_api/',
                        '/autotest/dashboard/ios/insert_api/']
        if request.path_info in exclude_urls:
            # 如果请求的URL在排除列表中，则直接跳过验证
            response = self.get_response(request)
            return response

            # 验证登录状态
        info_dict = request.session.get("info")
        if not info_dict:
            # 如果没有session信息，则重定向到登录页面
            return redirect('/autotest/login/')

            # 如果有session信息，则继续执行请求
        response = self.get_response(request)
        return response
