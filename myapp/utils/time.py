import requests


def call_api_task():
    url = 'http://10.41.1.89:8000/autotest/resource_mount_increase/'
    response = requests.get(url)
    if response:
        # 处理API响应
        print('定时任务执行中')
    else:
        print(f'API call failed with status code: {response.status_code}')
