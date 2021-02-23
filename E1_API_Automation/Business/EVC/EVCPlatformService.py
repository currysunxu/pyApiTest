import string
import os
from random import Random
import urllib
import jmespath
import requests
import base36
import math
import re
from hamcrest import assert_that, equal_to, is_not

from functools import wraps


def need_count(if_need):
    def counter_id(func):
        @wraps(func)
        def count(*args, **kwargs):
            if if_need:
                WebsyncCounter.count += 1
            else:
                pass
            return func(*args, **kwargs)

        WebsyncCounter.count = 0
        return count

    return counter_id


class WebsyncCounter:
    count = 0


class ComponentType:
    meeting = 'meeting'
    media = 'media'
    whiteboard = 'whiteboard'
    chat = 'chat'
    note = 'note'


class EVCComponent:
    def __init__(self, type, components_json):

        self.type = type
        self.component_detail = components_json['component_detail']
        self.request_token = components_json['request_token']
        self.param = {'token': self.request_token,
                      'src': 'js',
                      'AspxAutoDetectCookieSupport': '1'}

    @property
    def component_token(self):
        return jmespath.search("[?componentTypeCode=='{0}'].componentToken".format(self.type), self.component_detail)[0]

    @property
    def websync_endpoint(self):
        return \
            jmespath.search("[?componentTypeCode=='{0}'].endpoints.syncUrl".format(self.type), self.component_detail)[0]

    @property
    def websync_channel_name(self):
        channel_name = jmespath.search("[?componentTypeCode=='{0}'].endpoints.syncChannelName".format(self.type),
                               self.component_detail)[0]
        return channel_name

    @need_count(True)
    def subscribe(self, client_Id, session_id, data=None):
        if data:
            json = [
                {"clientId": client_Id, "channel": "/meta/subscribe", "data": data,
                 "ext": {"fm.meta": {}, "fm.sessionId": session_id}, "id": str(WebsyncCounter.count),
                 "subscription": [self.websync_channel_name]}]

        else:
            json = [{"clientId": client_Id, "channel": "/meta/subscribe", "ext": {"fm.sessionId": session_id},
                     "id": str(WebsyncCounter.count), "subscription": [self.websync_channel_name]}]
        response = requests.post(self.websync_endpoint, params=self.param, json=json)
        return response


class MeetingComponent(EVCComponent):
    @need_count(True)
    def handshake(self):
        hand_shake_data = [{"channel": "/meta/handshake", "id": str(WebsyncCounter.count), "minimumVersion": "1.0",
                            "supportedConnectionTypes": ["long-polling"], "version": "1.0"}]
        shake_response = requests.post(self.websync_endpoint, params=self.param, json=hand_shake_data).json()
        return shake_response

    @need_count(True)
    def connect(self, client_id, session_id, ack=False):
        meta_json = [
            {"clientId": client_id, "channel": "/meta/connect", "connectionType": "long-polling",
             "ext": {"fm.ack": ack, "fm.sessionId": session_id}, "id": str(WebsyncCounter.count)}]

        connect_response = requests.post(self.websync_endpoint, params=self.param, json=meta_json).json()
        return connect_response

    @need_count(True)
    def binding(self, client_id, session_id, attendance_token, access_key):
        # meta_binding
        instance_id = str(base36.dumps(int(str(Random().random())[2:])))
        binding_data = [{"clientId": client_id, "binding": [
            {"key": "attendanceToken", "private": True, "value": attendance_token},
            {"key": "accessKey", "private": True, "value": access_key},
            {"key": "instanceId", "private": True, "value": instance_id}], "channel": "/meta/bind",
                         "ext": {"fm.sessionId": session_id}, "id": str(WebsyncCounter.count)}]

        requests.post(self.websync_endpoint, params=self.param, json=binding_data).json()


