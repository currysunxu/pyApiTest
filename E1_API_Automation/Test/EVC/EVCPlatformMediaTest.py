from hamcrest import assert_that, equal_to
from ptest.decorator import TestClass, Test, BeforeClass

from E1_API_Automation.Business.EVC.EVCPlatformMediaService import EVCPlatformMediaService
from E1_API_Automation.Business.EVC.EVCPlatformMeetingService import EVCPlatformMeetingService
from E1_API_Automation.Settings import EVC_DEMO_PAGE_ENVIRONMENT


@TestClass()
class EVCPlatformMediaTest:
    @BeforeClass()
    def before_method(self):
        self.evc_meeting_service = EVCPlatformMeetingService(EVC_DEMO_PAGE_ENVIRONMENT)
        self.evc_media_service = EVCPlatformMediaService(EVC_DEMO_PAGE_ENVIRONMENT)

    @Test(tags="stg, live")
    def test_kids_fm_techcheck(self):
        # generate attendance token of FM PL
        attendance_token = self.evc_meeting_service.create_or_join_classroom(use_agora="False")["attendanceToken"]
        response = self.evc_media_service.load_tech_check_options(attendance_token)

        # get parameters from response
        check_techcheck_required = response.json()["requireTechCheck"]

        # check tech check isn't required in FM PL
        assert_that(check_techcheck_required, equal_to(False))

    @Test(tags="stg, live")
    def test_kids_agore_techcheck(self):
        # generate attendance token of Agora PL
        attendance_token = self.evc_meeting_service.create_or_join_classroom()["attendanceToken"]
        response = self.evc_media_service.load_tech_check_options(attendance_token)

        # get parameters from response
        check_techcheck_required = response.json()["requireTechCheck"]

        # check tech check is required in Agora_PL
        assert_that(check_techcheck_required, equal_to(True))
