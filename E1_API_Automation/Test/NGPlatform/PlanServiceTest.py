from ptest.decorator import TestClass, Test
from E1_API_Automation.Business.NGPlatform.NGPlatformUtils.LearningPlanUtils import LearningPlanUtils
from E1_API_Automation.Business.NGPlatform.NGPlatformUtils.LearningDBUtils import LearningDBUtils
from E1_API_Automation.Business.NGPlatform.NGPlatformUtils.LearningCommonUtils import LearningCommonUtils
from E1_API_Automation.Business.NGPlatform.LearningPlanService import LearningPlanService
from E1_API_Automation.Business.NGPlatform.LearningPlanEntity import LearningPlanEntity
from E1_API_Automation.Business.NGPlatform.LearningFieldTemplate import FieldValueType
from E1_API_Automation.Business.NGPlatform.NGPlatformUtils.LearningEnum import LearningPlanAPIType
from ...Settings import LEARNING_PLAN_ENVIRONMENT
from hamcrest import assert_that
import random
import string
import uuid
import datetime

# plan service has been deprecated, but leave it here for now just in case
# @TestClass()
class PlanServiceTestCases:
    # test learning plan insert API with valid fields
    @Test(tags="qa")
    def test_learning_plan_insert_valid_all_fields(self):
        self.test_learning_plan_insert_valid_values(FieldValueType.Valid, False)

    # test learning plan insert API with valid fields
    @Test(tags="qa")
    def test_learning_plan_insert_valid_required_fields(self):
        self.test_learning_plan_insert_valid_values(FieldValueType.Valid, True)

    # test learning plan insert API with valid min fields
    @Test(tags="qa")
    def test_learning_plan_insert_valid_min(self):
        self.test_learning_plan_insert_valid_values(FieldValueType.Min)

    # test learning plan insert API with valid max fields
    @Test(tags="qa")
    def test_learning_plan_insert_valid_max(self):
        self.test_learning_plan_insert_valid_values(FieldValueType.Max)

    # called by other test cases
    def test_learning_plan_insert_valid_values(self, field_value_type, is_only_required=False):
        learning_plan_service = LearningPlanService(LEARNING_PLAN_ENVIRONMENT)

        learning_plan = \
            LearningPlanUtils.construct_learning_plan_by_template_and_is_only_required(None, field_value_type,
                                                                                       is_only_required)
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

    # method can be called by other test cases
    def test_learning_plan_batch_insert_valid_values(self, field_value_type, is_only_required=False,
                                                     is_single_plan=False):
        learning_plan_service = LearningPlanService(LEARNING_PLAN_ENVIRONMENT)

        # batch insert need the whole batch have same partition,that means,
        # need same product_id plan_business_key and bucket_id
        learning_plan_template = LearningPlanUtils.construct_learning_plan_template(False)
        # construct valid learning plan list
        if is_single_plan:
            batch_number = 1
        else:
            batch_number = random.randint(3, 10)
        learning_plan_list = \
            LearningPlanUtils.construct_multiple_plans_by_template_and_value_type(learning_plan_template,
                                                                                  field_value_type,
                                                                                  batch_number, is_only_required)
        # call learning plan batch insert api
        learning_plan_batch_insert_api_response = \
            learning_plan_service.post_learning_plan_batch_insert(learning_plan_list)
        assert_that(learning_plan_batch_insert_api_response.status_code == 200)

        # verify what it returned in response will be consistent what we want to batch insert
        error_message = LearningPlanUtils.verify_learning_plan_batch_insert_data(learning_plan_batch_insert_api_response.json(),
                                                                                 learning_plan_list)
        assert_that(error_message == '', error_message)

        # check when get specific plan, the return message will consistent what we want to insert through API
        learning_plan_get_api_response = \
            learning_plan_service.get_partition_plan_without_limit_page(learning_plan_template)
        error_message = \
            LearningPlanUtils.verify_learning_plan_get_data_with_entity_list(learning_plan_get_api_response.json(),
                                                                             learning_plan_list)
        assert_that(error_message == '', error_message)

        # delete these whole learning plan at last
        delete_response = learning_plan_service.delete_partition_plan(learning_plan_template)
        assert_that(delete_response.status_code == 200)

    @Test(tags="qa")
    def test_learning_plan_batch_insert_valid_all_fields(self):
        self.test_learning_plan_batch_insert_valid_values(FieldValueType.Valid, False)

    @Test(tags="qa")
    def test_learning_plan_batch_insert_valid_required_fields(self):
        self.test_learning_plan_batch_insert_valid_values(FieldValueType.Valid, True)

    @Test(tags="qa")
    def test_learning_plan_batch_insert_valid_min(self):
        self.test_learning_plan_batch_insert_valid_values(FieldValueType.Min)

    @Test(tags="qa")
    def test_learning_plan_batch_insert_valid_max(self):
        self.test_learning_plan_batch_insert_valid_values(FieldValueType.Max)

    @Test(tags="qa")
    def test_learning_plan_batch_insert_valid_single_plan(self):
        self.test_learning_plan_batch_insert_valid_values(FieldValueType.Valid, False, True)

    # method will be called by test cases
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
            delete_response = learning_plan_service.delete_partition_plan(learning_plan_template)
        assert_that(delete_response.status_code == 200)

    def test_get_plan_with_limit(self, batch_number, limit_list, is_user_plan):
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

        for limit in limit_list:
            if is_user_plan:
                learning_plan_get_api_response = learning_plan_service.get_user_plan_with_limit(learning_plan_template,
                                                                                                limit)
            else:
                learning_plan_get_api_response = \
                    learning_plan_service.get_partition_plan_with_limit(learning_plan_template, limit)

            assert_that(learning_plan_get_api_response.status_code == 200)

            expected_learning_plan_list_from_db = \
                LearningCommonUtils.get_expected_learning_data_from_db_by_limit_page(learning_plan_list_from_db,
                                                                                     limit, None)

            error_message = LearningCommonUtils.\
                verify_learning_get_api_data_with_db(learning_plan_get_api_response.json(),
                                                     expected_learning_plan_list_from_db)
            assert_that(error_message == '', "When limit is:" + str(limit) + ", the error message is:" + error_message)

        # delete these learning plan at last
        if is_user_plan:
            delete_response = learning_plan_service.delete_user_plan(learning_plan_template)
        else:
            delete_response = learning_plan_service.delete_partition_plan(learning_plan_template)
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
                    LearningCommonUtils.get_expected_learning_data_from_db_by_limit_page(learning_plan_list_from_db,
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
            delete_response = learning_plan_service.delete_partition_plan(learning_plan_template)
        assert_that(delete_response.status_code == 200)

    @Test(tags="qa")
    def test_get_partition_plan_without_limit_page_less_than_50(self):
        batch_number = random.randint(1, 30)
        self.test_get_plan_without_limit_page(batch_number, False)

    # when there's more than 50 records in the DB, get API will by default get 50 records
    @Test(tags="qa")
    def test_get_partition_plan_without_limit_page_larger_than_50(self):
        batch_number = 51
        self.test_get_plan_without_limit_page(batch_number, False)

    @Test(tags="qa")
    def test_get_user_plan_without_limit_page_less_than_50(self):
        batch_number = random.randint(1, 30)
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
        batch_number = random.randint(10, 30)
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
            delete_response = learning_plan_service.delete_partition_plan(learning_plan_template)

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
        batch_number = random.randint(10, 30)
        self.test_delete_user_partition_plan(batch_number, False)

    @Test(tags="qa")
    def test_delete_user_plan(self):
        batch_number = random.randint(10, 30)
        self.test_delete_user_partition_plan(batch_number, True)

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

    # called by update related cases, with valid values
    def test_learning_plan_update_valid_values(self, field_value_type, is_only_required=False):
        learning_plan_service = LearningPlanService(LEARNING_PLAN_ENVIRONMENT)
        # prepare learning plan first
        learning_plan = LearningPlanUtils.construct_random_valid_learning_plan(False)
        learning_plan_insert_api_response = learning_plan_service.post_learning_plan_insert(learning_plan)
        assert_that(learning_plan_insert_api_response.status_code == 200)

        # construct a update learning plan, it have same product_id, plan_business_key, bucket_id, student_key, system_key with original plan
        learning_plan_update = \
            LearningPlanUtils.construct_learning_plan_by_template_and_is_only_required(learning_plan, field_value_type,
                                                                                       is_only_required)

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

    # test learning plan update API with valid required fields
    # For update behavior, the product_id, plan_business_key, bucket_id, student_key, system_key are the primary key
    @Test(tags="qa")
    def test_learning_plan_update_valid_required_fields(self):
        self.test_learning_plan_update_valid_values(FieldValueType.Valid, True)

    @Test(tags="qa")
    def test_learning_plan_update_valid_all_fields(self):
        self.test_learning_plan_update_valid_values(FieldValueType.Valid, False)

    @Test(tags="qa")
    def test_learning_plan_update_valid_min(self):
        self.test_learning_plan_update_valid_values(FieldValueType.Min)

    @Test(tags="qa")
    def test_learning_plan_update_valid_max(self):
        self.test_learning_plan_update_valid_values(FieldValueType.Max)

    @Test(tags="qa")
    def test_learning_plan_update_not_exist_record(self):
        learning_plan_service = LearningPlanService(LEARNING_PLAN_ENVIRONMENT)
        # prepare learning plan first
        learning_plan = LearningPlanUtils.construct_random_valid_learning_plan(False)
        learning_plan_insert_api_response = learning_plan_service.post_learning_plan_insert(learning_plan)
        assert_that(learning_plan_insert_api_response.status_code == 200)

        # construct a update learning plan, it have same product_id, plan_business_key, bucket_id, student_key, system_key with original plan
        learning_plan_update = \
            LearningPlanUtils.construct_learning_plan_by_template(learning_plan, FieldValueType.Valid)
        # make the record not exist in DB
        learning_plan_update.student_key = learning_plan_update.student_key + '|updateTest'

        learning_plan_update_api_response = learning_plan_service.put_learning_plan(learning_plan_update)
        assert_that(learning_plan_update_api_response.status_code == 200)
        # verify the update API return response
        assert_that(learning_plan_update_api_response.json() is False, "update API should return false!")

        # delete this specific learning plan at last
        delete_response = learning_plan_service.delete_specific_plan(learning_plan)
        assert_that(delete_response.status_code == 200)

    # test when all the fields is null for insert and update APIs
    @Test(tags="qa")
    def test_learning_plan_insert_update_null_values(self):
        # all the filed value as null
        learning_plan = LearningPlanEntity(None, None, None, None)
        self.call_learning_plan_api_and_verify_errors(learning_plan, LearningPlanAPIType.TypeInsert)
        self.call_learning_plan_api_and_verify_errors(learning_plan, LearningPlanAPIType.TypeUpdate)

    # test when all the fields is empty for insert and update APIs
    @Test(tags="qa")
    def test_learning_plan_insert_update_empty_values(self):
        # all the filed value as empty
        learning_plan = LearningPlanUtils.construct_learning_plan_with_empty_fields()
        self.call_learning_plan_api_and_verify_errors(learning_plan, LearningPlanAPIType.TypeInsert)
        self.call_learning_plan_api_and_verify_errors(learning_plan, LearningPlanAPIType.TypeUpdate)

    # insert API with value below min for insert and update APIs
    @Test(tags="qa")
    def test_learning_plan_insert_update_invalid_value_below_min(self):
        # all the filed value below min
        learning_plan = LearningPlanUtils.construct_learning_plan_by_value_type(FieldValueType.BelowMin)
        self.call_learning_plan_api_and_verify_errors(learning_plan, LearningPlanAPIType.TypeInsert)
        self.call_learning_plan_api_and_verify_errors(learning_plan, LearningPlanAPIType.TypeUpdate)

    # insert API with value exceed max for insert and update APIs
    @Test(tags="qa")
    def test_learning_plan_insert_update_invalid_value_exceed_max(self):
        # all the filed value exceed max
        learning_plan = LearningPlanUtils.construct_learning_plan_by_value_type(FieldValueType.ExceedMax)
        self.call_learning_plan_api_and_verify_errors(learning_plan, LearningPlanAPIType.TypeInsert)
        self.call_learning_plan_api_and_verify_errors(learning_plan, LearningPlanAPIType.TypeUpdate)

    @Test(tags="qa")
    def test_learning_plan_batch_insert_single_plan_null_values(self):
        # all the filed value as null
        learning_plan = LearningPlanEntity(None, None, None, None)
        learning_plan_list = [learning_plan]

        self.call_learning_plan_api_and_verify_errors(learning_plan_list, LearningPlanAPIType.TypeBatchInsert)

    @Test(tags="qa")
    def test_learning_plan_batch_insert_single_plan_empty_values(self):
        # all the filed value as empty
        learning_plan = LearningPlanUtils.construct_learning_plan_with_empty_fields()
        learning_plan_list = [learning_plan]

        self.call_learning_plan_api_and_verify_errors(learning_plan_list, LearningPlanAPIType.TypeBatchInsert)

    # @Test(tags="qa")
    # def test_learning_plan_batch_insert_multiple_plan_null_empty_values(self):
    #     # all the filed value as null
    #     learning_plan_null = LearningPlanEntity(None, None, None, None)
    #     # all the filed value as empty
    #     learning_plan_empty = LearningPlanUtils.construct_learning_plan_with_empty_fields()
    #     learning_plan_list = [learning_plan_null, learning_plan_empty]
    #
    #     self.call_learning_plan_api_and_verify_errors(learning_plan_list, LearningPlanAPIType.TypeBatchInsert)

    # batch insert API with value below min
    @Test(tags="qa")
    def test_learning_plan_batch_insert_multiple_invalid_below_min(self):
        batch_number = random.randint(5, 10)
        learning_plan_list = \
            LearningPlanUtils.construct_multiple_plans_by_template_and_value_type(None, FieldValueType.BelowMin,
                                                                                  batch_number, False)

        self.call_learning_plan_api_and_verify_errors(learning_plan_list, LearningPlanAPIType.TypeBatchInsert)

    # batch insert API with value exceed max
    @Test(tags="qa")
    def test_learning_plan_batch_insert_multiple_invalid_exceed_max(self):
        batch_number = random.randint(5, 10)
        learning_plan_list = \
            LearningPlanUtils.construct_multiple_plans_by_template_and_value_type(None, FieldValueType.ExceedMax,
                                                                                  batch_number, False)

        self.call_learning_plan_api_and_verify_errors(learning_plan_list, LearningPlanAPIType.TypeBatchInsert)

    # batch insert data with different invalid values, null, empty, below min, exceed max
    @Test(tags="qa")
    def test_learning_plan_batch_insert_multiple_invalid_combination(self):
        # all the filed value as null
        learning_plan_null = LearningPlanEntity(None, None, None, None)
        # all the filed value as empty
        learning_plan_empty = LearningPlanUtils.construct_learning_plan_with_empty_fields()
        # all the filed value below min
        learning_plan_below_min = LearningPlanUtils.construct_learning_plan_by_value_type(FieldValueType.BelowMin)
        # all the filed value exceed max
        learning_plan_exceed_max = LearningPlanUtils.construct_learning_plan_by_value_type(FieldValueType.ExceedMax)
        learning_plan_list = [learning_plan_null, learning_plan_empty, learning_plan_below_min, learning_plan_exceed_max]

        self.call_learning_plan_api_and_verify_errors(learning_plan_list, LearningPlanAPIType.TypeBatchInsert)


    # common method which is called by test cases, for data with invalid values, call the API and verify errors
    def call_learning_plan_api_and_verify_errors(self, learning_plans, learning_plan_api_type):
        learning_plan_service = LearningPlanService(LEARNING_PLAN_ENVIRONMENT)

        if learning_plan_api_type == LearningPlanAPIType.TypeInsert:
            learning_plan_api_response = learning_plan_service.post_learning_plan_insert(learning_plans)
        elif learning_plan_api_type == LearningPlanAPIType.TypeBatchInsert:
            learning_plan_api_response = learning_plan_service.post_learning_plan_batch_insert(learning_plans)
        elif learning_plan_api_type == LearningPlanAPIType.TypeUpdate:
            learning_plan_api_response = learning_plan_service.put_learning_plan(learning_plans)

        assert_that(learning_plan_api_response.status_code == 400)

        error_message = \
            LearningPlanUtils.verify_insert_put_error_messages_by_api_type(learning_plan_api_response.json(),
                                                                           learning_plans, learning_plan_api_type)

        assert_that(error_message == '', error_message)

    # test the batch insert API with different partition
    @Test(tags="qa")
    def test_learning_plan_batch_insert_invalid_different_partition(self):
        learning_plan_service = LearningPlanService(LEARNING_PLAN_ENVIRONMENT)

        # create some items with same partition
        learning_plan_template = LearningPlanUtils.construct_learning_plan_template(False)
        # construct valid learning plan list
        batch_number = random.randint(5, 10)
        learning_plan_list = \
            LearningPlanUtils.construct_multiple_valid_learning_plans(learning_plan_template, batch_number)

        learning_plan_different_partition = LearningPlanUtils.construct_random_valid_learning_plan(False)

        learning_plan_list.append(learning_plan_different_partition)

        # call learning plan batch insert api
        learning_plan_batch_insert_api_response = \
            learning_plan_service.post_learning_plan_batch_insert(learning_plan_list)

        assert_that(learning_plan_batch_insert_api_response.status_code == 409)

    # test when product_id/bucket_id/plan_business_key is empty for all the query/delete APIs
    @Test(tags="qa")
    def test_get_delete_api_with_empty_value(self):
        learning_plan_service = LearningPlanService(LEARNING_PLAN_ENVIRONMENT)

        learning_plan_template = LearningPlanUtils.construct_learning_plan_template(True)
        learning_plan_template.system_key = uuid.uuid1()

        query_fields = ['product_id', 'bucket_id', 'plan_business_key']

        for field_name in query_fields:
            original_value = getattr(learning_plan_template, field_name)
            setattr(learning_plan_template, field_name, '')

            # for all the get APIs
            learning_plan_api_response = learning_plan_service.get_partition_plan_without_limit_page(
                learning_plan_template)
            assert_that(learning_plan_api_response.status_code == 404)

            learning_plan_api_response = learning_plan_service.get_partition_plan_with_limit(
                learning_plan_template, 2)
            assert_that(learning_plan_api_response.status_code == 404)

            learning_plan_api_response = learning_plan_service.get_partition_plan_with_limit_page(
                learning_plan_template, 2, 1)
            assert_that(learning_plan_api_response.status_code == 404)

            learning_plan_api_response = learning_plan_service.get_user_plan_without_limit_page(
                learning_plan_template)
            assert_that(learning_plan_api_response.status_code == 404)

            learning_plan_api_response = learning_plan_service.get_user_plan_with_limit(
                learning_plan_template, 2)
            assert_that(learning_plan_api_response.status_code == 404)

            learning_plan_api_response = learning_plan_service.get_user_plan_with_limit_page(
                learning_plan_template, 2, 1)
            assert_that(learning_plan_api_response.status_code == 404)

            learning_plan_api_response = learning_plan_service.get_specific_plan(learning_plan_template)
            assert_that(learning_plan_api_response.status_code == 404)

            # for all the delete APIs
            learning_plan_api_response = learning_plan_service.delete_partition_plan(
                learning_plan_template)
            assert_that(learning_plan_api_response.status_code == 404)

            learning_plan_api_response = learning_plan_service.delete_user_plan(
                learning_plan_template)
            assert_that(learning_plan_api_response.status_code == 404)

            learning_plan_api_response = learning_plan_service.delete_specific_plan(
                learning_plan_template)
            assert_that(learning_plan_api_response.status_code == 404)

            setattr(learning_plan_template, field_name, original_value)

    # this method can be called by test case
    def assert_api_response_with_invalid_format_for_int(self, get_api_response, field_value):
        assert_that(get_api_response.status_code == 400)
        expected_message = "Failed to convert value of type 'java.lang.String' to required type 'int'; nested exception is java.lang.NumberFormatException: For input string: \"{0}\"".format(
            field_value)
        assert_that(get_api_response.json()['message'].find('expected_message'),
                    expected_message + " can't be found in message")

    # called by cases, test when product_id/bucket_id value is not int or exceed int's max value
    def test_get_delete_api_with_invalid_int_field(self, invalid_value):
        learning_plan_service = LearningPlanService(LEARNING_PLAN_ENVIRONMENT)

        learning_plan_template = LearningPlanUtils.construct_learning_plan_template(True)
        learning_plan_template.system_key = uuid.uuid1()

        query_fields = ['product_id', 'bucket_id']

        for field_name in query_fields:
            original_value = getattr(learning_plan_template, field_name)
            # invalid_value = ''.join(random.sample(string.ascii_letters, 5))
            setattr(learning_plan_template, field_name, invalid_value)

            # for all the get APIs
            learning_plan_api_response = learning_plan_service.get_partition_plan_without_limit_page(
                learning_plan_template)
            self.assert_api_response_with_invalid_format_for_int(learning_plan_api_response, invalid_value)

            learning_plan_api_response = \
                learning_plan_service.get_partition_plan_with_limit(learning_plan_template, 2)
            self.assert_api_response_with_invalid_format_for_int(learning_plan_api_response, invalid_value)

            learning_plan_api_response = \
                learning_plan_service.get_partition_plan_with_limit_page(learning_plan_template, 2, 1)
            self.assert_api_response_with_invalid_format_for_int(learning_plan_api_response, invalid_value)

            learning_plan_api_response = learning_plan_service.get_user_plan_without_limit_page(
                learning_plan_template)
            self.assert_api_response_with_invalid_format_for_int(learning_plan_api_response, invalid_value)

            learning_plan_api_response = learning_plan_service.get_user_plan_with_limit(
                learning_plan_template, 2)
            self.assert_api_response_with_invalid_format_for_int(learning_plan_api_response, invalid_value)

            learning_plan_api_response = learning_plan_service.get_user_plan_with_limit_page(
                learning_plan_template, 2, 1)
            self.assert_api_response_with_invalid_format_for_int(learning_plan_api_response, invalid_value)

            learning_plan_api_response = learning_plan_service.get_specific_plan(learning_plan_template)
            self.assert_api_response_with_invalid_format_for_int(learning_plan_api_response, invalid_value)

            # for all the delete APIs
            learning_plan_api_response = learning_plan_service.delete_partition_plan(
                learning_plan_template)
            self.assert_api_response_with_invalid_format_for_int(learning_plan_api_response, invalid_value)

            learning_plan_api_response = learning_plan_service.delete_user_plan(
                learning_plan_template)
            self.assert_api_response_with_invalid_format_for_int(learning_plan_api_response, invalid_value)

            learning_plan_api_response = learning_plan_service.delete_specific_plan(
                learning_plan_template)
            self.assert_api_response_with_invalid_format_for_int(learning_plan_api_response, invalid_value)

            setattr(learning_plan_template, field_name, original_value)

    # test when product_id/bucket_id value is not int
    @Test(tags="qa")
    def test_get_delete_api_with_invalid_format_int_field(self):
        invalid_format_int_value = ''.join(random.sample(string.ascii_letters, 5))
        self.test_get_delete_api_with_invalid_int_field(invalid_format_int_value)

    # test when product_id/bucket_id value exceed int max value
    @Test(tags="qa")
    def test_get_delete_api_with_exceed_max_int_field(self):
        exceed_max_int_value = 2147483648
        self.test_get_delete_api_with_invalid_int_field(exceed_max_int_value)

    # test when limit/page value is not int
    @Test(tags="qa")
    def test_get_api_with_invalid_format_limit_page(self):
        learning_plan_service = LearningPlanService(LEARNING_PLAN_ENVIRONMENT)

        learning_plan_template = LearningPlanUtils.construct_learning_plan_template(True)

        query_param = ['limit', 'page']

        for param in query_param:
            invalid_value = ''.join(random.sample(string.ascii_letters, 5))

            limit = 1
            page = 1

            if param == 'limit':
                limit = invalid_value
            else:
                page = invalid_value

            if param == 'limit':
                learning_plan_api_response = \
                    learning_plan_service.get_partition_plan_with_limit(learning_plan_template, limit)
                self.assert_api_response_with_invalid_format_for_int(learning_plan_api_response, invalid_value)

            learning_plan_api_response = \
                learning_plan_service.get_partition_plan_with_limit_page(learning_plan_template, limit, page)
            self.assert_api_response_with_invalid_format_for_int(learning_plan_api_response, invalid_value)

            if param == 'limit':
                learning_plan_api_response = learning_plan_service.get_user_plan_with_limit(learning_plan_template,
                                                                                            limit)
                self.assert_api_response_with_invalid_format_for_int(learning_plan_api_response, invalid_value)

            learning_plan_api_response = learning_plan_service.get_user_plan_with_limit_page(learning_plan_template,
                                                                                             limit, page)
            self.assert_api_response_with_invalid_format_for_int(learning_plan_api_response, invalid_value)

            # set the param back to default one
            if param == 'limit':
                limit = 1
            else:
                page = 1

    # test when limit value is not allowed int value, that is, below 1, exceed 50
    @Test(tags="qa")
    def test_get_api_with_invalid_value_limit(self):
        learning_plan_service = LearningPlanService(LEARNING_PLAN_ENVIRONMENT)

        learning_plan_template = LearningPlanUtils.construct_learning_plan_template(True)

        limit_list = [0, random.randint(-10, 0), 51, random.randint(52, 60)]

        for limit in limit_list:
            learning_plan_api_response = \
                learning_plan_service.get_partition_plan_with_limit(learning_plan_template, limit)
            assert_that(learning_plan_api_response.status_code == 400)

            learning_plan_api_response = \
                learning_plan_service.get_partition_plan_with_limit_page(learning_plan_template, limit, 1)
            assert_that(learning_plan_api_response.status_code == 400)

            learning_plan_api_response = \
                learning_plan_service.get_user_plan_with_limit(learning_plan_template, limit)
            assert_that(learning_plan_api_response.status_code == 400)

            learning_plan_api_response = \
                learning_plan_service.get_user_plan_with_limit_page(learning_plan_template, limit, 1)
            assert_that(learning_plan_api_response.status_code == 400)

    # test when page value is not allowed int value, that is, below 1
    @Test(tags="qa")
    def test_get_api_with_invalid_value_page(self):
        learning_plan_service = LearningPlanService(LEARNING_PLAN_ENVIRONMENT)

        learning_plan_template = LearningPlanUtils.construct_learning_plan_template(True)

        page_list = [0, random.randint(-10, 0)]

        for page in page_list:
            learning_plan_api_response = \
                learning_plan_service.get_partition_plan_with_limit_page(learning_plan_template, 1, page)
            assert_that(learning_plan_api_response.status_code == 400)

            learning_plan_api_response = \
                learning_plan_service.get_user_plan_with_limit_page(learning_plan_template, 1, page)
            assert_that(learning_plan_api_response.status_code == 400)

    # test when there's no record can be found with the param
    @Test(tags="qa")
    def test_get_delete_api_with_not_existing_record(self):
        learning_plan_service = LearningPlanService(LEARNING_PLAN_ENVIRONMENT)

        learning_plan = LearningPlanUtils.construct_learning_plan_template(True)
        learning_plan.system_key = uuid.uuid1()

        # test the get APIs
        learning_plan_api_response = learning_plan_service.get_partition_plan_without_limit_page(
            learning_plan)
        assert_that(learning_plan_api_response.status_code == 200)
        assert_that(len(learning_plan_api_response.json()) == 0)

        learning_plan_api_response = learning_plan_service.get_partition_plan_with_limit(
            learning_plan, 10)
        assert_that(learning_plan_api_response.status_code == 200)
        assert_that(len(learning_plan_api_response.json()) == 0)

        learning_plan_api_response = learning_plan_service.get_partition_plan_with_limit_page(
            learning_plan, 10, 1)
        assert_that(learning_plan_api_response.status_code == 200)
        assert_that(len(learning_plan_api_response.json()) == 0)

        learning_plan_api_response = learning_plan_service.get_user_plan_without_limit_page(
            learning_plan)
        assert_that(learning_plan_api_response.status_code == 200)
        assert_that(len(learning_plan_api_response.json()) == 0)

        learning_plan_api_response = learning_plan_service.get_user_plan_with_limit(
            learning_plan, 10)
        assert_that(learning_plan_api_response.status_code == 200)
        assert_that(len(learning_plan_api_response.json()) == 0)

        learning_plan_api_response = learning_plan_service.get_user_plan_with_limit_page(
            learning_plan, 10, 1)
        assert_that(learning_plan_api_response.status_code == 200)
        assert_that(len(learning_plan_api_response.json()) == 0)

        learning_plan_api_response = learning_plan_service.get_specific_plan(learning_plan)
        assert_that(learning_plan_api_response.status_code == 200)
        assert_that(len(learning_plan_api_response.json()) == 0)

        # test the delete APIs
        learning_plan_api_response = learning_plan_service.delete_partition_plan(learning_plan)
        assert_that(learning_plan_api_response.status_code == 200)
        assert_that(learning_plan_api_response.json() is True)

        learning_plan_api_response = learning_plan_service.delete_user_plan(learning_plan)
        assert_that(learning_plan_api_response.status_code == 200)
        assert_that(learning_plan_api_response.json() is True)

        learning_plan_api_response = learning_plan_service.delete_specific_plan(learning_plan)
        assert_that(learning_plan_api_response.status_code == 200)
        assert_that(learning_plan_api_response.json() is True)

    # called by other methods
    def verify_api_result_with_db(self, api_response, learning_plan_list_from_db, limit=None, page=None):
        assert_that(api_response.status_code == 200)

        expected_learning_plan_list_from_db = \
            LearningCommonUtils.get_expected_learning_data_from_db_by_limit_page(learning_plan_list_from_db,
                                                                                 limit, page)

        error_message = LearningCommonUtils. \
            verify_learning_get_api_data_with_db(api_response.json(),
                                                 expected_learning_plan_list_from_db)
        assert_that(error_message == '', "When limit is:" + str(limit) + "page is:" + str(page)
                    + ",the error message is:" + error_message)

    # called by other methods, to test the get user plan APIs with empty student key
    def test_get_user_plan_with_empty_student_key(self, batch_number, limit_page_list):
        learning_plan_service = LearningPlanService(LEARNING_PLAN_ENVIRONMENT)

        # batch insert need the whole batch have same partition,that means,need same product_id plan_business_key and bucket_id
        # user plan need student key
        learning_plan_template = LearningPlanUtils.construct_learning_plan_template(True)
        # construct valid learning plan list
        learning_plan_list_1 = LearningPlanUtils.construct_multiple_valid_learning_plans(learning_plan_template,
                                                                                         batch_number)
        #create some different student_key learning plans
        learning_plan_template.student_key = learning_plan_template.student_key + '|Update'
        learning_plan_list_2 = LearningPlanUtils.construct_multiple_valid_learning_plans(learning_plan_template,
                                                                                         10)
        learning_plan_list = learning_plan_list_1 + learning_plan_list_2
        partition_plan_number = batch_number + 10

        # call learning plan batch insert api
        learning_plan_batch_insert_api_response = \
            learning_plan_service.post_learning_plan_batch_insert(learning_plan_list)
        assert_that(learning_plan_batch_insert_api_response.status_code == 200)

        # when student_key param is empty, the result will be same as it get by partition
        learning_plan_list_from_db = LearningDBUtils.get_partition_plan(learning_plan_template)
        assert_that(len(learning_plan_list_from_db) == partition_plan_number,
                    'Length of Learning plan list you got from DB not as expected!')

        learning_plan_with_empty_student_key = learning_plan_template
        learning_plan_with_empty_student_key.student_key = ''

        if limit_page_list is None:
            learning_plan_get_api_response = \
                learning_plan_service.get_user_plan_without_limit_page(learning_plan_with_empty_student_key)
            self.verify_api_result_with_db(learning_plan_get_api_response, learning_plan_list_from_db)
        else:
            for limit_page in limit_page_list:
                limit = limit_page['limit']
                page_list = limit_page['page']

                if page_list is None:
                    learning_plan_get_api_response = \
                        learning_plan_service.get_user_plan_with_limit(learning_plan_with_empty_student_key, limit)
                    self.verify_api_result_with_db(learning_plan_get_api_response, learning_plan_list_from_db, limit)
                else:
                    for page in page_list:
                        learning_plan_get_api_response = \
                            learning_plan_service.get_user_plan_with_limit_page(learning_plan_with_empty_student_key,
                                                                                limit, page)

                        self.verify_api_result_with_db(learning_plan_get_api_response,
                                                       learning_plan_list_from_db, limit, page)

        # delete these learning plan at last
        delete_response = learning_plan_service.delete_partition_plan(learning_plan_template)
        assert_that(delete_response.status_code == 200)

    # test get user plan with empty student_key without limit and page
    @Test(tags="qa")
    def test_get_user_plan_with_empty_student_key_without_limit_page(self):
        batch_number = random.randint(10, 30)
        self.test_get_user_plan_with_empty_student_key(batch_number, None)

    # test get user plan with empty student_key with limit
    @Test(tags="qa")
    def test_get_user_plan_with_empty_student_key_with_limit(self):
        batch_number = random.randint(10, 30)
        # there will be 10 learning plans with other student_key value
        partition_batch_number = batch_number + 10
        limit_1 = random.randint(1, batch_number-1)
        # there will be 10 learning plans with other student_key value
        limit_2 = random.randint(batch_number, partition_batch_number-1)
        limit_3 = partition_batch_number
        limit_4 = random.randint(partition_batch_number + 1, 50)
        limit_page_list = [{'limit': limit_1, 'page': None},
                           {'limit': limit_2, 'page': None},
                           {'limit': limit_3, 'page': None},
                           {'limit': limit_4, 'page': None},
                           {'limit': None, 'page': None}]

        self.test_get_user_plan_with_empty_student_key(batch_number, limit_page_list)

    # test get user plan with empty student_key with limit and page
    @Test(tags="qa")
    def test_get_user_plan_with_empty_student_key_with_limit_page(self):
        batch_number = random.randint(11, 30)
        # there will be 10 learning plans with other student_key value
        partition_batch_number = batch_number + 10
        limit_1 = random.randint(1, 9)
        limit_2 = random.randint(10, batch_number-1)
        limit_3 = random.randint(batch_number, partition_batch_number-1)
        limit_4 = partition_batch_number
        limit_page_list = [{'limit': limit_1,
                            'page': [random.randint(1, partition_batch_number // limit_1),
                                     random.randint(partition_batch_number // limit_1 + 1, 50),
                                     None]},
                           {'limit': limit_2,
                            'page': [random.randint(1, partition_batch_number // limit_2),
                                     random.randint(partition_batch_number // limit_2 + 1, 50),
                                     None]},
                           {'limit': limit_3,
                            'page': [random.randint(1, partition_batch_number // limit_3),
                                     random.randint(partition_batch_number // limit_3 + 1, 50),
                                     None]},
                           {'limit': limit_4,
                            'page': [1, random.randint(2, 10), None]},
                           {'limit': None, 'page': [None]}]
        self.test_get_user_plan_with_empty_student_key(batch_number, limit_page_list)

    # called by other methods, to test the get specific plan API with empty student key, empty/invalid system key
    def test_get_specific_plan_with_empty_invalid_key(self, student_key, system_key):
        learning_plan_service = LearningPlanService(LEARNING_PLAN_ENVIRONMENT)
        batch_number = random.randint(2, 10)

        # batch insert need the whole batch have same partition,that means,need same product_id plan_business_key and bucket_id
        # user plan need student key
        learning_plan_template = LearningPlanUtils.construct_learning_plan_template(True)
        # construct valid learning plan list
        learning_plan_list_1 = LearningPlanUtils.construct_multiple_valid_learning_plans(learning_plan_template,
                                                                                         batch_number)
        learning_plan_list = learning_plan_list_1
        #create some different student_key learning plans
        if student_key == '':
            learning_plan_template.student_key = learning_plan_template.student_key + '|Update'
            learning_plan_list_2 = LearningPlanUtils.construct_multiple_valid_learning_plans(learning_plan_template,
                                                                                             10)
            learning_plan_list = learning_plan_list + learning_plan_list_2
            partition_plan_number = batch_number + 10

        # call learning plan batch insert api
        learning_plan_batch_insert_api_response = \
            learning_plan_service.post_learning_plan_batch_insert(learning_plan_list)
        assert_that(learning_plan_batch_insert_api_response.status_code == 200)

        # get the first learning plan as to test get specific plan
        learning_plan_with_empty_invalid_key = learning_plan_list[0]

        if student_key == '':
            # when student_key param is empty, the result will be same as it get by partition
            learning_plan_list_from_db = LearningDBUtils.get_partition_plan(learning_plan_template)
            assert_that(len(learning_plan_list_from_db) == partition_plan_number,
                        'Length of Learning plan list you got from DB not as expected!')
            learning_plan_with_empty_invalid_key.student_key = student_key
        elif system_key is not None:
            # when system_key is empty or invalid, it will return all the result with productid, bucketid, planbusinesskey, studentkey params
            learning_plan_list_from_db = LearningDBUtils.get_user_plan(learning_plan_template)
            assert_that(len(learning_plan_list_from_db) == batch_number,
                        'Length of Learning plan list you got from DB not as expected!')
            learning_plan_with_empty_invalid_key.system_key = system_key

        learning_plan_get_api_response = \
            learning_plan_service.get_specific_plan(learning_plan_with_empty_invalid_key)
        self.verify_api_result_with_db(learning_plan_get_api_response, learning_plan_list_from_db)

        # delete these learning plan at last
        delete_response = learning_plan_service.delete_partition_plan(learning_plan_template)
        assert_that(delete_response.status_code == 200)

    # test get specific plan with empty student_key, but with valid system_key
    @Test(tags="qa")
    def test_get_specific_plan_with_empty_student_key(self):
        self.test_get_specific_plan_with_empty_invalid_key('', None)

    # test get specific plan with empty system_key, but with valid student_key
    @Test(tags="qa")
    def test_get_specific_plan_with_empty_system_key(self):
        self.test_get_specific_plan_with_empty_invalid_key(None, '')

    # test get specific plan with invalid system_key, not UUID format, but with valid student_key, with HF-285 for this
    @Test(tags="qa")
    def test_get_specific_plan_with_invalid_system_key(self):
        self.test_get_specific_plan_with_empty_invalid_key(None, ''.join(random.sample(string.ascii_letters, 5)))

    # test when student_key , plan_business_key with invalid format
    @Test(tags="qa")
    def test_get_delete_api_with_invalid_business_student_key(self):
        learning_plan_service = LearningPlanService(LEARNING_PLAN_ENVIRONMENT)

        learning_plan = LearningPlanUtils.construct_random_valid_learning_plan(False)
        learning_plan_insert_api_response = learning_plan_service.post_learning_plan_insert(learning_plan)
        assert_that(learning_plan_insert_api_response.status_code == 200)

        query_fields = ['plan_business_key', 'student_key']

        for field_name in query_fields:
            original_value = getattr(learning_plan, field_name)
            # these values was not allowed in student_key and plan_business_key
            not_allowable_format = '^*<>!{}'
            invalid_field_value = original_value + not_allowable_format
            setattr(learning_plan, field_name, invalid_field_value)

            if field_name == 'plan_business_key':
                learning_plan_api_response = learning_plan_service.get_partition_plan_without_limit_page(
                    learning_plan)
                assert_that(learning_plan_api_response.status_code == 200)
                assert_that(len(learning_plan_api_response.json()) == 0)

                learning_plan_api_response = learning_plan_service.get_partition_plan_with_limit(
                    learning_plan, 10)
                assert_that(learning_plan_api_response.status_code == 200)
                assert_that(len(learning_plan_api_response.json()) == 0)

                learning_plan_api_response = learning_plan_service.get_partition_plan_with_limit_page(
                    learning_plan, 10, 1)
                assert_that(learning_plan_api_response.status_code == 200)
                assert_that(len(learning_plan_api_response.json()) == 0)

            learning_plan_api_response = learning_plan_service.get_user_plan_without_limit_page(
                learning_plan)
            assert_that(learning_plan_api_response.status_code == 200)
            assert_that(len(learning_plan_api_response.json()) == 0)

            learning_plan_api_response = learning_plan_service.get_user_plan_with_limit(
                learning_plan, 10)
            assert_that(learning_plan_api_response.status_code == 200)
            assert_that(len(learning_plan_api_response.json()) == 0)

            learning_plan_api_response = learning_plan_service.get_user_plan_with_limit_page(
                learning_plan, 10, 1)
            assert_that(learning_plan_api_response.status_code == 200)
            assert_that(len(learning_plan_api_response.json()) == 0)

            learning_plan_api_response = learning_plan_service.get_specific_plan(learning_plan)
            assert_that(learning_plan_api_response.status_code == 200)
            assert_that(len(learning_plan_api_response.json()) == 0)

            # test the delete APIs
            if field_name == 'plan_business_key':
                learning_plan_api_response = learning_plan_service.delete_partition_plan(learning_plan)
                assert_that(learning_plan_api_response.status_code == 200)
                assert_that(learning_plan_api_response.json() is True)

            learning_plan_api_response = learning_plan_service.delete_user_plan(learning_plan)
            assert_that(learning_plan_api_response.status_code == 200)
            assert_that(learning_plan_api_response.json() is True)

            learning_plan_api_response = learning_plan_service.delete_specific_plan(learning_plan)
            assert_that(learning_plan_api_response.status_code == 200)
            assert_that(learning_plan_api_response.json() is True)

            setattr(learning_plan, field_name, original_value)

        # delete this specific learning plan at last
        delete_response = learning_plan_service.delete_specific_plan(learning_plan)
        assert_that(delete_response.status_code == 200)

    # test when student_key , plan_business_key with value exceed the allowed
    @Test(tags="qa")
    def test_get_delete_api_with_business_student_key_value_exceed_max(self):
        learning_plan_service = LearningPlanService(LEARNING_PLAN_ENVIRONMENT)

        # with this construction, those two fields already have the value exceed the max they allowed
        learning_plan = LearningPlanUtils.construct_learning_plan_by_value_type(FieldValueType.ExceedMax)
        learning_plan.system_key = uuid.uuid1()

        query_fields = ['plan_business_key', 'student_key']

        for field_name in query_fields:
            if field_name == 'plan_business_key':
                learning_plan_api_response = learning_plan_service.get_partition_plan_without_limit_page(
                    learning_plan)
                assert_that(learning_plan_api_response.status_code == 200)
                assert_that(len(learning_plan_api_response.json()) == 0)

                learning_plan_api_response = learning_plan_service.get_partition_plan_with_limit(
                    learning_plan, 10)
                assert_that(learning_plan_api_response.status_code == 200)
                assert_that(len(learning_plan_api_response.json()) == 0)

                learning_plan_api_response = learning_plan_service.get_partition_plan_with_limit_page(
                    learning_plan, 10, 1)
                assert_that(learning_plan_api_response.status_code == 200)
                assert_that(len(learning_plan_api_response.json()) == 0)

            learning_plan_api_response = learning_plan_service.get_user_plan_without_limit_page(
                learning_plan)
            assert_that(learning_plan_api_response.status_code == 200)
            assert_that(len(learning_plan_api_response.json()) == 0)

            learning_plan_api_response = learning_plan_service.get_user_plan_with_limit(
                learning_plan, 10)
            assert_that(learning_plan_api_response.status_code == 200)
            assert_that(len(learning_plan_api_response.json()) == 0)

            learning_plan_api_response = learning_plan_service.get_user_plan_with_limit_page(
                learning_plan, 10, 1)
            assert_that(learning_plan_api_response.status_code == 200)
            assert_that(len(learning_plan_api_response.json()) == 0)

            learning_plan_api_response = learning_plan_service.get_specific_plan(learning_plan)
            assert_that(learning_plan_api_response.status_code == 200)
            assert_that(len(learning_plan_api_response.json()) == 0)

            # test the delete APIs
            if field_name == 'plan_business_key':
                learning_plan_api_response = learning_plan_service.delete_partition_plan(learning_plan)
                assert_that(learning_plan_api_response.status_code == 200)
                assert_that(learning_plan_api_response.json() is False)

            learning_plan_api_response = learning_plan_service.delete_user_plan(learning_plan)
            assert_that(learning_plan_api_response.status_code == 200)
            assert_that(learning_plan_api_response.json() is False)

            learning_plan_api_response = learning_plan_service.delete_specific_plan(learning_plan)
            assert_that(learning_plan_api_response.status_code == 200)
            assert_that(learning_plan_api_response.json() is False)

            # set the field back to valid value to not impact the next field validation
            setattr(learning_plan, field_name,
                    ''.join(random.choices(string.ascii_letters + string.digits + '|-', k=10)))

    # called by other methods, to test the delete plan API with empty student key, empty/invalid system key
    def test_delete_plan_with_empty_invalid_key(self, is_delete_user_plan, student_key, system_key):
        learning_plan_service = LearningPlanService(LEARNING_PLAN_ENVIRONMENT)
        batch_number = random.randint(2, 10)

        # batch insert need the whole batch have same partition,that means,need same product_id plan_business_key and bucket_id
        # user plan need student key
        learning_plan_template = LearningPlanUtils.construct_learning_plan_template(True)
        # construct valid learning plan list
        learning_plan_list_1 = LearningPlanUtils.construct_multiple_valid_learning_plans(learning_plan_template,
                                                                                         batch_number)
        learning_plan_list = learning_plan_list_1
        #create some different student_key learning plans
        if student_key == '':
            learning_plan_template.student_key = learning_plan_template.student_key + '|Update'
            second_batch_number = random.randint(2, 10)
            learning_plan_list_2 = LearningPlanUtils.construct_multiple_valid_learning_plans(learning_plan_template,
                                                                                             second_batch_number)
            learning_plan_list = learning_plan_list + learning_plan_list_2
            partition_plan_number = batch_number + second_batch_number

        # call learning plan batch insert api
        learning_plan_batch_insert_api_response = \
            learning_plan_service.post_learning_plan_batch_insert(learning_plan_list)
        assert_that(learning_plan_batch_insert_api_response.status_code == 200)

        # get the first learning plan to test the delete API
        learning_plan_with_empty_invalid_key = learning_plan_list[0]

        # check data before delete API
        if student_key == '':
            learning_plan_api_response = learning_plan_service.get_partition_plan_without_limit_page(learning_plan_template)
            assert_that(learning_plan_api_response.status_code == 200)
            assert_that(len(learning_plan_api_response.json()) == partition_plan_number,
                        'Length of Learning plan list you got from partition API not as expected!')
            learning_plan_with_empty_invalid_key.student_key = student_key
        elif system_key is not None:
            # when system_key is empty or invalid, it will return all the result with productid, bucketid, planbusinesskey, studentkey params
            learning_plan_api_response = learning_plan_service.get_user_plan_without_limit_page(learning_plan_template)
            assert_that(learning_plan_api_response.status_code == 200)
            assert_that(len(learning_plan_api_response.json()) == batch_number,
                        'Length of Learning plan list you got from user plan API not as expected!')
            learning_plan_with_empty_invalid_key.system_key = system_key

        # call delete APIs
        if is_delete_user_plan:
            learning_plan_delete_api_response = \
                learning_plan_service.delete_user_plan(learning_plan_with_empty_invalid_key)
        else:
            learning_plan_delete_api_response = \
                learning_plan_service.delete_specific_plan(learning_plan_with_empty_invalid_key)

        assert_that(learning_plan_delete_api_response.status_code == 200)

        # verify after the delete API
        if student_key == '':
            # when student_key is empty or invalid, delete API will delete all the result with productid, bucketid, planbusinesskey params
            learning_plan_api_response = learning_plan_service.get_partition_plan_without_limit_page(learning_plan_template)
            assert_that(learning_plan_api_response.status_code == 200)
            assert_that(len(learning_plan_api_response.json()) == 0,
                        'The get partition plan API should return empty after delete API!')
        elif system_key is not None:
            # when system_key is empty or invalid, delete API will delete all the result with productid, bucketid, planbusinesskey, studentkey params
            learning_plan_api_response = learning_plan_service.get_user_plan_without_limit_page(learning_plan_template)
            assert_that(learning_plan_api_response.status_code == 200)
            assert_that(len(learning_plan_api_response.json()) == 0,
                        'The get user plan API should return empty after delete API!')

    # test delete user plan with empty student key
    @Test(tags="qa")
    def test_delete_user_plan_with_empty_student_key(self):
        self.test_delete_plan_with_empty_invalid_key(True, '', None)

    # test delete specific plan with empty student key
    @Test(tags="qa")
    def test_delete_specific_plan_with_empty_student_key(self):
        self.test_delete_plan_with_empty_invalid_key(False, '', None)

    # test delete specific plan with empty system key
    @Test(tags="qa")
    def test_delete_specific_plan_with_empty_system_key(self):
        self.test_delete_plan_with_empty_invalid_key(False, None, '')

    # test delete specific plan with invalid system key
    @Test(tags="qa")
    def test_delete_specific_plan_with_invalid_system_key(self):
        self.test_delete_plan_with_empty_invalid_key(False, None, ''.join(random.sample(string.ascii_letters, 5)))

    # call learning plan api and verify the errors message for invalid date/int fields
    def call_api_and_verify_errors_for_invalid_date_int_fields(self, learning_plans, field_value, learning_plan_api_type,
                                                               is_check_date_type, is_exceed_int=False):
        learning_plan_service = LearningPlanService(LEARNING_PLAN_ENVIRONMENT)

        if learning_plan_api_type == LearningPlanAPIType.TypeInsert:
            learning_plan_api_response = learning_plan_service.post_learning_plan_insert(
                learning_plans)
        elif learning_plan_api_type == LearningPlanAPIType.TypeBatchInsert:
            learning_plan_api_response = learning_plan_service.post_learning_plan_batch_insert(learning_plans)
        elif learning_plan_api_type == LearningPlanAPIType.TypeUpdate:
            learning_plan_api_response = learning_plan_service.put_learning_plan(learning_plans)

        assert_that(learning_plan_api_response.status_code == 400)

        api_response_json = learning_plan_api_response.json()
        if is_check_date_type:
            expected_message = "JSON decoding error: Cannot deserialize value of type `java.util.Date` from String \"{0}\"".format(
                field_value)
        else:
            if not is_exceed_int:
                expected_message = "JSON decoding error: Cannot deserialize value of type `int` from String \"{0}\"".format(
                    field_value)
            else:
                expected_message = "JSON decoding error: Numeric value ({0}) out of range of int (-2147483648 - 2147483647)".format(
                    field_value)
        assert_that(api_response_json['message'].find('expected_message'),
                    expected_message + " can't be found in message")

    # test insert, update and batch insert with single plan API for date/int type field with invalid format value
    # called by test cases
    def test_learning_plan_insert_update_invalid_date_int_fields(self, learning_plan_api_type,
                                                                 is_check_date_type, is_exceed_int=False):
        if is_check_date_type:
            # following is the date type fields in learning plan entity
            test_type_fields = ['created_time', 'last_updated_time', 'start_time', 'end_time']
        else:
            # following is the int type fields in learning plan entity
            test_type_fields = ['product_id', 'plan_type', 'state', 'bucket_id']

        learning_plan = LearningPlanUtils.construct_learning_plan_by_value_type(FieldValueType.Valid)
        if learning_plan_api_type == LearningPlanAPIType.TypeUpdate:
            learning_plan.system_key = str(uuid.uuid1())

        for test_type_field in test_type_fields:
            original_value = getattr(learning_plan, test_type_field)
            if is_check_date_type:
                value_year = str(datetime.datetime.now().year)
                value_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                field_value = random.choice([value_year, value_time])
            else:
                if not is_exceed_int:
                    field_value = ''.join(random.sample(string.ascii_letters, 5))
                else:
                    field_value = 2147483648  # 2147483647 is int's maxvalue
            
            # set the invalid format value for date field
            setattr(learning_plan, test_type_field, field_value)
            learning_plans = learning_plan
            # deal with batch insert API
            if learning_plan_api_type == LearningPlanAPIType.TypeBatchInsert:
                learning_plans = [learning_plan]

            self.call_api_and_verify_errors_for_invalid_date_int_fields(learning_plans,
                                                                        field_value,
                                                                        learning_plan_api_type,
                                                                        is_check_date_type,
                                                                        is_exceed_int)
            # as need to check other fields, so, set this field back to valid value at last
            setattr(learning_plan, test_type_field, original_value)

    # test insert API for date type field with invalid format value
    @Test(tags="qa")
    def test_learning_plan_insert_invalid_date_fields(self):
        self.test_learning_plan_insert_update_invalid_date_int_fields(LearningPlanAPIType.TypeInsert, True)

    # test update API for date type field with invalid format value
    @Test(tags="qa")
    def test_learning_plan_update_invalid_date_fields(self):
        self.test_learning_plan_insert_update_invalid_date_int_fields(LearningPlanAPIType.TypeUpdate, True)

    # test batch insert API with single plan for date type field with invalid format value
    @Test(tags="qa")
    def test_learning_plan_batch_insert_with_single_plan_invalid_date_fields(self):
        self.test_learning_plan_insert_update_invalid_date_int_fields(LearningPlanAPIType.TypeBatchInsert, True)

    # test insert API for int type field with invalid format value
    @Test(tags="qa")
    def test_learning_plan_insert_invalid_int_fields(self):
        self.test_learning_plan_insert_update_invalid_date_int_fields(LearningPlanAPIType.TypeInsert, False)

    # test update API for int type field with invalid format value
    @Test(tags="qa")
    def test_learning_plan_update_invalid_int_fields(self):
        self.test_learning_plan_insert_update_invalid_date_int_fields(LearningPlanAPIType.TypeUpdate, False)

    # test batch insert API with single plan for int type field with invalid format value
    @Test(tags="qa")
    def test_learning_plan_batch_insert_with_single_plan_invalid_int_fields(self):
        self.test_learning_plan_insert_update_invalid_date_int_fields(LearningPlanAPIType.TypeBatchInsert, False)

    # test insert API for int type field with exceed max value
    @Test(tags="qa")
    def test_learning_plan_insert_exceed_max_int_fields(self):
        self.test_learning_plan_insert_update_invalid_date_int_fields(LearningPlanAPIType.TypeInsert, False, True)

    # test update API for int type field with exceed max value
    @Test(tags="qa")
    def test_learning_plan_update_exceed_max_int_fields(self):
        self.test_learning_plan_insert_update_invalid_date_int_fields(LearningPlanAPIType.TypeUpdate, False, True)

    # test batch insert API with single plan for int type field with exceed max value
    @Test(tags="qa")
    def test_learning_plan_batch_insert_with_single_plan_exceed_max_int_fields(self):
        self.test_learning_plan_insert_update_invalid_date_int_fields(LearningPlanAPIType.TypeBatchInsert, False, True)

    # test batch insert API for date type field with invalid format value
    # call by test cases
    def test_learning_plan_batch_insert_with_multiple_plans_invalid_date_int_fields(self, is_check_date_type,
                                                                                    is_exceed_int=False):
        if is_check_date_type:
            # following is the date type fields in learning plan entity
            test_type_fields = ['created_time', 'last_updated_time', 'start_time', 'end_time']
        else:
            # following is the int type fields in learning plan entity
            test_type_fields = ['product_id', 'plan_type', 'state', 'bucket_id']

        # batch insert need the whole batch have same partition,that means,
        # need same product_id plan_business_key and bucket_id
        learning_plan_template = LearningPlanUtils.construct_learning_plan_template(False)
        # construct valid learning plan list
        batch_number = random.randint(2, 5)
        learning_plan_list = \
            LearningPlanUtils.construct_multiple_valid_learning_plans(learning_plan_template, batch_number)

        for learning_plan in learning_plan_list:
            for test_type_field in test_type_fields:
                original_value = getattr(learning_plan, test_type_field)
                if is_check_date_type:
                    value_year = str(datetime.datetime.now().year)
                    value_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    field_value = random.choice([value_year, value_time])
                else:
                    if not is_exceed_int:
                        field_value = ''.join(random.sample(string.ascii_letters, 5))
                    else:
                        field_value = 2147483648  # 2147483647 is int's maxvalue

                # set the invalid value for date/int field
                setattr(learning_plan, test_type_field, field_value)
                self.call_api_and_verify_errors_for_invalid_date_int_fields(learning_plan_list,
                                                                            field_value,
                                                                            LearningPlanAPIType.TypeBatchInsert,
                                                                            is_check_date_type,
                                                                            is_exceed_int)
                # as need to check other fields, so, set this field as valid value at last
                setattr(learning_plan, test_type_field, original_value)

    # test batch insert API for date type field with invalid format value
    @Test(tags="qa")
    def test_learning_plan_batch_insert_with_multiple_plans_invalid_date_fields(self):
        self.test_learning_plan_batch_insert_with_multiple_plans_invalid_date_int_fields(True)

    # test batch insert API for int type field with invalid format value
    @Test(tags="qa")
    def test_learning_plan_batch_insert_with_multiple_plans_invalid_int_fields(self):
        self.test_learning_plan_batch_insert_with_multiple_plans_invalid_date_int_fields(False)

    # test batch insert API for int type field with exceed max value
    @Test(tags="qa")
    def test_learning_plan_batch_insert_with_multiple_plans_exceed_max_int_fields(self):
        self.test_learning_plan_batch_insert_with_multiple_plans_invalid_date_int_fields(False, True)