class EVCPlatformService:

    def __init__(self, host):
        self.host = host
        self.access_key = self.__create_api_access_Key()

    def __create_api_access_Key(self):
        param = {
            'username': 'abc',
            'password': '123'
        }
        response = requests.post(self.host + '/evc15/meeting/api/create_accesskey', json=param)
        if response.status_code == 200:
            return response.json()['accessKey']
        else:
            raise Exception;

    def join_classroom(self, user_name, room_name, content_id, duration, role_code, layout_code, use_agora):
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
        return response.json()

    def meeting_bootstrap(self, attendance_token, url):
        headers = {
            'x-accesskey': self.access_key,
            'X-AttendanceToken': attendance_token
        }
        payload = {
            "attendanceToken": attendance_token
        }
        response = requests.post(url, json=payload, headers=headers).json()
        return response

    def get_meeting_room_info(self, user_name, room_name, content_id, duration, role_code, layout_code,
                              use_agora):
        class_info = self.join_classroom(user_name, room_name, content_id, duration, role_code, layout_code, use_agora)
        bootstrap_url = urllib.parse.unquote(class_info['bootstrapApi'], encoding='utf-8', errors='replace')
        bootstrap_response = self.meeting_bootstrap(class_info['attendanceToken'], bootstrap_url)
        components = bootstrap_response['components']
        room_info = {
            'user_name':user_name,
            'room_name': room_name,
            'role': role_code,
            'request_token': Random().randint(10000000, 99999999),
            'component_detail': components,
            'attendance_token': class_info['attendanceToken']
        }
        return room_info

    def websync(self, room_info):
        meeting_component = MeetingComponent(ComponentType.meeting, room_info)
        url = self.host + '/evc15/meeting/home?room={0}&token={1}&accesskey={2}&fmdebug=true'.format(
            room_info['room_name'], room_info['attendance_token'], self.access_key)
        requests.get(url)
        shake = meeting_component.handshake()
        connect = meeting_component.connect(shake[0]['clientId'], shake[0]['ext']['fm.sessionId'], False)
        binding = meeting_component.binding(shake[0]['clientId'], shake[0]['ext']['fm.sessionId'],
                                            room_info['attendance_token'], self.access_key)
        meeting_component.subscribe(shake[0]['clientId'], shake[0]['ext']['fm.sessionId'])
        media_component = EVCComponent(ComponentType.media, room_info)
        media_component.subscribe(shake[0]['clientId'], shake[0]['ext']['fm.sessionId'])
        note_component = EVCComponent(ComponentType.note, room_info)
        note_component.subscribe(shake[0]['clientId'], shake[0]['ext']['fm.sessionId'])
        chat_component = EVCComponent(ComponentType.chat, room_info)
        chat_component.subscribe(shake[0]['clientId'], shake[0]['ext']['fm.sessionId'])
        whiteboard_component = EVCComponent(ComponentType.whiteboard, room_info)
        whiteboard_component.subscribe(shake[0]['clientId'], shake[0]['ext']['fm.sessionId'])
        connect = meeting_component.connect(shake[0]['clientId'], shake[0]['ext']['fm.sessionId'], True)
        chat_body = {
            "data": {"message": "abcddd-", "displayName": room_info['user_name'], "attendanceRefCode": room_info['attendance_token'],
                     "roleCode": room_info['role']}, "params": {"topic": "MESSAGE.NEW"}}
        return chat_component.subscribe(shake[0]['clientId'], shake[0]['ext']['fm.sessionId'], chat_body).json()

    def websync_2(self, room_info):
        meeting_component = MeetingComponent(ComponentType.meeting, room_info)
        url = self.host + '/evc15/meeting/home?room={0}&token={1}&accesskey={2}&fmdebug=true'.format(
            room_info['room_name'], room_info['attendance_token'], self.access_key)
        requests.get(url)
        shake = meeting_component.handshake()
        connect = meeting_component.connect(shake[0]['clientId'], shake[0]['ext']['fm.sessionId'], False)
        binding = meeting_component.binding(shake[0]['clientId'], shake[0]['ext']['fm.sessionId'],
                                            room_info['attendance_token'], self.access_key)
        meeting_component.subscribe(shake[0]['clientId'], shake[0]['ext']['fm.sessionId'])
        media_component = EVCComponent(ComponentType.media, room_info)
        media_component.subscribe(shake[0]['clientId'], shake[0]['ext']['fm.sessionId'])
        note_component = EVCComponent(ComponentType.note, room_info)
        note_component.subscribe(shake[0]['clientId'], shake[0]['ext']['fm.sessionId'])
        chat_component = EVCComponent(ComponentType.chat, room_info)
        chat_response = chat_component.subscribe(shake[0]['clientId'], shake[0]['ext']['fm.sessionId'])

        whiteboard_component = EVCComponent(ComponentType.whiteboard, room_info)
        whiteboard_component.subscribe(shake[0]['clientId'], shake[0]['ext']['fm.sessionId'])
        return chat_response.json()


if __name__ == '__main__':
    evc = EVCPlatformService('https://evc-ts-staging.ef.com.cn')
    evc_classroom = evc.get_meeting_room_info('t1', 'room080911111111111', '10223', '30', 'host', 'kids_pl_v2', True)
    print(evc.websync(evc_classroom))

    evc_2  = EVCPlatformService('https://evc-ts-staging.ef.com.cn')
    room2  = evc_2.get_meeting_room_info('s1', 'room080911111', '10223', '30', 'participant', 'kids_pl_v2', True)
    chat = evc_2.websync_2(room2)
    print(chat)

