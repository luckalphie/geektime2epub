#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

:author alphie.chen
:version 1.0.0
:date 2022/05/14
"""
import json
import time

import requests

from lib.coms import *

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,fr;q=0.5,pt;q=0.4',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'DNT': '1',
    'Origin': 'https://time.geekbang.org',
    'Referer': 'https://time.geekbang.org/dashboard/usercenter',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Microsoft Edge";v="101"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1 Edg/100.0.4896.60'
}


class GeekTimeApi:
    baseUrl = 'https://time.geekbang.org'
    accountUrl = 'https://account.geekbang.org'

    def __init__(self):
        self.read_cookie()

    def my_product_list(self):
        url = f"{self.baseUrl}/serv/v3/learn/product"

        payload = json.dumps({
            "desc": True,
            "expire": 1,
            "last_learn": 0,
            "learn_status": 0,
            "prev": 0,
            "size": 100,
            "sort": 1,
            "type": "c1",
            "with_learn_count": 1
        })

        response = requests.request("POST", url, headers=headers, data=payload)

        return json.loads(response.text.strip(), strict=False).get('data').get('products')

    def get_article(self, article_id):
        url = f"{self.baseUrl}/serv/v1/article"

        payload = json.dumps({
            "id": article_id,
            "include_neighbors": True,
            "is_freelyread": True
        })
        time.sleep(4)

        response = requests.request("POST", url, headers=headers, data=payload)
        print_gray("\tresponse header", response.headers)
        print_gray('\tresponse text', response.text)

        time.sleep(1)
        return json.loads(response.text.strip(), strict=False).get('data')

    def get_product_info(self, product_id):
        url = "https://time.geekbang.org/serv/v3/column/info"

        payload = json.dumps({
            "product_id": product_id,
            "with_recommend_article": True
        })

        time.sleep(1)
        response = requests.request("POST", url, headers=headers, data=payload)

        print_gray(response.text)
        return json.loads(response.text).get('data', {})

    def get_article_list(self, product_id):
        url = "https://time.geekbang.org/serv/v1/column/articles"

        payload = json.dumps({
            "cid": product_id,
            "size": 500,
            "prev": 0,
            "order": "earliest",
            "sample": False
        })

        response = requests.request("POST", url, headers=headers, data=payload)

        print_gray(response.text)

        return json.loads(response.text).get('data').get('list')

    def get_user_info(self):
        url = f"{self.accountUrl}/serv/v1/user/auth?t=" + str(int(time.time() * 1000))

        payload = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        print_gray(response.text)
        return json.loads(response.text)

    def login(self, cellphone: str, password: str):
        import requests
        import json

        url = f"{self.accountUrl}/account/ticket/login"

        payload = json.dumps({
            "platform": 3,
            "appid": 1,
            "remember": 1,
            "data": "",
            "source": "",
            "ucode": "",
            "sc": {
                "uid": "",
                "report_source": "Web",
                "utm_identify": "",
                "utm_source": "",
                "utm_medium": "",
                "utm_campaign": "",
                "utm_content": "",
                "utm_term": "",
                "share_code": "",
                "original_id": "180c2182deb452-0896c8ce591a75-654d2141-1296000-180c2182dec1862",
                "refer": "极客时间"
            },
            "country": 86,
            "cellphone": cellphone,
            "password": password
        })

        response = requests.request("POST", url, headers=headers, data=payload)

        cookie_list = []
        set_cookie = response.headers.get("Set-Cookie")

        for co in set_cookie.split(','):
            cookie_list.append(co.split(';')[0])

        print("set-cookie:", len(cookie_list))

        return ';'.join(cookie_list)

    def save_cookie(self, cookie: str):
        headers['Cookie'] = cookie
        with open("./temp/cookie.tmp", 'w') as f:
            f.write(cookie)

    def read_cookie(self):
        if not os.path.exists("./temp/cookie.tmp"):
            return
        with open("./temp/cookie.tmp") as f:
            headers['Cookie'] = f.read()


if __name__ == '__main__':
    products = GeekTimeApi().my_product_list()

    for p in products:
        print(p['id'], p['title'])
