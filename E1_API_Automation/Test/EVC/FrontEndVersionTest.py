import requests,json
from hamcrest import assert_that, equal_to
from ptest.decorator import TestClass, Test, BeforeClass

from E1_API_Automation.Business.EVC.EVCFrontendService import EVCFrontendService
from E1_API_Automation.Settings import EVC_CDN_ENVIRONMENT, EVC_PROXY_ENVIRONMENT, EVC_DEMO_PAGE_ENVIRONMENT
from E1_API_Automation.Test_Data.EVCData import EVC_AGORA_FRONTEND_VERSION, EVCPlatform, EVCLayoutCode, \
    EVC_FM_FRONTEND_VERSION


@TestClass()
class FrontEndVersionTest:
    @BeforeClass()
    def before_method(self):
        self.evc_frontend_service = EVCFrontendService(EVC_CDN_ENVIRONMENT)

    @Test(tags="stg, live", data_provider={"CN", "US", "UK", "SG"})
    def test_kids_frontend_deployed(self, location):
        # get url list from test data
        frontend_file_list = self.evc_frontend_service.get_frontend_file_url()

        # check each file is deployed with correct version
        if len(frontend_file_list) > 0:
            for url in frontend_file_list:
                url = url.format(EVC_AGORA_FRONTEND_VERSION)
                response = self.evc_frontend_service.request_frontend_js(url, EVC_PROXY_ENVIRONMENT[location])

                assert_that(response.headers["vary"], equal_to("Origin"))
                assert_that(response.headers["Access-Control-Allow-Origin"], equal_to("*"))

    @Test(tags="stg, live", data_provider={EVCPlatform.IOS, EVCPlatform.ANDROID})
    def test_kids_agora_frontend_version(self, platform):
        # generate attendance token
        request_url = self.evc_frontend_service.generate_join_classroom_url()
        attendance_token = self.evc_frontend_service.generate_user_access_token(request_url)

        # get version from api
        agora_response = self.evc_frontend_service.get_client_version_by_attendance_token(attendance_token,
                                                                                          platform)
        expect_file_name = EVC_CDN_ENVIRONMENT + "/_shared/evc15-fe-{0}-bundle_kids/{1}/{0}.zip".format(platform,
                                                                                                        EVC_AGORA_FRONTEND_VERSION)

        # check version and url
        assert_that(agora_response["Version"], equal_to(EVC_AGORA_FRONTEND_VERSION))
        assert_that(agora_response["FileName"], equal_to(expect_file_name))

    @Test(tags="stg, live", data_provider={EVCPlatform.IOS, EVCPlatform.ANDROID})
    def test_kids_fm_frontend_version(self, platform):
        # generate attendance token
        request_url = self.evc_frontend_service.generate_join_classroom_url(
            layout_code=EVCLayoutCode.FM_Kids_PL, use_agora=False)
        attendance_token = self.evc_frontend_service.generate_user_access_token(request_url)

        # get version from api
        fm_response = self.evc_frontend_service.get_client_version_by_attendance_token(attendance_token,
                                                                                       platform)
        expect_file_name = EVC_CDN_ENVIRONMENT + "/_shared/evc15-fe-{0}-bundle_kids/{1}/{0}.zip".format(platform,
                                                                                                        EVC_FM_FRONTEND_VERSION)
        # check version and url
        assert_that(fm_response["Version"], equal_to(EVC_FM_FRONTEND_VERSION))
        assert_that(fm_response["FileName"], equal_to(expect_file_name))

    @Test(tags="stg, live", data_provider={EVCPlatform.IOS, EVCPlatform.ANDROID})
    def test_kids_efstudy_frontend_version(self, platform):
        url = "{0}/_shared/evc15-fe-{1}-bundle_kids/version.json".format(EVC_CDN_ENVIRONMENT, platform)
        response = requests.get(url)

        # get parameters from response
        version = response.json()["Version"]
        file_name = response.json()["FileName"]

        # check version and file_name
        assert_that(version, equal_to(EVC_FM_FRONTEND_VERSION))
        assert_that(file_name, equal_to(EVC_FM_FRONTEND_VERSION + "/" + platform + ".zip"))
