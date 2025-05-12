import datetime
import threading
import json
import requests
from datetime import datetime


def candy_party_sugar(times, cname, cookie):
    url = 'https://m-test.starmakerstudios.com/go-v1/candy-party-sugar/6113/play-game'
    buy_free = 'https://m-test.starmakerstudios.com/go-v1/candy-party-sugar/6113/buy-free-game'
    bonus_list = []
    payload = json.dumps({
        "gold": 100,
        "IsFree": False
    })
    b = 0
    free_game = []
    error = []
    buy_free_game = []
    headers = {
        'Host': 'm-test.starmakerstudios.com',
        'Cookie': cookie,  # <<< 这里动态用传进来的 cookie！
        'content-type': 'application/json',
        'accept': '*/*',
        'user-agent': 'sm/8.85.2/Android/10/google play/900F120FD7FC1D4BF57C90B96C2DF766/wifi/zh-TW/V1924A/12666376951981700///China',
        # 可以加上你原来需要的其他headers
    }

    url1 = 'https://m-test.starmakerstudios.com/go-v1/candy-party-sugar/6113/index?'
    response = requests.get(url1, headers=headers)
    # print(response.text)
    user_gold = response.json()['data']['user_gold']
    print(f'开始！时间 {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}{cname} 初始金币{user_gold}')
    requests.post(url, headers=headers, data=payload)
    for i in range(times):
        try:
            if i % 999999 == 0 and i != 0:
                payload1 = json.dumps({
                    "gold": 100,
                })
                response1 = requests.post(buy_free, headers=headers, data=payload1)
                if response1.json()['code'] == 0:
                    response2 = requests.post(url, headers=headers, data=payload)
                    c = response2.json()['data']['gold']
                    # f = response.json()['data']['DateGold']
                    # d = response.json()['data']['PoolGold']
                    # e = response.json()['data']['BaseGold']
                    buy_free_game.append(c)
                    print(f'{cname} 第{b}次执行中奖{c}')
                    # print(f'{cname} 第{b}次执行买免费游戏成功{c},奖池，DateGold：{f}，PoolGold：{d}，BaseGold：{e}')
                else:
                    print(f'{cname} 第{b}次执行买免费游戏失败{response1.text}')
                    requests.post(url, headers=headers, data=payload)
                    error.append(f'{cname} 第{b}次执行买免费游戏失败{response1.text}')
                # print(f'{cname} 第{b}次执行买免费游戏{c}')
            else:
                response = requests.post(url, headers=headers, data=payload)
                if response.json()['data']['use_free_game'] is False:

                    a = response.json()['data']['gold']
                    # c = response.json()['data']['DateGold']
                    # d = response.json()['data']['PoolGold']
                    # e = response.json()['data']['BaseGold']
                    bonus_list.append(a)
                    print(f'{cname} 第{b}次执行中奖{a}')

                    # print(f'{cname} 第{b}次执行中奖{a},奖池，DateGold：{c}，PoolGold：{d}，BaseGold：{e}')
                else:
                    a = response.json()['data']['gold']
                    free_game.append(a)
                    print(f'{cname} 第{b}次执行FREE{a}')
            b += 1
        except Exception as e:
            print(f'{cname} 第{b}次执行异常{e},{response.text}')
            # print(f'{cname} 第{b}次执行异常{e},{response1.text}')
            error.append(f'{cname} 第{b}次执行异常{response.text}')
            continue

    response = requests.get(url1, headers=headers)
    user_last_gold = response.json()['data']['user_gold']
    print(f'{cname} :初始金币{user_gold}，'
          f'剩余金币{user_last_gold}，'
          f'总中奖金额包含买FREE：{user_last_gold - user_gold}，'
          f'总中奖金额不包含买FREE：{sum(bonus_list) + sum(free_game)}，'
          f'常规下次数：{len(bonus_list)},free次数：{len(free_game)}, 购买free次数：{len(buy_free_game)},'
          f'常规中奖金币：{sum(bonus_list)}，'
          f'正常free中奖金币:{sum(free_game)},'
          f'购买free总金币：{(len(buy_free_game) + 1) * 10000}，'
          f'买免费游戏共赚取金币：{sum(buy_free_game)}')
    print(f"常规：{bonus_list}")
    print(f'free_game：{free_game}')
    print(f'买免费游戏：{buy_free_game}')
    print(f"error:{error}")


def run_candy(cookie, idx):
    cname = f"账号{idx}"
    candy_party_sugar(times=10000, cname=cname, cookie=cookie)


