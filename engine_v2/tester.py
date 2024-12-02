import asyncio
import aiohttp

import settings
from schemas.proxy import Proxy
from storages.get_storage import DEFAULT_STORAGE_CLASS
from storages.redis_storage import RedisStorage
from utils.log import SimpleLogger


class Tester(object):
    def __init__(self,storage=DEFAULT_STORAGE_CLASS):
        self.storage = storage.get_client_from_config()
        self.loop = asyncio.get_event_loop()
        self.logger = SimpleLogger(log_file=settings.TESTER_LOG_PATH)
        pass
    def run(self):
        self.logger.info('stating tester...')
        cursor =0
        while True:
            self.logger.debug(f'testing proxies use cursor {cursor}, count {settings.TEST_BATCH_COUNT}')
            cursor, proxies = self.storage.batch(cursor, count=settings.TEST_BATCH_COUNT)
            if proxies:
                tasks = [self.loop.create_task(self.test(proxy)) for proxy in proxies]
                self.loop.run_until_complete(asyncio.wait(tasks))
            if not cursor:
                break

    async def test(self, proxy: Proxy):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            try:
                self.logger.debug(f'testing proxy {proxy}')
                if settings.TEST_ANONYMOUS:
                    url = 'https://httpbin.org/ip'
                    async with session.get(url, timeout=settings.TEST_TIMEOUT) as response:
                        resp_json = await response.json()
                        origin_ip = resp_json['origin']
                    async with session.get(url, proxy=f'http://{proxy.string()}', timeout=settings.TEST_TIMEOUT) as response:
                        resp_json = await response.json()
                        anonymous_ip = resp_json['origin']
                    assert origin_ip != anonymous_ip
                    assert proxy.host == anonymous_ip
                async with session.get(settings.TEST_URL, proxy=f'http://{proxy}', timeout=settings.TEST_TIMEOUT,
                                       allow_redirects=False) as response:
                    if response.status in settings.TEST_VALID_STATUS:
                        if settings.TEST_DONT_SET_MAX_SCORE:
                            self.logger.debug(f'proxy {proxy} is valid, remain current score')
                        else:
                            self.storage.max(proxy)
                            self.logger.debug(f'proxy {proxy} is valid, set max score')
                    else:
                        self.storage.decrease(proxy)
                        self.logger.debug(f'proxy {proxy} is invalid, decrease score')
            except Exception:
                self.storage.decrease(proxy)
                self.logger.debug(f'proxy {proxy} is invalid, decrease score')

def run_tester():
    host = '96.113.165.182'
    port = 3128
    tasks = [tester.test(Proxy(host=host, port=port))]
    tester.loop.run_until_complete(asyncio.wait(tasks))


if __name__ == '__main__':
    tester = Tester()
    #tester.run()
    run_tester()