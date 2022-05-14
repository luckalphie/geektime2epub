import getpass

from lib.geektime_api import GeekTimeApi


class LoginChecker:
    def __init__(self):
        self.api = GeekTimeApi()

    def quit(self):
        self.api.save_cookie("")

    def check(self):
        result = self.api.get_user_info()

        if result.get('code') == 0:
            return True

        print("未登录，请先登录\n\n1:输入cookie\n2:手机号+密码)")

        loginWay = input("请选择登录方式: ")

        if loginWay.strip() == "1":
            cookie = input("输入Cookie: ")
            self.api.save_cookie(cookie)
            return

        if loginWay.strip() == "2":
            cell_phone = input("输入手机号: ")
            password = getpass.getpass("输入密码: ")
            cookie = self.api.login(cell_phone, password)
            self.api.save_cookie(cookie)
            return
