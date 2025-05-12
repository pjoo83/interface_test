import json
import os

import requests
import plotly.graph_objects as go
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.safestring import mark_safe

from Interface_Test.settings import BASE_DIR
from collections import Counter


def generate_charts(bonus_list, free_game, cname, money, user_gold, user_last_gold):
    """
    :param user_last_gold: 结束时金币
    :param user_gold: 用户初始金币
    :param money: 下注金额
    :param free_game: free的金额
    :param cname: 名称
    :param bonus_list:表格数据
    :return: 弹出表格
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=bonus_list,
        mode='lines+markers',
        name='下注反奖'
    ))
    fig.add_trace(go.Scatter(
        y=free_game,
        mode='lines+markers',
        name='free'
    ))
    fig.update_layout(
        title=f"用户初始金币:{user_gold}，结束时间金币：{user_last_gold}，"
              f"下注金额：{len(bonus_list) * money}，反奖金币{sum(bonus_list)}，free_game金币:{sum(free_game)}",
        xaxis_title=f"下注次数:{len(bonus_list)}",
        yaxis_title="反奖金额",
        template="plotly_white"
    )
    fig.write_html(f"{cname}.html")
    fig.show()


def candy_party(times, cname):
    """
    :return:返回糖果派对下注结果
    """
    url = 'https://m-test.starmakerstudios.com/go-v1/candy-party/5275/play-game'
    bonus_list = []
    payload = json.dumps({
        "gold": 10,
        "is_free": False
    })
    headers = {
        'Host': 'm-test.starmakerstudios.com',
        'Cookie': 'PHPSESSID=sn1eqi3mrupcd7vdo89ntfvr26; _ga=GA1.1.2017341577.1740466070; SM_GOLBAL_device_token=v2:'
                  'ixoGZu7Kei+aMvorJmWan/5dmUSZ/JWx6MhPnvMTjiYdzCozbivkDm9uSWxl/QYcOIXFQwBye7EkZQ7c2Syw98Us8WhGMgOc'
                  'OHg28pMpgISw19NobOqw6McZ3pkuydpUNfY9nuOemX/idwtTIdI2JQmufKN3WYuKDEfsrZO4xWwK4gRcdlTl1MYgKuCjVgrM'
                  'ZSdNwDLcLN815a+y7Jwzr4nRi59C2HwSkFjNc//9pZ/zrmt1cm58/oEPiHJxqyJto361IuPmHdaMNGFeyv0W+3f/99XrW6Gv'
                  'aF1LJ+y5niV+tYmUxOZmzn41qA==; oauth_token=h4h9LDGJ4e1QOi2S5ULvYGGaPxAdyjJs; oauth_token_secret=R'
                  'P8EAPjxwokQ3YKmMVwlqeSPhUidMVZO; _ga_Y5QLWEHNZ4=GS1.1.1742286324.54.1.1742286476.45.0.0; tgw_l7_'
                  'route=431e385792b86f59a26ac8466105f32c',
        'sec-ch-ua-platform': '"Android"',
        'user-agent': 'sm/8.82.0/Android/10/google play/9810673D62FC4E6646AAEE7B452256A4/wifi/zh-TW/V1924A/126663'
                      '76951981700///China',
        'accept': 'application/json, text/plain, */*',
        'sec-ch-ua': '"Not(A:Brand";v="99", "Android WebView";v="133", "Chromium";v="133"',
        'content-type': 'application/json',
        'token': 'h4h9LDGJ4e1QOi2S5ULvYGGaPxAdyjJs',
        'sec-ch-ua-mobile': '?1',
        'origin': 'https://m-test.starmakerstudios.com',
        'x-requested-with': 'com.starmakerinteractive.starmaker',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://m-test.starmakerstudios.com/a-vue3/spa-candy-match/index?promotion_i'
                   'd=5275&showBar=0&showNavigation=false&isStatusBarStyle=true&sp=game_center&_sxiq_open_o'
                   'rigin=game_center',
        'accept-language': 'zh-TW,zh-CN;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6',
        'priority': 'u=1, i'
    }
    a = 1
    b = 0
    free_game = []
    for i in range(times):
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.json()['code'] == -3:
            payload1 = json.dumps(
                {"position": a}
            )
            url1 = 'https://m-test.starmakerstudios.com/go-v1/candy-party/5275/play-free-game'
            response = requests.request("POST", url1, headers=headers, data=payload1)
            if response.json()['data']['rebase_gold'] != 0:
                free_game.append(response.json()['data']['rebase_gold'])
                print(free_game)
            a += 1
        else:
            bonus_list.append(response.json()['data']['gold'])
            b += 1
            print(f'第{b}次执行{bonus_list}')
    generate_charts(bonus_list, free_game, cname)


def candy_party_sugar(times, cname):
    """
    :param times:
    :param cname:
    :return: 新糖果派对下注结果
    """
    url = 'https://m-test.starmakerstudios.com/go-v1/candy-party-sugar/6113/play-game'
    bonus_list = []
    payload = json.dumps({
        "gold": 100,
        "IsFree": False
    })
    b = 0
    headers = {
        'Host': 'm-test.starmakerstudios.com',
        'Cookie': 'PHPSESSID=fp336gojppqdf6c2if0lpicahg; _ga=GA1.1.665879783.1745206274; '
                  'SM_GOLBAL_device_token=v2'
                  ':ixoGo09BNLUiANECr6gTeAfqx5FVBh4IYifjNmwIwNx5ajrILyDVtT0qrFaPaIZgNTKSPPDLBUykxiRZyUgBoWOo0C5'
                  '+TNwkMYRvkrvbHRx7OUOEctBbyyoKLSMk0x0YUT'
                  '/WiWQMTMkik5aMRxFsQgUENwBg7vlpzUg5mPV2680dOC1WdtCndOUyRhBJBqi3UvNrAQf4L4GyX0'
                  '+fxArVEuofhhj2GhBqtvH90abcT0qxGqWwgNryUzxculvyWGeaVXhmj1bB117Cb6EXefobawX0hHFKi0tr0E4JZm'
                  '+bFbcXhyqldC+5+d1R7A==; oauth_token=h4h9LDGJ4e1QOi2S5ULvYGGaPxAdyjJs; '
                  'oauth_token_secret=RP8EAPjxwokQ3YKmMVwlqeSPhUidMVZO; '
                  'tgw_l7_route=431e385792b86f59a26ac8466105f32c; '
                  '_ga_Y5QLWEHNZ4=GS1.1.1745224146.3.1.1745227521.58.0.0',
        'sec-ch-ua-platform': '"Android"',
        'sec-ch-ua': '"Android WebView";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?1',
        'baggage': 'sentry-environment=production,sentry-public_key=4e49a22048c8f8e694c4b0ad56971a1a,'
                   'sentry-trace_id=33362d44597348999fab343a0c373661,sentry-sample_rate=0.2,sentry-sampled=false',
        'sentry-trace': '33362d44597348999fab343a0c373661-9acc5cf1fbf763ea-0',
        'user-agent': 'sm/8.85.0/Android/12/google play/d3e95e3be0841ba6/wifi/zh-CN/SM-N9700/12666376951981700///China',
        'content-type': 'application/json',
        'token': 'h4h9LDGJ4e1QOi2S5ULvYGGaPxAdyjJs',
        'accept': '*/*',
        'origin': 'https://m-test.starmakerstudios.com',
        'x-requested-with': 'com.starmakerinteractive.starmaker',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://m-test.starmakerstudios.com/mini-game/sugarRush/?promotion_id=6113&showBar=0'
                   '&showNavigation=false&heightPercent=80&_sxiq_open_origin=banner_officialevent',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en-GB;q=0.7,en;q=0.6,ko-KR;q=0.5,ko;q=0.4',
        'priority': 'u=1, i'
    }
    b = 0
    free_game = []
    error = []
    url1 = 'https://m-test.starmakerstudios.com/go-v1/candy-party-sugar/6113/index?'
    response = requests.request("GET", url1, headers=headers)
    user_gold = response.json()['data']['user_gold']
    print(f'用户金币{user_gold}')
    for i in range(times):
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            if response.json()['data']['has_free_game'] is False:
                a = response.json()['data']['gold']
                bonus_list.append(a)
                print(f'第{b}次执行中奖{a}')
                free_game.append(0)
            else:
                a = response.json()['data']['gold']
                bonus_list.append(a)
                print(f'第{b}次执行FREE{a}')
                bonus_list.append(0)
            b += 1
        except Exception as e:
            print(f'第{b}次执行异常{e},{response.json()}')
            error.append(f'第{b}次执行异常{response.json()}')
            continue
    response = requests.request("GET", url1, headers=headers)
    user_last_gold = response.json()['data']['user_gold']
    generate_charts(bonus_list, free_game, cname, 100, user_gold, user_last_gold)
    print(bonus_list)
    print(free_game)
    print(error)


def coin_volcano(times, cname):
    """
    :param times: 次数
    :param cname: 游戏名称
    :return: 返回结果
    """
    url = 'https://m-test.starmakerstudios.com/go-v1/coin-volcano/5676/play'
    payload = json.dumps({
        "bet_gold": 100,
        "bet_type": 1
    })
    bonus_list = []
    headers = {
        'Host': 'm-test.starmakerstudios.com',
        'Cookie': 'PHPSESSID=fp336gojppqdf6c2if0lpicahg; _ga=GA1.1.665879783.1745206274; '
                  'SM_GOLBAL_device_token=v2'
                  ':ixoGo09BNLUiANECr6gTeAfqx5FVBh4IYifjNmwIwNx5ajrILyDVtT0qrFaPaIZgNTKSPPDLBUykxiRZyUgBoWOo0C5'
                  '+TNwkMYRvkrvbHRx7OUOEctBbyyoKLSMk0x0YUT'
                  '/WiWQMTMkik5aMRxFsQgUENwBg7vlpzUg5mPV2680dOC1WdtCndOUyRhBJBqi3UvNrAQf4L4GyX0'
                  '+fxArVEuofhhj2GhBqtvH90abcT0qxGqWwgNryUzxculvyWGeaVXhmj1bB117Cb6EXefobawX0hHFKi0tr0E4JZm'
                  '+bFbcXhyqldC+5+d1R7A==; oauth_token=h4h9LDGJ4e1QOi2S5ULvYGGaPxAdyjJs; '
                  'oauth_token_secret=RP8EAPjxwokQ3YKmMVwlqeSPhUidMVZO; '
                  '_ga_Y5QLWEHNZ4=GS1.1.1745238102.6.0.1745238102.60.0.0; '
                  'tgw_l7_route=431e385792b86f59a26ac8466105f32c',
        'sec-ch-ua-platform': '"Android"',
        'sec-ch-ua': '"Android WebView";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?1',
        'baggage': 'sentry-environment=production,sentry-public_key=daf09c5d923b5638040f559c79dd2a8c,'
                   'sentry-trace_id=bd383c3c9ad5496c8683c4381225d351,sentry-sample_rate=0.1,sentry-sampled=false',
        'sentry-trace': 'bd383c3c9ad5496c8683c4381225d351-8ec2dd532feedbd5-0',
        'user-agent': 'sm/8.85.0/Android/12/google play/d3e95e3be0841ba6/wifi/zh-CN/SM-N9700/12666376951981700///China',
        'content-type': 'application/json',
        'token': 'h4h9LDGJ4e1QOi2S5ULvYGGaPxAdyjJs',
        'accept': '*/*',
        'origin': 'https://m-test.starmakerstudios.com',
        'x-requested-with': 'com.starmakerinteractive.starmaker',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://m-test.starmakerstudios.com/mini-game/coinVolcano/?promotion_id=5676&showBar=0'
                   '&showNavigation=false&heightPercent=80&sp=game_center&_sxiq_open_origin=game_center',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en-GB;q=0.7,en;q=0.6,ko-KR;q=0.5,ko;q=0.4',
        'priority': 'u=1, i'
    }
    free_game = []
    a = 0
    url1 = 'https://m-test.starmakerstudios.com/go-v1/coin-volcano/5676/index?'
    response = requests.request("GET", url1, headers=headers)
    user_gold = response.json()['data']['user_gold']
    for i in range(times):
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            if response.json()['code'] == -4:
                payload1 = json.dumps({
                })
                url2 = "https://m-test.starmakerstudios.com/go-v1/coin-volcano/5676/play-free-game"
                response = requests.request("POST", url2, headers=headers, data=payload1)
                print(response.json())
                free_game.append(response.json()['data']['total_reward_gold'])
                bonus_list.append(0)
                print(f"第{a}次下注时，free了{free_game}")
            else:
                bonus_list.append(response.json()['data']['total_reward_gold'])
                free_game.append(0)
                print(response.json())
                print(f"第{a}次下注时{bonus_list}")
            a += 1
        except Exception as e:
            print("请求异常", e, response.json())
            continue
    response = requests.request("GET", url1, headers=headers)
    user_last_gold = response.json()['data']['user_gold']
    generate_charts(bonus_list, free_game, cname, 100, user_gold, user_last_gold)


def check_candy_party_sugar(request):
    return render(request, 'candy_party_sugar.html')


def new_fish(times):
    """
    :return: 返回钓鱼次数
    """
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Content-Type': 'application/json',
        'Origin': 'http://wanghaobin.box.ushow.media:84',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://wanghaobin.box.ushow.media:84/a-vue3/fantasy-fishing?promotion_id=6198&showBar=0&showNavigation=false&_sxiq_open_origin=banner_officialevent',
        'User-Agent': 'sm/8.86.0/Android/10/google play/74A40EF7E711D3F2B20B6081AAF5E2B7/wifi/zh-CN/V1924A/12666376951981700///China',
        'X-Requested-With': 'com.starmakerinteractive.starmaker',
        'token': 'bGW6i7835P3qwHIFI3zEVnAAfAEDV3i3',
        'Cookie': 'PHPSESSID=gleim5bu8s11lic4u4bjai3jj1; _ga=GA1.1.2132221105.1747016566; oauth_token=bGW6i7835P3qwHIFI3zEVnAAfAEDV3i3; oauth_token_secret=66TuuTbpcFNTiHFVfDJ1ojBhlFRusj6G; SM_GOLBAL_device_token=v2:ixoGX+uNId0YEY3d3NNw194VOqF5jlwDIFM7kSYTzRYFOtpfihKIPfy9QCFwdPveBfsUVKuLxq6Rgu30/wZYS6nsP4qPdwZIZvckO5HeodOYLzjWh6tkOhkBHnlNC0uNPK6XqSgKu0R1oqPnsviGwq8K/BFsQ+0AVQvu2frtW1CmQ+Kw5CBBXfVsH5+OHNM5phj2P0eU76g8MTofqCZLJPMdjotvh2XotkJrqRNji2TS+tu1uMBmNfuuNlxg2xNwLmVg5UqDvCMe4uHPHxoKy+wemqTEgIKxiCPhZmNqC3CX1gNWKb77T6NuaQ==; _ga_Y5QLWEHNZ4=GS2.1.s1747030633$o3$g1$t1747031147$j8$l0$h0'
    }
    fish_URL = 'http://wanghaobin.box.ushow.media:84/go-v1/fantasy-fishing/6198/fish'
    payload = json.dumps({
        "fish_count": 1, "bait_id": 1
    })
    fish_list = []
    prices = []
    a = 0
    ticket_url = 'http://wanghaobin.box.ushow.media:9923/go-v1/fantasy-fishing/gm/ticket/add?test_user_id=12666376951981700&promotion_id=6198&count=1000'
    for i in range(times):
        response = requests.request("POST", fish_URL, headers=headers, data=payload)
        if response.json()['data']['code'] == 0:
            data = response.json()['data']['fishes'][0]
            fish = data['fish_id']
            fish_list.append(fish)
            price = data['price']
            prices.append(price)
            print(f'第{a}次上鱼{fish}，价格{price}')
            a += 1
        else:
            response = requests.request("GET", ticket_url)
            print(response.json())
    print(fish_list)
    count = Counter(fish_list)
    total = len(fish_list)
    for num, freq in count.items():
        probability = freq / total*100
        print(f"鱼 {num} 出现了 {freq} 次，概率为 {probability:.2f}")

if __name__ == '__main__':
    new_fish(10000)
    # candy_party_sugar(20000, 'candy_party_sugar')
    # candy_party(100, 'candy_party')
    # coin_volcano(10000, 'coin_volcano')
