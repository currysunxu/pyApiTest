import json
import requests

from hamcrest import assert_that, equal_to


class EVCPlatformMediaService:
    def __init__(self, host):
        self.host = host
        # self.access_key = self.create_api_access_Key()
        self.header = {
            # "x-accesskey": self.access_key,
            "Accept": "application/json",
            "Content-Type": "application/json",
            'Origin': host,
            'Referer': host,
        }

    def load_tech_check_options(self, attendance_token):
        url = self.host + "/evc15/media/api/loadtechcheckoptions"
        payload = {'attendanceToken': attendance_token}

        response = requests.post(url, headers=self.header, data=json.dumps(payload))
        assert_that(response.status_code, equal_to(200))

        return response.json()