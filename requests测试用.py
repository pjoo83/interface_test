import requests

jsons = {
    "anon_device_id": "5084F5165265986DDD92C62914F6EDF9",
    "email": "ch005@qq.com",
    "mode": "email",
    "password": "a1111111"
}

url = "https://api-test.starmakerstudios.com/api/v17/android/tvp/zh-CN/phone/xxhdpi/sm/login"
a = requests.post(url, params=jsons)
print(a.text)
