import requests
from ptest.decorator import TestClass, Test, BeforeClass
from E1_API_Automation.Business.EVC.EVCComponentEntity import MeetingComponent, EVCComponent
from E1_API_Automation.Business.EVC.EVCPlatformMediaService import EVCPlatformMediaService
from E1_API_Automation.Business.EVC.EVCPlatformMeetingService import EVCPlatformMeetingService
# from E1_API_Automation.Settings import EVC_BACKEND_ENVIRONMENT
from E1_API_Automation.Settings import EVC_PROXY_ENVIRONMENT, EVC_MEETING_WEBSYNC_ENVIRONMENT, \
    EVC_MEDIA_WEBSYNC_ENVIRONMENT
from E1_API_Automation.Test_Data.EVCData import EVCComponentType


@TestClass()
class EVCWebSyncTest:

    @Test(tags="stg, live", data_provider=["CN","SG", "US", "SG", "CN_NEW", "SG_NEW", "US_NEW", "SG_NEW"])
    def test_meeting_websync_new(self, location):
        host = EVC_MEETING_WEBSYNC_ENVIRONMENT[location][8:]
        print(host)

        evc_hots = EVC_PROXY_ENVIRONMENT[location]
        url = EVC_MEETING_WEBSYNC_ENVIRONMENT[location]+"/evc15/signal/websync?token=99059960&src=js&AspxAutoDetectCookieSupport=1"
        print(url)

        payload = {}
        headers = {
            'Host': host,
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Accept': '*/*',
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'content-type',
            'Origin': evc_hots,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Dest': 'empty',
            'Referer': evc_hots,
            'Accept-Language': 'en-US,en;q=0.9'
        }

        response = requests.request("OPTIONS", url, headers=headers, data=payload)

        print(response.text)

        payload_new = "[{\"clientId\":\"ca972df7-2eff-4136-bedf-ad250032a1fb\",\"channel\":\"/media/9d128c49-b0f6-4098-b25f-0d3226210d54\",\"data\":{\"data\":{\"id\":\"f02c0f8a-13bc-4c42-934f-4d2ab9926640\"},\"params\":{\"topic\":\"USER.SPEAKING\"}},\"ext\":{\"fm.meta\":{},\"fm.sessionId\":\"0711f5fc-3c10-4815-adbe-d71c9c17b0ca\"},\"id\":\"97\"}]"
        headers_new = {
            'Host': host,
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
            'Content-Type': 'application/json, application/json',
            'Accept': '*/*',
            'Origin': evc_hots,
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': evc_hots,
            'Accept-Language': 'en-US,en;q=0.9'
        }

        response_new = requests.request("POST", url, headers=headers_new, data=payload_new)

        print(response_new.text)

    @Test(tags="stg, live", data_provider=["CN", "SG", "US", "SG", "CN_NEW", "SG_NEW", "US_NEW", "SG_NEW"])
    def test_media_websync_new(self, location):
        host = EVC_MEDIA_WEBSYNC_ENVIRONMENT[location][8:]
        print(host)

        evc_hots = EVC_PROXY_ENVIRONMENT[location]

        url = EVC_MEDIA_WEBSYNC_ENVIRONMENT[location] + "/websync/websync.ashx?token=99061105&src=js&AspxAutoDetectCookieSupport=1"

        payload = {}
        headers = {
            'Host': host,
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Accept': '*/*',
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'content-type',
            'Origin': evc_hots,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Dest': 'empty',
            'Referer': evc_hots,
            'Accept-Language': 'en-US,en;q=0.9'
        }

        response = requests.request("OPTIONS", url, headers=headers, data=payload)

        print(response.text)

        payload_new = "[{\"clientId\":\"8e2ecf62-8ade-43ec-9929-ad250035f492\",\"channel\":\"/meta/connect\",\"connectionType\":\"long-polling\",\"ext\":{\"fm.ack\":true,\"fm.sessionId\":\"5efefb2e-4b23-4497-bd6e-7b8493a7809f\"},\"id\":\"83\"}]"
        headers_new = {
            'Host': host,
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
            'Content-Type': 'application/json, application/json',
            'Accept': '*/*',
            'Origin': evc_hots,
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': evc_hots,
            'Accept-Language': 'en-US,en;q=0.9'
        }

        response = requests.request("POST", url, headers=headers_new, data=payload_new)

        print(response.text)

    @Test()
    def test_teacher_meeting_websync(self):
        meeting_service = EVCPlatformMeetingService("https://evc-ts-staging.ef.com.cn")
        room_info = meeting_service.get_meeting_room_info()
        meeting_service.load_meeting_home(room_info)

        meeting_component = MeetingComponent(EVCComponentType.MEETING, room_info)

        shake = meeting_component.handshake()
        connect = meeting_component.connect(shake[0]['clientId'], shake[0]['ext']['fm.sessionId'], False)
        binding = meeting_component.binding(shake[0]['clientId'], shake[0]['ext']['fm.sessionId'],
                                            room_info['attendance_token'], meeting_service.access_key)

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