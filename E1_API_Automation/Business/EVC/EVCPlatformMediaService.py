import json

import requests
from hamcrest import assert_that, equal_to
from ptest.plogger import preporter


class EVCPlatformMediaService:
    def __init__(self, host):
        self.host = host
        self.header = {
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
        preporter.info(response.json())
        return response.json()
