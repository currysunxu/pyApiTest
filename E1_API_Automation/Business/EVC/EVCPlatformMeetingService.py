import json
import string
from datetime import datetime, timedelta
from random import Random
from time import sleep

import requests
from hamcrest import assert_that, equal_to
from ptest.plogger import preporter
from requests import request

from E1_API_Automation.Business.EVC.EVCContentService import EVCContentService
from E1_API_Automation.Settings import EVC_CONTENT_ENVIRONMENT
from E1_API_Automation.Test_Data.EVCData import EVCMeetingRole, EVCLayoutCode, EVCProxyLocation, EVCMediaType


class EVCPlatformMeetingService:
    def __init__(self, host):
        self.host = host
        self.access_key = self.create_api_access_Key()
        self.header = {
            "x-accesskey": self.access_key,
            "Accept": "application/json",
            "Content-Type": "application/json",
            'Origin': host,
            'Referer': host,
        }

    def create_api_access_Key(self):
        param = {
            'username': 'default',
            'password': '123'
        }
        response = requests.post(self.host + '/evc15/meeting/api/create_accesskey', json=param)
        if response.status_code == 200:
            return response.json()['accessKey']
        else:
            raise Exception()

    def meeting_create(self, start_time, end_time, real_start_time, layout_code=EVCLayoutCode.Kids_PL):
        external_key = "".join(Random().sample(string.ascii_letters, 26))

        url = "/evc15/meeting/api/create"

        meeting_meta = {
            "realStartTime": real_start_time,
            "program": layout_code,
            "pdDesignation": "",
            "contentMap": "null",
            "useNewRecord": True
        }

        param = {
            "layoutCode": layout_code,
            "startTime": start_time,
            "endTime": end_time,
            "externalSysCode": "EVC-TEST",
            "externalSysKey": external_key,
            "meetingMeta": json.dumps(meeting_meta)
        }
        preporter.info(self.host + url)
        response = requests.post(self.host + url, data=json.dumps(param), headers=self.header)
        assert_that(response.status_code, equal_to(200))
        return response.json()

    def meeting_register(self, location, component_token, role_code=EVCMeetingRole.TEACHER, display_name="test user"):
        url = "/evc15/meeting/api/register"

        if role_code == EVCMeetingRole.TEACHER:
            if location != EVCProxyLocation.CN:
                user_meta = {
                    "turnFlag": location,
                    "forceTurn": False,
                    "useProxy": True,
                    "initState": 2270
                }
            else:
                user_meta = {
                    "initState": 2270
                }
        elif role_code == EVCMeetingRole.STUDENT:
            if location != EVCProxyLocation.CN:
                user_meta = {
                    "turnFlag": location,
                    "forceTurn": False,
                    "useProxy": True,
                    "initState": 1502
                }
            else:
                user_meta = {
                    "initState": 1502
                }
        else:
            raise Exception("Do not support to register meeting with {0}:".format(role_code))

        param = {
            "componentToken": component_token,
            "displayName": display_name,
            "roleCode": role_code,
            "externalSysCode": "EVC-TEST",
            "userMeta": json.dumps(user_meta),
            "externalUserId": ""
        }
        preporter.info(self.host + url)
        response = requests.post(self.host + url, data=json.dumps(param), headers=self.header)
        preporter.info(response.json())
        assert_that(response.status_code, equal_to(200))
        return response.json()

    def meeting_bootstrap(self, attendance_token):
        url = "/evc15/meeting/api/bootstrap"

        param = {
            "attendanceToken": attendance_token
        }
        preporter.info(self.host + url)
        response = requests.post(self.host + url, data=json.dumps(param), headers=self.header)
        assert_that(response.status_code, equal_to(200))
        return response.json()

    def meeting_update(self, component_token, topic_id):
        url = "/evc15/meeting/api/update"

        content_service = EVCContentService(EVC_CONTENT_ENVIRONMENT)

        material_payload = content_service.get_lesson_by_id(topic_id).json()[0]
        action_arguments = {"materialPayload": material_payload, "materialCode": topic_id}
        update_actions = [{"actionName": "materialset", "actionArguments": action_arguments}]

        component_update_info = [{"componentCode": "whiteboard", "updateActions": update_actions}]

        param = {
            "componentToken": component_token,
            "componentUpdateInfo": component_update_info
        }
        preporter.info(self.host + url)
        response = requests.post(self.host + url, data=json.dumps(param), headers=self.header)
        assert_that(response.status_code, equal_to(200))
        return response

    def meeting_update_by_material(self, component_token):
        url = "/evc15/meeting/api/update"
        material_payload = {
            "MaterialType": "athena",
            "TopicId": 0,
            "Title": "null",
            "Description": "",
            "HtmlMaterialFilePath": "",
            "Metatag": [],
            "AudioFile": []
        }

        action_arguments = {"materialPayload": material_payload, "materialCode": 0}
        update_actions = [{"actionName": "materialset", "actionArguments": action_arguments}]

        component_update_info = [{"componentCode": "whiteboard", "updateActions": update_actions}]

        param = {
            "componentToken": component_token,
            "componentUpdateInfo": component_update_info
        }

        preporter.info(self.host + url)
        response = requests.post(self.host + url, data=json.dumps(param), headers=self.header)
        assert_that(response.status_code, equal_to(200))
        return response

    def get_class_entry_url(self, attendance_token):
        url = self.host + "/evc15/meeting/home?token={0}&accesskey={1}".format(attendance_token, self.access_key)
        print(url)
        return url

    def meeting_loadstate(self, attendance_token):
        url = "/evc15/meeting/api/loadstate"
        param = {
            "attendanceToken": attendance_token
        }
        preporter.info(self.host + url)
        response = requests.post(self.host + url, data=json.dumps(param), headers=self.header)
        assert_that(response.status_code, equal_to(200))
        return response.json()

    def meeting_load(self, component_token):
        url = "/evc15/meeting/api/load"
        param = {
            "componentToken": component_token
        }
        preporter.info(self.host + url)
        response = requests.post(self.host + url, data=json.dumps(param), headers=self.header)
        assert_that(response.status_code, equal_to(200))
        return response.json()

    def create_or_join_classroom(self, user_name="test", room_name=None, content_id="10223", duration=5,
                                 role_code=EVCMeetingRole.STUDENT, layout_code=EVCLayoutCode.Kids_PL, use_agora=True,
                                 media_type=EVCMediaType.AGORA, center_code="S"):

        if room_name is None:
            r = Random()
            room_name = "".join(r.sample(string.ascii_letters, 8))

        url = "/evc15/meeting/tools/CreateOrJoinClassroom/?userDisplayName={0}&roomName={1}&contentId={2}&duration={3}&roleCode={4}&centerCode={5}&layoutCode={6}&videoUnMute=true&videoDisplay=true&externalUserId=&useAgora={7}&mediaType={8}".format(
            user_name, room_name, content_id, duration, role_code, center_code, layout_code, use_agora, media_type)

        payload = ""
        print(url)
        response = requests.request("POST", self.host + url, headers=self.header, data=payload)

        assert_that(response.status_code, equal_to(200))
        return response.json()

    def create_end_to_end_class(self, start_time=None, end_time=None, real_start_time=None, class_duration=5,
                                layout_code=EVCLayoutCode.Kids_PL):
        if start_time is None:
            start_time = datetime.now()
        if real_start_time is None:
            real_start_time = start_time
        if end_time is None:
            end_time = real_start_time + timedelta(minutes=class_duration)

        meeting_response = self.meeting_create(int(start_time.timestamp() * 1000),
                                               int(end_time.timestamp() * 1000),
                                               int(real_start_time.timestamp() * 1000),
                                               layout_code)
        return meeting_response

    def get_meeting_room_info(self, start_time=None, end_time=None, real_start_time=None, class_duration=5,
                              layout_code=EVCLayoutCode.Kids_PL, role_code=EVCMeetingRole.STUDENT,
                              user_name="default user", location=EVCProxyLocation.CN):

        meeting_response = self.create_end_to_end_class(start_time=start_time, end_time=end_time,
                                                        real_start_time=real_start_time, class_duration=class_duration,
                                                        layout_code=layout_code)
        meeting_token = (meeting_response["componentToken"])
        preporter.info("----Meeting token----: {0}".format(meeting_token))

        # register meeting & bootstrap
        user_info = self.meeting_register(location, meeting_token, role_code, user_name)
        sleep(5)
        bootstrap_response = self.meeting_bootstrap(user_info["attendanceToken"])
        components = bootstrap_response['components']
        room_info = {
            'user_name': user_name,
            'role': role_code,
            'request_token': Random().randint(10000000, 99999999),
            'component_detail': components,
            'attendance_token': user_info['attendanceToken']
        }
        return room_info

    def trigger_record_class(self, meeting_token):
        sleep(5)  # not sure the reason, but it would fail without sleep
        url = self.host + '/evc15/meeting/api/recording'
        params = {
            'meetingToken': meeting_token
        }

        response = requests.post(url, data='{}', params=params, headers=self.header)
        print(url)

        if response.status_code != 204:
            response = requests.post(url, data='{}', params=params, headers=self.header)
            assert_that(response.status_code, equal_to(204))

        return response

    def load_batch_attendance(self, meeting_token_list):
        url = '/evc15/meeting/tools/loadbatchattendance'
        param = {
            "componentTokens": meeting_token_list
        }
        preporter.info(self.host + url)
        response = requests.post(self.host + url, params=param, headers=self.header)
        assert_that(response.status_code, equal_to(200))
        return response.json()

    # init_flag = 0: when student entering the classroom;
    # class_end_flag = 1: when received the class end Kafka event;
    # merger_done_flag = 2: when video merger completed
    def update_record_flag(self, meeting_token, merger_done_flag='2'):
        url = self.host + "/evc15/meeting/api/updaterecordflag?flag={0}&meetingToken={1}&setFlag=true".format(
            merger_done_flag, meeting_token)
        preporter.info(url)
        response = request("POST", url, headers=self.header)
        assert_that(response.status_code, equal_to(200))
        return response

    def load_meeting_home(self, room_info):
        url = self.host + '/evc15/meeting/home?room={0}&token={1}&accesskey={2}&fmdebug=true'.format(
            room_info['room_name'], room_info['attendance_token'], self.access_key)
        preporter.info("load {0}".format(url))
        response = requests.get(url)
        assert_that(response.status_code, equal_to(200))

    def meeting_agora_uid_data_fix(self, meeting_token):
        url = self.host + "/evc15/meeting/api/agorauiddatafix?meetingToken={0}".format(meeting_token)
        payload = {}
        headers = {
            'Accept': 'application/json',
            'x-accesskey': self.access_key
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        assert_that(response.status_code, equal_to(200))
