from ptest.decorator import TestClass, Test
from E1_API_Automation.Business.MockTestBFFService import MockTestBFFService
from E1_API_Automation.Settings import MOCK_TEST_ENVIRONMENT, env_key
from E1_API_Automation.Test_Data.MockTestData import *

import random
from hamcrest import assert_that
import jmespath


@TestClass()
class MockTestCases():
    def __init__(self):
        self.mt_service = MockTestBFFService(MOCK_TEST_ENVIRONMENT)
        self.valid_test_id = self.mt_service.get_valid_test_id_by_test_id_from_db()["id"]
        self.finished_test_id = TestDataList.TestId[env_key]['finished_test_id']
        self.part = random.randint(0, 2)
        self.learner_vector_key = TestDataList.Remediation[env_key]['learner_vector_key']
        self.correct_answer_count = random.randint(0, 5)
        self.total_question_count = random.randint(5, 10)
        self.total_seconds_spent = random.randint(0,1200)
        self.has_mt_student = MockTestStudentType.HasMockTest.value
        self.no_mt_student = MockTestStudentType.HasNoMockTest.value
        self.mt_service.login(self.has_mt_student)

    @Test(tags="qa, stg")
    def verify_has_test_student(self):
        mt_response = self.mt_service.post_load_user_mt_list()
        self.mt_service.check_bff_get_current_user_structure(mt_response, self.has_mt_student)
        assert_that(len(jmespath.search("data.currentUser.tests", mt_response.json())) > 0)

    @Test(tags="qa, stg")
    def verify_no_test_student(self):
        self.mt_service.login(self.no_mt_student)
        mt_response = self.mt_service.post_load_user_mt_list()
        self.mt_service.check_bff_get_current_user_structure(mt_response, self.no_mt_student)
        assert_that(len(jmespath.search("data.currentUser.tests", mt_response.json())) == 0)

    @Test(tags="qa, stg", data_provider=["invalid", "noToken", "expired"])
    def verify_get_test_list_with_invalid_auth_token(self, negative_token):
        self.mt_service.set_negative_token(negative_token)
        mt_response = self.mt_service.post_load_user_mt_list()
        self.mt_service.check_bff_with_invalid_auth_structure(mt_response, negative_token)

    @Test(tags="qa, stg")
    def verify_get_paper_resource_with_valid_test_id(self):
        mt_response = self.mt_service.get_paper_resource(self.valid_test_id)
        self.mt_service.check_bff_get_paper_resource_structure(mt_response, self.valid_test_id)

    @Test(tags="qa, stg", data_provider=["", "00000000-0000-0000-0000-000000000000"])
    def verify_get_paper_resource_with_invalid_test_id(self, invalid_test_id):
        mt_response = self.mt_service.get_paper_resource(invalid_test_id)
        self.mt_service.check_get_invalid_test_structure(mt_response, invalid_test_id)

    @Test(tags="qa, stg")
    def get_test_introduction(self):
        mt_response = self.mt_service.post_load_test_intro(self.valid_test_id)
        self.mt_service.check_bff_get_test_intro_structure(mt_response, self.valid_test_id)

    @Test(tags="qa, stg", data_provider=["invalid", "noToken", "expired"])
    def verify_get_test_introduction_invalid_auth_token(self, negative_token):
        self.mt_service.set_negative_token(negative_token)
        mt_response = self.mt_service.post_load_test_intro(self.valid_test_id)
        self.mt_service.check_bff_with_invalid_auth_structure(mt_response, negative_token)

    @Test(tags="qa, stg", data_provider=["", "00000000-0000-0000-0000-000000000000"])
    def verify_get_test_introduction_with_invalid_test_id(self, invalid_test_id):
        mt_response = self.mt_service.post_load_test_intro(invalid_test_id)
        self.mt_service.check_get_invalid_test_structure(mt_response, invalid_test_id)

    @Test(tags="qa, stg")
    def verify_insert_test_with_valid_test_id(self):
        mt_response = self.mt_service.post_insert_test_by_student(self.valid_test_id)
        student_id = MockTestUsers.MTUserPw[env_key][self.has_mt_student][0]['custom_id']
        self.mt_service.check_insert_valid_test(mt_response, self.valid_test_id, student_id)

    @Test(tags="qa, stg", data_provider=["", "00000000-0000-0000-0000-000000000000"])
    def verify_insert_test_with_invalid_test_id(self, invalid_test_id):
        mt_response = self.mt_service.post_insert_test_by_student(invalid_test_id)
        self.mt_service.check_insert_invalid_test_structure(mt_response, invalid_test_id)

    @Test(tags="qa, stg")
    def verify_get_test_result_with_valid_test_id(self):
        mt_response = self.mt_service.get_test_result_by_testid(self.finished_test_id)
        self.mt_service.check_bff_get_test_result_structure(mt_response, self.finished_test_id)

    @Test(tags="qa, stg", data_provider=["invalid", "noToken", "expired"])
    def verify_get_test_result_with_invalid_auth_token(self, negative_token):
        self.mt_service.set_negative_token(negative_token)
        mt_response = self.mt_service.get_test_result_by_testid(self.finished_test_id)
        self.mt_service.check_bff_with_invalid_auth_structure(mt_response, negative_token)

    @Test(tags="qa, stg", data_provider=["", "00000000-0000-0000-0000-000000000000"])
    def verify_get_test_result_with_invalid_test_id(self, invalid_test_id):
        mt_response = self.mt_service.get_test_result_by_testid(invalid_test_id)
        self.mt_service.check_get_invalid_test_structure(mt_response, invalid_test_id)

    @Test(tags="qa, stg")
    def verify_get_remediation_with_valid_test_id(self):
        mt_response = self.mt_service.get_remediation_by_testid(self.finished_test_id, self.part)
        self.mt_service.check_bff_get_remediation_structure(mt_response, self.part)

    @Test(tags="qa, stg", data_provider=["invalid", "noToken", "expired"])
    def verify_get_remediation_with_invalid_auth_token(self, negative_token):
        self.mt_service.set_negative_token(negative_token)
        mt_response = self.mt_service.get_remediation_by_testid(self.finished_test_id, self.part)
        self.mt_service.check_bff_with_invalid_auth_structure(mt_response, negative_token)

    @Test(tags="qa, stg", data_provider=["", "00000000-0000-0000-0000-000000000000"])
    def verify_get_remediation_with_invalid_test_id(self, invalid_test_id):
        mt_response = self.mt_service.get_remediation_by_testid(invalid_test_id, self.part)
        self.mt_service.check_get_invalid_remediation_structure(mt_response, invalid_test_id)

    @Test(tags="qa, stg", data_provider=["", "100"])
    def verify_get_remediation_with_invalid_part(self, invalid_part):
        mt_response = self.mt_service.get_remediation_by_testid(self.finished_test_id, invalid_part)
        self.mt_service.check_get_invalid_remediation_structure(mt_response, invalid_part)

    @Test(tags="qa, stg")
    def verify_get_test_processing_with_finished_test_id(self):
        mt_response = self.mt_service.get_test_processing_by_test_id(self.finished_test_id)
        self.mt_service.check_bff_get_test_processing_structure(self.has_mt_student, mt_response, self.finished_test_id)

    @Test(tags="qa, stg", data_provider=["invalid", "noToken", "expired"])
    def verify_get_test_processing_with_invalid_auth_token(self, negative_token):
        self.mt_service.set_negative_token(negative_token)
        mt_response = self.mt_service.get_test_processing_by_test_id(self.finished_test_id)
        self.mt_service.check_bff_with_invalid_auth_structure(mt_response, negative_token)

    @Test(tags="qa, stg", data_provider=["", "00000000-0000-0000-0000-000000000000"])
    def verify_get_test_processing_with_invalid_test_id(self, invalid_test_id):
        mt_response = self.mt_service.get_test_processing_by_test_id(invalid_test_id)
        self.mt_service.check_get_invalid_test_structure(mt_response, invalid_test_id)

    @Test(tags="qa, stg")
    def verify_submit_remediation_with_valid_data(self):
        mt_response = self.mt_service.submit_remediation_by_test_id(self.finished_test_id, self.learner_vector_key,
                                                                    self.correct_answer_count,
                                                                    self.total_question_count)
        self.mt_service.check_bff_submit_remediation_result_structure(mt_response, self.finished_test_id,
                                                                      self.correct_answer_count,
                                                                      self.total_question_count)

    @Test(tags="qa, stg", data_provider=["invalid", "noToken", "expired"])
    def verify_submit_remediation_with_invalid_auth_token(self, negative_token):
        self.mt_service.set_negative_token(negative_token)
        mt_response = self.mt_service.submit_remediation_by_test_id(self.finished_test_id, self.learner_vector_key, 1,
                                                                    10)
        self.mt_service.check_bff_with_invalid_auth_structure(mt_response, negative_token)

    @Test(tags="qa, stg", data_provider=["", "00000000-0000-0000-0000-000000000000"])
    def verify_submit_remediation_with_invalid_test_id(self, invalid_test_id):
        mt_response = self.mt_service.submit_remediation_by_test_id(invalid_test_id, self.learner_vector_key,
                                                                    self.correct_answer_count,
                                                                    self.total_question_count)
        self.mt_service.check_post_invalid_remediation_structure(mt_response, invalid_test_id)

    @Test(tags="qa, stg", data_provider=["", "0000000000000000000"])
    def verify_submit_remediation_with_invalid_vector_key(self, invalid_learner_vector_key):
        mt_response = self.mt_service.submit_remediation_by_test_id(self.finished_test_id, invalid_learner_vector_key,
                                                                    self.correct_answer_count,
                                                                    self.total_question_count)
        assert_that(jmespath.search("errors[0].extensions.code", mt_response.json()) == 500)

    @Test(tags="qa, stg")
    def verify_get_remediation_with_valid_data(self):
        self.mt_service.submit_remediation_by_test_id(self.finished_test_id, self.learner_vector_key,
                                                      self.correct_answer_count, self.total_question_count)
        mt_response = self.mt_service.get_remediation_result_by_test_id(self.finished_test_id)
        self.mt_service.check_bff_get_remediation_result_structure(mt_response, self.correct_answer_count,
                                                                   self.total_question_count)

    @Test(tags="qa, stg", data_provider=["invalid", "noToken", "expired"])
    def verify_get_remediation_result_with_invalid_auth_token(self, negative_token):
        self.mt_service.set_negative_token(negative_token)
        mt_response = self.mt_service.get_remediation_result_by_test_id(self.finished_test_id)
        self.mt_service.check_bff_with_invalid_auth_structure(mt_response, negative_token)

    @Test(tags="qa, stg", data_provider=["", "00000000-0000-0000-0000-000000000000"])
    def verify_get_remediation_result_with_invalid_test_id(self, invalid_test_id):
        mt_response = self.mt_service.get_remediation_result_by_test_id(invalid_test_id)
        self.mt_service.check_get_invalid_remediation_structure(mt_response, invalid_test_id)

    @Test(tags="qa, stg")
    def verify_submit_test_with_valid_data(self):
        mt_response = self.mt_service.post_submit_test_result_by_test_id(self.finished_test_id, self.total_seconds_spent)
        self.mt_service.check_bff_submit_test_result_structure(mt_response, self.finished_test_id)

    @Test(tags="qa, stg", data_provider=["invalid", "noToken", "expired"])
    def verify_submit_test_with_invalid_auth_token(self, negative_token):
        self.mt_service.set_negative_token(negative_token)
        mt_response = self.mt_service.post_submit_test_result_by_test_id(self.finished_test_id, self.total_seconds_spent)
        self.mt_service.check_bff_with_invalid_auth_structure(mt_response, negative_token)

    @Test(tags="qa, stg", data_provider=["", "00000000-0000-0000-0000-000000000000"])
    def verify_submit_test_result_with_invalid_test_id(self, invalid_test_id):
        mt_response = self.mt_service.post_submit_test_result_by_test_id(invalid_test_id, self.total_seconds_spent)
        self.mt_service.check_submit_invalid_test_result_structure(mt_response, invalid_test_id)