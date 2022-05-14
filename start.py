#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

:author alphie.chen
:version 1.0.0
:date 2022/05/14
"""
from lib.geektime_epub import GeekTime2Epub
from lib.login_checker import LoginChecker
from lib.product_list import ProductListGetter


def down_all():
    list1 = ProductListGetter().get_product_list()

    for p in list1:
        print("开始下载：", p.productTitle)
        GeekTime2Epub(p.productId).start()


def down_one(productId):
    print("开始下载：", productId)
    GeekTime2Epub(productId).start()


def main():
    LoginChecker().check()

    print("1:全部专栏\n2:指定专栏\n3:退出账号")
    opt_value = input("选择操作: ").strip()
    if opt_value == "1":
        down_all()
        return

    if opt_value == "2":
        productId = int(input("输入课程ID: ").strip())
        down_one(productId)
        return

    if opt_value == "3":
        LoginChecker().quit()
        return


if __name__ == '__main__':
    main()
