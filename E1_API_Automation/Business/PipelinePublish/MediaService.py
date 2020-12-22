import time

import requests
from E1_API_Automation.Lib.Moutai import Moutai


class MediaService:
    def __init__(self, host, api_key):
        self.host = host
        headers = {"Content-Type": "application/json",
                   "x-api-key": api_key}
        self.mou_tai = Moutai(host=self.host, headers=headers)

    def get_media(self, media_url):
        # return self.mou_tai.get(media_url)
        i = 0
        # retry three times if exception happens
        while i < 3:
            try:
                get_media_response = self.mou_tai.get(media_url, timeout=5)
                return get_media_response
            except requests.exceptions.RequestException:
                i += 1
                time.sleep(1)
