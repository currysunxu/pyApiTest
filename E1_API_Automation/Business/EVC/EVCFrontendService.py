from hamcrest import assert_that

from E1_API_Automation.Lib.Moutai import Moutai


class EVCFrontendService(object):
    def __init__(self, host):
        self.host = host
        self.mou_tai = Moutai(host=self.host)

    def generate_header(self, proxy_domain):
        headers = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'sec-ch-ua': '"Chromium";v="87", "\\"Not;A\\\\Brand";v="99", "Microsoft Edge";v="87"',
            'Origin': proxy_domain,
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47',
            'Accept': '*/*',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'script',
            'Referer': proxy_domain,
            'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8,fr;q=0.7,fr-FR;q=0.6,zh-CN;q=0.5,zh;q=0.4',
        }
        return headers

    def request_frontend_js(self, url):
        response = self.mou_tai.get(url)

        if response.status_code != 200:
            raise Exception(
                "Failed to get frontend version, status code: %s, response content: %s" % (
                    response.status_code, response.content.decode("utf-8")))

        return response

    def verify_header_info(self, header):
        assert_that(header["vary"], "Origin")
        assert_that(header["Access-Control-Allow-Origin"], "*")
