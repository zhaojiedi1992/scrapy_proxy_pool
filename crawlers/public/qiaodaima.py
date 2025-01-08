import time

from crawlers.base import BaseCrawler
from schemas.proxy import Proxy
import re
from scrapy.selector import Selector

BASE_URL = 'https://ip.uqidata.com/free/type/http-1.html'
from loguru import logger
from playwright.sync_api import sync_playwright

class QiaoDaiMaCrawler(BaseCrawler):
    """
      https://ip.uqidata.com/free/type/http-1.html
    """
    urls = [BASE_URL]
    enable = True
    name = "https://ip.uqidata.com/free/type/http-1.html"

    def parse_content(self, html):
        response = Selector(text=html)

        for tr in response.css("tbody tr"):
            # 使用css选择器提前第一个td标签的文本内容
            #print(tr)
            # 提取IP信息
            ip_parts = tr.css(
                'td.ip span:not([style*="display: none"])::text,td.ip div:not([style*="display: none"])::text,td.ip span:not([style*="display: none"])::text').getall()
            ip = "".join(ip_parts).strip()

            # 提取端口信息
            port = tr.css('td.port::text').get()
            if ip and port :
                yield Proxy(host=ip, port=port)

    def fetch_one_content(self, url):
        with sync_playwright() as p:
            # Channel can be "chrome", "msedge", "chrome-beta", "msedge-beta" or "msedge-dev".
            browser = p.chromium.launch(channel="chrome")
            page = browser.new_page()
            page.goto(url)
            html_content = page.content()
            browser.close()
            return html_content


if __name__ == '__main__':
    crawler = QiaoDaiMaCrawler()
    result = list(crawler.run())
    print(len(result))
    print(result)
