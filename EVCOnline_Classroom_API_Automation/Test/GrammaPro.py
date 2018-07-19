import jmespath
from enum import Enum
from time import sleep
from hamcrest import assert_that, equal_to

from ptest.decorator import TestClass, Test, AfterMethod, BeforeSuite, AfterSuite
from Lib.HamcrestMatcher import match_to

import Settings

GPUsers = {'QA': {'username': 'gptest1', 'password': '12345'},
           'Staging': {'username': 'gptest1', 'password': '12345'},
           'Live': {'username': 'gptest1', 'password': '12345'}}

from Business.GP import GPService


@TestClass()
class GPAPITestCases():
    @BeforeSuite()
    def create_gp(self):
        self.gptest = GPService(Settings.ENVIRONMENT)

    @AfterSuite()
    def sign_out(self):
        self.gptest.sign_out()
        print("Logout")

    @Test()
    def test_student_profile(self):
        self.gptest.login(GPUsers[Settings.env_key]['username'], GPUsers[Settings.env_key]['password'])
        student_profile = self.gptest.get_student_profile()
        assert_that(student_profile.json(), match_to("Birthday"))
        assert_that(student_profile.json(), match_to("CultureCode"))
        assert_that(student_profile.json(), match_to("EducationGradeKey"))
        assert_that(student_profile.json(), match_to("EducationRegionKey"))
        assert_that(student_profile.json(), match_to("StartPointGradeKey"))
