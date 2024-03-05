# 定义一个抽象类，所有存储的基类都继承这个抽象类
from abc import ABCMeta, abstractmethod

from schemas.proxy import Proxy
from loguru import logger


class BaseStorage(metaclass=ABCMeta):

    def __init__(self, client):
        self.client = client

    @abstractmethod
    def add(self, proxy: Proxy, score: int):
        raise NotImplementedError

    @abstractmethod
    def decrease(self, proxy: Proxy):
        raise NotImplementedError

    @abstractmethod
    def remove(self, proxy: Proxy):
        raise NotImplementedError

    @abstractmethod
    def exists(self, proxy: Proxy) -> bool:
        raise NotImplementedError

    @abstractmethod
    def max(self, proxy: Proxy) -> int:
        raise NotImplementedError

    @abstractmethod
    def count(self)->int:
        raise NotImplementedError

    @abstractmethod
    def random(self)-> Proxy:
        raise NotImplementedError

    @abstractmethod
    def is_full(self):
        raise NotImplementedError

    @abstractmethod
    def batch(self, cursor, count):
        raise NotImplementedError

    def is_valid_proxy(self, proxy: Proxy) -> bool:
        if not self.exists(proxy):
            logger.warning("Proxy {} is not in storage".format(proxy))
            return False
