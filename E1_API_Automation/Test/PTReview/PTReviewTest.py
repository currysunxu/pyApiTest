from ptest.decorator import TestClass, Test
from E1_API_Automation.Business.PTReviewService import PTReviewService
from ...Settings import OSP_ENVIRONMENT, env_key
from hamcrest import assert_that
import jmespath


@TestClass()
class PTReviewTestCases():

    @Test()
    def test_get_hf_all_books(self):

        self.PTReviewService = PTReviewService(OSP_ENVIRONMENT)
        response = self.PTReviewService.get_hf_all_books_url()
        api_response_json = response.json()
        code_list = jmespath.search('[].Code', api_response_json)

        expected_code_list = ['HFC', 'HFD', 'HFE', 'HFF', 'HFG', 'HFH', 'HFI', 'HFJ']
        assert_that(code_list == expected_code_list, "Code returned is not as expected.")

        # if it's not Live environment, then do the rest verification with DB
        if not env_key.startswith('Live'):
            # get the result from DB
            db_query_result = self.PTReviewService.get_hf_all_books_from_db()

            # the list length should be equal for the response list and DB list
            assert_that(len(api_response_json) == len(db_query_result))

            # check if all the data return from API is consistent with DB
            error_message = self.PTReviewService.verify_api_db_result(api_response_json, db_query_result)
            assert_that(error_message == '', error_message)
