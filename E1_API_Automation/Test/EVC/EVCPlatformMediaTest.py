from hamcrest import assert_that, equal_to, is_, is_not
from ptest.decorator import TestClass, Test
from ptest.plogger import preporter

from E1_API_Automation.Business.EVC.EVCPlatformMediaService import EVCPlatformMediaService
from E1_API_Automation.Business.EVC.EVCPlatformMeetingService import EVCPlatformMeetingService
from E1_API_Automation.Settings import EVC_ENVIRONMENT


@TestClass()
class EVCPlatformMediaTest:
    @Test(tags="stg, live", data_provider=["CN"])
    def test_kids_fm_techcheck(self, location):
        self.evc_meeting_service = EVCPlatformMeetingService(EVC_ENVIRONMENT[location])
        self.evc_media_service = EVCPlatformMediaService(EVC_ENVIRONMENT[location])

        # generate attendance token of FM PL
        attendance_token = self.evc_meeting_service.create_or_join_classroom(use_agora=False, media_type="IceLink")[
            "attendanceToken"]
        preporter.info(attendance_token)

        response = self.evc_media_service.load_tech_check_options(attendance_token)

        assert_that(response["agoraOptions"], is_(None))
        assert_that(response["trtcOptions"], is_(None))
        assert_that(response["audioThreshold"], equal_to(-20.0))
        assert_that(response["requireTechCheck"], equal_to(False))

    @Test(tags="stg, live", data_provider=["CN"])
    def test_kids_agore_techcheck(self, location):
        self.evc_meeting_service = EVCPlatformMeetingService(EVC_ENVIRONMENT[location])
        self.evc_media_service = EVCPlatformMediaService(EVC_ENVIRONMENT[location])

        # generate attendance token of Agora PL
        attendance_token = self.evc_meeting_service.create_or_join_classroom()["attendanceToken"]
        response = self.evc_media_service.load_tech_check_options(attendance_token)

        # get parameters from response
        assert_that(response["agoraOptions"], is_not(None))
        assert_that(response["trtcOptions"], is_(None))
        assert_that(response["audioThreshold"], equal_to(-20.0))
        assert_that(response["requireTechCheck"], equal_to(True))

    @Test(tags="stg, live", data_provider=["CN"])
    def test_kids_trtc_techcheck(self, location):
        self.evc_meeting_service = EVCPlatformMeetingService(EVC_ENVIRONMENT[location])
        self.evc_media_service = EVCPlatformMediaService(EVC_ENVIRONMENT[location])

        # generate attendance token of Agora PL
        attendance_token = self.evc_meeting_service.create_or_join_classroom(use_agora=False, media_type="Trtc")[
            "attendanceToken"]
        response = self.evc_media_service.load_tech_check_options(attendance_token)

        # check tech check is required in TRTC PL
        assert_that(response["agoraOptions"], is_(None))
        assert_that(response["trtcOptions"], is_not(None))
        assert_that(response["audioThreshold"], equal_to(-20.0))
        assert_that(response["requireTechCheck"], equal_to(True))
