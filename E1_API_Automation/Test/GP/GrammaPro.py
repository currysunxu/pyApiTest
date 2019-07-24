from hamcrest import assert_that
from ptest.decorator import TestClass, Test

from E1_API_Automation.Lib.HamcrestExister import exist
from ...Lib.HamcrestMatcher import match_to
from ...Lib.ResetGPGradeTool import EducationRegion
from ...Settings import env_key
from ...Test.GP.GrammerProBase import GrammarProBaseClass
from ...Test_Data.GPData import GP_user


@TestClass()
class GPAPITestCases(GrammarProBaseClass):

    @Test()
    def test_all_dt_pass(self):
        self.gptest.login(GP_user.GPDTUsers[env_key]['username'], GP_user.GPDTUsers[env_key]['password'])
        self.gptest.finish_first_dt(0)
        self.gptest.finish_not_first_dt(0, False, 7)

    @Test()
    def test_dt_save_result_all_pass(self):
        self.gptest.login(GP_user.GPDTUsers[env_key]['username'], GP_user.GPDTUsers[env_key]['password'])
        submit_json = self.gptest.get_dt_submit_answer(0, True)
        dt_save = self.gptest.put_dt_save(submit_json[0])
        assert_that(dt_save.status_code == 204)

    @Test()
    def test_lower_grade_remediation_save(self):
        self.gptest.login(GP_user.GPDTUsers[env_key]['username'], GP_user.GPDTUsers[env_key]['password'])
        self.gptest.finish_first_dt(0)
        self.gptest.save_lower_grade_quiz_answer()

    @Test()
    def test_dt_save_result_all_failed(self):
        self.gptest.login(GP_user.GPDTUsers[env_key]['username'], GP_user.GPDTUsers[env_key]['password'])
        submit_json = self.gptest.get_dt_submit_answer(5)
        dt_save = self.gptest.put_dt_save(submit_json[0])
        assert_that(dt_save.status_code == 204)

    @Test()
    def test_finish_all_the_quiz_and_ct(self):
        self.gptest.login(GP_user.GPDTUsers[env_key]['username'], GP_user.GPDTUsers[env_key]['password'])
        submit_json = self.gptest.get_dt_submit_answer(5)
        dt_save = self.gptest.put_dt_save(submit_json[0])
        ct_module = submit_json[1]
        assert_that(dt_save.status_code == 204)
        student_progress = self.gptest.get_student_progress()
        assert_that(student_progress.json(), match_to("DiagnosticTestProgress.NextDiagnosticTest.NeedToBeVerified"))
        self.gptest.save_all_module_quiz_answer()
        self.gptest.finish_not_first_dt(5)
        test_answer = self.gptest.get_custom_test_answer(ct_module)
        ct_save = self.gptest.put_custom_test_save(test_answer)
        assert_that(ct_save.status_code == 204)

    @Test()
    def test_student_profile(self):
        self.gptest.login(GP_user.GPUsers[env_key]['username'], GP_user.GPUsers[env_key]['password'])
        student_profile = self.gptest.get_student_profile()
        assert_that(student_profile.json(), exist("Birthday"))
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
    def test_local_privacy_policy(self):
        self.gptest.login(GP_user.GPUsers[env_key]['username'], GP_user.GPUsers[env_key]['password'])
        local_privacy_policy = self.gptest.get_local_privacy_policy(GP_user.GPUsers[env_key]['culture_code'])
        assert_that(local_privacy_policy.json(), match_to("StudentId"))
        assert_that(local_privacy_policy.json(), match_to("ProductId"))
        assert_that(local_privacy_policy.json(), match_to("LatestPrivacyPolicyDocumentResult.Id"))
        assert_that(local_privacy_policy.json(), match_to("LatestPrivacyPolicyDocumentResult.Url"))

    @Test()
    def test_module_latest(self):
        self.gptest.login(GP_user.GPUsers[env_key]['username'], GP_user.GPUsers[env_key]['password'])
        module_latest = self.gptest.get_module_latest()
        assert_that(module_latest.json(), match_to("[*].ActivityKey"))
        assert_that(module_latest.json(), match_to("[*].ModuleKey"))
        assert_that(module_latest.json(), match_to("[*].QuestionAnswer.QuestionKey"))
        assert_that(module_latest.json(), match_to("[*].QuestionAnswer.TotalScore"))

    @Test()
    def test_local_language_student_report(self):
        self.gptest.login(GP_user.GPUsers[env_key]['username'], GP_user.GPUsers[env_key]['password'])
        local_language_student_report = self.gptest.get_local_language_student_report(
            GP_user.GPUsers[env_key]['culture_code'])
        assert_that(local_language_student_report.json(), exist("IsRead"))
        assert_that(local_language_student_report.json(), exist("Key"))
        assert_that(local_language_student_report.json(), exist("Url"))

    @Test()
    def test_en_student_report(self):
        self.gptest.login(GP_user.GPUsers[env_key]['username'], GP_user.GPUsers[env_key]['password'])
        en_student_report = self.gptest.get_en_student_report()
        assert_that(en_student_report.json(), exist("IsRead"))
        assert_that(en_student_report.json(), exist("Key"))
        assert_that(en_student_report.json(), exist("Url"))

    @Test()
    def test_custom_test(self):
        self.gptest.login(GP_user.GPUsers[env_key]['username'], GP_user.GPUsers[env_key]['password'])
        custom_test = self.gptest.get_custom_test()
        assert_that(custom_test.status_code == 200)

    @Test()
    def test_available_grade(self):
        self.gptest.login(GP_user.GPUsers[env_key]['username'], GP_user.GPUsers[env_key]['password'])
        city_list = {}
        culture_code = GP_user.GPUsers[env_key]['culture_code']
        if culture_code == 'zh-CN':
            city_list = EducationRegion.cn_city_list
        elif culture_code == 'id-ID':
            city_list = EducationRegion.id_city_list

        for city_name in city_list:
            available_grade = self.gptest.get_available_grade(city_list[city_name], culture_code)
            assert_that(available_grade.json(), match_to("[*].Grade.Key"))

    @Test()
    def test_student_progress(self):
        self.gptest.login(GP_user.GPUsers[env_key]['username'], GP_user.GPUsers[env_key]['password'])
        students_progress = self.gptest.get_student_progress()
        assert_that(students_progress.json(), exist("DiagnosticTestProgress.DiagnosticTestNumber"))
        assert_that(students_progress.json(), exist("RemediationProgress.RemediationModulesResult"))

    @Test()
    def test_region_and_grade(self):
        self.gptest.login(GP_user.GPUsers[env_key]['username'], GP_user.GPUsers[env_key]['password'])
        region_and_grade = self.gptest.get_region_and_grade()
        assert_that(region_and_grade.json(), match_to("[*].Region.Name"))
        assert_that(region_and_grade.json(), match_to("[*].Grades[*].Grade.Key"))

    @Test()
    def test_no_new_dt_generate(self):
        self.gptest.login(GP_user.GPDTUsers[env_key]['username'], GP_user.GPDTUsers[env_key]['password'])
        submit_json = self.gptest.get_dt_submit_answer(3, True)
        dt_save = self.gptest.put_dt_save(submit_json[0])
        assert_that(dt_save.status_code == 204)
        submit_json = self.gptest.get_dt_submit_answer(0, False)
        assert_that(submit_json == 403)

    @Test()
    def test_dt_start_lowest_grade_and_average_score_above_40(self):
        self.gptest.login(GP_user.GPDTUsers[env_key]['username'], GP_user.GPDTUsers[env_key]['password'])
        self.gptest.setup_student_profile(GP_user.GradeList[env_key]['lowest_grade'],
                                          GP_user.GPDTUsers[env_key]['culture_code'])
        self.gptest.finish_not_first_dt(2)
        new_module_list = self.gptest.get_new_recommend_module()
        expected_new_module_list = self.gptest.get_new_recommended_module(2)
        assert new_module_list == expected_new_module_list

    @Test()
    def test_dt_start_lowest_grade_and_average_score_equal_40(self):
        self.gptest.login(GP_user.GPDTUsers[env_key]['username'], GP_user.GPDTUsers[env_key]['password'])
        self.gptest.setup_student_profile(GP_user.GradeList[env_key]['lowest_grade'],
                                          GP_user.GPDTUsers[env_key]['culture_code'])
        self.gptest.finish_not_first_dt(3)
        new_module_list = self.gptest.get_new_recommend_module()
        expected_new_module_list = self.gptest.get_new_recommended_module(3)
        assert new_module_list == expected_new_module_list

    @Test()
    def test_dt_start_lowest_grade_and_average_score_below_40(self):
        self.gptest.login(GP_user.GPDTUsers[env_key]['username'], GP_user.GPDTUsers[env_key]['password'])
        self.gptest.setup_student_profile(GP_user.GradeList[env_key]['lowest_grade'],
                                          GP_user.GPDTUsers[env_key]['culture_code'])
        self.gptest.finish_not_first_dt(4)
        new_module_list = self.gptest.get_new_recommend_module()
        expected_new_module_list = self.gptest.get_new_recommended_module(4)
        assert new_module_list == expected_new_module_list

    @Test()
    def test_dt_start_middle_grade_and_average_score_above_40(self):
        self.gptest.login(GP_user.GPDTUsers[env_key]['username'], GP_user.GPDTUsers[env_key]['password'])
        self.gptest.setup_student_profile('Gth6', GP_user.GPDTUsers[env_key]['culture_code'])
        self.gptest.finish_not_first_dt(2)
        new_module_list = self.gptest.get_new_recommend_module()
        expected_new_module_list = self.gptest.get_new_recommended_module(2)
        new_module_list.sort()
        expected_new_module_list.sort()
        assert new_module_list == expected_new_module_list

    @Test()
    def test_dt_start_middle_grade_and_average_score_equal_40(self):
        self.gptest.login(GP_user.GPDTUsers[env_key]['username'], GP_user.GPDTUsers[env_key]['password'])
        self.gptest.setup_student_profile('Gth6', GP_user.GPDTUsers[env_key]['culture_code'])
        self.gptest.finish_not_first_dt(3)
        new_module_list = self.gptest.get_new_recommend_module()
        expected_new_module_list = self.gptest.get_new_recommended_module(3)
        assert new_module_list == expected_new_module_list

    @Test()
    def test_dt_start_middle_grade_and_average_score_below_40(self):
        self.gptest.login(GP_user.GPDTUsers[env_key]['username'], GP_user.GPDTUsers[env_key]['password'])
        self.gptest.setup_student_profile('Gth6', GP_user.GPDTUsers[env_key]['culture_code'])
        self.gptest.finish_not_first_dt(4)
        new_module_list = self.gptest.get_new_recommend_module()
        expected_new_module_list = self.gptest.get_new_recommended_module(4)
        assert new_module_list == expected_new_module_list

    @Test()
    def test_dt_start_highest_grade_and_average_score_above_40(self):
        self.gptest.login(GP_user.GPDTUsers[env_key]['username'], GP_user.GPDTUsers[env_key]['password'])
        self.gptest.setup_student_profile(GP_user.GradeList[env_key]['highest_grade'],
                                          GP_user.GPDTUsers[env_key]['culture_code'])
        self.gptest.finish_not_first_dt(2)
        new_module_list = self.gptest.get_new_recommend_module()
        expected_new_module_list = self.gptest.get_new_recommended_module(2)
        assert new_module_list == expected_new_module_list

    @Test()
    def test_dt_start_highest_grade_and_average_score_equal_40(self):
        self.gptest.login(GP_user.GPDTUsers[env_key]['username'], GP_user.GPDTUsers[env_key]['password'])
        self.gptest.setup_student_profile(GP_user.GradeList[env_key]['highest_grade'],
                                          GP_user.GPDTUsers[env_key]['culture_code'])
        self.gptest.finish_not_first_dt(3)
        new_module_list = self.gptest.get_new_recommend_module()
        expected_new_module_list = self.gptest.get_new_recommended_module(3)
        assert new_module_list == expected_new_module_list

    @Test()
    def test_dt_start_highest_grade_and_average_score_below_40(self):
        self.gptest.login(GP_user.GPDTUsers[env_key]['username'], GP_user.GPDTUsers[env_key]['password'])
        self.gptest.setup_student_profile(GP_user.GradeList[env_key]['highest_grade'],
                                          GP_user.GPDTUsers[env_key]['culture_code'])
        self.gptest.finish_not_first_dt(4)
        new_module_list = self.gptest.get_new_recommend_module()
        expected_new_module_list = self.gptest.get_new_recommended_module(4)
        assert new_module_list == expected_new_module_list
