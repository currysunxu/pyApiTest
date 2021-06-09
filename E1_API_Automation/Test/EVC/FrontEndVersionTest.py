import requests
from hamcrest import assert_that, equal_to
from ptest.decorator import TestClass, Test, BeforeClass

from E1_API_Automation.Business.EVC.EVCFrontendService import EVCFrontendService
from E1_API_Automation.Business.EVC.EVCPlatformMeetingService import EVCPlatformMeetingService
from E1_API_Automation.Settings import EVC_ENVIRONMENT
from E1_API_Automation.Test_Data.EVCData import EVC_AGORA_FRONTEND_VERSION, EVCPlatform, EVC_FM_FRONTEND_VERSION, \
    EVC_TECH_CHECK_VERSION, EVC_INDO_DEMO_VERSION


@TestClass()
class FrontEndVersionTest:
    @BeforeClass()
    def before_method(self):
        self.evc_frontend_service = EVCFrontendService()

    @Test(tags="stg, live", data_provider={"CN"})
    def test_kids_frontend_deployed(self, location):
        # get url list from test data
        frontend_file_list = self.evc_frontend_service.get_frontend_file_url()

        # check each file is deployed with correct version
        if len(frontend_file_list) > 0:
            for url in frontend_file_list:
                if url.find("techcheck") != -1:
                    version = EVC_TECH_CHECK_VERSION
                elif url.find("indodemo") != -1:
                    version = EVC_INDO_DEMO_VERSION
                else:
                    version = EVC_AGORA_FRONTEND_VERSION

                url = url.format(version)
                response = self.evc_frontend_service.request_frontend_js(url, EVC_ENVIRONMENT[location])

                assert_that(response.headers["vary"], equal_to("Origin"))
                assert_that(response.headers["Access-Control-Allow-Origin"], equal_to("*"))

    @Test(tags="stg, live", data_provider={EVCPlatform.IOS, EVCPlatform.ANDROID})
    def test_kids_agora_frontend_version(self, platform):
        # generate attendance token
        meeting_service = EVCPlatformMeetingService(EVC_ENVIRONMENT["CN"])
        attendance_token = meeting_service.create_or_join_classroom()["attendanceToken"]

        # get version from api
        agora_response = self.evc_frontend_service.get_client_version_by_attendance_token(attendance_token, platform)
        expect_file_name = self.evc_frontend_service.host + "/_shared/evc15-fe-{0}-bundle_kids/{1}/{0}.zip".format(platform,
                                                                                                        EVC_AGORA_FRONTEND_VERSION)

        # check version and url
        assert_that(agora_response["Version"], equal_to(EVC_AGORA_FRONTEND_VERSION))
        assert_that(agora_response["FileName"], equal_to(expect_file_name))



