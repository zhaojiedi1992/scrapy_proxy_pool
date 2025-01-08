import settings
from storages.get_storage import DEFAULT_STORAGE_CLASS

from crawlers import CRAWLER_CLASS_LIST
from utils.log import SimpleLogger

from panda_python_kit.scrapy.ip_location import get_ip_info
from concurrent.futures import ThreadPoolExecutor, as_completed

class Getter:
    def __init__(self, storage_class=DEFAULT_STORAGE_CLASS):
        self.storage_class = DEFAULT_STORAGE_CLASS.get_client_from_config()
        self.crawlers = [crawlers_cls() for crawlers_cls in CRAWLER_CLASS_LIST]
        self.logger = SimpleLogger(log_file=settings.GETTER_LOG_PATH)

    def run(self):
        if self.storage_class.is_full():
            self.logger.warning('Redis storage is full')
            return
        # 帮忙给我下面的这个代码升级为并行的， 让每个crawler独立运行
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(crawler.run): crawler for crawler in self.crawlers}
            for future in as_completed(futures):
                crawler = futures[future]
                try:
                    for proxy in future.result():
                        proxy.source = crawler.name
                        try:
                            info = get_ip_info(proxy.host)
                            proxy.country = info.country_short
                            proxy.province = info.region
                            proxy.city = info.city
                        except Exception as e:
                            pass
                        self.logger.debug(f'add proxy {proxy} to storage')
                        self.storage_class.add(proxy)
                except Exception as e:
                    self.logger.error(f'Error running crawler {crawler.name}: {e}')
        # for crawler in self.crawlers:
        #     for proxy in crawler.run():
        #         proxy.source = crawler.name
        #         try:
        #             info = get_ip_info(proxy.host)
        #             proxy.country = info.country_short
        #             proxy.province = info.region
        #             proxy.city = info.city
        #         except Exception as e:
        #             pass
        #         self.logger.debug(f'add proxy {proxy} to storage')
        #         self.storage_class.add(proxy)


if __name__ == '__main__':
    getter = Getter()
    getter.run()
