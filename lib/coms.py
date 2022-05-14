import hashlib
import os
import sys
from typing import NoReturn, Any, Tuple

__current_path__ = os.path.dirname(__file__)
TEMP_PATH = os.path.abspath(os.path.join(__current_path__, '../temp'))


def md5(text):
    return hashlib.md5(text.encode(encoding='UTF-8')).hexdigest()


def wrap_color(color_no: int, text: str) -> str:
    if hasattr(sys.stdout, 'isatty') and sys.stdout.isatty():
        return text

    return "\033[0;%d;1m%s\033[0m" % (color_no, text)


def join_string(message: Tuple[Any, ...]) -> str:
    """
    拼接变量

    :param message: 变量元祖
    :return: 字符串
    """
    return " ".join(map(lambda x: '%s', message)) % message


def print_gray(*message: Any, max_length=100) -> NoReturn:
    """
    灰色打印

    :param max_length: 最大长度
    :param message: 打印内容元祖
    """
    text = join_string(message)[0:max_length]
    print(f"\033[0;37;1m{text}\033[0m")


def print_blue(*message: Any) -> NoReturn:
    print("\033[0;34;1m" + join_string(message) + "\033[0m")


def print_yellow(*message: Any) -> NoReturn:
    print(wrap_color(33, join_string(message)) + "\033[0m")
