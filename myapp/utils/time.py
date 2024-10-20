from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
import requests


# 定义你的任务函数
def call_api_task():
    url = 'http://127.0.0.1:8000/autotest/resource_mount_increase/'  # 替换为你的API URL
    response = requests.get(url)
    if response:
        # 处理API响应
        print(response.json())
    else:
        print(f'API call failed with status code: {response.status_code}')


scheduler = BackgroundScheduler()

# 配置任务（例如，每天上午9点执行一次）
# 注意：这里的配置是每两小时执行一次，但你可以根据需要调整
# trigger = CronTrigger(hour='*/2', minute=0)
# 每两小时的第0分钟执行
trigger = CronTrigger(minute='*')
scheduler.add_job(call_api_task, trigger=trigger, id='call_api_job')

