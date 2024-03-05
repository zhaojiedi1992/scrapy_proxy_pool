import time
from abc import ABCMeta, abstractmethod

import requests
from fake_headers import Headers
from loguru import logger
from retrying import RetryError, retry

import settings
from storages.base import BaseStorage


class BaseCrawler(metaclass=ABCMeta):
    urls = []
    name="base"

    @retry(stop_max_attempt_number=3, retry_on_result=lambda x: x is None, wait_fixed=2000)
    def fetch_one_content(self, url, **kwargs):
        try:
            headers = Headers(headers=True).generate()
            kwargs.setdefault('timeout', settings.CRAWL_TIMEOUT)
            kwargs.setdefault('verify', False)
            kwargs.setdefault('headers', headers)
            response = requests.get(url, **kwargs)
            if response.status_code == 200:
                response.encoding = 'utf-8'
                return response.text
        except (requests.ConnectionError, requests.ReadTimeout):
            return

    @abstractmethod
    def parse_content(self, html):
        raise NotImplementedError

    # @abstractmethod
    # def save_content(self, data):
    #     raise NotImplementedError

    def process(self, html, url):
        for proxy in self.parse_content(html):
            logger.info(f'fetch proxy {proxy} from {url}')
            yield proxy

    def run(self):
        try:
            for url in self.urls:
                logger.info('start crawl %s' % url)
                html = self.fetch_one_content(url)
                if not html:
                    continue
                time.sleep(0.5)
                yield from self.process(html, url)
        except RetryError as e:
            logger.error(f'crawl {self.name} error')
