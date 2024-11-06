import requests


def call_api_task():
    url = 'http://127.0.0.1:8000/autotest/resource_mount_increase/'
    url2 = 'http://127.0.0.1:8000/autotest/pendant_mount_increase/'
    response = requests.get(url)
    response2 = requests.get(url2)
    if response:
        # 处理API响应
        print('定时任务执行中')
    else:
        print(f'API call failed with status code1: {response.status_code}',
              f'API call failed with status code2: {response2.status_code}')
