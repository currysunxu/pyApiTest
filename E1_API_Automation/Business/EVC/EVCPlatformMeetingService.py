import json
import string
import urllib
from random import Random
from time import sleep

import requests
from hamcrest import assert_that, equal_to
from ptest.plogger import preporter
from requests import request

from E1_API_Automation.Business.EVC.EVCComponentEntity import EVCComponent, MeetingComponent
from E1_API_Automation.Business.EVC.EVCContentService import EVCContentService
from E1_API_Automation.Settings import EVC_CONTENT_ENVIRONMENT
from E1_API_Automation.Test_Data.EVCData import EVCMeetingRole, EVCLayoutCode, EVCComponentType


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
        preporter.info(self.host + url)
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
        preporter.info(self.host + url)
        response = requests.post(self.host + url, data=json.dumps(param), headers=self.header)
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
        return response.json()

    def meeting_load(self, component_token):
        url = "/evc15/meeting/api/load"
        param = {
            "componentToken": component_token
        }
        preporter.info(self.host + url)
        response = requests.post(self.host + url, data=json.dumps(param), headers=self.header)
        return response.json()

    def create_or_join_classroom(self, user_name="test", room_name=None, content_id="10223", duration=5,
                                 role_code=EVCMeetingRole.STUDENT, layout_code=EVCLayoutCode.Kids_PL, use_agora=True,
                                 media_type="agora"):

        if room_name is None:
            r = Random()
            room_name = "".join(r.sample(string.ascii_letters, 8))

        url = "/evc15/meeting/tools/CreateOrJoinClassroom/?userDisplayName={0}&roomName={1}&contentId={2}&duration={3}&roleCode={4}&centerCode=S&layoutCode={5}&videoUnMute=true&videoDisplay=true&externalUserId=&useAgora={6}&mediaType={7}".format(
            user_name, room_name, content_id, duration, role_code, layout_code, use_agora, media_type)

        payload = ""

        response = requests.request("POST", self.host + url, headers=self.header, data=payload)

        assert_that(response.status_code, equal_to(200))
        return response.json()

    def get_meeting_room_info(self, user_name="default user", room_name=None, content_id="10223", duration=30,
                              role_code=EVCMeetingRole.STUDENT, layout_code=EVCLayoutCode.Kids_PL,
                              use_agora=True):
        class_info = self.create_or_join_classroom(user_name, room_name, content_id, duration, role_code, layout_code,
                                                   use_agora)
        bootstrap_url = urllib.parse.unquote(class_info['bootstrapApi'], encoding='utf-8', errors='replace')
        bootstrap_response = self.meeting_bootstrap(class_info['attendanceToken'])
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
        sleep(5)  # not sure the reason, but it would fail without sleep
        url = self.host + '/evc15/meeting/api/recording'
        params = {
            'meetingToken': meeting_token
        }

        response = requests.post(url, data='{}', params=params, headers=self.header)

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

    def websync_teacher(self, room_info):
        meeting_component = MeetingComponent(EVCComponentType.MEETING, room_info)

        print("call home?room url")
        url = self.host + '/evc15/meeting/home?room={0}&token={1}&accesskey={2}&fmdebug=true'.format(
            room_info['room_name'], room_info['attendance_token'], self.access_key)
        requests.get(url)

        print("handshake meeting component")
        shake = meeting_component.handshake()
        print(shake)

        connect = meeting_component.connect(shake[0]['clientId'], shake[0]['ext']['fm.sessionId'], False)
        print(connect)
        binding = meeting_component.binding(shake[0]['clientId'], shake[0]['ext']['fm.sessionId'],
                                            room_info['attendance_token'], self.access_key)

        print(binding)
        meeting_component.subscribe(shake[0]['clientId'], shake[0]['ext']['fm.sessionId'])
        media_component = EVCComponent(EVCComponentType.MEDIA, room_info)
        media_component.subscribe(shake[0]['clientId'], shake[0]['ext']['fm.sessionId'])
        note_component = EVCComponent(EVCComponentType.NOTE, room_info)
        note_component.subscribe(shake[0]['clientId'], shake[0]['ext']['fm.sessionId'])
        chat_component = EVCComponent(EVCComponentType.CHAT, room_info)
        chat_component.subscribe(shake[0]['clientId'], shake[0]['ext']['fm.sessionId'])
        whiteboard_component = EVCComponent(EVCComponentType.WHITEBOARD, room_info)
        whiteboard_component.subscribe(shake[0]['clientId'], shake[0]['ext']['fm.sessionId'])
        connect = meeting_component.connect(shake[0]['clientId'], shake[0]['ext']['fm.sessionId'], True)

        chat_body = {
            "data": {"message": "abcddd-", "displayName": room_info['user_name'],
                     "attendanceRefCode": room_info['attendance_token'],
                     "roleCode": room_info['role']}, "params": {"topic": "MESSAGE.NEW"}}
        return chat_component.subscribe(shake[0]['clientId'], shake[0]['ext']['fm.sessionId'], chat_body).json()
