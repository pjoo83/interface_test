# scheduler_runner.py

import os
import django
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

# 设置 Django 环境变量（根据你项目名称修改）
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Interface_Test.settings')
django.setup()

# 导入你要执行的定时任务函数
from myapp.utils.time import call_api_task  # 根据你实际路径调整


def main():
    scheduler = BlockingScheduler()

    # 示例：每工作日的每小时第0分钟执行
    trigger = CronTrigger(hour='*', minute='0', day_of_week='mon-fri')
    # trigger = CronTrigger(minute='*')

    scheduler.add_job(
        call_api_task,
        trigger=trigger,
        id='call_api_job',
        max_instances=1,
        replace_existing=True
    )

    print("✅ APScheduler 已启动，定时任务注册成功")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("⛔ 调度器已退出")


if __name__ == '__main__':
    main()
