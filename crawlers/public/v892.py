from crawlers.base import BaseCrawler
from schemas.proxy import Proxy
import re
from scrapy.selector import Selector

BASE_URL = 'https://api.89ip.cn/tqdl.html?api=1&num=4000&port=&address=&isp='


class V89V2Crawler(BaseCrawler):
    """
     89 https://www.89ip.cn/
    """
    urls = [BASE_URL]
    enable = True
    name = "https://www.89ip.cn/"

    def parse_content(self, html):

        pattern = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d{1,5})"
        matches = re.findall(pattern, html)
        for match in matches:
            if len(match) !=2:
                continue
            ip = match[0]
            port = match[1]
            if ip and port:
                yield Proxy(host=ip, port=int(port))

if __name__ == '__main__':
    crawler = V89V2Crawler()
    proxy_list = list(crawler.run())
    print(len(proxy_list))
