from hamcrest import assert_that, equal_to, is_, isnot, is_not
from ptest.decorator import TestClass, Test, BeforeClass

from E1_API_Automation.Business.EVC.EVCPlatformMediaService import EVCPlatformMediaService
from E1_API_Automation.Business.EVC.EVCPlatformMeetingService import EVCPlatformMeetingService
from E1_API_Automation.Settings import EVC_PROXY_ENVIRONMENT


@TestClass()
class EVCPlatformMediaTest:
    @BeforeClass()
    def before_method(self):
        pass
        # self.evc_meeting_service = EVCPlatformMeetingService(EVC_PROXY_ENVIRONMENT["CN"])
        # self.evc_media_service = EVCPlatformMediaService(EVC_PROXY_ENVIRONMENT["CN"])

    # @Test(tags="stg, live", data_provider=["CN", "SG", "US", "SG", "CN_NEW", "SG_NEW", "US_NEW", "SG_NEW"])
    @Test(tags="qa, stg, live")
    def test_kids_fm_techcheck(self):
        # generate attendance token of FM PL
        # evc_meeting_service = EVCPlatformMeetingService(EVC_PROXY_ENVIRONMENT[location])
        # evc_media_service = EVCPlatformMediaService(EVC_PROXY_ENVIRONMENT[location])

        evc_meeting_service = EVCPlatformMeetingService(EVC_PROXY_ENVIRONMENT)
        evc_media_service = EVCPlatformMediaService(EVC_PROXY_ENVIRONMENT)
        attendance_token = evc_meeting_service.create_or_join_classroom(use_agora=False, media_type="IceLink")[
            "attendanceToken"]
        print(attendance_token)

        response = evc_media_service.load_tech_check_options(attendance_token)
        print(response.text)

        assert_that(response["agoraOptions"], is_(None))
        assert_that(response["trtcOptions"], is_(None))
        assert_that(response["audioThreshold"], equal_to(-20.0))
        assert_that(response["requireTechCheck"], equal_to(False))

    @Test(tags="stg, live", data_provider=["CN", "SG", "US", "SG", "CN_NEW", "SG_NEW", "US_NEW", "SG_NEW"])
    def test_kids_agore_techcheck(self, location):
        evc_meeting_service = EVCPlatformMeetingService(EVC_PROXY_ENVIRONMENT[location])
        evc_media_service = EVCPlatformMediaService(EVC_PROXY_ENVIRONMENT[location])

        # generate attendance token of Agora PL
        attendance_token = evc_meeting_service.create_or_join_classroom()["attendanceToken"]
        response = evc_media_service.load_tech_check_options(attendance_token)

        # get parameters from response
        assert_that(response["agoraOptions"], is_not(None))
        assert_that(response["trtcOptions"], is_(None))
        assert_that(response["audioThreshold"], equal_to(-20.0))
        assert_that(response["requireTechCheck"], equal_to(True))

    @Test(tags="qa, stg, live")
    def test_kids_trtc_techcheck(self):
        evc_meeting_service = EVCPlatformMeetingService(EVC_PROXY_ENVIRONMENT)
        evc_media_service = EVCPlatformMediaService(EVC_PROXY_ENVIRONMENT)

        # generate attendance token of Agora PL
        attendance_token = evc_meeting_service.create_or_join_classroom(use_agora=False, media_type="Trtc")[
            "attendanceToken"]
        response = evc_media_service.load_tech_check_options(attendance_token)

        # check tech check is required in TRTC PL
        assert_that(response["agoraOptions"], is_(None))
        assert_that(response["trtcOptions"], is_not(None))
        assert_that(response["audioThreshold"], equal_to(-20.0))
        assert_that(response["requireTechCheck"], equal_to(True))
