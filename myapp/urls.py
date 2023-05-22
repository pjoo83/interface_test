from django.urls import path
from .views import login_view, register_view, index, intertools_view, interface_view, business_view

urlpatterns = [
    # 登录注册
    path("login/", login_view.user_login, name='user_login'),
    path("logout/", login_view.user_logout, name='user_logout'),
    path("register/", register_view.register, name='user_register'),

    # 首页
    path("index/", index.index),

    # 工具
    path("inter_tools/", intertools_view.inter_tools),

    # 接口管理
    path("inter/manage", interface_view.interface_manage),
    path("inter/list/", interface_view.interface_list),
    path("inter/creat/", interface_view.interface_creat),

    # 业务管理
    path("business/", business_view.business_list),
    path("business/del/", business_view.business_del),
    path("business/add/", business_view.business_add),
    path("business/edit/", business_view.business_edit)

]
