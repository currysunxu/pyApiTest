import os
import requests

from hamcrest import assert_that, equal_to, is_not
from ptest.plogger import preporter
from E1_API_Automation.Settings import EVC_DEMO_PAGE_ENVIRONMENT


class EVCFrontendService(object):
    def __init__(self, host):
        self.host = host

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

    def request_frontend_js(self, url, proxy_domain):
        headers = self.generate_header(proxy_domain)
        response = requests.get(self.host + url, headers=headers)
        preporter.info("check front end file: {0}".format(self.host + url))
        assert_that(response.status_code, equal_to(200))

        return response

    def get_frontend_file_url(self):
        file_location = os.getcwd() + "\E1_API_Automation\Test_Data\EVC_Frontend_File_List"
        file_list = []

        try:
            files = open(file_location, "r")
        except IOError:
            print("Cannot find the specific file: {0}".format(file_location))
        else:
            lines = files.read().splitlines()

            if lines is not None:
                for line in lines:
                    file_list.append(line)

        return file_list

    def get_client_version_by_attendance_token(self, attendance_token, platform):
        url = EVC_DEMO_PAGE_ENVIRONMENT + "/evc15/meeting/api/clientversion?platform={0}&attendanceToken={1}".format(
            platform, attendance_token)
        response = requests.get(url)
        assert_that(response.status_code, equal_to(200))
        return response.json()
