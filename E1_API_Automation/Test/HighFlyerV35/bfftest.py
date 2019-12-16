import json
from hamcrest import assert_that, equal_to, contains_string
from ptest.decorator import TestClass, Test,BeforeMethod

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
from E1_API_Automation.Business.HighFlyer35.Hf35BffService import Hf35BffService
from E1_API_Automation.Settings import *
import jmespath


@TestClass()
class HighFlyer(HfBffTestBase):


    @Test(tags='qa')
    def test_bootstrap_controller_status(self):
        pass

    @Test(tags='qa')
    def test_bff_auth_login_valid_username(self):
        product_keys = BffUsers.BffUserPw[env_key].keys()
        for key in product_keys:
            user_name = BffUsers.BffUserPw[env_key][key][0]['username']
            password = BffUsers.BffUserPw[env_key][key][0]['password']
            if key.__contains__('HF'):
                print("HF user is : %s" % (user_name))
                response = self.bff_service.login(user_name, password)
                print("Bff login response is : %s" % (response.__str__()))
                id_token = self.bff_service.get_auth_token()
                print("Bff login Token is : %s" % (id_token))
                assert_that((not id_token == "" and id_token.__str__() is not None))


