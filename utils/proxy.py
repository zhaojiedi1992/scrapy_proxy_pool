import re

from schemas.proxy import Proxy

IP_PATTERN_STR = "(?P<ip>((25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|\d)\.){3}(25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|\d))"
PORT_PATTERN_STR = "(?P<port>\d{1,5})"
USERNAME_PATTERN_STR = "(?P<username>\S+)"
PASSWORD_PATTERN_STR = "(?P<password>\S+)"
PROXY_PATTERN_STR = "({}:{}@)?{}:{}".format(USERNAME_PATTERN_STR, PASSWORD_PATTERN_STR,
                                            IP_PATTERN_STR, PORT_PATTERN_STR)

IP_PATTERN = re.compile(r"^{}$".format(IP_PATTERN_STR))
PORT_PATTERN = re.compile(r"^{}$".format(PORT_PATTERN_STR))
PROXY_PATTERN = re.compile(r"^{}$".format(PROXY_PATTERN_STR))


# 判断一个字符串是否是一个合法的ip地址
def is_valid_ip(ip):
    if IP_PATTERN.match(ip):
        return True
    return False


def is_valid_port(port):
    if PORT_PATTERN.match(port):
        return True
    return False


def extract_auth_proxy(data):
    result = PROXY_PATTERN.match(data)
    if result:
        return Proxy(host=result.group('ip'),
                     port=int(result.group('port')),
                     username=result.group('username'),
                     password=result.group('password'))
    return None


def is_valid_proxy(data):
    if PROXY_PATTERN.match(data):
        return True
    return False


if __name__ == '__main__':
    proxy = 'test1234:test5678.@117.68.216.212:32425'
    print(extract_auth_proxy(proxy))
    print(is_valid_proxy('127.0.0.1:80'))
    print(is_valid_proxy(proxy))
