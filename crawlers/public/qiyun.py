from crawlers.base import BaseCrawler
from crawlers.public.kuaidaili import MAX_PAGE
from schemas.proxy import Proxy
import re
from scrapy.selector import Selector

BASE_URL = 'https://proxy.ip3366.net/free/?action=china&page={page}'
MAX_PAGE = 10

class QiYunCrawler(BaseCrawler):
    """
     qiyun https://proxy.ip3366.net/free/?action=china&page=11
    """
    urls =  [BASE_URL.format(page=page) for page in range(1, MAX_PAGE + 1)]
    enable = True
    name = "https://proxy.ip3366.net"

    def parse_content(self, html):
        response = Selector(text=html)
        for tr in response.css("table tbody tr"):
            #print(tr)
            # 使用css选择器提前第一个td标签的文本内容
            ip = tr.css("td:nth-child(1)::text").get().strip()
            port = tr.css("td:nth-child(2)::text").get().strip()

            if ip and port:
                yield Proxy(host=ip, port=int(port))


if __name__ == '__main__':
    crawler = QiYunCrawler()
    for proxy in crawler.run():
        print(proxy)
