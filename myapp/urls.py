from django.urls import path
from .views import login_view, register_view, index, intertools_view, business_view, dashboard_view, interface_view, \
    uitest_view, resource_increase_view

urlpatterns = [
    # 登录注册
    path("login/", login_view.user_login, name='user_login'),
    path("logout/", login_view.user_logout, name='user_logout'),
    path("register/", register_view.register, name='user_register'),

    # 首页
    path("index/", index.index),
    path("index/index_translate_bar/", index.translate_bar, name='translate_bar'),
    path("index/index_translate_pie/", index.translate_pie, name='translate_pie'),

    # 仪表页面
    path("dashboard/", dashboard_view.dashboard_index, name='dashboard_index'),
    # 多语言区域
    path("dashboard/dashboard_translate_bar/", dashboard_view.dashboard_translate_bar,
         name='rom ..utils.database_tools import execute_sql'),
    path("dashboard/dashboard_language_count/", dashboard_view.dashboard_language_count,
         name='dashboard_language_count'),
    path("dashboard/dashboard_executions_translate_total/", dashboard_view.dashboard_executions_translate_total,
         name='dashboard_executions_total'),
    path("dashboard/dashboard_translate_pie/", dashboard_view.dashboard_translate_pie, name='dashboard_translate_pie'),

    #  接口数据插入
    path('dashboard/interface/insert_api/', interface_view.interface_insert_data, name='interface_insert_data'),
    # 接口折线图显示区域
    path('dashboard/dashboard_executions_interface_total/', interface_view.dashboard_executions_interface_total,
         name='interface_executions_total'),
    path('dashboard/dashboard_executions_interface_detail/', interface_view.dashboard_executions_interface_detail,
         name='dashboard_executions_interface_detail'),

    # ui安卓接口数据插入
    path('dashboard/android/insert_api/', uitest_view.ui_android_insert_data, name='android_insert_api'),
    # ui苹果接口输入插入
    path('dashboard/ios/insert_api/', uitest_view.ui_ios_insert_data, name='ios_insert_api'),
    # 安卓饼图结果
    path('dashboard/android_ui_results/', uitest_view.android_ui_results, name='android_ui_results'),
    # ios饼图结果
    path('dashboard/ios_ui_results/', uitest_view.ios_ui_results, name='ios_ui_results'),

    path('dashboard/ui_test_statistics/',uitest_view.ui_test_statistics,name ='ui_test_statistics'),
    # 工具
    path("inter_tools/", intertools_view.inter_tools),
    # 资源添加
    path('resource_mount_increase/', resource_increase_view.resource_mount_increase, name='resource_mount_increase'),
    # 业务管理
    path("business/", business_view.business_list),
    path("business/del/", business_view.business_del),
    path("business/add/", business_view.business_add),
    path("business/edit/", business_view.business_edit)

]
