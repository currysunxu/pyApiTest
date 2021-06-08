from ptest.decorator import TestClass, Test
from E1_API_Automation.Business.NGPlatform.NGPlatformUtils.LearningResultUtils import LearningResultUtils, LearningResultQueryType
from E1_API_Automation.Business.NGPlatform.LearningResultService import LearningResultService
from E1_API_Automation.Business.NGPlatform.NGPlatformUtils.LearningDBUtils import LearningDBUtils
from E1_API_Automation.Business.NGPlatform.NGPlatformUtils.LearningCommonUtils import LearningCommonUtils
from E1_API_Automation.Business.NGPlatform.LearningResultEntity import LearningResultEntity
from E1_API_Automation.Business.NGPlatform.LearningFieldTemplate import FieldValueType
from E1_API_Automation.Business.Utils.EnvUtils import EnvUtils
from hamcrest import assert_that
import random
import string
import datetime


@TestClass()
class PlanResultTestCases:

    # test learning result insert API with single detail
    @Test(tags="qa, stg")
    def test_learning_result_insert_valid_single_detail(self):
        learning_result_service = LearningResultService()

        learning_result = LearningResultUtils.construct_learning_result_valid(1)
        learning_result_insert_api_response = learning_result_service.post_learning_result_insert(learning_result)
        assert_that(learning_result_insert_api_response.status_code == 200)

        # verify what it returned in response will be consistent what we want to insert
        error_message = LearningCommonUtils.verify_result_with_entity(learning_result_insert_api_response.json(),
                                                                      learning_result)
        assert_that(error_message == '', error_message)

    # test learning result insert API with multiple details
    @Test(tags="qa, stg")
    def test_learning_result_insert_valid_multiple_details(self):
        learning_result_service = LearningResultService()

        learning_result = LearningResultUtils.construct_learning_result_valid(random.randint(2, 5))
        learning_result_insert_api_response = learning_result_service.post_learning_result_insert(learning_result)
        assert_that(learning_result_insert_api_response.status_code == 200)

        # verify what it returned in response will be consistent what we want to insert
        error_message = LearningCommonUtils.verify_result_with_entity(learning_result_insert_api_response.json(),
                                                                      learning_result)
        assert_that(error_message == '', error_message)

    # test learning result with only required fields
    @Test(tags="qa, stg")
    def test_learning_result_insert_valid_only_required(self):
        learning_result_service = LearningResultService()

        learning_result = LearningResultUtils.construct_learning_result_valid_by_is_only_required(random.randint(1, 5),
                                                                                                  True)
        learning_result_insert_api_response = learning_result_service.post_learning_result_insert(learning_result)
        assert_that(learning_result_insert_api_response.status_code == 200)

        # verify what it returned in response will be consistent what we want to insert
        error_message = LearningCommonUtils.verify_result_with_entity(learning_result_insert_api_response.json(),
                                                                      learning_result)
        assert_that(error_message == '', error_message)

    # test get specific result
    @Test(tags="qa, stg")
    def test_get_specific_result(self):
        learning_result_service = LearningResultService()

        learning_result = LearningResultUtils.construct_learning_result_valid(1)
        learning_result_insert_api_response = learning_result_service.post_learning_result_insert(learning_result)
        assert_that(learning_result_insert_api_response.status_code == 200)

        learning_result_get_api_response = learning_result_service.get_specific_result(learning_result)
        assert_that(learning_result_get_api_response.status_code == 200)

        if not EnvUtils.is_env_live_cn() and not EnvUtils.is_env_live_sg():
            learning_result_list_from_db = LearningDBUtils.get_specific_result(learning_result)

            error_message = \
                LearningCommonUtils.verify_learning_get_api_data_with_db(learning_result_get_api_response.json(),
                                                                         learning_result_list_from_db)

            assert_that(error_message == '', error_message)


    # Test when all the fields are null
    @Test(tags="qa, stg")
    def test_learning_result_insert_null_values(self):
        learning_result_service = LearningResultService()
        # all the filed value as null
        learning_result = LearningResultEntity(None, None, None)
        learning_result_insert_api_response = learning_result_service.post_learning_result_insert(learning_result)
        assert_that(learning_result_insert_api_response.status_code == 400)

        error_message = \
            LearningResultUtils.verify_result_insert_error_messages(learning_result_insert_api_response.json(),
                                                                    learning_result)

        assert_that(error_message == '', error_message)

    # Test when all the fields are empty
    @Test(tags="qa, stg")
    def test_learning_result_insert_empty_values(self):
        learning_result_service = LearningResultService()
        # all the filed value as ''
        learning_result = LearningResultUtils.construct_learning_result_by_value_type(None,
                                                                                      FieldValueType.EmptyValue)
        learning_result_insert_api_response = learning_result_service.post_learning_result_insert(learning_result)
        assert_that(learning_result_insert_api_response.status_code == 400)

        error_message = \
            LearningResultUtils.verify_result_insert_error_messages(learning_result_insert_api_response.json(),
                                                                    learning_result)

        assert_that(error_message == '', error_message)

    # test when all the fields, including fields in details are null
    @Test(tags="qa, stg")
    def test_learning_result_insert_null_values_including_details_fields(self):
        learning_result_service = LearningResultService()
        # all the filed value as null, also with details list with null fields
        learning_result = LearningResultUtils.construct_learning_result_by_value_type(2,
                                                                                      FieldValueType.NoneValue)
        learning_result_insert_api_response = learning_result_service.post_learning_result_insert(learning_result)
        assert_that(learning_result_insert_api_response.status_code == 400)

        error_message = \
            LearningResultUtils.verify_result_insert_error_messages(learning_result_insert_api_response.json(),
                                                                    learning_result)

        assert_that(error_message == '', error_message)

    # test when all the fields, including fields in details are empty
    @Test(tags="qa, stg")
    def test_learning_result_insert_empty_values_including_details_fields(self):
        learning_result_service = LearningResultService()
        # all the filed value as null, also with details list with null fields
        learning_result = LearningResultUtils.construct_learning_result_by_value_type(random.randint(1, 5),
                                                                                      FieldValueType.EmptyValue)
        learning_result_insert_api_response = learning_result_service.post_learning_result_insert(learning_result)
        assert_that(learning_result_insert_api_response.status_code == 400)

        error_message = \
            LearningResultUtils.verify_result_insert_error_messages(learning_result_insert_api_response.json(),
                                                                    learning_result)

        assert_that(error_message == '', error_message)

    # test when fields with values below min
    @Test(tags="qa, stg")
    def test_learning_result_insert_invalid_value_below_min(self):
        learning_result_service = LearningResultService()
        # all the filed value below min
        learning_result = LearningResultUtils.construct_learning_result_by_value_type(random.randint(1, 5),
                                                                                      FieldValueType.BelowMin)
        learning_result_insert_api_response = learning_result_service.post_learning_result_insert(learning_result)
        assert_that(learning_result_insert_api_response.status_code == 400)

        error_message = \
            LearningResultUtils.verify_result_insert_error_messages(learning_result_insert_api_response.json(),
                                                                    learning_result)

        assert_that(error_message == '', error_message)

    # test when fields with values exceed max
    @Test(tags="qa, stg")
    def test_learning_result_insert_invalid_value_exceed_max(self):
        learning_result_service = LearningResultService()
        # all the filed value as ''
        learning_result = LearningResultUtils.construct_learning_result_by_value_type(random.randint(1, 5),
                                                                                      FieldValueType.ExceedMax)
        learning_result_insert_api_response = learning_result_service.post_learning_result_insert(learning_result)
        assert_that(learning_result_insert_api_response.status_code == 400)

        error_message = \
            LearningResultUtils.verify_result_insert_error_messages(learning_result_insert_api_response.json(),
                                                                    learning_result)

        assert_that(error_message == '', error_message)


    # this method will be called by other method to check int type field with invalid value,
    # including invalid format value and value exceed int's max value
    def validate_int_type_field_with_invalid_value(self, learning_result_service, learning_result, learning_entity,
                                                   field_name, is_exceed_int):

        if not is_exceed_int:
            field_value = ''.join(random.sample(string.ascii_letters, 5))
        else:
            field_value = 2147483648  # 2147483647 is int's maxvalue
        setattr(learning_entity, field_name, field_value)

        learning_result_insert_api_response = learning_result_service.post_learning_result_insert(learning_result)
        assert_that(learning_result_insert_api_response.status_code == 400)

        api_response_json = learning_result_insert_api_response.json()
        if not is_exceed_int:
            expected_message = "JSON decoding error: Cannot deserialize value of type `int` from String \"{0}\"".format(
                field_value)
        else:
            expected_message = "JSON decoding error: Numeric value ({0}) out of range of int (-2147483648 - 2147483647)".format(
                field_value)
        assert_that(api_response_json['message'].find('expected_message'),
                    expected_message + " can't be found in message")
        # as need to check other fields, so, set this field as valid value at last
        setattr(learning_entity, field_name, 0)

    # this method will be called by test cases
    def test_learning_result_insert_invalid_int_fields(self, is_exceed_int):
        learning_result_service = LearningResultService()
        # following is the int type fields in result entity and details entity
        int_type_fields = ['product', 'product_module', 'expected_score', 'actual_score', 'duration']
        int_type_details_fields = ['expected_score', 'actual_score', 'duration']

        detail_number = random.randint(1, 3)
        learning_result = LearningResultUtils.construct_learning_result_by_value_type(detail_number,
                                                                                      FieldValueType.Valid)

        for int_type_field in int_type_fields:
            self.validate_int_type_field_with_invalid_value(learning_result_service, learning_result, learning_result,
                                                            int_type_field, is_exceed_int)

        learning_details = learning_result.details
        for int_type_details_field in int_type_details_fields:
            for i in range(detail_number):
                learning_detail_entity = learning_details[i]
                self.validate_int_type_field_with_invalid_value(learning_result_service, learning_result,
                                                                learning_detail_entity, int_type_details_field, is_exceed_int)

    # test when int type fields with invalid format value
    @Test(tags="qa, stg")
    def test_learning_result_insert_invalid_value_for_int_fields(self):
        self.test_learning_result_insert_invalid_int_fields(False)

    # test when int type fields with value exceed int's max value
    @Test(tags="qa, stg")
    def test_learning_result_insert_exceed_int_value_for_int_fields(self):
        self.test_learning_result_insert_invalid_int_fields(True)

    def validate_date_type_field_with_invalid_value(self, learning_result_service, learning_result, learning_entity,
                                                   field_name):
        value_year = str(datetime.datetime.now().year)
        value_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        field_value = random.choice([value_year, value_time])

        setattr(learning_entity, field_name, field_value)

        learning_result_insert_api_response = learning_result_service.post_learning_result_insert(
            learning_result)
        assert_that(learning_result_insert_api_response.status_code == 400)

        api_response_json = learning_result_insert_api_response.json()
        expected_message = "JSON decoding error: Cannot deserialize value of type `java.util.Date` from String \"{0}\"".format(
            field_value)
        assert_that(api_response_json['message'].find('expected_message'),
                    expected_message + " can't be found in message")
        # as need to check other fields, so, set this field as valid value at last
        setattr(learning_entity, field_name, None)

    # test when date type field with invalid format value
    @Test(tags="qa, stg")
    def test_learning_result_insert_invalid_date_fields(self):
        learning_result_service = LearningResultService()
        # following is the date type fields in details entity
        date_type_fields = ['start_time', 'end_time']

        detail_number = random.randint(1, 3)
        learning_result = LearningResultUtils.construct_learning_result_by_value_type(detail_number,
                                                                                      FieldValueType.Valid)

        for date_type_field in date_type_fields:
            self.validate_date_type_field_with_invalid_value(learning_result_service, learning_result,
                                                             learning_result, date_type_field)

        learning_details = learning_result.details
        for date_type_details_field in date_type_fields:
            for i in range(detail_number):
                learning_detail_entity = learning_details[i]
                self.validate_date_type_field_with_invalid_value(learning_result_service, learning_result,
                                                            learning_detail_entity, date_type_details_field)

    # test insert with max values
    @Test(tags="qa, stg")
    def test_learning_result_insert_valid_value_max(self):
        learning_result_service = LearningResultService()
        # all the filed value with max value
        learning_result = LearningResultUtils.construct_learning_result_by_value_type(random.randint(1, 5),
                                                                                      FieldValueType.Max)
        learning_result_insert_api_response = learning_result_service.post_learning_result_insert(learning_result)
        assert_that(learning_result_insert_api_response.status_code == 200)

        # verify what it returned in response will be consistent what we want to insert
        error_message = LearningCommonUtils.verify_result_with_entity(learning_result_insert_api_response.json(),
                                                                      learning_result)
        assert_that(error_message == '', error_message)

    # test insert with min values
    @Test(tags="qa, stg")
    def test_learning_result_insert_valid_value_min(self):
        learning_result_service = LearningResultService()
        # all the filed value with max value
        learning_result = LearningResultUtils.construct_learning_result_by_value_type(random.randint(1, 5),
                                                                                      FieldValueType.Min)
        learning_result_insert_api_response = learning_result_service.post_learning_result_insert(learning_result)
        assert_that(learning_result_insert_api_response.status_code == 200)

        # verify what it returned in response will be consistent what we want to insert
        error_message = LearningCommonUtils.verify_result_with_entity(learning_result_insert_api_response.json(),
                                                                      learning_result)
        assert_that(error_message == '', error_message)

    # this method can be called by different test cases
    def test_get_result_api(self, record_number, limit_list, learning_result_query_type):
        learning_result_service = LearningResultService()

        # get result api need some same fields, so, use it as template
        learning_result_template = LearningResultUtils.construct_learning_result_template(learning_result_query_type)
        # construct valid learning result list
        learning_result_list = LearningResultUtils.construct_multiple_results_by_template(record_number,
                                                                                          learning_result_template)
        learning_result_batch_insert_api_response = learning_result_service.post_learning_result_batch_insert(
            learning_result_list)
        assert_that(learning_result_batch_insert_api_response.status_code == 200,
                    'batch insert api response status is:' + str(learning_result_batch_insert_api_response.status_code))

        # get data from DB
        if not EnvUtils.is_env_live_cn() and not EnvUtils.is_env_live_sg():
            if learning_result_query_type == LearningResultQueryType.TypeGetUser:
                learning_result_list_from_db = LearningDBUtils.get_user_result(learning_result_template)
            elif learning_result_query_type == LearningResultQueryType.TypeGetPartition:
                learning_result_list_from_db = LearningDBUtils.get_partition_result(learning_result_template)
            elif learning_result_query_type == LearningResultQueryType.TypeGetSpecific:
                learning_result_list_from_db = LearningDBUtils.get_specific_result(learning_result_template)

        # if limit_list is None, means it test the get API without limit
        if limit_list is None:
            if learning_result_query_type == LearningResultQueryType.TypeGetUser:
                learning_result_get_api_response = \
                    learning_result_service.get_user_result_without_limit(learning_result_template)
            elif learning_result_query_type == LearningResultQueryType.TypeGetPartition:
                learning_result_get_api_response = \
                    learning_result_service.get_partition_result_without_limit(learning_result_template)
            elif learning_result_query_type == LearningResultQueryType.TypeGetSpecific:
                learning_result_get_api_response = \
                    learning_result_service.get_specific_result(learning_result_template)

            assert_that(learning_result_get_api_response.status_code == 200)

            if not EnvUtils.is_env_live_cn() and not EnvUtils.is_env_live_sg():
                # if there's more than 50 records fit the condition, the get API will by default get 50 records
                if record_number > 50:
                    learning_result_list_from_db = learning_result_list_from_db[:50]

                error_message = LearningCommonUtils.verify_learning_get_api_data_with_db(
                    learning_result_get_api_response.json(),
                    learning_result_list_from_db)

                assert_that(error_message == '', error_message)
        else:
            for limit in limit_list:
                if learning_result_query_type == LearningResultQueryType.TypeGetUser:
                    learning_result_get_api_response = learning_result_service.get_user_result_with_limit(
                        learning_result_template,
                        limit)
                elif learning_result_query_type == LearningResultQueryType.TypeGetPartition:
                    learning_result_get_api_response = \
                        learning_result_service.get_partition_result_with_limit(learning_result_template, limit)

                assert_that(learning_result_get_api_response.status_code == 200)

                if not EnvUtils.is_env_live_cn() and not EnvUtils.is_env_live_sg():
                    expected_learning_result_list_from_db = \
                        LearningCommonUtils.get_expected_learning_data_from_db_by_limit_page(
                            learning_result_list_from_db,
                            limit, None)

                    error_message = LearningCommonUtils. \
                        verify_learning_get_api_data_with_db(learning_result_get_api_response.json(),
                                                             expected_learning_result_list_from_db)
                    assert_that(error_message == '',
                                "When limit is:" + str(limit) + ", the error message is:" + error_message)

    @Test(tags="qa, stg")
    def test_get_partition_result_without_limit_less_than_50(self):
        record_number = random.randint(1, 30)
        self.test_get_result_api(record_number, None, LearningResultQueryType.TypeGetPartition)

    # when there's more than 50 records in the DB, get API will by default get 50 records
    @Test(tags="qa, stg")
    def test_get_partition_result_without_limit_larger_than_50(self):
        record_number = 51
        self.test_get_result_api(record_number, None, LearningResultQueryType.TypeGetPartition)

    @Test(tags="qa, stg")
    def test_get_user_result_without_limit_less_than_50(self):
        record_number = random.randint(1, 30)
        self.test_get_result_api(record_number, None, LearningResultQueryType.TypeGetUser)

    # when there's more than 50 records in the DB, get API will by default get 50 records
    @Test(tags="qa, stg")
    def test_get_user_result_without_limit_larger_than_50(self):
        record_number = 51
        self.test_get_result_api(record_number, None, LearningResultQueryType.TypeGetUser)

    @Test(tags="qa, stg")
    def test_get_partition_result_with_limit_less_than_size(self):
        record_number = 51
        # limit list, default limit value is 50
        limit_list = [1, random.randint(2, 10), random.randint(11, 30), random.randint(31, 49), 50, None, '']

        self.test_get_result_api(record_number, limit_list, LearningResultQueryType.TypeGetPartition)

    @Test(tags="qa, stg")
    def test_get_partition_result_with_limit_larger_than_size(self):
        record_number = random.randint(10, 30)
        limit_list = [random.randint(1, record_number-1), record_number, record_number + 1,
                      random.randint(record_number + 2, 50)]
        self.test_get_result_api(record_number, limit_list, LearningResultQueryType.TypeGetPartition)

    @Test(tags="qa, stg")
    def test_get_user_result_with_limit_less_than_size(self):
        record_number = 51
        # limit list, default limit value is 50
        limit_list = [1, random.randint(2, 10), random.randint(11, 30), random.randint(31, 49), 50, None, '']

        self.test_get_result_api(record_number, limit_list, LearningResultQueryType.TypeGetUser)

    @Test(tags="qa, stg")
    def test_get_user_result_with_limit_larger_than_size(self):
        record_number = random.randint(10, 30)
        limit_list = [random.randint(1, record_number - 1), record_number, record_number + 1,
                      random.randint(record_number + 2, 50)]
        self.test_get_result_api(record_number, limit_list, LearningResultQueryType.TypeGetUser)

    @Test(tags="qa, stg")
    def test_get_specific_result_less_than_50(self):
        record_number = random.randint(1, 20)
        self.test_get_result_api(record_number, None, LearningResultQueryType.TypeGetSpecific)

    # when there's more than 50 records in the DB, get API will by default get 50 records
    @Test(tags="qa, stg")
    def test_get_specific_result_larger_than_50(self):
        record_number = 51
        self.test_get_result_api(record_number, None, LearningResultQueryType.TypeGetSpecific)

    # test when product/student_key is empty for all the query APIs
    @Test(tags="qa, stg")
    def test_get_api_with_empty_value(self):
        learning_result_service = LearningResultService()

        learning_result_template = \
            LearningResultUtils.construct_learning_result_template(LearningResultQueryType.TypeGetSpecific)

        query_fields = ['product', 'student_key']

        for field_name in query_fields:
            original_value = getattr(learning_result_template, field_name)
            setattr(learning_result_template, field_name, '')

            learning_result_get_api_response = learning_result_service.get_partition_result_without_limit(
                learning_result_template)
            assert_that(learning_result_get_api_response.status_code == 404)

            learning_result_get_api_response = learning_result_service.get_partition_result_with_limit(
                learning_result_template, 2)
            assert_that(learning_result_get_api_response.status_code == 404)

            learning_result_get_api_response = learning_result_service.get_user_result_without_limit(
                learning_result_template)
            assert_that(learning_result_get_api_response.status_code == 404)

            learning_result_get_api_response = learning_result_service.get_user_result_with_limit(
                learning_result_template, 2)
            assert_that(learning_result_get_api_response.status_code == 404)

            learning_result_get_api_response = learning_result_service.get_specific_result(learning_result_template)
            assert_that(learning_result_get_api_response.status_code == 404)

            setattr(learning_result_template, field_name, original_value)

    # this method can be called by test case
    def assert_get_api_response_with_invalid_format_for_int(self, learning_result_get_api_response, field_value):
        assert_that(learning_result_get_api_response.status_code == 400)
        expected_message = "Failed to convert value of type 'java.lang.String' to required type 'int'; nested exception is java.lang.NumberFormatException: For input string: \"{0}\"".format(
            field_value)
        assert_that(learning_result_get_api_response.json()['message'].find('expected_message'),
                    expected_message + " can't be found in message")

    # test when product, product_module value is not int
    @Test(tags="qa, stg")
    def test_get_api_with_invalid_format_product_id(self):
        learning_result_service = LearningResultService()

        learning_result_template = \
            LearningResultUtils.construct_learning_result_template(LearningResultQueryType.TypeGetSpecific)

        query_fields = ['product', 'product_module']

        for field_name in query_fields:
            original_value = getattr(learning_result_template, field_name)
            invalid_value = ''.join(random.sample(string.ascii_letters, 5))
            setattr(learning_result_template, field_name, invalid_value)

            if field_name == 'product':
                learning_result_get_api_response = learning_result_service.get_partition_result_without_limit(
                    learning_result_template)
                self.assert_get_api_response_with_invalid_format_for_int(learning_result_get_api_response,
                                                                         invalid_value)

                learning_result_get_api_response = \
                    learning_result_service.get_partition_result_with_limit(learning_result_template, 2)
                self.assert_get_api_response_with_invalid_format_for_int(learning_result_get_api_response,
                                                                         invalid_value)

            learning_result_get_api_response = learning_result_service.get_user_result_without_limit(
                learning_result_template)
            self.assert_get_api_response_with_invalid_format_for_int(learning_result_get_api_response,
                                                                     invalid_value)

            learning_result_get_api_response = learning_result_service.get_user_result_with_limit(
                learning_result_template, 2)
            self.assert_get_api_response_with_invalid_format_for_int(learning_result_get_api_response,
                                                                     invalid_value)

            learning_result_get_api_response = learning_result_service.get_specific_result(learning_result_template)
            self.assert_get_api_response_with_invalid_format_for_int(learning_result_get_api_response,
                                                                     invalid_value)

            setattr(learning_result_template, field_name, original_value)



    # test when limit value is not int
    @Test(tags="qa, stg")
    def test_get_api_with_invalid_format_limit(self):
        learning_result_service = LearningResultService()

        learning_result_template = \
            LearningResultUtils.construct_learning_result_template(LearningResultQueryType.TypeGetSpecific)

        limit = ''.join(random.sample(string.ascii_letters, 5))

        learning_result_get_api_response = \
            learning_result_service.get_partition_result_with_limit(learning_result_template, limit)
        self.assert_get_api_response_with_invalid_format_for_int(learning_result_get_api_response, limit)

        learning_result_get_api_response = learning_result_service.get_user_result_with_limit(learning_result_template,
                                                                                              limit)
        self.assert_get_api_response_with_invalid_format_for_int(learning_result_get_api_response, limit)

    # test when limit value is not allowed int value, that is, below 1, exceed 50
    @Test(tags="qa, stg")
    def test_get_api_with_invalid_value_limit(self):
        learning_result_service = LearningResultService()

        learning_result_template = \
            LearningResultUtils.construct_learning_result_template(LearningResultQueryType.TypeGetSpecific)

        limit_list = [0, random.randint(-10,0), 51, random.randint(52,60)]

        for limit in limit_list:
            learning_result_get_api_response = \
                learning_result_service.get_partition_result_with_limit(learning_result_template, limit)
            assert_that(learning_result_get_api_response.status_code == 400)

            learning_result_get_api_response = \
                learning_result_service.get_user_result_with_limit(learning_result_template, limit)
            assert_that(learning_result_get_api_response.status_code == 400)

    # test when student_key , business_key with invalid format
    @Test(tags="qa, stg")
    def test_get_api_with_invalid_value_key(self):
        learning_result_service = LearningResultService()

        learning_result = LearningResultUtils.construct_learning_result_valid(2)
        learning_result_insert_api_response = learning_result_service.post_learning_result_insert(learning_result)
        assert_that(learning_result_insert_api_response.status_code == 200)

        query_fields = ['student_key', 'business_key']

        for field_name in query_fields:
            original_value = getattr(learning_result, field_name)
            # these values was not allowed in student_key and plan_business_key
            not_allowable_format = '^*<>!{}'
            invalid_field_value = ''.join(
                            random.choices(string.ascii_letters + string.digits + '|-', k=10))

            invalid_field_value = invalid_field_value + not_allowable_format
            setattr(learning_result, field_name, invalid_field_value)

            if field_name == 'student_key':
                learning_result_get_api_response = learning_result_service.get_partition_result_without_limit(
                    learning_result)
                assert_that(learning_result_get_api_response.status_code == 200)
                assert_that(len(learning_result_get_api_response.json()) == 0)

                learning_result_get_api_response = learning_result_service.get_partition_result_with_limit(
                    learning_result, 2)
                assert_that(learning_result_get_api_response.status_code == 200)
                assert_that(len(learning_result_get_api_response.json()) == 0)

                learning_result_get_api_response = learning_result_service.get_user_result_without_limit(
                    learning_result)
                assert_that(learning_result_get_api_response.status_code == 200)
                assert_that(len(learning_result_get_api_response.json()) == 0)

                learning_result_get_api_response = learning_result_service.get_user_result_with_limit(
                    learning_result, 2)
                assert_that(learning_result_get_api_response.status_code == 200)
                assert_that(len(learning_result_get_api_response.json()) == 0)

            learning_result_get_api_response = learning_result_service.get_specific_result(learning_result)
            assert_that(learning_result_get_api_response.status_code == 200)
            assert_that(len(learning_result_get_api_response.json()) == 0)

            setattr(learning_result, field_name, original_value)

    # test when business_key is empty for get specific result
    @Test(tags="qa, stg")
    def test_get_specific_result_with_empty_business_key(self):
        learning_result_service = LearningResultService()

        learning_result_template = \
            LearningResultUtils.construct_learning_result_template(LearningResultQueryType.TypeGetSpecific)
        learning_result_template.business_key = ''
        learning_result_get_api_response = learning_result_service.get_specific_result(learning_result_template)
        assert_that(learning_result_get_api_response.status_code == 500)
        expected_message = 'PRIMARY KEY column \"plansystemkey\" cannot be restricted as preceding column \"planbusinesskey\" is not restricted'
        assert_that(learning_result_get_api_response.json()['message'].find('expected_message'),
        expected_message + " can't be found in message")

    # test when product_module is empty for get user results
    @Test(tags="qa, stg")
    def test_get_user_result_with_empty_product_module(self):
        learning_result_service = LearningResultService()

        # get result api need some same fields, so, use it as template
        learning_result_template = \
            LearningResultUtils.construct_learning_result_template(LearningResultQueryType.TypeGetPartition)
        # construct valid learning result list, with same product, student_key, but different product_module
        result_number = 10
        for i in range(result_number):
            details_number = random.randint(1, 3)
            learning_result = LearningResultUtils.construct_learning_result_valid_by_template(learning_result_template,
                                                                                              details_number)
            learning_result_insert_api_response = learning_result_service.post_learning_result_insert(learning_result)
            assert_that(learning_result_insert_api_response.status_code == 200)

        get_partition_api_response = \
            learning_result_service.get_partition_result_without_limit(learning_result_template)
        learning_result_template.product_module = ''
        get_user_without_limit_api_response = \
            learning_result_service.get_user_result_without_limit(learning_result_template)
        # when product_module is empty, the get user result API will return same result as get partition api
        assert_that(get_user_without_limit_api_response.json() == get_partition_api_response.json(),
                    'get user without limit API return result should be same as get partition api when product_module is empty')
        limit_number = random.randint(1, result_number)
        get_user_with_limit_api_response = \
            learning_result_service.get_user_result_with_limit(learning_result_template, limit_number)
        assert_that(get_user_with_limit_api_response.json() == get_partition_api_response.json()[:limit_number],
                    'get user with limit API return result should be same as get partition api when product_module is empty')


    # test when business_key is empty for get specific_result
    @Test(tags="qa, stg")
    def test_get_specific_result_with_empty_business_key(self):
        learning_result_service = LearningResultService()

        # get result api need some same fields, so, use it as template
        learning_result_template = \
            LearningResultUtils.construct_learning_result_template(LearningResultQueryType.TypeGetUser)
        # construct valid learning result list, with same product_id, student_key, product_module, but different plan_business_key
        result_number = 10
        for i in range(result_number):
            details_number = random.randint(1, 3)
            learning_result = LearningResultUtils.construct_learning_result_valid_by_template(learning_result_template,
                                                                                              details_number)
            learning_result_insert_api_response = learning_result_service.post_learning_result_insert(learning_result)
            assert_that(learning_result_insert_api_response.status_code == 200)

        get_user_without_limit_api_response = \
            learning_result_service.get_user_result_without_limit(learning_result_template)
        learning_result_template.business_key = ''
        get_specific_result_api_response = \
            learning_result_service.get_specific_result(learning_result_template)
        # when business_key is empty, the get specific result API will return same result as get user api
        assert_that(get_specific_result_api_response.json() == get_user_without_limit_api_response.json(),
                    'get specific result API return result should be same as user without limit api when business_key is empty')

    # test when there's no record can be found with the param
    @Test(tags="qa, stg")
    def test_get_api_with_not_existing_record(self):
        learning_result_service = LearningResultService()

        learning_result = \
            LearningResultUtils.construct_learning_result_template(LearningResultQueryType.TypeGetSpecific)

        learning_result_get_api_response = learning_result_service.get_partition_result_without_limit(
            learning_result)
        assert_that(learning_result_get_api_response.status_code == 200)
        assert_that(len(learning_result_get_api_response.json()) == 0)

        learning_result_get_api_response = learning_result_service.get_partition_result_with_limit(
            learning_result, 10)
        assert_that(learning_result_get_api_response.status_code == 200)
        assert_that(len(learning_result_get_api_response.json()) == 0)

        learning_result_get_api_response = learning_result_service.get_user_result_without_limit(
            learning_result)
        assert_that(learning_result_get_api_response.status_code == 200)
        assert_that(len(learning_result_get_api_response.json()) == 0)

        learning_result_get_api_response = learning_result_service.get_user_result_with_limit(
            learning_result, 10)
        assert_that(learning_result_get_api_response.status_code == 200)
        assert_that(len(learning_result_get_api_response.json()) == 0)

        learning_result_get_api_response = learning_result_service.get_specific_result(learning_result)
        assert_that(learning_result_get_api_response.status_code == 200)
        assert_that(len(learning_result_get_api_response.json()) == 0)
