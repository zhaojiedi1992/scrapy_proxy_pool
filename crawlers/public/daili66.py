from crawlers.base import BaseCrawler
from schemas.proxy import Proxy
import re
from scrapy.selector import Selector

BASE_URL = 'http://www.66ip.cn/'
MAX_PAGE = 3


class DaiLi66Crawler(BaseCrawler):
    """
     代理66 http://www.66ip.cn/
    """
    urls = [BASE_URL]
    enable = False

    def parse_content(self, html):
        """
        parse html file to get proxies
        :return:
        """
        response = Selector(text=html)
        for tr in response.xpath("//table)[3]//tr"):
            #print(tr)
            ip = "".join(tr.xpath("./td[1]/text()")).strip()
            port = "".join(tr.xpath("./td[2]/text()")).strip()
            if ip and port:
                yield Proxy(host=ip, port=port)


if __name__ == '__main__':
    crawler = DaiLi66Crawler()
    for proxy in crawler.run():
        print(proxy)
