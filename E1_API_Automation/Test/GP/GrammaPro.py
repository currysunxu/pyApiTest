import jmespath
from enum import Enum
from time import sleep
from hamcrest import assert_that, equal_to

from ptest.decorator import TestClass, Test, AfterMethod, BeforeSuite, AfterSuite
from ...Lib.HamcrestMatcher import match_to
from ...Lib.ResetGPGradeTool import EducationRegion

from ...Settings import ENVIRONMENT, env_key
from ...Test.GP.GrammerProBase import GrammarProBaseClass

from .jsondata import JsonData
import json

GPUsers = {'QA': {'username': 'gptest1', 'password': '12345'},
           'Staging': {'username': 'gp0606cn', 'password': '12345'},
           'Live': {'username': 'gptest3', 'password': '12345'}}
GPDTUsers = {'QA': {'username': 'gptest1', 'password': '12345'},
           'Staging': {'username': 'gp0606cn', 'password': '12345'},
           'Live': {'username': 'gptest3', 'password': '12345'}}


@TestClass()
class GPAPITestCases(GrammarProBaseClass):
    @Test()
    def test_student_profile(self):
        self.gptest.login(GPUsers[env_key]['username'], GPUsers[env_key]['password'])
        student_profile = self.gptest.get_student_profile()


        assert_that(student_profile.json(), match_to("Birthday"))
        assert_that(student_profile.json(), match_to("CultureCode"))
        assert_that(student_profile.json(), match_to("EducationGradeKey"))
        assert_that(student_profile.json(), match_to("EducationRegionKey"))
        assert_that(student_profile.json(), match_to("StartPointGradeKey"))

    @Test()
    def test_access_token(self):
        self.gptest.login(GPUsers[env_key]['username'], GPUsers[env_key]['password'])
        access_token = self.gptest.post_access_token()
        assert_that(access_token.json(), match_to("Token"))


    @Test()
    def test_student_profile_gp(self):

        self.gptest.login(GPUsers[env_key]['username'], GPUsers[env_key]['password'])
        student_profile = self.gptest.get_student_profile_gp()
        assert_that(student_profile.json(), match_to("UserId"))
        assert_that(student_profile.json(), match_to("UserStatus"))

    @Test()
    def test_cn_privacy_policy(self):
        self.gptest.login(GPUsers[env_key]['username'], GPUsers[env_key]['password'])
        cn_privacy_policy = self.gptest.get_cn_privacy_policy()
        assert_that(cn_privacy_policy.json(), match_to("StudentId"))
        assert_that(cn_privacy_policy.json(), match_to("ProductId"))
        assert_that(cn_privacy_policy.json(), match_to("LatestPrivacyPolicyDocumentResult.Id"))
        assert_that(cn_privacy_policy.json(), match_to("LatestPrivacyPolicyDocumentResult.Url"))

    @Test()
    def test_module_latest(self):
        self.gptest.login(GPUsers[env_key]['username'], GPUsers[env_key]['password'])
        module_latest = self.gptest.get_module_latest()
        assert_that(module_latest.json(), match_to("[*].ActivityKey"))
        assert_that(module_latest.json(), match_to("[*].ModuleKey"))
        assert_that(module_latest.json(), match_to("[*].QuestionAnswer.QuestionKey"))
        assert_that(module_latest.json(), match_to("[*].QuestionAnswer.TotalScore"))

    @Test()
    def test_students_lesson_activity(self):
        self.gptest.login(GPUsers[env_key]['username'], GPUsers[env_key]['password'])
        students_lesson_activity = self.gptest.post_students_lesson_activity(JsonData.module_info)
        assert_that(students_lesson_activity.json(), match_to("Activities[*].Key"))
        assert_that(students_lesson_activity.json(), match_to("Activities[*].Title"))
        assert_that(students_lesson_activity.json(), match_to("Resources[*].ResourceId"))
        assert_that(students_lesson_activity.json(), match_to("Resources[*].Name"))

    @Test()
    def test_student_lesson_progress(self):
        self.gptest.login(GPUsers[env_key]['username'], GPUsers[env_key]['password'])

        students_lesson_progress = self.gptest.post_students_lesson_progress(JsonData.module_key)
        assert_that(students_lesson_progress.status_code == 200)

    '''student report only for real student '''

    # @Test()
    # def test_cn_student_report(self):
    #     self.gptest.login(GPUsers[env_key]['username'], GPUsers[env_key]['password'])
    #     cn_student_report = self.gptest.get_cn_student_report()
    #     assert_that(cn_student_report.json(), match_to("IsRead"))
    #     assert_that(cn_student_report.json(), match_to("Key"))
    #     assert_that(cn_student_report.json(), match_to("Url"))
    #

    # @Test()
    # def test_en_student_report(self):
    #     self.gptest.login(GPUsers[env_key]['username'], GPUsers[env_key]['password'])
    #     en_student_report = self.gptest.get_en_student_report()
    #     assert_that(en_student_report.json(), match_to("IsRead"))
    #     assert_that(en_student_report.json(), match_to("Key"))
    #     assert_that(en_student_report.json(), match_to("Url"))


    @Test()
    def test_custom_test(self):
        self.gptest.login(GPUsers[env_key]['username'], GPUsers[env_key]['password'])
        custom_test = self.gptest.get_custom_test()
        assert_that(custom_test.status_code == 200)

    @Test()
    def test_available_grade(self):
        self.gptest.login(GPUsers[env_key]['username'], GPUsers[env_key]['password'])
        available_grade = self.gptest.get_available_grade(EducationRegion.Shanghai)
        assert_that(available_grade.json(), match_to("[*].Grade.Name"))
        assert_that(available_grade.json(), match_to("[*].Modules[*].Name"))

    @Test()
    def test_student_progress(self):
        self.gptest.login(GPUsers[env_key]['username'], GPUsers[env_key]['password'])
        students_progress = self.gptest.get_student_progress()
        assert_that(students_progress.json(), match_to("DiagnosticTestProgress.DiagnosticTestNumber"))

    @Test()
    def test_region_and_grade(self):
        self.gptest.login(GPUsers[env_key]['username'], GPUsers[env_key]['password'])
        region_and_grade = self.gptest.get_region_and_grade()
        assert_that(region_and_grade.json(), match_to("[*].Region.Name"))
        assert_that(region_and_grade.json(), match_to("[*].Grades[*].Grade.Key"))

    @Test()
    def test_quiz_start(self):
        self.gptest.login(GPUsers[env_key]['username'], GPUsers[env_key]['password'])
        quiz_start = self.gptest.post_quiz_start(JsonData.lesson_key)
        assert_that(quiz_start.status_code == 200)

    @Test()
    def test_quiz_save(self):
        self.gptest.login(GPUsers[env_key]['username'], GPUsers[env_key]['password'])
        quiz_save = self.gptest.post_quiz_save(json.loads(JsonData.submit_answer))
        assert_that(quiz_save.status_code == 204)


        # @Test()
        # def test_student_profile_save(self):
        #     self.gptest.login(GPUsers[env_key]['username'], GPUsers[env_key]['password'])
        #     students_profile = self.gptest.put_profile_save(JsonData.student_profile)
        #     assert_that(students_profile.status_code==204)
        #
    @Test()
    def test_dt_save(self):
        self.gptest.login(GPDTUsers[env_key]['username'], GPDTUsers[env_key]['password'])

        submit_json = self.gptest.get_sumbit_anwser()
        dt_save = self.gptest.put_dt_save(submit_json)
        assert_that(dt_save.status_code == 204)