if __name__ == "__main__":
    cookies = [
        'PHPSESSID=0h2ku0f1kclo0kqljnub4hgrq3; SM_GOLBAL_device_token=v2:ixoGNH15Aj0SKskcqOHkyPmD+JWBoj9LhbnEPL5ggZpQm53jZpqsvEq2qBBtQSqGDoL6GK2hntdS4PnHGWSlyllVxAbAsWrHfOTxcdZZprca1nprQSrJRoFmKPjRNo32WDGFijL1IR1LSjUirHL8BTDg/0+3WRqOKqOC7g8tjJNMLSnt24hPy1+FlZCmSpcOa5DBfL9HCACQMZ04lMnjI7eoRiZQlP04r7dDBilDcbYlVIkw4ricLu42QShYlZYi0VrFUJ5Cw/BC1GpTS2dHyU42HD0OIMSX8Yl7+YvVp0EJJfeOlz+L; _ga=GA1.1.1047954399.1745742844; spa-crazy-monster_4520_hideNewbie=true; oauth_token=bGW6i7835P3qwHIFI3zEVnAAfAEDV3i3; oauth_token_secret=66TuuTbpcFNTiHFVfDJ1ojBhlFRusj6G; _ga_Y5QLWEHNZ4=GS1.1.1745808200.3.1.1745808584.17.0.0; tgw_l7_route=431e385792b86f59a26ac8466105f32c',
        'PHPSESSID=0h2ku0f1kclo0kqljnub4hgrq3; _ga=GA1.1.1047954399.1745742844; spa-crazy-monster_4520_hideNewbie=true; SM_GOLBAL_device_token=v2:ixoG6kaThqpayZfDKcIrkQVcoNPB29Y3bmfwsfMgkgOLMbG2yxMrCpRxu2dxHxpN1uzMXJFgQpQaD5ZbDdjo8rj3NRXnahbsNV+5dhTLbnPImwuDJ/wJz21rbHG0cYXUWNO8eDBgjJtLjAbmlJEgg2g7LNHwdriMk5kKIVC2LEXX9Y+4Fl4qF+jdVLTPTJi839E7PvpZzGEOokPEjRi5tkEmcUn2gW27NijgPm+7baFcoa+DENgaIlsg9H4BWID/Q1eWDJfaava4+LnwzymQ4lj+7q/dJstcXqEk7IAH34iWZCtiLF6Q; _ga_Y5QLWEHNZ4=GS1.1.1745814517.4.0.1745814517.60.0.0; oauth_token=AMwq3V0GRh8N6CXgJ9Nb7H4zZCmfJH9s; oauth_token_secret=zSYnFTYoZLb4Htd6oq3liqeisKvODkH5; tgw_l7_route=431e385792b86f59a26ac8466105f32c',
        'oauth_token_secret=pNdwit8wPR1nVSTl6Sjk2ykK5YHFG8zl; oauth_token=Jti0dzKzhVEWnyONH2jD94MCX25gQcCF; _ga_Y5QLWEHNZ4=GS2.1.s1746583550$o47$g1$t1746584181$j60$l0$h0; _ga=GA1.1.1163989122.1742812969; SM_GOLBAL_device_token=v2:jBoG3hIxf1ZmTqAl3L14BKfk24+nC73iOfiJuUIGXzL591Ee0WZ1fENnhgz0PNyGZcpzrnx81Wh1qe9Xrn/vuhxER26mghCfHzT7UE8/7D4ljUQeRw0ZEIxNzqVGhaeR7xkNG70JGTTAJ1beIrK4Ip1Hun5haFTvX2NA3ATTlhLTeGxrDGqA8aPtoUPFmrUVq+FkyRCtHHcWLbAn93CpSrm4hxIAHAfKMSN8LMIKeGYSIihVOtVCt8YHc/m7q4veyuXSbEteMF3K7ql2nagzrRNRXDTC5TpkyIj2nOc4HVJKUIeNxnuM',
        'PHPSESSID=0h2ku0f1kclo0kqljnub4hgrq3; _ga=GA1.1.1047954399.1745742844; spa-crazy-monster_4520_hideNewbie=true; SM_GOLBAL_device_token=v2:ixoG6kaThqpayZfDKcIrkQVcoNPB29Y3bmfwsfMgkgOLMbG2yxMrCpRxu2dxHxpN1uzMXJFgQpQaD5ZbDdjo8rj3NRXnahbsNV+5dhTLbnPImwuDJ/wJz21rbHG0cYXUWNO8eDBgjJtLjAbmlJEgg2g7LNHwdriMk5kKIVC2LEXX9Y+4Fl4qF+jdVLTPTJi839E7PvpZzGEOokPEjRi5tkEmcUn2gW27NijgPm+7baFcoa+DENgaIlsg9H4BWID/Q1eWDJfaava4+LnwzymQ4lj+7q/dJstcXqEk7IAH34iWZCtiLF6Q; _ga_Y5QLWEHNZ4=GS1.1.1745814517.4.0.1745814517.60.0.0; oauth_token=SSZrmhXzD8Y52SYgew0iu9TtZCS44ItO; oauth_token_secret=GUkCcwYtntVEa3fAZAx6Nw4lKmCWMEhj; tgw_l7_route=431e385792b86f59a26ac8466105f32c',
        'oauth_token=xF7IdfDB9c1OIZWBH9IooyKNFkHO9M87; oauth_token_secret=Pi4EE7lZjq0V5JfGCgouV0OmnNsLo6h1; tgw_l7_route=431e385792b86f59a26ac8466105f32c',
        'oauth_token=o4Ee0quNK55bp7OYHD1uNyBo3v2jSZ9c; oauth_token_secret=SHqqJp5SyFpw5v1tuuSFvd5xEBzyKJ3j; tgw_l7_route=431e385792b86f59a26ac8466105f32c; PHPSESSID=bdgbeflvo1l44idgk45736k3os; SM_GOLBAL_device_token=v2:ixoG6kaThqpayZfDKcIrkQVcoNPB29Y3bmfwsfMgkgOLMbG2yxMrCpRxu2dxHxpN1uzMXJFgQpQaD5ZbDdjo8rj3NRXnahbsNV+5dhTLbnPImwuDJ/wJz21rbHG0cYXUWNO8eDBgjJtLjAbmlJEgg2g7LNHwdriMk5kKIVC2LEXX9Y+4Fl4qF+jdVLTPTJi839E7PvpZzGEOokPEjRi5tkEmcUn2gW27NijgPm+7baFcoa+DENgaIlsg9H4BWID/Q1eWDJfaava4+LnwzymQ4lj+7q/dJstcXqEk7IAH34iWZCtiLF6Q',
        'PHPSESSID=01esgcgad3iupvef1aqu057u63; _ga=GA1.1.1841150804.1745218482; spa-crazy-monster_4520_hideNewbie=true; oauth_token=3MzQzCJFm6uKo5NlZOF9RszMu08WcB9q; oauth_token_secret=WvPRgvRUCecV7w8HZYP8fmqRKre4ndQf; SM_GOLBAL_device_token=v2:ixoG4+VAQ1bGySERBhRt75ZAbU1uKdUQOSyJwzY4QGAtho2OwQo37DyQNthhWJMnvSsMGt3Vu79AjatJZV3dW/WiOlsGWEAJTCnhPnYiv17+116JVaL7mlFspGVpljFYVWhdcEBgijvMCZQJVt4Bq2py8q2I9Gy7C/e0tqmLP1I2oCAFpxpK3NvR1rak6aXFbb5vGnGrFLdgsUmxX55CpnzuIw0GDhNd2lWgxeZXs263FLdnSz1Ez6IrSJ/T9B/oiZzgS1NHuL8aRyyAYZZVExMBBL3T/7ipMqg/x7BEGVcBw2sqnMP/z6QeUA==; _ga_Y5QLWEHNZ4=GS1.1.1745819815.22.0.1745819815.60.0.0; tgw_l7_route=431e385792b86f59a26ac8466105f32c',
        'PHPSESSID=01esgcgad3iupvef1aqu057u63; _ga=GA1.1.1841150804.1745218482; spa-crazy-monster_4520_hideNewbie=true; SM_GOLBAL_device_token=v2:ixoG4+VAQ1bGySERBhRt75ZAbU1uKdUQOSyJwzY4QGAtho2OwQo37DyQNthhWJMnvSsMGt3Vu79AjatJZV3dW/WiOlsGWEAJTCnhPnYiv17+116JVaL7mlFspGVpljFYVWhdcEBgijvMCZQJVt4Bq2py8q2I9Gy7C/e0tqmLP1I2oCAFpxpK3NvR1rak6aXFbb5vGnGrFLdgsUmxX55CpnzuIw0GDhNd2lWgxeZXs263FLdnSz1Ez6IrSJ/T9B/oiZzgS1NHuL8aRyyAYZZVExMBBL3T/7ipMqg/x7BEGVcBw2sqnMP/z6QeUA==; oauth_token=oDADX6XaaiEDSlLqWdbYLaPAnvoJsYJ1; oauth_token_secret=2ThcV384rR4PjYiTEOPpW1veqnjvIVWp; tgw_l7_route=431e385792b86f59a26ac8466105f32c; _ga_Y5QLWEHNZ4=GS1.1.1745819815.22.1.1745820023.58.0.0',
        'oauth_token=DGC993OfmPD7M7d81HpeEye5bGlT4tol; oauth_token_secret=YFXAIcqN5TRNSrh5ZIWv2IHeJ3vKbhkW; tgw_l7_route=431e385792b86f59a26ac8466105f32c',
        'oauth_token=m7YdODMWsInw2oh3n6ECLkn5dP55ZHYX; oauth_token_secret=p8Ao47j59QLLJdqMmDUiWPAKz2bUUYWi; tgw_l7_route=431e385792b86f59a26ac8466105f32c',
    ]

    threads = []

    for idx, cookie in enumerate(cookies, start=1):
        t = threading.Thread(target=run_candy, args=(cookie, idx))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("所有账号执行完毕！")
