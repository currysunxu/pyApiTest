import time

import requests

from E1_API_Automation.Business.BaseService import BaseService


class Hf35MediaService(BaseService):
    def __init__(self, access_token):
        super().__init__("", {'EF-Access-Token': access_token})

    def get_media(self, media_url):
        api_url = '/{0}'.format(media_url)
        i = 0
        # retry three times if exception happens
        while i < 3:
            try:
                get_media_response = self.mou_tai.get(api_url, timeout=5)
                return get_media_response
            except requests.exceptions.RequestException:
                i += 1
                time.sleep(1)
