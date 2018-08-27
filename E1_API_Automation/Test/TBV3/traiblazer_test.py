import jmespath
from enum import Enum
from time import sleep
from hamcrest import assert_that, equal_to

from ptest.decorator import TestClass, Test, AfterMethod, BeforeSuite, AfterSuite
from ...Lib.HamcrestMatcher import match_to
from ...Lib.ResetGPGradeTool import EducationRegion

from ...Settings import ENVIRONMENT, env_key
from .traiblazer_base import TraiblazerBaseClass

import json



@TestClass()
class TBTestCases(TraiblazerBaseClass):
    @Test()
    def test_student_profile(self):
        self.tb_test.login('autounlock01', '12345')
        student_profile = self.tb_test.get_student_profile()

    @Test()
    def test_student_school_info(self):
        self.tb_test.query_school_info()

    @Test()
    def test_get_all_books(self):
        self.tb_test.get_all_books()

    @Test()
    def test_course_node_synchronize(self):
        self.course_node_synchronize()


