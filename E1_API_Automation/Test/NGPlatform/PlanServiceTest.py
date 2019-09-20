from ptest.decorator import TestClass, Test
from E1_API_Automation.Business.NGPlatform.NGPlatformUtils.LearningPlanUtils import LearningPlanUtils
from E1_API_Automation.Business.NGPlatform.NGPlatformUtils.LearningDBUtils import LearningDBUtils
from E1_API_Automation.Business.NGPlatform.NGPlatformUtils.LearningCommonUtils import LearningCommonUtils
from E1_API_Automation.Business.NGPlatform.LearningPlanService import LearningPlanService
from E1_API_Automation.Business.NGPlatform.LearningPlan import LearningPlan
from E1_API_Automation.Business.NGPlatform.LearningPlanFieldTemplate import FieldValueType
from ...Settings import LEARNING_PLAN_ENVIRONMENT
from hamcrest import assert_that
import random


@TestClass()
class PlanServiceTestCases:

    # test learning plan insert API with valid fields
    @Test(tags="qa")
    def test_learning_plan_insert_valid_fields(self):
        learning_plan_service = LearningPlanService(LEARNING_PLAN_ENVIRONMENT)

        learning_plan = LearningPlanUtils.construct_random_valid_learning_plan(False)
        learning_plan_insert_api_response = learning_plan_service.post_learning_plan_insert(learning_plan)
        assert_that(learning_plan_insert_api_response.status_code == 200)
        # verify what it returned in response will be consistent what we want to insert
        error_message = LearningCommonUtils.verify_result_with_entity(learning_plan_insert_api_response.json(),
                                                                      learning_plan)
        assert_that(error_message == '', error_message)

        # check when get specific plan, the return message will consistent what we want to insert through API
        learning_plan_get_api_response = learning_plan_service.get_specific_plan(learning_plan)
        error_message = LearningCommonUtils.verify_result_with_entity(learning_plan_get_api_response.json()[0],
                                                                      learning_plan)
        assert_that(error_message == '', error_message)

        # delete this specific learning plan at last
        delete_response = learning_plan_service.delete_specific_plan(learning_plan)
        assert_that(delete_response.status_code == 200)

    @Test(tags="qa")
    def test_get_specific_plan(self):
        learning_plan_service = LearningPlanService(LEARNING_PLAN_ENVIRONMENT)

        learning_plan = LearningPlanUtils.construct_random_valid_learning_plan(False)
        learning_plan_insert_api_response = learning_plan_service.post_learning_plan_insert(learning_plan)
        assert_that(learning_plan_insert_api_response.status_code == 200)
        learning_plan_get_api_response = learning_plan_service.get_specific_plan(learning_plan)
        assert_that(learning_plan_get_api_response.status_code == 200)
        learning_plan_list_from_db = LearningDBUtils.get_specific_plan(learning_plan)

        error_message = LearningCommonUtils.verify_learning_get_api_data_with_db(learning_plan_get_api_response.json(),
                                                                                 learning_plan_list_from_db)

        assert_that(error_message == '', error_message)

        # delete this specific learning plan at last
        delete_response = learning_plan_service.delete_specific_plan(learning_plan)
        assert_that(delete_response.status_code == 200)

    @Test(tags="qa")
    def test_delete_specific_plan(self):
        learning_plan_service = LearningPlanService(LEARNING_PLAN_ENVIRONMENT)
        # insert data
        learning_plan = LearningPlanUtils.construct_random_valid_learning_plan(False)
        learning_plan_insert_api_response = learning_plan_service.post_learning_plan_insert(learning_plan)
        assert_that(learning_plan_insert_api_response.status_code == 200)
        # check data with the API
        learning_plan_get_api_response = learning_plan_service.get_specific_plan(learning_plan)
        assert_that(len(learning_plan_get_api_response.json())>0, 'The get specific plan API return empty!')

        # delete specific API
        delete_response = learning_plan_service.delete_specific_plan(learning_plan)
        assert_that(delete_response.status_code == 200)
        # get specific API, check there's no return entity
        learning_plan_get_api_response = learning_plan_service.get_specific_plan(learning_plan)
        assert_that(len(learning_plan_get_api_response.json()) == 0, 'The get specific plan API should return empty!')

    @Test(tags="qa")
    def test_learning_plan_batch_insert_valid(self):
        learning_plan_service = LearningPlanService(LEARNING_PLAN_ENVIRONMENT)

        # batch insert need the whole batch have same partition,that means,need same product_id plan_business_key and bucket_id
        learning_plan_template = LearningPlanUtils.construct_learning_plan_template(False)
        # construct valid learning plan list
        batch_number = 10
        learning_plan_list = LearningPlanUtils.construct_multiple_valid_learning_plans(learning_plan_template,
                                                                                       batch_number)
        # call learning plan batch insert api
        learning_plan_batch_insert_api_response = \
            learning_plan_service.post_learning_plan_batch_insert(learning_plan_list)
        assert_that(learning_plan_batch_insert_api_response.status_code == 200)

        # verify what it returned in response will be consistent what we want to batch insert
        error_message = LearningPlanUtils.verify_learning_plan_batch_insert_data(learning_plan_batch_insert_api_response.json(),
                                                                                 learning_plan_list)
        assert_that(error_message == '', error_message)

        # check when get specific plan, the return message will consistent what we want to insert through API
        learning_plan_get_api_response = learning_plan_service.get_partition_plan_without_limit_page(learning_plan_template)
        error_message = LearningPlanUtils.verify_learning_plan_get_data_with_entity_list(learning_plan_get_api_response.json(),
                                                                    learning_plan_list)
        assert_that(error_message == '', error_message)

        # delete these whole learning plan at last
        delete_response = learning_plan_service.delete_plan_by_partition(learning_plan_template)
        assert_that(delete_response.status_code == 200)

    def test_get_plan_without_limit_page(self, batch_number, is_user_plan):
        learning_plan_service = LearningPlanService(LEARNING_PLAN_ENVIRONMENT)

        # batch insert need the whole batch have same partition,that means,need same product_id plan_business_key and bucket_id
        learning_plan_template = LearningPlanUtils.construct_learning_plan_template(is_user_plan)
        # construct valid learning plan list
        learning_plan_list = LearningPlanUtils.construct_multiple_valid_learning_plans(learning_plan_template,
                                                                                       batch_number)
        # call learning plan batch insert api
        learning_plan_batch_insert_api_response = \
            learning_plan_service.post_learning_plan_batch_insert(learning_plan_list)
        assert_that(learning_plan_batch_insert_api_response.status_code == 200)
        # call get partition API
        if is_user_plan:
            learning_plan_get_api_response = learning_plan_service.get_user_plan_without_limit_page(
                learning_plan_template)
            learning_plan_list_from_db = LearningDBUtils.get_user_plan(learning_plan_template)
        else:
            learning_plan_get_api_response = \
                learning_plan_service.get_partition_plan_without_limit_page(learning_plan_template)
            learning_plan_list_from_db = LearningDBUtils.get_partition_plan(learning_plan_template)

        assert_that(learning_plan_get_api_response.status_code == 200)

        # if there's more than 50 records fit the condition, the get API will by default get 50 records
        if batch_number > 50:
            learning_plan_list_from_db = learning_plan_list_from_db[:50]

        error_message = LearningCommonUtils.verify_learning_get_api_data_with_db(learning_plan_get_api_response.json(),
                                                                                 learning_plan_list_from_db)

        assert_that(error_message == '', error_message)

        # delete these partition learning plan at last
        if is_user_plan:
            delete_response = learning_plan_service.delete_user_plan(learning_plan_template)
        else:
            delete_response = learning_plan_service.delete_plan_by_partition(learning_plan_template)
        assert_that(delete_response.status_code == 200)

    def test_get_plan_with_limit(self, batch_number, limit_list, is_user_plan):
        learning_plan_service = LearningPlanService(LEARNING_PLAN_ENVIRONMENT)

        # batch insert need the whole batch have same partition,that means,need same product_id plan_business_key and bucket_id
        # user plan need student key
        learning_plan_template = LearningPlanUtils.construct_learning_plan_template(is_user_plan)
        # construct valid learning plan list
        # batch_number = 51
        learning_plan_list = LearningPlanUtils.construct_multiple_valid_learning_plans(learning_plan_template,
                                                                                       batch_number)
        # call learning plan batch insert api
        learning_plan_batch_insert_api_response = \
            learning_plan_service.post_learning_plan_batch_insert(learning_plan_list)
        assert_that(learning_plan_batch_insert_api_response.status_code == 200)
        # limit list, default limit value is 50
        # limit_list = [1, random.randint(2, 10), random.randint(10, 30), random.randint(30, 50), 50, None]

        if is_user_plan:
            learning_plan_list_from_db = LearningDBUtils.get_user_plan(learning_plan_template)
        else:
            learning_plan_list_from_db = LearningDBUtils.get_partition_plan(learning_plan_template)

        for limit in limit_list:
            if is_user_plan:
                learning_plan_get_api_response = learning_plan_service.get_user_plan_with_limit(learning_plan_template,
                                                                                                limit)
            else:
                learning_plan_get_api_response = \
                    learning_plan_service.get_partition_plan_with_limit(learning_plan_template, limit)

            assert_that(learning_plan_get_api_response.status_code == 200)

            expected_learning_plan_list_from_db = \
                LearningPlanUtils.get_expected_learning_plan_from_db_by_limit_page(learning_plan_list_from_db,
                                                                                   limit, None)

            error_message = LearningCommonUtils.\
                verify_learning_get_api_data_with_db(learning_plan_get_api_response.json(),
                                                     expected_learning_plan_list_from_db)
            assert_that(error_message == '', "When limit is:" + str(limit) + ", the error message is:" + error_message)

        # delete these learning plan at last
        if is_user_plan:
            delete_response = learning_plan_service.delete_user_plan(learning_plan_template)
        else:
            delete_response = learning_plan_service.delete_plan_by_partition(learning_plan_template)
        assert_that(delete_response.status_code == 200)

    def test_get_plan_with_limit_page(self, batch_number, limit_page_list, is_user_plan):
        learning_plan_service = LearningPlanService(LEARNING_PLAN_ENVIRONMENT)

        # batch insert need the whole batch have same partition,that means,need same product_id plan_business_key and bucket_id
        # user plan need student key
        learning_plan_template = LearningPlanUtils.construct_learning_plan_template(is_user_plan)
        # construct valid learning plan list
        learning_plan_list = LearningPlanUtils.construct_multiple_valid_learning_plans(learning_plan_template,
                                                                                       batch_number)
        # call learning plan batch insert api
        learning_plan_batch_insert_api_response = \
            learning_plan_service.post_learning_plan_batch_insert(learning_plan_list)
        assert_that(learning_plan_batch_insert_api_response.status_code == 200)

        if is_user_plan:
            learning_plan_list_from_db = LearningDBUtils.get_user_plan(learning_plan_template)
        else:
            learning_plan_list_from_db = LearningDBUtils.get_partition_plan(learning_plan_template)

        for limit_page in limit_page_list:
            limit = limit_page['limit']
            page_list = limit_page['page']

            if page_list is None:
                page_list = [None]

            for page in page_list:
                if is_user_plan:
                    learning_plan_get_api_response = \
                        learning_plan_service.get_user_plan_with_limit_page(learning_plan_template, limit, page)
                else:
                    learning_plan_get_api_response = \
                        learning_plan_service.get_partition_plan_with_limit_page(learning_plan_template, limit, page)

                assert_that(learning_plan_get_api_response.status_code == 200)

                expected_learning_plan_list_from_db = \
                    LearningPlanUtils.get_expected_learning_plan_from_db_by_limit_page(learning_plan_list_from_db,
                                                                                       limit, page)

                error_message = LearningCommonUtils.\
                    verify_learning_get_api_data_with_db(learning_plan_get_api_response.json(),
                                                         expected_learning_plan_list_from_db)
                assert_that(error_message == '', "When limit is:" + str(limit) + "page is:" + str(page)
                            + ",the error message is:" + error_message)

        # delete these learning plan at last
        if is_user_plan:
            delete_response = learning_plan_service.delete_user_plan(learning_plan_template)
        else:
            delete_response = learning_plan_service.delete_plan_by_partition(learning_plan_template)
        assert_that(delete_response.status_code == 200)

    @Test(tags="qa")
    def test_get_partition_plan_without_limit_page_less_than_50(self):
        batch_number = 15
        self.test_get_plan_without_limit_page(batch_number, False)

    # when there's more than 50 records in the DB, get API will by default get 50 records
    @Test(tags="qa")
    def test_get_partition_plan_without_limit_page_larger_than_50(self):
        batch_number = 51
        self.test_get_plan_without_limit_page(batch_number, False)

    @Test(tags="qa")
    def test_get_user_plan_without_limit_page_less_than_50(self):
        batch_number = 15
        self.test_get_plan_without_limit_page(batch_number, True)

    # when there's more than 50 records in the DB, get API will by default get 50 records
    @Test(tags="qa")
    def test_get_user_plan_without_limit_page_larger_than_50(self):
        batch_number = 51
        self.test_get_plan_without_limit_page(batch_number, True)

    @Test(tags="qa")
    def test_get_partition_plan_with_limit_less_than_size(self):
        batch_number = 51
        # limit list, default limit value is 50
        limit_list = [1, random.randint(2, 10), random.randint(11, 30), random.randint(31, 49), 50, None]

        self.test_get_plan_with_limit(batch_number, limit_list, False)

    @Test(tags="qa")
    def test_get_partition_plan_with_limit_larger_than_size(self):
        batch_number = 15
        limit_list = [random.randint(1, batch_number-1), batch_number, batch_number + 1,
                      random.randint(batch_number + 2, 50)]
        self.test_get_plan_with_limit(batch_number-1, limit_list, False)

    @Test(tags="qa")
    def test_get_partition_plan_with_limit_page_less_than_size(self):
        batch_number = 51
        limit_1 = 10
        limit_2 = 50
        limit_page_list = [{'limit': limit_1,
                            'page': [1, random.randint(2, batch_number // limit_1 - 1), batch_number // limit_1,
                                     batch_number // limit_1 + 1, random.randint(batch_number // limit_1 + 2, 50),
                                     None]},
                           {'limit': limit_2,
                            'page': [1, batch_number // limit_2 + 1, random.randint(batch_number // limit_2 + 2, 50),
                                     None]},
                           {'limit': None, 'page': None}]
        self.test_get_plan_with_limit_page(batch_number, limit_page_list, False)

    @Test(tags="qa")
    def test_get_partition_plan_with_limit_page_larger_than_size(self):
        batch_number = 20
        limit_1 = random.randint(1, batch_number)
        limit_2 = random.randint(batch_number, 50)
        limit_page_list = [{'limit': limit_1,
                            'page': [random.randint(1, batch_number // limit_1),
                                     random.randint(batch_number // limit_1 + 1, 50),
                                     None]},
                           {'limit': limit_2,
                            'page': [1, random.randint(2, 10), None]},
                           {'limit': None, 'page': None}]
        self.test_get_plan_with_limit_page(batch_number, limit_page_list, False)

    @Test(tags="qa")
    def test_get_user_plan_with_limit_less_than_size(self):
        batch_number = 51
        # limit list, default limit value is 50
        limit_list = [1, random.randint(2, 10), random.randint(11, 30), random.randint(31, 49), 50, None]

        self.test_get_plan_with_limit(batch_number, limit_list, True)

    @Test(tags="qa")
    def test_get_user_plan_with_limit_larger_than_size(self):
        batch_number = 15
        limit_list = [random.randint(1, batch_number - 1), batch_number, batch_number + 1,
                      random.randint(batch_number + 2, 50)]
        self.test_get_plan_with_limit(batch_number, limit_list, True)

    @Test(tags="qa")
    def test_get_user_plan_with_limit_page_less_than_size(self):
        batch_number = 51
        limit_1 = 10
        limit_2 = 50
        limit_page_list = [{'limit': limit_1,
                            'page': [1, random.randint(2, batch_number // limit_1 - 1), batch_number // limit_1,
                                     batch_number // limit_1 + 1, random.randint(batch_number // limit_1 + 2, 50),
                                     None]},
                           {'limit': limit_2,
                            'page': [1, batch_number // limit_2 + 1, random.randint(batch_number // limit_2 + 2, 50),
                                     None]},
                           {'limit': None, 'page': None}]
        self.test_get_plan_with_limit_page(batch_number, limit_page_list, True)

    @Test(tags="qa")
    def test_get_user_plan_with_limit_page_larger_than_size(self):
        batch_number = 20
        limit_1 = random.randint(1, batch_number)
        limit_2 = random.randint(batch_number, 50)
        limit_page_list = [{'limit': limit_1,
                            'page': [random.randint(1, batch_number // limit_1),
                                     random.randint(batch_number // limit_1 + 1, 50),
                                     None]},
                           {'limit': limit_2,
                            'page': [1, random.randint(2, 10), None]},
                           {'limit': None, 'page': None}]
        self.test_get_plan_with_limit_page(batch_number, limit_page_list, True)

    # test delete user/partition plan
    def test_delete_user_partition_plan(self, batch_number, is_user_plan):
        learning_plan_service = LearningPlanService(LEARNING_PLAN_ENVIRONMENT)
        # insert data
        # batch insert need the whole batch have same partition,that means,need same product_id plan_business_key and bucket_id
        learning_plan_template = LearningPlanUtils.construct_learning_plan_template(is_user_plan)
        # construct valid learning plan list
        learning_plan_list = LearningPlanUtils.construct_multiple_valid_learning_plans(learning_plan_template,
                                                                                       batch_number)
        # call learning plan batch insert api
        learning_plan_batch_insert_api_response = \
            learning_plan_service.post_learning_plan_batch_insert(learning_plan_list)
        assert_that(learning_plan_batch_insert_api_response.status_code == 200)

        # check data with the API
        if is_user_plan:
            learning_plan_get_api_response = learning_plan_service.get_user_plan_without_limit_page(
                learning_plan_template)
        else:
            learning_plan_get_api_response = \
                learning_plan_service.get_partition_plan_without_limit_page(learning_plan_template)

        assert_that(len(learning_plan_get_api_response.json()) == batch_number,
                    'The get partition/user plan API return empty!')

        # delete specific API
        if is_user_plan:
            delete_response = learning_plan_service.delete_user_plan(learning_plan_template)
        else:
            delete_response = learning_plan_service.delete_plan_by_partition(learning_plan_template)

        assert_that(delete_response.status_code == 200)
        # get specific API, check there's no return entity
        if is_user_plan:
            learning_plan_get_api_response = learning_plan_service.get_user_plan_without_limit_page(
                learning_plan_template)
        else:
            learning_plan_get_api_response = \
                learning_plan_service.get_partition_plan_without_limit_page(learning_plan_template)

        assert_that(len(learning_plan_get_api_response.json()) == 0,
                    'The get partition/user plan API should return empty!')

    @Test(tags="qa")
    def test_delete_partition_plan(self):
        batch_number = 15
        self.test_delete_user_partition_plan(batch_number, False)

    @Test(tags="qa")
    def test_delete_user_plan(self):
        batch_number = 15
        self.test_delete_user_partition_plan(batch_number, True)

    # test learning plan update API with valid required fields
    # For update behavior, the product_id, plan_business_key, bucket_id, student_key, system_key are the primary key
    @Test(tags="qa")
    def test_learning_plan_update_valid(self):
        learning_plan_service = LearningPlanService(LEARNING_PLAN_ENVIRONMENT)
        # prepare learning plan first
        learning_plan = LearningPlanUtils.construct_random_valid_learning_plan(False)
        learning_plan_insert_api_response = learning_plan_service.post_learning_plan_insert(learning_plan)
        assert_that(learning_plan_insert_api_response.status_code == 200)

        # construct a update learning plan, it have same product_id, plan_business_key, bucket_id, student_key, system_key with original plan
        learning_plan_update = LearningPlanUtils.construct_learning_plan_by_template(learning_plan, FieldValueType.Valid)

        learning_plan_update_api_response = learning_plan_service.put_learning_plan(learning_plan_update)
        assert_that(learning_plan_update_api_response.status_code == 200)
        # verify the update API return response
        assert_that(learning_plan_update_api_response.json() is True, "update API should return true!")

        # check when get specific plan, the return message will consistent what we want to insert through API
        learning_plan_get_api_response = learning_plan_service.get_specific_plan(learning_plan_update)
        error_message = LearningCommonUtils.verify_result_with_entity(learning_plan_get_api_response.json()[0],
                                                                    learning_plan_update)
        assert_that(error_message == '', error_message)

        # delete this specific learning plan at last
        delete_response = learning_plan_service.delete_specific_plan(learning_plan_update)
        assert_that(delete_response.status_code == 200)

    @Test(tags="qa")
    def test_learning_plan_insert_null_values(self):
        learning_plan_service = LearningPlanService(LEARNING_PLAN_ENVIRONMENT)
        # all the filed value as null
        learning_plan = LearningPlan(None, None, None, None)
        learning_plan_insert_api_response = learning_plan_service.post_learning_plan_insert(learning_plan)
        assert_that(learning_plan_insert_api_response.status_code == 400)

        error_message = LearningPlanUtils.verify_insert_put_error_messages(learning_plan_insert_api_response.json(),
                                                                           learning_plan)

        assert_that(error_message == '', error_message)

    @Test(tags="qa")
    def test_learning_plan_insert_empty_values(self):
        learning_plan_service = LearningPlanService(LEARNING_PLAN_ENVIRONMENT)
        # all the filed value as empty
        learning_plan = LearningPlanUtils.construct_learning_plan_with_empty_fields()
        learning_plan_insert_api_response = learning_plan_service.post_learning_plan_insert(learning_plan)
        assert_that(learning_plan_insert_api_response.status_code == 400)

        error_message = LearningPlanUtils.verify_insert_put_error_messages(learning_plan_insert_api_response.json(),
                                                                           learning_plan)

        assert_that(error_message == '', error_message)

    @Test(tags="qa")
    def test_learning_plan_batch_insert_single_plan_null_values(self):
        learning_plan_service = LearningPlanService(LEARNING_PLAN_ENVIRONMENT)
        # all the filed value as null
        learning_plan = LearningPlan(None, None, None, None)
        learning_plan_list = [learning_plan]

        learning_plan_batch_insert_api_response = learning_plan_service.post_learning_plan_batch_insert(learning_plan_list)
        assert_that(learning_plan_batch_insert_api_response.status_code == 400)

        error_message = LearningPlanUtils.verify_insert_put_error_messages(learning_plan_batch_insert_api_response.json(),
                                                                           learning_plan_list)

        assert_that(error_message == '', error_message)

    @Test(tags="qa")
    def test_learning_plan_batch_insert_single_plan_empty_values(self):
        learning_plan_service = LearningPlanService(LEARNING_PLAN_ENVIRONMENT)
        # all the filed value as empty
        learning_plan = LearningPlanUtils.construct_learning_plan_with_empty_fields()
        learning_plan_list = [learning_plan]

        learning_plan_batch_insert_api_response = learning_plan_service.post_learning_plan_batch_insert(learning_plan_list)
        assert_that(learning_plan_batch_insert_api_response.status_code == 400)

        error_message = LearningPlanUtils.verify_insert_put_error_messages(learning_plan_batch_insert_api_response.json(),
                                                                           learning_plan_list)

        assert_that(error_message == '', error_message)

    @Test(tags="qa")
    def test_learning_plan_batch_insert_multiple_plan_null_empty_values(self):
        learning_plan_service = LearningPlanService(LEARNING_PLAN_ENVIRONMENT)
        # all the filed value as null
        learning_plan_null = LearningPlan(None, None, None, None)
        # all the filed value as empty
        learning_plan_empty = LearningPlanUtils.construct_learning_plan_with_empty_fields()
        learning_plan_list = [learning_plan_null, learning_plan_empty]

        learning_plan_batch_insert_api_response = learning_plan_service.post_learning_plan_batch_insert(learning_plan_list)
        assert_that(learning_plan_batch_insert_api_response.status_code == 400)

        error_message = LearningPlanUtils.verify_insert_put_error_messages(learning_plan_batch_insert_api_response.json(),
                                                                           learning_plan_list)

        assert_that(error_message == '', error_message)

    @Test(tags="qa")
    def test_learning_plan_insert_invalid_value_below_min(self):
        learning_plan_service = LearningPlanService(LEARNING_PLAN_ENVIRONMENT)
        # all the filed value as null
        learning_plan = LearningPlanUtils.construct_learning_plan_with_invalid_value(FieldValueType.BelowMin)
        learning_plan_insert_api_response = learning_plan_service.post_learning_plan_insert(learning_plan)
        assert_that(learning_plan_insert_api_response.status_code == 400)

        error_message = LearningPlanUtils.verify_insert_put_error_messages(learning_plan_insert_api_response.json(),
                                                                           learning_plan)

        assert_that(error_message == '', error_message)

    @Test(tags="qa")
    def test_learning_plan_insert_invalid_value_exceed_max(self):
        learning_plan_service = LearningPlanService(LEARNING_PLAN_ENVIRONMENT)
        # all the filed value as null
        learning_plan = LearningPlanUtils.construct_learning_plan_with_invalid_value(FieldValueType.ExceedMax)
        learning_plan_insert_api_response = learning_plan_service.post_learning_plan_insert(learning_plan)
        assert_that(learning_plan_insert_api_response.status_code == 400)

        error_message = LearningPlanUtils.verify_insert_put_error_messages(learning_plan_insert_api_response.json(),
                                                                           learning_plan)

        assert_that(error_message == '', error_message)


