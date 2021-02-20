from collectors import AbstractCollector, PagesCollector
from parsers import RegexParser

import http_client
import lxml.html


class BaseHideMyNameCollector(PagesCollector):
    def __init__(self, url):
        super(BaseHideMyNameCollector, self).__init__()
        self.url = url
        self.processing_period = 30 * 60

    async def process_page(self, page_index):
        result = []
        if page_index > 0:
            self.url = f"&start={page_index * 64}#".join(self.url.split("#"))

        resp = await http_client.get_text(url=self.url)
        tree = lxml.html.fromstring(resp)

        ips = tree.xpath("//div[@class='table_block']//table//tbody//td[position() mod 7 = 1]/text()")
        ports = tree.xpath("//div[@class='table_block']//table//tbody//td[position() mod 7 = 2]/text()")
        countries = tree.xpath("//div[@class='table_block']//table//tbody//td/span[@class='country']/text()")
        type_ = tree.xpath("//div[@class='table_block']//table//tbody//td[position() mod 7 = 5]/text()")

        for i in range(0, len(ips)-1, 1):
            if countries[i].find("Russia") == -1:
                try:
                    result.append(f"{type_[i].split(',')[1].lower()}://{ips[i]}:{ports[i]}")
                except IndexError:
                    result.append(f"{type_[i].split(',')[0].lower()}://{ips[i]}:{ports[i]}")
        return result


class Collector(BaseHideMyNameCollector):
    __collector__ = True
    
    def __init__(self):
        super(Collector, self).__init__("http://localhost:8050/render.html?timeout=10&url="
                                        "https://hidemy.name/en/proxy-list/?anon=234#list")
