import settings
from crawlers.zhandaye import ZhangDaYeCrawler
from storages.get_storage import DEFAULT_STORAGE_CLASS
from storages.redis_storage import RedisStorage

from crawlers import CRAWLER_CLASS_LIST
from storages.sqllite_storage import SQLiteStorage
from utils.log import SimpleLogger


class Getter:
    def __init__(self, storage_class=DEFAULT_STORAGE_CLASS):
        self.storage_class = DEFAULT_STORAGE_CLASS.get_client_from_config()
        self.crawlers = [crawlers_cls() for crawlers_cls in CRAWLER_CLASS_LIST]
        self.logger = SimpleLogger(log_file=settings.GETTER_LOG_PATH)

    def run(self):
        if self.storage_class.is_full():
            self.logger.warning('Redis storage is full')
            return
        for crawler in self.crawlers:
            for proxy in crawler.run():
                self.logger.debug(f'add proxy {proxy} to storage')
                self.storage_class.add(proxy)


if __name__ == '__main__':
    getter = Getter()
    getter.run()
