from abc import ABC
import random

from loguru import logger

from schemas.proxy import Proxy
from storages.base import BaseStorage
import settings
import redis

from utils.proxy import extract_auth_proxy, is_valid_proxy


class RedisStorage(BaseStorage):

    def __init__(self, client):
        super().__init__(client)

    def max(self, proxy: Proxy):
        return self.client.zadd(settings.REDIS_KEY_PREFIX, {str(proxy): settings.PROXY_SCORE_MAX})

    def count(self) ->int :
        return self.client.zcard(settings.REDIS_KEY_PREFIX)

    def decrease(self, proxy: Proxy):
        self.client.zincrby(settings.REDIS_KEY_PREFIX,-1, str(proxy))
        score = self.client.zscore(settings.REDIS_KEY_PREFIX, str(proxy))
        if score <= settings.PROXY_SCORE_MIN:
            self.remove(proxy)

    def remove(self, proxy: Proxy):
        self.client.zrem(settings.REDIS_KEY_PREFIX, str(proxy))
        logger.info(f'Proxy {proxy} removed')

    def exists(self, proxy: Proxy) -> bool:
        pass

    def add(self, proxy: Proxy, score=settings.PROXY_SCORE_INIT) -> int:
        if not is_valid_proxy(str(proxy)):
            logger.info(f'Invalid proxy: {proxy}')
            return 0
        return self.client.zadd(settings.REDIS_KEY_PREFIX, {str(proxy): score})

    def random(self) -> Proxy:
        proxies = self.client.zrangebyscore(settings.REDIS_KEY_PREFIX, settings.PROXY_SCORE_MAX,
                                            settings.PROXY_SCORE_MAX)
        if len(proxies) > 0:
            return extract_auth_proxy(random.choice(proxies))
        proxies = self.client.zrangebyscore(settings.REDIS_KEY_PREFIX, settings.PROXY_SCORE_MIN,
                                            settings.PROXY_SCORE_MAX)
        if len(proxies) > 0:
            return extract_auth_proxy(random.choice(proxies))
        raise Exception('No proxy available')

    def batch(self,cursor,count):
        cursor, proxies = self.client.zscan(settings.REDIS_KEY_PREFIX, cursor, count=count)
        return cursor, [extract_auth_proxy(i[0]) for i in proxies]


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
