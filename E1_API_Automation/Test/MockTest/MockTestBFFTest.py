from ptest.decorator import TestClass, Test
from E1_API_Automation.Business.MockTestBFFService import MockTestBFFService
from E1_API_Automation.Settings import MOCK_TEST_ENVIRONMENT
from hamcrest import assert_that
import jmespath


@TestClass()
class MockTestCases():
    @Test(tags="qa")
    def verify_has_test_student(self):
        mt_service = MockTestBFFService(MOCK_TEST_ENVIRONMENT)
        student_type = 'HMT'
        mt_service.login(student_type)
        mt_response = mt_service.post_load_user_mt_list()
        mt_service.check_bff_get_current_user_structure(mt_response, student_type)
        assert_that(len(jmespath.search("data.currentUser.tests", mt_response.json())) > 0)

    @Test(tags="qa")
    def verify_no_test_student(self):
        mt_service = MockTestBFFService(MOCK_TEST_ENVIRONMENT)
        student_type = 'HNMT'
        mt_service.login(student_type)
        mt_response = mt_service.post_load_user_mt_list()
        mt_service.check_bff_get_current_user_structure(mt_response, student_type)
        assert_that(len(jmespath.search("data.currentUser.tests", mt_response.json())) == 0)

    @Test(tags="qa")
    def get_test_introduction(self):
        test_id = '00000000-0000-0000-0000-202000000005'
        mt_service = MockTestBFFService(MOCK_TEST_ENVIRONMENT)
        mt_service.login('HMT')
        mt_response = mt_service.post_load_test_intro(test_id)
        mt_service.check_bff_get_test_intro_structure(mt_response, test_id)
        assert_that(len(jmespath.search("data.test", mt_response.json())) > 0)