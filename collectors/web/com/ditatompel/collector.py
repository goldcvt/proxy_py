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

    @staticmethod
    def parse_from_splash_page(tree):
        return []  # TODO return a list, don't forget to filter out RU proxies

    async def process_page(self, page_index):
        result = []
        if page_index > 0:
            self.url = "http://localhost:8050/render.html?timeout=10&url=https://www.ditatompel.com/proxy/anonymity/elite"

        resp = await http_client.get_text(url=self.url)
        tree = lxml.html.fromstring(resp)
        result += self.parse_from_splash_page(tree)
        _script = """
                        local bounds = element:bounds()
                        assert(element:mouse_click{x=bounds.width/3, y=bounds.height/3})
                        return splash:html()
                    end"""
        # and then get every rest of 'em
        for i in range(2, 30, 1):
            # inserting a lua script into the thingie
            script = f"""
                function main(splash)
                    local element = splash:select('li.paginate_button > a.page-link[data-dt-idx="{i}"]')
                    """  # we need to know what page to go to
            url = self.url.split("url")[0] + script + _script + "url" + self.url.split("url")[1]
            # TODO what if there's no ith page?
            resp = await http_client.get_text(url=url)
            tree = lxml.html.fromstring(resp)

            result += self.parse_from_splash_page(tree)
        return result


class Collector(BaseDitaTompelCollector):
    __collector__ = True

    def __init__(self):
        super(Collector, self).__init__("http://localhost:8050/render.html?timeout=10&url=https://www.ditatompel.com/proxy/anonymity/anon", 2)
