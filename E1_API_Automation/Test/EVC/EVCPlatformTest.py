import json
import requests
from hamcrest import assert_that, equal_to
from ptest.decorator import TestClass, Test, BeforeClass

from E1_API_Automation.Business.EVC.EVCFrontendService import EVCFrontendService
from E1_API_Automation.Settings import EVC_CDN_ENVIRONMENT, EVC_DEMO_PAGE_ENVIRONMENT
from E1_API_Automation.Test_Data.EVCData import EVCLayoutCode


@TestClass()
class EVCPlatformTest:
    @BeforeClass()
    def before_method(self):
        self.evc_frontend_service = EVCFrontendService(EVC_CDN_ENVIRONMENT)

    @Test(tags="stg, live")
    def test_kids_fm_techcheck(self):
        # generate attendance token of FM PL
        request_url = self.evc_frontend_service.generate_join_classroom_url(
            layout_code=EVCLayoutCode.FM_Kids_PL, use_agora=False)
        attendance_token = self.evc_frontend_service.generate_user_access_token(request_url)

        url = EVC_DEMO_PAGE_ENVIRONMENT + "/evc15/media/api/loadtechcheckoptions"
        payload = {'attendanceToken': attendance_token}
        headers = {'Content-Type': 'application/json'}

        response = requests.post(url, headers=headers, data=json.dumps(payload))

        # get parameters from response
        check_techcheck_required = response.json()["requireTechCheck"]

        # check tech check isn't required in FM PL
        assert_that(check_techcheck_required, equal_to(False))

    @Test(tags="stg, live")
    def test_kids_agore_techcheck(self):
        # generate attendance token of Agora PL
        request_url = self.evc_frontend_service.generate_join_classroom_url(
            layout_code=EVCLayoutCode.Agora_Kids_PL, use_agora=True)
        attendance_token = self.evc_frontend_service.generate_user_access_token(request_url)

        url = EVC_DEMO_PAGE_ENVIRONMENT +"/evc15/media/api/loadtechcheckoptions"
        payload = {'attendanceToken': attendance_token}
        headers = {'Content-Type': 'application/json'}

        response = requests.post(url, headers=headers, data=json.dumps(payload))

        # get parameters from response
        check_techcheck_required = response.json()["requireTechCheck"]

        # check tech check is required in Agora_PL
        assert_that(check_techcheck_required, equal_to(True))
