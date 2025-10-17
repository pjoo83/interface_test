import requests


def call_api_task():
    url = 'http://10.41.1.89:8000/autotest/resource_mount_increase/'
    url2 = 'http://10.41.1.89:8000/autotest/pendant_mount_increase/'
    url3 = 'http://10.41.1.89:8000/autotest/debris_mount_increase/'
    url4 = 'http://10.41.1.89:8000/autotest/ab_experiment_increase/'
    url5 = 'http://10.41.1.89:8000/autotest/bubble_mount_increase/'
    url6 = 'http://10.41.1.89:8000/autotest/check_crazy_monster_all/'
    url7 = 'http://10.41.1.89:8000/autotest/no_testing_time/'
    response = requests.get(url)
    response2 = requests.get(url2)
    response3 = requests.get(url3)
    response4 = requests.get(url4)
    response5 = requests.get(url5)
    response6 = requests.get(url6)
    response7 = requests.get(url7)
    if response:
        # 处理API响应
        print('定时任务执行中')
    else:
        print(f'API call failed with status code1: {response.status_code}',
              f'API call failed with status code2: {response2.status_code}',
              f'API call failed with status code3: {response3.status_code}',
              f'API call failed with status code4: {response4.status_code}',
              f'API call failed with status code5: {response5.status_code}',
              f'API call failed with status code6: {response6.status_code}',
              f'API call failed with status code7: {response7.status_code}')
