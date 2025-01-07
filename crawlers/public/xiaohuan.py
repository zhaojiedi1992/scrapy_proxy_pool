from crawlers.base import BaseCrawler
from schemas.proxy import Proxy
import re
from scrapy.selector import Selector

BASE_URL = 'https://ip.ihuan.me/'


class XiaoHuanCrawler(BaseCrawler):
    """
     小幻 https://ip.ihuan.me/
    """
    urls = [BASE_URL]
    enable = False

    def parse_content(self, html):
        response = Selector(text=html)
        for tr in response.css("tbody tr"):
            print(tr)
            ip =11
            port = "".join(tr.xpath("./td[2]/text()")).strip()
            if ip and port:
                yield Proxy(host=ip, port=port)


if __name__ == '__main__':
    crawler = XiaoHuanCrawler()
    for proxy in crawler.run():
        print(proxy)
