from collectors import AbstractCollector, PagesCollector
from parsers import RegexParser
import js2py
from lxml import etree
import dateparser

import http_client
import lxml.html
import re
import async_requests


class BaseDitaTompelCollector(PagesCollector):
    def __init__(self, url, pages_count):
        super(BaseCollectorPremProxyCom, self).__init__()
        self.url = url
        self.pages_count = pages_count

    async def process_page(self, page_index):
        result = []
        if page_index > 0:
            self.url += '%02d.htm' % (page_index + 1,)


class Collector(BaseDitaTompelCollector):
    __collector__ = True
    
    def __init__(self):
        super(Collector, self).__init__("https://www.ditatompel.com/proxy/type/http", 2)
