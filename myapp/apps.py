from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.apps import AppConfig

from myapp.utils.time import call_api_task


class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    # def ready(self):
    #     scheduler = BackgroundScheduler()
    #     # # 每两小时的第0分钟执行
    #     # # trigger = CronTrigger(minute='*')
    #     # trigger = CronTrigger(hour='*', minute='0',day_of_week='mon-fri')
    #     # scheduler.add_job(call_api_task, trigger=trigger, id='call_api_job', max_instances=1)
    #     # scheduler.start()
