from abc import ABC
import random

from loguru import logger

from schemas.proxy import Proxy
from storages.base import BaseStorage
import settings
import redis

# from utils.proxy import extract_auth_proxy, is_valid_proxy


class RedisStorage(BaseStorage):

    def __init__(self, client):
        super().__init__(client)

    def max(self, proxy: Proxy):
        return self.client.zadd(settings.REDIS_KEY_PREFIX, {proxy.to_json(): settings.PROXY_SCORE_MAX})

    def count(self) ->int :
        return self.client.zcard(settings.REDIS_KEY_PREFIX)

    def decrease(self, proxy: Proxy):
        self.client.zincrby(settings.REDIS_KEY_PREFIX,-1, proxy.to_json())
        score = self.client.zscore(settings.REDIS_KEY_PREFIX, proxy.to_json())
        if score <= settings.PROXY_SCORE_MIN:
            self.remove(proxy)

    def remove(self, proxy: Proxy):
        cnt = self.client.zrem(settings.REDIS_KEY_PREFIX, proxy.to_json())
        logger.info(f'Proxy {proxy} removed, {cnt} removed')
        return cnt >= 1

    def exists(self, proxy: Proxy) -> bool:
        pass

    def add(self, proxy: Proxy, score=settings.PROXY_SCORE_INIT) -> int:
        if not proxy.is_valid():
            logger.info(f'Invalid proxy: {proxy}')
            return 0
        return self.client.zadd(settings.REDIS_KEY_PREFIX, {proxy.to_json(): score})

    def random(self) -> Proxy:
        proxies = self.client.zrangebyscore(settings.REDIS_KEY_PREFIX, settings.PROXY_SCORE_MAX,
                                            settings.PROXY_SCORE_MAX)
        if len(proxies) > 0:
            return Proxy.load_proxy(random.choice(proxies))
        proxies = self.client.zrangebyscore(settings.REDIS_KEY_PREFIX, settings.PROXY_SCORE_MIN,
                                            settings.PROXY_SCORE_MAX)
        if len(proxies) > 0:
            return Proxy.load_proxy(random.choice(proxies))
        raise Exception('No proxy available')

    def all(self):
        proxies = self.client.zrangebyscore(settings.REDIS_KEY_PREFIX, settings.PROXY_SCORE_MAX,
                                            settings.PROXY_SCORE_MAX)
        if len(proxies) > 0:
            return [Proxy.load_proxy(proxy) for proxy in proxies]

        proxies = self.client.zrangebyscore(settings.REDIS_KEY_PREFIX, settings.PROXY_SCORE_MIN,
                                            settings.PROXY_SCORE_MAX)
        if len(proxies) > 0:
            return[Proxy.load_proxy(proxy) for proxy in proxies]
        return []


    def batch(self,cursor,count):
        cursor, proxies = self.client.zscan(settings.REDIS_KEY_PREFIX, cursor, count=count)
        return cursor, [Proxy.load_proxy(i[0]) for i in proxies]


    def is_full(self):
        return self.count() >= settings.REDIS_STORAGE_LIMIT
    @classmethod
    def get_client_from_config(cls):
        client = redis.StrictRedis(host=settings.REDIS_HOST,
                                   port=settings.REDIS_PORT,
                                   db=settings.REDIS_DB,
                                   password=settings.REDIS_PASSWORD,
                                   decode_responses=True)
        return cls(client)



if __name__ == '__main__':
    conn = RedisStorage.get_client_from_config()
    conn.add(proxy=Proxy(host='127.0.0.1', port=80),score=10)
    conn.max(proxy=Proxy(host='127.0.0.1', port=80))
    result = conn.random()
    a,b= conn.batch(0,2)
    print(a,b)
    print(result)
