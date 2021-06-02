from functools import wraps
from random import Random

import base36
import jmespath
import requests
from ptest.plogger import preporter


class WebsyncCounter:
    count = 0


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
        component_token = \
            jmespath.search("[?componentTypeCode=='{0}'].componentToken".format(self.type), self.component_detail)[0]
        return component_token

    @property
    def websync_endpoint(self):
        websync_endpoint = \
            jmespath.search("[?componentTypeCode=='{0}'].endpoints.syncUrl".format(self.type), self.component_detail)[0]
        return websync_endpoint

    @property
    def websync_channel_name(self):
        channel_name = jmespath.search("[?componentTypeCode=='{0}'].endpoints.syncChannelName".format(self.type),
                                       self.component_detail)[0]
        return channel_name

    @need_count(True)
    def subscribe(self, client_id, session_id, data=None):
        if data:
            json = [
                {"clientId": client_id, "channel": "/meta/subscribe", "data": data,
                 "ext": {"fm.meta": {}, "fm.sessionId": session_id}, "id": str(WebsyncCounter.count),
                 "subscription": [self.websync_channel_name]}]

        else:
            json = [{"clientId": client_id, "channel": "/meta/subscribe", "ext": {"fm.sessionId": session_id},
                     "id": str(WebsyncCounter.count), "subscription": [self.websync_channel_name]}]

        preporter.info("subscribe for {0} with {1}".format(self.websync_endpoint, self.param))
        response = requests.post(self.websync_endpoint, params=self.param, json=json)

        preporter.info("subscribe response {0}".format(response))
        preporter.info(response.json())
        return response


class MeetingComponent(EVCComponent):
    @need_count(True)
    def handshake(self):
        hand_shake_data = [{"channel": "/meta/handshake", "id": str(WebsyncCounter.count), "minimumVersion": "1.0",
                            "supportedConnectionTypes": ["long-polling"], "version": "1.0"}]
        preporter.info("HandShake for {0} with {1}".format(self.websync_endpoint, hand_shake_data))
        shake_response = requests.post(self.websync_endpoint, params=self.param, json=hand_shake_data).json()
        return shake_response

    @need_count(True)
    def connect(self, client_id, session_id, ack=False):
        meta_json = [
            {"clientId": client_id, "channel": "/meta/connect", "connectionType": "long-polling",
             "ext": {"fm.ack": ack, "fm.sessionId": session_id}, "id": str(WebsyncCounter.count)}]
        preporter.info("connect for {0} with {1}".format(self.websync_endpoint, meta_json))
        connect_response = requests.post(self.websync_endpoint, params=self.param, json=meta_json).json()
        return connect_response

    @need_count(True)
    def binding(self, client_id, session_id, attendance_token, access_key):
        instance_id = str(base36.dumps(int(str(Random().random())[2:])))
        preporter.info("instance_id: {0}".format(instance_id))
        binding_data = [{"clientId": client_id, "binding": [
            {"key": "attendanceToken", "private": True, "value": attendance_token},
            {"key": "accessKey", "private": True, "value": access_key},
            {"key": "instanceId", "private": True, "value": instance_id}], "channel": "/meta/bind",
                         "ext": {"fm.sessionId": session_id}, "id": str(WebsyncCounter.count)}]
        binding_response = requests.post(self.websync_endpoint, params=self.param, json=binding_data).json()
        return binding_response
