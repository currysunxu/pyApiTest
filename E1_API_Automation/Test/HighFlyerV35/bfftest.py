import json
from hamcrest import assert_that, equal_to, contains_string
from ptest.decorator import TestClass, Test

from E1_API_Automation.Business.NGPlatform.ContentRepoService import ContentRepoService
from E1_API_Automation.Business.NGPlatform.HomeworkService import HomeworkService
from E1_API_Automation.Business.NGPlatform.LearningPlanEntity import LearningPlanEntity
from E1_API_Automation.Business.NGPlatform.LearningResultEntity import LearningResultEntity
from E1_API_Automation.Business.NGPlatform.LearningResultDetailEntity import LearningResultDetailEntity
from E1_API_Automation.Business.NGPlatform.NGPlatformUtils.ContentRepoCommonData import ContentRepoCommonData
from E1_API_Automation.Settings import env_key, HOMEWORK_ENVIRONMENT, CONTENT_REPO_ENVIRONMENT
from E1_API_Automation.Test.HighFlyerV35.HfBffTestBase import HfBffTestBase
from E1_API_Automation.Test_Data.BffData import BffUsers
from E1_API_Automation.Business.HighFlyer35.HighFlyerUtils.Hf35BffCommonData import Hf35BffCommonData
from E1_API_Automation.Lib.HamcrestMatcher import match_to

import jmespath


@TestClass()
class HighFlyer(HfBffTestBase):

    @Test(tags='qa')
    def test_bootstrap_controller_status(self):
        response = self.bff_service.get_bootstrap_controller(platform=2)
        assert_that(response.status_code == 200)
        assert_that(response.json(), match_to("provision"))
        assert_that(response.json(), match_to("userContext.availableBooks"))
        assert_that(response.json(), match_to("userContext.currentBook"))

    @Test(tags='qa')
    def test_bootstrap_controller_with_wrong_platform_number(self):
        response = self.bff_service.get_bootstrap_controller(platform=None)
        assert_that(response.status_code == 400)

    @Test(tags='qa')
    def test_bootstrap_controller_ios_platform(self):
        response = self.bff_service.get_bootstrap_controller(platform='ios')
        assert_that(jmespath.search('provision.name', response.json()), contains_string('iOS'))

    @Test(tags='qa')
    def test_bootstrap_controller_android_platform(self):
        response = self.bff_service.get_bootstrap_controller(platform='android')
        assert_that(jmespath.search('provision.name', response.json()), contains_string('andriod'))

    @Test(tags='qa')
    def test_get_unlock_progress(self):
        current_book = jmespath.search('userContext.currentBook',
                                       self.bff_service.get_bootstrap_controller('ios').json())
        print(current_book)
        response = self.bff_service.get_unlock_progress_controller(current_book)
        assert_that(response.status_code == 200)


