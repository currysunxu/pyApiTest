from ptest.decorator import TestClass, Test, BeforeClass

from E1_API_Automation.Business.EVC.EVCFrontendService import EVCFrontendService
from E1_API_Automation.Settings import EVC_CDN_ENVIRONMENT
from E1_API_Automation.Test_Data.EVCData import EVCProxyDomain, EVC_FRONTEND_VERSION


@TestClass()
class FrontEndVersionTest:
    @BeforeClass()
    def before_method(self):
        self.evc_frontend_service = EVCFrontendService(EVC_CDN_ENVIRONMENT)

    @Test(tags="stg, live", data_provider={"US", "UK", "SG"})
    def test_kids_web_frontend(self, location):
        url = "/_shared/evc15-fe_kids/{0}/main.js".format(EVC_FRONTEND_VERSION)

        self.evc_frontend_service.mou_tai.set_header(
            self.evc_frontend_service.generate_header(EVCProxyDomain.STG_Proxy_Domain[location]))
        response = self.evc_frontend_service.request_frontend_js(url)
        self.evc_frontend_service.verify_header_info(response.headers)

    @Test(tags="stg, live", data_provider={"US", "UK", "SG"})
    def test_kids_ios_frontend(self, location):
        url = "/_shared/evc15-fe-ios-bundle_kids/{0}/ios.zip".format(EVC_FRONTEND_VERSION)

        self.evc_frontend_service.mou_tai.set_header(
            self.evc_frontend_service.generate_header(EVCProxyDomain.STG_Proxy_Domain[location]))
        response = self.evc_frontend_service.request_frontend_js(url)
        self.evc_frontend_service.verify_header_info(response.headers)

    @Test(tags="stg, live", data_provider={"US", "UK", "SG"})
    def test_kids_android_frontend(self, location):
        url = "/_shared/evc15-fe-android-bundle_kids/{0}/android.zip".format(EVC_FRONTEND_VERSION)

        self.evc_frontend_service.mou_tai.set_header(
            self.evc_frontend_service.generate_header(EVCProxyDomain.STG_Proxy_Domain[location]))
        response = self.evc_frontend_service.request_frontend_js(url)
        self.evc_frontend_service.verify_header_info(response.headers)
