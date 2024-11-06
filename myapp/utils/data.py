def sql_data():
    url = 'https://sql.ushow.media/query/'
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': 'csrftoken=EvGaao1X07aN4AkfgDxKGcZyOMlbhGdKMz3euVCfYUjSGqWPqp8za896B8iPPF5x; '
                  'sessionid=n1o7ailnty4sa6wsxc3ep3ezsz8hp1ut',
        'origin': 'https://sql.ushow.media',
        'priority': 'u=1, i',
        'referer': 'https://sql.ushow.media/sqlquery/',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/128.0.0.0 Safari/537.36',
        'x-csrftoken': 'EvGaao1X07aN4AkfgDxKGcZyOMlbhGdKMz3euVCfYUjSGqWPqp8za896B8iPPF5x',
        'x-requested-with': 'XMLHttpRequest'
    }
    return url, headers
