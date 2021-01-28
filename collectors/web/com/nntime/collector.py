from collectors import AbstractCollector, PagesCollector
from parsers import RegexParser
import js2py
from lxml import etree
import dateparser

import http_client
import lxml.html
import re
import async_requests


class BaseNNTimeCollector(PagesCollector):
    __collector__ = True

    def __init__(self, url):
        super(BaseNNTimeCollector, self).__init__()
        self.url = url

    async def process_page(self, page_index):
        result = []
        if page_index > 0:
            self.url += '%02d.htm' % (page_index + 1,)

        resp = await async_requests.get(url=self.url)
        html = resp.text
        tree = lxml.html.fromstring(html)
        try:
            elements = tree.xpath("//table[@class='data']//td")
            elements.pop(0)

            port_variables = tree.xpath("//script[text()[contains(., '=')]]/text()")[0].replace("\n", "")
            if port_variables[-1] == ";":
                port_variables = port_variables[:-1]
            port_variables = dict((k.strip(), int(v.strip())) for k,v in
                                  (item.split('=') for item in port_variables[:-1].split(';')))

            scripts = tree.xpath("//td/script/text()")
            # dates = tree.xpath("//td/dfn/text()")
            port_list = []

            for script in scripts:
                keys = script.replace('document.write(":"+', '').replace(")", "").split("+")
                port_list += ["".join(str(port_variables[key]) for key in keys)]

            for i in range(0, len(elements) - 1, 6):
                if elements[i+1].find("Russian") != -1:
                    results.append(f"{elements[i + 1].text}:{port_list[i // 6]}")

        except KeyError:
            pass
        except IndexError:
            pass
        return result


class Collector(BaseNNTimeCollector):
    __collector__ = True

    def __init__(self):
        super(Collector, self).__init__("http://nntime.com/proxy-list-")
