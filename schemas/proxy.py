import json

import attrs
from panda_python_kit.scrapy.ip_location import get_ip_info
from dataclasses import dataclass

class Proxy(object):
    def __init__(self, host, port=80, username=None, password=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.source = None
        self.country = None
        self.region = None
        self.city = None
        self.isp = None


    def __str__(self):
        """
        to string, for print
        :return:
        """
        if self.username and self.password:
            return f'{self.username}:{self.password}@{self.host}:{self.port}'
        return f'{self.host}:{self.port}'

    # def string(self):
    #     """
    #     to string
    #     :return: <host>:<port>
    #     """
    #     return self.__str__()

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            "host":self.host,
            "port":self.port,
            "proxy": str(self),
            "username":self.username,
            "password":self.password,
            "source":self.source,
            "country":self.country,
            "region":self.region,
            "city":self.city,
            "isp":self.isp
        }
    def is_valid(self):
        if self.host and self.port:
            return True
        return False

    @staticmethod
    def load_proxy(json_data):
        obj_dict =json.loads(json_data)
        proxy =   Proxy(
            host=obj_dict['host'],
            port=obj_dict['port'],
            username=obj_dict['username'],
            password=obj_dict['password']
        )
        proxy.country = obj_dict['country']
        proxy.region = obj_dict['region']
        proxy.city = obj_dict['city']
        proxy.isp = obj_dict['isp']
        return proxy

    @staticmethod
    def fill_proxy_info(proxy_str):
        parts = proxy_str.split('@')
        if len(parts) == 2:
            username, password = parts[0].split(':')
            ip_port = parts[1]
        else:
            username = password = None
            ip_port = parts[0]

        ip, port = ip_port.split(':')
        port = int(port)
        proxy = Proxy(host=ip, port=port, username=username, password=password)
        try:
            info = get_ip_info(proxy.ip)
            proxy.country = info.country
            proxy.region = info.region
            proxy.city = info.city
        except  Exception as e:
            pass
        return proxy

