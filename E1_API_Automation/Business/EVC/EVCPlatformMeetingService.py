import json
import string
import urllib
from random import Random

import requests
from hamcrest import assert_that, equal_to
from requests import request

from E1_API_Automation.Business.EVC.EVCContentService import EVCContentService
from E1_API_Automation.Settings import EVC_CONTENT_ENVIRONMENT
from E1_API_Automation.Test_Data.EVCData import EVCMeetingRole, EVCLayoutCode


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
            "program": "indo_fr_gl",
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

        response = requests.post(self.host + url, data=json.dumps(param), headers=self.header)
        assert_that(response.status_code, equal_to(200))
        return response.json()

    def meeting_register(self, location, component_token, role_code=EVCMeetingRole.TEACHER, display_name="test user"):
        url = "/evc15/meeting/api/register"

        if role_code == EVCMeetingRole.TEACHER:
            user_meta = {
                "initState": 2270,
                "turnFlag": location,
                "forceTurn": True,
                "useProxy": True
            }
        elif role_code == EVCMeetingRole.STUDENT:
            user_meta = {
                "initState": 1502
            }
        else:
            raise Exception("Do not support to register meeting with {0}:".format(role_code))

        param = {
            "componentToken": component_token,
            "displayName": display_name,
            "roleCode": role_code,
            "externalSysCode": "System",
            "userMeta": json.dumps(user_meta),
            "externalUserId": ""
        }

        response = requests.post(self.host + url, data=json.dumps(param), headers=self.header)
        assert_that(response.status_code, equal_to(200))
        return response.json()

    def meeting_bootstrap(self, attendance_token):
        url = "/evc15/meeting/api/bootstrap"

        param = {
            "attendanceToken": attendance_token
        }

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

        print(param)
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

        response = requests.post(self.host + url, data=json.dumps(param), headers=self.header)
        return response.json()

    def meeting_load(self, component_token):
        url = "/evc15/meeting/api/load"
        param = {
            "componentToken": component_token
        }

        response = requests.post(self.host + url, data=json.dumps(param), headers=self.header)
        return response.json()

    def create_or_join_classroom(self, user_name="test", room_name=None, content_id="10223", duration=5,
                                 role_code=EVCMeetingRole.STUDENT, layout_code=EVCLayoutCode.Kids_PL, use_agora="True"):
        if room_name is None:
            r = Random()
            room_name = "".join(r.sample(string.ascii_letters, 8))

        header = {'x-accesskey': self.access_key}
        url = '/evc15/meeting/tools/CreateOrJoinClassroom'
        param = {
            'userDisplayName': user_name,
            'roomName': room_name,
            'contentId': content_id,
            'duration': duration,
            'roleCode': role_code,
            'videoUnMute': True,
            'videoDisplay': True,
            'layoutCode': layout_code,
            'centerCode': 'S',
            'useAgora': use_agora
        }
        response = requests.post(self.host + url, params=param, headers=header)
        assert_that(response.status_code, equal_to(200))
        return response.json()

    def get_meeting_room_info(self, user_name="default user", room_name=None, content_id="10223", duration=30,
                              role_code=EVCMeetingRole.STUDENT, layout_code=EVCLayoutCode.Kids_PL,
                              use_agora=True):
        class_info = self.create_or_join_classroom(user_name, room_name, content_id, duration, role_code, layout_code,
                                                   use_agora)
        bootstrap_url = urllib.parse.unquote(class_info['bootstrapApi'], encoding='utf-8', errors='replace')
        bootstrap_response = self.meeting_bootstrap(class_info['attendanceToken'], bootstrap_url)
        components = bootstrap_response['components']
        room_info = {
            'user_name': user_name,
            'room_name': room_name,
            'role': role_code,
            'request_token': Random().randint(10000000, 99999999),
            'component_detail': components,
            'attendance_token': class_info['attendanceToken']
        }
        return room_info

    def trigger_record_class(self, meeting_token):
        url = self.host + "/evc15/meeting/api/recording?meetingToken={0}".format(meeting_token)
        response = request("POST", url, headers=self.header)
        print('status_code')
        print(response.status_code)
        print('body')
        print(response.text)
        import os
        for k in os.environ.keys():
            print('{k}:{v}'.format(k=k, v=os.environ[k]))

        if response.status_code != 204:
            response = request("POST", url, headers=self.header)
            assert_that(response.status_code, equal_to(204))

        return response

    def load_batch_attendance(self, meeting_token_list):
        url = '/evc15/meeting/tools/loadbatchattendance'
        param = {
            "componentTokens": meeting_token_list
        }
        response = requests.post(self.host + url, params=param, headers=self.header)
        assert_that(response.status_code, equal_to(200))
        return response.json()

    # init_flag = 0: when student entering the classroom;
    # class_end_flag = 1: when received the class end Kafka event;
    # merger_done_flag = 2: when video merger completed
    def update_record_flag(self, meeting_token, merger_done_flag='2'):
        url = self.host + "/evc15/meeting/api/updaterecordflag?flag={0}&meetingToken={1}&setFlag=true".format(merger_done_flag, meeting_token)

        response = request("POST", url, headers=self.header)
        assert_that(response.status_code, equal_to(200))
        return response


