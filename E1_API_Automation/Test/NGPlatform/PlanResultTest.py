from ptest.decorator import TestClass, Test
from E1_API_Automation.Business.NGPlatform.NGPlatformUtils.LearningResultUtils import LearningResultUtils
from E1_API_Automation.Business.NGPlatform.LearningResultService import LearningResultService
from E1_API_Automation.Business.NGPlatform.LearningResultEntity import LearningResultEntity
from E1_API_Automation.Business.NGPlatform.LearningPlanFieldTemplate import FieldValueType
from ...Settings import LEARNING_RESULT_ENVIRONMENT
from hamcrest import assert_that
import random


@TestClass()
class PlanResultTestCases:

    # test learning result insert API
    @Test(tags="qa")
    def test_learning_result_insert_valid(self):
        learning_result_service = LearningResultService(LEARNING_RESULT_ENVIRONMENT)

        learning_result = LearningResultUtils.construct_learning_result_valid(1)
        learning_plan_insert_api_response = learning_result_service.post_learning_result_insert(learning_result)
        assert_that(learning_plan_insert_api_response.status_code == 200)
        # content = LearningResultUtils.convert_name_from_camel_case_to_lower_case("productId")
        # print(content)
        # content = LearningResultUtils.convert_name_from_camel_case_to_lower_case("planBusinessKey")
        # print(content)



