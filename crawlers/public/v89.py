from crawlers.base import BaseCrawler
from schemas.proxy import Proxy
import re
from scrapy.selector import Selector

BASE_URL = 'https://www.89ip.cn/'


class V89Crawler(BaseCrawler):
    """
     89 https://www.89ip.cn/
    """
    urls = [BASE_URL]
    enable = True
    name = "https://www.89ip.cn/"

    def parse_content(self, html):
        response = Selector(text=html)
        for tr in response.css("table tbody tr"):
            # 使用css选择器提前第一个td标签的文本内容
            ip = tr.css("td:nth-child(1)::text").get().strip()
            port = tr.css("td:nth-child(2)::text").get().strip()

            if ip and port:
                yield Proxy(host=ip, port=int(port))


if __name__ == '__main__':
    crawler = V89Crawler()
    for proxy in crawler.run():
        print(proxy)
