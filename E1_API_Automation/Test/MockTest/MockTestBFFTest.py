from ptest.decorator import TestClass, Test
from E1_API_Automation.Business.MockTestBFFService import MockTestBFFService
from E1_API_Automation.Settings import MOCK_TEST_ENVIRONMENT, env_key
from E1_API_Automation.Test_Data.MockTestData import MockTestStudentType, TestIdList

from hamcrest import assert_that
import jmespath


@TestClass()
class MockTestCases():
    def __init__(self):
        self.mt_service = MockTestBFFService(MOCK_TEST_ENVIRONMENT)
        self.valid_test_id = TestIdList.TestId[env_key]['valid_test_id']

    @Test(tags="qa, stg")
    def verify_has_test_student(self):
        student_type = MockTestStudentType.HasMockTest.value
        self.mt_service.login(student_type)
        mt_response = self.mt_service.post_load_user_mt_list()
        self.mt_service.check_bff_get_current_user_structure(mt_response, student_type)
        assert_that(len(jmespath.search("data.currentUser.tests", mt_response.json())) > 0)

    @Test(tags="qa, stg")
    def verify_no_test_student(self):
        student_type = MockTestStudentType.HasNoMockTest.value
        self.mt_service.login(student_type)
        mt_response = self.mt_service.post_load_user_mt_list()
        self.mt_service.check_bff_get_current_user_structure(mt_response, student_type)
        assert_that(len(jmespath.search("data.currentUser.tests", mt_response.json())) == 0)

    @Test(tags="qa, stg", data_provider=["invalid", "noToken", "expired"])
    def verify_get_test_list_with_invalid_auth_token(self, negative_token):
        student_type = MockTestStudentType.HasMockTest.value
        self.mt_service.login(student_type)
        self.mt_service.set_negative_token(negative_token)
        mt_response = self.mt_service.post_load_user_mt_list()
        self.mt_service.check_bff_get_test_with_invalid_auth_structure(mt_response, negative_token)

    @Test(tags="qa, stg")
    def verify_get_paper_resource_with_valid_test_id(self):
        student_type = MockTestStudentType.HasMockTest.value
        self.mt_service.login(student_type)
        mt_response = self.mt_service.get_paper_resource(self.valid_test_id)
        self.mt_service.check_bff_get_paper_resource_structure(mt_response, self.valid_test_id)

    @Test(tags="qa, stg", data_provider=["", "00000000-0000-0000-0000-000000000"])
    def verify_get_paper_resource_with_invalid_test_id(self, invalid_test_id):
        student_type = MockTestStudentType.HasMockTest.value
        self.mt_service.login(student_type)
        mt_response = self.mt_service.get_paper_resource(invalid_test_id)
        self.mt_service.check_get_invalid_test_structure(mt_response, invalid_test_id)

    @Test(tags="qa, stg")
    def get_test_introduction(self):
        student_type = MockTestStudentType.HasMockTest.value
        self.mt_service.login(student_type)
        mt_response = self.mt_service.post_load_test_intro(self.valid_test_id)
        self.mt_service.check_bff_get_test_intro_structure(mt_response, self.valid_test_id)

    @Test(tags="qa, stg", data_provider=["invalid", "noToken", "expired"])
    def verify_get_test_introduction_invalid_auth_token(self, negative_token):
        student_type = MockTestStudentType.HasMockTest.value
        self.mt_service.login(student_type)
        self.mt_service.set_negative_token(negative_token)
        mt_response = self.mt_service.post_load_test_intro(self.valid_test_id)
        self.mt_service.check_bff_get_test_with_invalid_auth_structure(mt_response, negative_token)

    @Test(tags="qa, stg", data_provider=["", "00000000-0000-0000-0000-000000000"])
    def verify_get_test_introduction_with_invalid_test_id(self, invalid_test_id):
        student_type = MockTestStudentType.HasMockTest.value
        self.mt_service.login(student_type)
        mt_response = self.mt_service.post_load_test_intro(invalid_test_id)
        self.mt_service.check_get_invalid_test_structure(mt_response, invalid_test_id)

    @Test(tags="qa, stg")
    def verify_insert_test_with_valid_test_id(self):
        student_type = MockTestStudentType.HasMockTest.value
        self.mt_service.login(student_type)
        mt_response = self.mt_service.post_insert_test_by_student(self.valid_test_id)
        self.mt_service.check_insert_valid_test(mt_response, self.valid_test_id)

    @Test(tags="qa, stg", data_provider=["", "00000000-0000-0000-0000-000000000"])
    def verify_insert_test_with_invalid_test_id(self, invalid_test_id):
        student_type = MockTestStudentType.HasMockTest.value
        self.mt_service.login(student_type)
        mt_response = self.mt_service.post_insert_test_by_student(invalid_test_id)
        self.mt_service.check_insert_invalid_test_structure(mt_response, invalid_test_id)