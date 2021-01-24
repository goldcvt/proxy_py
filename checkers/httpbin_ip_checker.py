from checkers.base_checker import BaseChecker, CheckerResult
import aiohttp
from json.decoder import JSONDecodeError


class HTTPBinIPChecker(BaseChecker):
    def __init__(self, timeout=None):
        super(htpbin_ip_checker, self).__init__("http://httpbin.org/ip", timeout=timeout)

    async def validate(self, response: aiohttp.ClientResponse, checker_result: CheckerResult) -> bool:
        try:
            json_result = await response.json(content_type=None)
        except JSONDecodeError:
            json_result = ""
        if response.status != 200:
            return False
        elif not json_result:
            return False
        elif 'origin' in json_result:
            CheckerResult.ipv4 = json_result['origin']
            return True
        return True
