import string
import os
from random import Random
import urllib
import jmespath
import requests
import base36
import math
import re

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


class EVCPlatformWebsync:
    def __init__(self, host):
        self.host = host
        self.headers = {'x-accesskey': self.access_key}


    def websync(self, room_info):
        meeting_component = MeetingComponent(ComponentType.meeting, room_info)

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
            "data": {"message": "abcddd-", "displayName": room_info['user_name'],
                     "attendanceRefCode": room_info['attendance_token'],
                     "roleCode": room_info['role']}, "params": {"topic": "MESSAGE.NEW"}}
        return chat_component.subscribe(shake[0]['clientId'], shake[0]['ext']['fm.sessionId'], chat_body).json()
