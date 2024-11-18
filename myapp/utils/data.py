def sql_data():
    url = 'https://sql.ushow.media/query/'
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': '_ga=GA1.1.1792866753.1713751715; _ga_Y5QLWEHNZ4=GS1.1.1731316808.31.0.1731316851.17.0.0; '
                  'csrftoken=4jB3JRrZfEtoB24MKGQ13Xkvgzg5tQKPhxnph33PK89csvNkwLFUzlQAUd1XAgip; '
                  'sessionid=bfz8vpilj0o1nk29difwxqrdyhnb15w2; tgw_l7_route=7a3b5e35664bcb9b34e8b8e8ba155169; '
                  'sessionid=bfz8vpilj0o1nk29difwxqrdyhnb15w2',
        'origin': 'https://sql.ushow.media',
        'priority': 'u=1, i',
        'referer': 'https://sql.ushow.media/sqlquery/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, '
                      'like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
        'x-csrftoken': '4jB3JRrZfEtoB24MKGQ13Xkvgzg5tQKPhxnph33PK89csvNkwLFUzlQAUd1XAgip',
        'x-requested-with': 'XMLHttpRequest'
    }
    return url, headers
