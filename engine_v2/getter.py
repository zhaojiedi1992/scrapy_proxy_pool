import settings
from crawlers.zhandaye import ZhangDaYeCrawler
from storages.redis_storage import RedisStorage

from crawlers import CRAWLER_CLASS_LIST
class Getter:
    def __init__(self, storage_class=RedisStorage):

        self.storage_class = storage_class.get_client_from_config()
        self.crawlers = [crawlers_cls() for crawlers_cls in CRAWLER_CLASS_LIST]

    def run(self):
        if self.storage_class.is_full():
            print('Redis storage is full')
            return
        for crawler in self.crawlers:
            for proxy in crawler.run():
                self.storage_class.add(proxy)


if __name__ == '__main__':
    getter = Getter()
    getter.run()
