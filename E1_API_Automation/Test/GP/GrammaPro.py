import jmespath
from enum import Enum
from time import sleep
from hamcrest import assert_that, equal_to

from ptest.decorator import TestClass, Test, AfterMethod, BeforeSuite, AfterSuite
from ...Lib.HamcrestMatcher import match_to
from ...Lib.ResetGPGradeTool import EducationRegion

from ...Settings import ENVIRONMENT, env_key
from ...Test.GP.GrammerProBase import GrammarProBaseClass
from ...Test_Data.GPData import GP_user
from .jsondata import JsonData
import json




@TestClass()
class GPAPITestCases(GrammarProBaseClass):
    @Test()
    def test_student_profile(self):
        self.gptest.login(GP_user.GPUsers[env_key]['username'], GP_user.GPUsers[env_key]['password'])
        student_profile = self.gptest.get_student_profile()
        assert_that(student_profile.json(), match_to("Birthday"))
        assert_that(student_profile.json(), match_to("CultureCode"))
        assert_that(student_profile.json(), match_to("EducationGradeKey"))
        assert_that(student_profile.json(), match_to("EducationRegionKey"))
        assert_that(student_profile.json(), match_to("StartPointGradeKey"))

    @Test()
    def test_access_token(self):
        self.gptest.login(GP_user.GPUsers[env_key]['username'], GP_user.GPUsers[env_key]['password'])
        access_token = self.gptest.post_access_token()
        assert_that(access_token.json(), match_to("Token"))


    @Test()
    def test_student_profile_gp(self):

        self.gptest.login(GP_user.GPUsers[env_key]['username'], GP_user.GPUsers[env_key]['password'])
        student_profile = self.gptest.get_student_profile_gp()
        assert_that(student_profile.json(), match_to("UserId"))
        assert_that(student_profile.json(), match_to("UserStatus"))

    @Test()
    def test_cn_privacy_policy(self):
        self.gptest.login(GP_user.GPUsers[env_key]['username'], GP_user.GPUsers[env_key]['password'])
        cn_privacy_policy = self.gptest.get_cn_privacy_policy()
        assert_that(cn_privacy_policy.json(), match_to("StudentId"))
        assert_that(cn_privacy_policy.json(), match_to("ProductId"))
        assert_that(cn_privacy_policy.json(), match_to("LatestPrivacyPolicyDocumentResult.Id"))
        assert_that(cn_privacy_policy.json(), match_to("LatestPrivacyPolicyDocumentResult.Url"))

    @Test()
    def test_module_latest(self):
        self.gptest.login(GP_user.GPUsers[env_key]['username'], GP_user.GPUsers[env_key]['password'])
        module_latest = self.gptest.get_module_latest()
        assert_that(module_latest.json(), match_to("[*].ActivityKey"))
        assert_that(module_latest.json(), match_to("[*].ModuleKey"))
        assert_that(module_latest.json(), match_to("[*].QuestionAnswer.QuestionKey"))
        assert_that(module_latest.json(), match_to("[*].QuestionAnswer.TotalScore"))

    @Test()
    def test_cn_student_report(self):
        self.gptest.login(GP_user.GPUsers[env_key]['username'], GP_user.GPUsers[env_key]['password'])
        cn_student_report = self.gptest.get_cn_student_report()
        assert_that(cn_student_report.json(), match_to("IsRead"))
        assert_that(cn_student_report.json(), match_to("Key"))
        assert_that(cn_student_report.json(), match_to("Url"))


    @Test()
    def test_en_student_report(self):
        self.gptest.login(GP_user.GPUsers[env_key]['username'], GP_user.GPUsers[env_key]['password'])
        en_student_report = self.gptest.get_en_student_report()
        assert_that(en_student_report.json(), match_to("IsRead"))
        assert_that(en_student_report.json(), match_to("Key"))
        assert_that(en_student_report.json(), match_to("Url"))


    @Test()
    def test_custom_test(self):
        self.gptest.login(GP_user.GPUsers[env_key]['username'], GP_user.GPUsers[env_key]['password'])
        custom_test = self.gptest.get_custom_test()
        assert_that(custom_test.status_code == 200)

    @Test()
    def test_available_grade(self):
        self.gptest.login(GP_user.GPUsers[env_key]['username'], GP_user.GPUsers[env_key]['password'])
        for city_list in EducationRegion.city_list:
             available_grade = self.gptest.get_available_grade(EducationRegion.city_list[city_list])
             print(available_grade.json())
             assert_that(available_grade.json(), match_to("[*].Grade.Key"))


    @Test()
    def test_student_progress(self):
        self.gptest.login(GP_user.GPUsers[env_key]['username'], GP_user.GPUsers[env_key]['password'])
        students_progress = self.gptest.get_student_progress()
        assert_that(students_progress.json(), match_to("DiagnosticTestProgress.DiagnosticTestNumber"))

    @Test()
    def test_region_and_grade(self):
        self.gptest.login(GP_user.GPUsers[env_key]['username'], GP_user.GPUsers[env_key]['password'])
        region_and_grade = self.gptest.get_region_and_grade()
        assert_that(region_and_grade.json(), match_to("[*].Region.Name"))
        assert_that(region_and_grade.json(), match_to("[*].Grades[*].Grade.Key"))



    @Test()
    def test_dt_save_result_all_pass(self):
        self.gptest.login(GP_user.GPDTUsers[env_key]['username'], GP_user.GPDTUsers[env_key]['password'])
        submit_json = self.gptest.get_dt_first_time_submit_answer(0)
        dt_save = self.gptest.put_dt_save(submit_json[0])
        assert_that(dt_save.status_code == 204)


    @Test()
    def test_finish_all_the_quiz_and_ct(self):
        self.gptest.login(GP_user.GPDTUsers[env_key]['username'], GP_user.GPDTUsers[env_key]['password'])
        submit_json = self.gptest.get_dt_first_time_submit_answer(5)
        dt_save = self.gptest.put_dt_save(submit_json[0])
        ct_module=submit_json[1]
        assert_that(dt_save.status_code == 204)
        student_progress=self.gptest.get_student_progress()
        assert_that(student_progress.json(), match_to("DiagnosticTestProgress.NextDiagnosticTest.NeedToBeVerified"))
        self.gptest.get_all_module_quiz_answer()
        self.gptest.finish_not_first_dt()
        test_answer = self.gptest.get_custom_test_answer(ct_module)
        ct_save=self.gptest.put_custom_test_save(test_answer)
        assert_that(ct_save.status_code == 204)

    @Test()
    def test_dt_save_result_all_failed(self):
        self.gptest.login(GP_user.GPDTUsers[env_key]['username'], GP_user.GPDTUsers[env_key]['password'])
        submit_json = self.gptest.get_dt_first_time_submit_answer(5)
        dt_save = self.gptest.put_dt_save(submit_json[0])
        assert_that(dt_save.status_code == 204)













