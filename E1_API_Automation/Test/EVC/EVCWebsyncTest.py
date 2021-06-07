from ptest.decorator import TestClass, Test

from E1_API_Automation.Business.EVC.EVCComponentEntity import MeetingComponent, EVCComponent
from E1_API_Automation.Business.EVC.EVCPlatformMeetingService import EVCPlatformMeetingService
from E1_API_Automation.Settings import EVC_ENVIRONMENT
from E1_API_Automation.Test_Data.EVCData import EVCComponentType, EVCMeetingRole


@TestClass()
class EVCWebSyncTest:
    # @Test(tags="stg", data_provider=["CN"])
    def test_agora_teacher_meeting_websync(self, location):
        meeting_service = EVCPlatformMeetingService(EVC_ENVIRONMENT[location])
        room_info = meeting_service.get_meeting_room_info(role_code=EVCMeetingRole.TEACHER, location=location)

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

        # connect = meeting_component.connect(shake[0]['clientId'], shake[0]['ext']['fm.sessionId'], True)

        chat_body = {
            "data": {"message": "abcddd-", "displayName": room_info['user_name'],
                     "attendanceRefCode": room_info['attendance_token'],
                     "roleCode": room_info['role']}, "params": {"topic": "MESSAGE.NEW"}}
        return chat_component.subscribe(shake[0]['clientId'], shake[0]['ext']['fm.sessionId'], chat_body).json()

    # @Test(tags="stg, live", data_provider=["CN", "SG", "US", "SG"])
    def test_agora_student_meeting_websync(self, location):
        meeting_service = EVCPlatformMeetingService(EVC_ENVIRONMENT[location])
        room_info = meeting_service.get_meeting_room_info(role_code=EVCMeetingRole.STUDENT, location=location)

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

        chat_body = {
            "data": {"message": "abcddd-", "displayName": room_info['user_name'],
                     "attendanceRefCode": room_info['attendance_token'],
                     "roleCode": room_info['role']}, "params": {"topic": "MESSAGE.NEW"}}
        return chat_component.subscribe(shake[0]['clientId'], shake[0]['ext']['fm.sessionId'], chat_body).json()
