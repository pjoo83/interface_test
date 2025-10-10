from apscheduler.schedulers.background import BackgroundScheduler
from django.apps import AppConfig
from utils.feishu_get_token import _plugin_token_cache, get_plugin_access_token
import datetime


def refresh_feishu_token():
    print("定时刷新飞书 token ...")
    new_token = get_plugin_access_token()
    _plugin_token_cache["token"] = new_token
    _plugin_token_cache["expire_time"] = datetime.datetime.now() + datetime.timedelta(hours=1, minutes=55)
    print("新 token 已缓存")


class MyAppConfig(AppConfig):
    name = 'myapp'

    def ready(self):
        scheduler = BackgroundScheduler()
        scheduler.add_job(refresh_feishu_token, 'interval', minutes=115)
        scheduler.start()
        print("✅ 启动 token 定时刷新任务")
