import requests
import jmespath
from hamcrest import assert_that, equal_to

from .HamcrestMatcher import match_to
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class Token():
    def __init__(self, name, jemspath):
        self.name = name
        self.token_jemspath = jemspath

    def get_name(self):
        return self.name

    def get_token_jemspath(self):
        return self.token_jemspath


class Moutai():
    def __init__(self, host, token=None, headers={"Content-Type": "application/json"}):
        self.token = token
        self.host = host
        self.headers = headers
        self.request_session = None

    def get_headers(self):
        return self.headers

    def set_header(self, headers):
        self.headers = headers

    def set_request_context(self, method, user_info, url, **kwargs):
        url_combined = self.host + url
        if self.token is None:
            self.request_session = requests.session()
            result = self.request_session.request(method, url_combined, json=user_info, verify=False, headers=self.headers, **kwargs)
            assert_that(result.status_code, equal_to(200))
            return result
        else:
            athentication_result = requests.request(method, url=url_combined, json=user_info,verify=False,
                                                 headers=self.headers, **kwargs)
            assert_that(athentication_result.status_code, equal_to(200), "Status code is not 200!")
            self.headers[self.token.get_name()] = self.__extract_token_value(self.token, athentication_result)
            return athentication_result

    def __extract_token_value(self, token, response):
        assert_that(response.json(), match_to(token.get_token_jemspath()),
                    "Unable to extract token value, the key might not exist.")
        return jmespath.search(token.get_token_jemspath(), response.json())

    def post(self, url, json=None, **kwargs):
        url_combined = self.host + url
        if self.token is None and self.request_session is not None:
            return self.request_session.post(url_combined, json=json,verify=False, headers=self.headers, **kwargs)
        else:
            return requests.post(url_combined, json=json,verify=False, headers=self.headers, **kwargs)

    def get(self, url, params=None, **kwargs):
        url_combined = self.host + url
        if self.token is None:
            if self.request_session is None:
                return requests.get(url_combined, verify=False, headers=self.headers, **kwargs, )
            else:
                return self.request_session.get(url_combined, verify=False,headers=self.headers, **kwargs,)
        else:
            return requests.get(url_combined, params, verify=False,headers=self.headers, **kwargs)

    def head(self, url, **kwargs):
        url_combined = self.host + url
        if self.token is None:
            return self.request_session.head(url_combined, headers=self.headers, **kwargs)
        else:
            return requests.head(url_combined, headers=self.headers, **kwargs)

    def options(self, url, **kwargs):
        url_combined = self.host + url
        if self.token is None and self.request_session is not None:
            return self.request_session.options(url_combined, headers=self.headers, **kwargs)
        else:
            return requests.options(url_combined, headers=self.headers, **kwargs)

    def requests(self, method, url, **kwargs):
        url_combined = self.host + url
        if self.token is None:
            return self.request_session.request(method, url_combined, verify=False,headers=self.headers, **kwargs)
        else:
            return requests.request(method, url_combined, verify=False,headers=self.headers, **kwargs)

    def delete(self, url,**kwargs):
        url_combined = self.host + url
        if self.token is None:
            return self.request_session.delete(url_combined, verify=False, headers=self.headers, **kwargs)
        else:
            return requests.delete(url_combined, verify=False, headers=self.headers, **kwargs)

    def put(self, url, json=None, **kwargs):
        url_combined = self.host + url
        if self.token is None and self.request_session is not None:
            return self.request_session.request("put", url_combined, verify=False,json=json, headers=self.headers, **kwargs)
        else:
            return requests.put(url_combined, json=json, verify=False, headers=self.headers, **kwargs)
