import requests
from hamcrest import assert_that, equal_to
from ptest.decorator import TestClass, Test, BeforeClass

from E1_API_Automation.Business.EVC.EVCPlatformService import EVCPlatformService
from E1_API_Automation.Settings import EVC_CDN_ENVIRONMENT, EVC_PROXY_ENVIRONMENT


@TestClass()
class EVCPlatformTest:
    @BeforeClass()
    def before_method(self):
        self.evc_meeting = EVCPlatformService(EVC_PROXY_ENVIRONMENT['CN'])

    @Test(tags="stg, live")
    def test_register(self):
        pass

