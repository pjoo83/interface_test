import json
import requests
import plotly.graph_objects as go


def generate_charts(bonus_list, free_game, cname, money):
    """
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
        title=f"下注金额：{len(bonus_list) * money}，反奖金币{sum(bonus_list)}，免费金币:{sum(free_game)}",
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
    url = 'https://m-test.starmakerstudios.com/go-v1/candy-party-sugar/6113/play-game'
    bonus_list = []
    payload = json.dumps({
        "gold": 20,
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
    free_game = []
    for i in range(times):
        response = requests.request("POST", url, headers=headers, data=payload)
        bonus_list.append(response.json()['data']['gold'])
        if response.json()['data']['has_free_game'] is False:
            print(f'第{b}次执行{bonus_list}')
        else:
            free_game.append(response.json()['data']['gold'])
    generate_charts(bonus_list, cname, free_game)


def coin_volcano(times, cname):
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
    b = 0
    for i in range(times):
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.json()['code'] == -4:
            payload1 = json.dumps({
            })
            url1 = "https://m-test.starmakerstudios.com/go-v1/coin-volcano/5676/play-free-game"
            response = requests.request("POST", url1, headers=headers, data=payload1)
            free_game.append(response.json()['data']['total_reward_gold'])
            print(f"第{a}次下注时，free了{free_game}")
            b += 1
            a += 1
        else:
            bonus_list.append(response.json()['data']['total_reward_gold'])
            print(f"第{a}次下注时{bonus_list}")
            b += 1
            a += 1
    generate_charts(bonus_list, free_game, cname, 100)


# candy_party_sugar(1000,'candy_party_sugar')

# candy_party(100, 'candy_party')


coin_volcano(1000, 'coin_volcano')