from ptest.decorator import TestClass, Test
from E1_API_Automation.Business.PTReviewService import PTReviewService
from E1_API_Automation.Business.Utils.PTReviewUtils import PTReviewUtils
from E1_API_Automation.Business.TPIService import TPIService
from ...Settings import OSP_ENVIRONMENT, TPI_ENVIRONMENT, env_key
from ...Test_Data.PTReviewData import PTReviewData
from E1_API_Automation.Business.Utils.EnvUtils import EnvUtils
from hamcrest import assert_that
import jmespath
import json


@TestClass()
class PTReviewTestCases:

    @Test(tags="qa, stg, live")
    def test_get_hf_all_books(self):
        pt_review_service = PTReviewService(OSP_ENVIRONMENT)
        response = pt_review_service.get_hf_all_books_url()
        api_response_json = response.json()
        code_list = jmespath.search('[].Code', api_response_json)

        expected_code_list = ['HFC', 'HFD', 'HFE', 'HFF', 'HFG', 'HFH', 'HFI', 'HFJ']
        assert_that(code_list == expected_code_list, "Code returned is not as expected.")

        # if it's not Live environment, then do the rest verification with DB
        if not EnvUtils.is_env_live():
            # get the result from DB
            db_query_result = pt_review_service.get_hf_all_books_from_db()

            # the list length should be equal for the response list and DB list
            assert_that(len(api_response_json) == len(db_query_result))

            # check if all the data return from API is consistent with DB
            error_message = PTReviewUtils.verify_hf_allbooks_api_db_result(api_response_json, db_query_result)
            assert_that(error_message == '', error_message)

    @Test(tags="qa, stg")
    def test_save_total_score_with_omni_api(self):
        # construct data to call the API
        skill_dic = PTReviewUtils.generate_pt_whole_skill_subskill_randomscore_list()
        student_id = PTReviewData.pt_hf_user_key_book_unit[env_key]['StudentId']
        student_skill = {}
        student_skill[student_id] = skill_dic
        pt_key = PTReviewData.pt_hf_user_key_book_unit[env_key]['TestPrimaryKey']
        omni_body = PTReviewUtils.generate_assessment_body_for_omni(pt_key, student_skill)

        omni_body_json = json.dumps(omni_body)
        print(omni_body_json)

        # call OmniProgressTestAssessment API to update overwritten score and total score
        tpi_service = TPIService(TPI_ENVIRONMENT)
        tpi_response = tpi_service.put_hf_student_omni_pt_assessment(omni_body)
        assert_that(tpi_response.status_code == 204)

        pt_review_service = PTReviewService(OSP_ENVIRONMENT)
        book_key = PTReviewData.pt_hf_user_key_book_unit[env_key]['BookKey']
        # call StudentPaperDigitalProgressTestAssessmentMetas API to get all the records from DB
        assess_metas = pt_review_service.post_hf_student_pt_assess_metas(student_id, book_key)
        assert_that(assess_metas.status_code == 200)
        assess_metas_response = assess_metas.json()

        # verify if the data get from the StudentPaperDigitalProgressTestAssessmentMetas API are as what you constructed
        PTReviewUtils.verify_pt_score_with_api_response(skill_dic, assess_metas_response)
