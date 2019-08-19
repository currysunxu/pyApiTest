from ptest.decorator import TestClass, Test
from E1_API_Automation.Business.HFV35.HFV35Utils.LearningPlanUtils import LearningPlanUtils
from E1_API_Automation.Business.HFV35.LearningPlanService import LearningPlanService
from ...Settings import LEARNING_PLAN_ENVIRONMENT
from hamcrest import assert_that


@TestClass()
class PlanServiceTestCases:

    # test learning plan insert API with valid required fields
    @Test(tags="qa")
    def test_learning_plan_insert_valid_required_fields(self):
        learning_plan = LearningPlanUtils.construct_random_valid_learning_plan(False)

        learning_plan_service = LearningPlanService(LEARNING_PLAN_ENVIRONMENT)
        learning_plan_insert_api_response = learning_plan_service.post_learning_plan_insert(learning_plan)
        assert_that(learning_plan_insert_api_response.status_code == 200)
        error_message = LearningPlanUtils.verify_learning_plan_data(learning_plan_insert_api_response.json(),
                                                                    learning_plan)
        assert_that(error_message == '', error_message)





