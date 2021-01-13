from ptest.decorator import TestClass, Test, BeforeClass

from E1_API_Automation.Business.EVC.EVCFrontendService import EVCFrontendService
from E1_API_Automation.Settings import EVC_CDN_ENVIRONMENT, EVC_PROXY_ENVIRONMENT
from E1_API_Automation.Test_Data.EVCData import EVC_AGORA_FRONTEND_VERSION, EVCPlatform, EVCLayoutCode, \
    EVC_FM_FRONTEND_VERSION


@TestClass()
class FrontEndVersionTest:
    @BeforeClass()
    def before_method(self):
        self.evc_frontend_service = EVCFrontendService(EVC_CDN_ENVIRONMENT)

    @Test(tags="stg, live", data_provider={"CN", "US", "UK", "SG"})
    def test_kids_web_frontend(self, location):
        url = "/_shared/evc15-fe_kids/{0}/main.js".format(EVC_AGORA_FRONTEND_VERSION)
        response = self.evc_frontend_service.request_frontend_js(url, EVC_PROXY_ENVIRONMENT[location])
        self.evc_frontend_service.check_header_info(response.headers)

    @Test(tags="stg, live", data_provider={"CN", "US", "UK", "SG"})
    def test_kids_ios_frontend(self, location):
        url = "/_shared/evc15-fe-ios-bundle_kids/{0}/ios.zip".format(EVC_AGORA_FRONTEND_VERSION)
        response = self.evc_frontend_service.request_frontend_js(url, EVC_PROXY_ENVIRONMENT[location])
        self.evc_frontend_service.check_header_info(response.headers)

    @Test(tags="stg, live", data_provider={"CN", "US", "UK", "SG"})
    def test_kids_android_frontend(self, location):
        url = "/_shared/evc15-fe-android-bundle_kids/{0}/android.zip".format(EVC_AGORA_FRONTEND_VERSION)
        response = self.evc_frontend_service.request_frontend_js(url, EVC_PROXY_ENVIRONMENT[location])
        self.evc_frontend_service.check_header_info(response.headers)

    @Test(tags="stg, live")
    def test_kids_agora_frontend_version(self):
        request_url = self.evc_frontend_service.generate_join_classroom_url()
        attendance_token = self.evc_frontend_service.generate_user_access_token(request_url)

        # get iOS version and do verification
        agora_ios_response = self.evc_frontend_service.get_client_version_by_attendance_token(attendance_token,
                                                                                              EVCPlatform.IOS)
        self.evc_frontend_service.check_frontend_version(agora_ios_response, EVCPlatform.IOS,
                                                         EVC_AGORA_FRONTEND_VERSION)

        # get android version and do verification
        agora_android_response = self.evc_frontend_service.get_client_version_by_attendance_token(attendance_token,
                                                                                                  EVCPlatform.ANDROID)
        self.evc_frontend_service.check_frontend_version(agora_android_response, EVCPlatform.ANDROID,
                                                         EVC_AGORA_FRONTEND_VERSION)

    @Test(tags="stg, live")
    def test_kids_fm_frontend_version(self):
        request_url = self.evc_frontend_service.generate_join_classroom_url(
            layout_code=EVCLayoutCode.FM_Kids_PL, use_agora=False)
        attendance_token = self.evc_frontend_service.generate_user_access_token(request_url)

        # get iOS version and do verification
        fm_ios_response = self.evc_frontend_service.get_client_version_by_attendance_token(attendance_token,
                                                                                           EVCPlatform.IOS)
        self.evc_frontend_service.check_frontend_version(fm_ios_response, EVCPlatform.IOS, EVC_FM_FRONTEND_VERSION)

        # get android version and do verification
        fm_android_response = self.evc_frontend_service.get_client_version_by_attendance_token(attendance_token,
                                                                                               EVCPlatform.ANDROID)
        self.evc_frontend_service.check_frontend_version(fm_android_response, EVCPlatform.ANDROID,
                                                         EVC_FM_FRONTEND_VERSION)
