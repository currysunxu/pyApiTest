from ptest.decorator import TestClass, Test
from E1_API_Automation.Business.NGPlatform.NGPlatformUtils.LearningResultUtils import LearningResultUtils
from E1_API_Automation.Business.NGPlatform.LearningResultService import LearningResultService
from E1_API_Automation.Business.NGPlatform.NGPlatformUtils.LearningDBUtils import LearningDBUtils
from E1_API_Automation.Business.NGPlatform.NGPlatformUtils.LearningCommonUtils import LearningCommonUtils
from ...Settings import LEARNING_RESULT_ENVIRONMENT
from hamcrest import assert_that


@TestClass()
class PlanResultTestCases:

    # test learning result insert API
    @Test(tags="qa")
    def test_learning_result_insert_valid(self):
        learning_result_service = LearningResultService(LEARNING_RESULT_ENVIRONMENT)

        learning_result = LearningResultUtils.construct_learning_result_valid(2)
        learning_result_insert_api_response = learning_result_service.post_learning_result_insert(learning_result)
        assert_that(learning_result_insert_api_response.status_code == 200)

        # verify what it returned in response will be consistent what we want to insert
        error_message = LearningCommonUtils.verify_result_with_entity(learning_result_insert_api_response.json(),
                                                                      learning_result)
        assert_that(error_message == '', error_message)

    @Test(tags="qa")
    def test_get_specific_result(self):
        learning_result_service = LearningResultService(LEARNING_RESULT_ENVIRONMENT)

        learning_result = LearningResultUtils.construct_learning_result_valid(3)
        learning_result_insert_api_response = learning_result_service.post_learning_result_insert(learning_result)
        assert_that(learning_result_insert_api_response.status_code == 200)

        learning_result_get_api_response = learning_result_service.get_specific_result(learning_result)
        assert_that(learning_result_get_api_response.status_code == 200)
        learning_result_list_from_db = LearningDBUtils.get_specific_result(learning_result)

        error_message = \
            LearningCommonUtils.verify_learning_get_api_data_with_db(learning_result_get_api_response.json(),
                                                                     learning_result_list_from_db)

        assert_that(error_message == '', error_message)



