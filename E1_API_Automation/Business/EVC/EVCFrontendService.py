import string
import os
from random import Random

import requests
from hamcrest import assert_that, equal_to, is_not
from requests import request

from E1_API_Automation.Business.Utils.EnvUtils import EnvUtils
from E1_API_Automation.Settings import EVC_DEMO_PAGE_ENVIRONMENT, EVC_PROXY_ENVIRONMENT, \
    ENVIRONMENT
from E1_API_Automation.Test_Data.EVCData import EVCLayoutCode, EVCMeetingRole


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

    def generate_join_classroom_url(self, user_display_name="test_user", room_name=None, content_id="10223",
                                    duration="30", role_code=EVCMeetingRole.STUDENT, center_code="S",
                                    layout_code=EVCLayoutCode.Agora_Kids_PL, video_unmute=True,
                                    video_display=True, use_agora=True):
        if room_name is None:
            r = Random()
            room_name = "".join(r.sample(string.ascii_letters, 8))

        request_url = EVC_DEMO_PAGE_ENVIRONMENT + "/evc15/meeting/tools/CreateOrJoinClassroom/?" + \
                      "userDisplayName={0}&roomName={1}&contentId={2}&duration={3}&roleCode={4}&centerCode={5}&layoutCode={6}&videoUnMute={7}&videoDisplay={8}&&useAgora={9}".format(
                          user_display_name, room_name, content_id, duration, role_code, center_code, layout_code,
                          video_unmute, video_display, use_agora)
        return request_url

    def generate_user_access_token(self, url):
        if EnvUtils.is_env_stg_cn():
            access_key = '414d95a5-b338-4356-adac-eacce520b114'
        elif EnvUtils.is_env_live_cn():
            access_key = "4f6d7f89-3779-42e0-a10d-8ad71aac4d80"
        else:
            raise Exception("Do not support to run this case on {0}".format(ENVIRONMENT))

        headers = {
            'Host': EVC_PROXY_ENVIRONMENT["CN"],
            'Connection': 'keep-alive',
            'Content-Length': '0',
            'Accept': '*/*',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
            'x-accesskey': access_key,
            'Origin': EVC_DEMO_PAGE_ENVIRONMENT,
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': EVC_DEMO_PAGE_ENVIRONMENT.join("/evc15/meeting/tools/demo"),
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9'
        }

        response = request("POST", url, headers=headers)
        assert_that(response.status_code, equal_to(200))
        assert_that(response.json()["attendanceToken"], is_not(None))
        return response.json()["attendanceToken"]

    def get_client_version_by_attendance_token(self, attendance_token, platform):
        url = EVC_DEMO_PAGE_ENVIRONMENT + "/evc15/meeting/api/clientversion?platform={0}&attendanceToken={1}".format(
            platform, attendance_token)
        response = requests.get(url)
        assert_that(response.status_code, equal_to(200))
        return response.json()
