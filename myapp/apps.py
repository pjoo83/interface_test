from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.apps import AppConfig

from myapp.utils.time import call_api_task
from myapp.utils.feishu_get_token import get_plugin_access_token

_plugin_token_cache = {"token": None}


def refresh_feishu_token():
    print("刷新飞书 Token ...")
    _plugin_token_cache["token"] = get_plugin_access_token()


class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        scheduler = BackgroundScheduler()
        scheduler.add_job(refresh_feishu_token, 'interval', minutes=115)
        scheduler.start()
        print("Token 自动刷新任务已启动")
    # def ready(self):
    #     scheduler = BackgroundScheduler()
    #     # # 每两小时的第0分钟执行
    #     # # trigger = CronTrigger(minute='*')
    #     # trigger = CronTrigger(hour='*', minute='0',day_of_week='mon-fri')
    #     # scheduler.add_job(call_api_task, trigger=trigger, id='call_api_job', max_instances=1)
    #     # scheduler.start()
