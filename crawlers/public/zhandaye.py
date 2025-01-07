import re

from loguru import logger

import settings
from crawlers.base import BaseCrawler
from fake_headers import Headers
import requests
from pyquery import PyQuery as pq

from schemas.proxy import Proxy

base_url = 'https://www.zdaye.com/dayProxy/{page}.html'
max_page = 10

class ZhangDaYeCrawler(BaseCrawler):
    enable=True
    name = 'ZhangDaYe'
    urls = []
    catalog_urls = [base_url.format(page=page) for page in range(1, max_page)]
    headers = {
        'User-Agent': 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def parse_catalog(self, html):
        doc = pq(html)
        for item in doc('.arccont a').items():
            url = 'https://www.zdaye.com' + item.attr('href')
            logger.info(f'get detail url: {url}')
            self.urls.append(url)
        pass

    def parse_content(self, html):
        doc = pq(html)
        rows = doc('#ipc tr').items()
        # 遍历所有的行
        for row in rows:
            # 选择当前行的前两个td标签，即IP和端口
            cells = row('td')
            ip = cells.eq(0).text()
            port = cells.eq(1).text()
            # 创建一个字典，包含ip和port信息，并添加到结果列表中
            yield Proxy(host=ip, port=port)

    def save_content(self, data):
        pass

    def run(self):
        self.run_catalog()
        yield from super().run()

    def run_catalog(self):
        for url in self.catalog_urls:
            logger.info(f'fetching {url}')
            html = self.fetch_one_content(url, headers=self.headers)
            self.parse_catalog(html)


if __name__ == '__main__':
    crawler = ZhangDaYeCrawler()
    result = crawler.run()
    # crawler2 = ZhangDaYeCrawler()
    # html = crawler2.fetch_one_content('https://www.zdaye.com/dayProxy/ip/335628.html', headers=crawler2.headers)
    # # html = ""
    # # with open('./a.html') as f :
    # #     html = f.read()
    # result = crawler2.parse_content(html)
    print(list(result))
