import jmespath
from enum import Enum
from time import sleep
from hamcrest import assert_that, equal_to

from ptest.decorator import TestClass, Test, AfterMethod, BeforeSuite, AfterSuite
from ...Lib.HamcrestMatcher import match_to
from ...Lib.ResetGPGradeTool import EducationRegion

from ...Settings import ENVIRONMENT, env_key


import json


from ptest.decorator import AfterMethod, BeforeSuite, AfterSuite,BeforeClass,AfterClass
from ...Business.SmallStarV3 import SmallStarService

@TestClass()
class SmallStarTestCases():
    @BeforeClass()
    def create_ss(self):
        self.ss_test = SmallStarService(ENVIRONMENT)

    @AfterClass()
    def sign_out(self):
        self.ss_test.sign_out()
        print("Logout")

    @Test()
    def test_student_profile(self):
        self.ss_test.login('ssv302', '12345')
        student_profile = self.ss_test.get_student_profile()