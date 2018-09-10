import jmespath
from enum import Enum
from time import sleep
from hamcrest import assert_that, equal_to

from ptest.decorator import TestClass, Test, AfterMethod, BeforeSuite, AfterSuite

from E1_API_Automation.Lib.HamcrestExister import exist
from E1_API_Automation.Test.SmallStar.SmallStarBase import SmallStarBase
from ...Lib.HamcrestMatcher import match_to
from ...Lib.ResetGPGradeTool import EducationRegion

from ...Settings import ENVIRONMENT, env_key


import json


from ptest.decorator import AfterMethod, BeforeSuite, AfterSuite,BeforeClass,AfterClass
from ...Business.SmallStarV3 import SmallStarService

@TestClass()
class SmallStarTestCases(SmallStarBase):

    @Test()
    def get_content(self):
        body = {
            "Activity":{
                "UpertsOnly":True,
            },
            "BinaryData":{
                "UpertsOnly":True,
            },
            "BookKey":self.current_book_key,
            "CourseNode":{
                "UpertsOnly":False,
            },
            "DigitalArticle":{
                "UpertsOnly":False,
            },
            "ProductCode": self.product_code
        }
        response = self.small_star_service.fetch_content_update_summary(body)
        assert_that(response.json(), exist('BinaryDataAmount'))
        assert_that(response.json(), exist('ActivityQuestionAmount'))
        assert_that(response.json(), exist('ActivityStimulusAmount'))
        assert_that(response.json(), exist('ActivityAmount'))
        assert_that(response.json(), exist('AcademicElementAmount'))
        assert_that(response.json(), exist('CourseNodeAmount'))
        assert_that(response.json(), exist('DigitalArticleAmount'))
        assert_that(response.json(), exist('BinaryDataSize'))


    @Test()
    def synchronize_binary_data(self):
        response = self.small_star_service.synchronize_binary_data(self.current_book_key, self.course_plan_key, self.product_code, amount=2147483617)
        assert_that(len(jmespath.search('Upserts', response.json())) != 0)
        assert_that(response.json(), exist('Upserts'))
        assert_that(len(jmespath.search('Upserts[*].ResourceId', response.json())) != 0)
        assert_that(len(jmespath.search('Upserts[*].Container', response.json())) != 0)
        assert_that(jmespath.search("Upserts[*].Container", response.json())[0] == 'e1-osp-staging' )

    @Test()
    def synchronize_course_node(self):
        response = self.small_star_service.synchronize_course_node(self.current_book_key, self.course_plan_key, self.product_code, amount=2147483647)


