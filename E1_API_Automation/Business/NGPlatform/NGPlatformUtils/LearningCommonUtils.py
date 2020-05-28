from E1_API_Automation.Business.NGPlatform.LearningFieldTemplate import FieldType, FieldValueType
from E1_API_Automation.Business.NGPlatform.LearningErrorEntity import LearningErrorEntity
import random
import string
import datetime
import uuid
import json
import jmespath
import re


class LearningCommonUtils:

    @staticmethod
    def construct_field_value_by_is_only_required(field_template, field_value_type, is_only_required):
        '''
        if case want to construct all the fields value, including not required field value, then,
        generate value for all fields, but, if case only want to construct entity with only required fields, then,
        generate value only for required fields
        '''
        if not is_only_required:
            return LearningCommonUtils.construct_field_value(field_template, field_value_type)
        else:
            if field_template.is_required:
                return LearningCommonUtils.construct_field_value(field_template, field_value_type)
            else:
                return None

    @staticmethod
    def construct_field_value(field_template, field_value_type):
        field_value = None

        if field_value_type == FieldValueType.NoneValue:
            return None
        elif field_value_type == FieldValueType.EmptyValue:
            return ''

        if field_template.field_type == FieldType.TypeInt:
            if field_template.content_format is not None:
                if field_value_type == FieldValueType.Valid:
                    field_value = random.choice(field_template.content_format)
                elif field_value_type == FieldValueType.Max:
                    field_value = field_template.content_format[-1]
                elif field_value_type == FieldValueType.Min:
                    field_value = field_template.content_format[0]
                elif field_value_type == FieldValueType.ExceedMax:
                    field_value = field_template.content_format[-1] + 1
                elif field_value_type == FieldValueType.BelowMin:
                    random_value = random.randint(field_template.content_format[0], field_template.content_format[-2])
                    field_value = 2 * random_value + 1
            else:
                min_value = field_template.min_value
                max_value = field_template.max_value

                if field_value_type == FieldValueType.BelowMin:
                    if min_value is not None:
                        field_value = min_value - 1
                    else:
                        field_value = -1
                elif field_value_type == FieldValueType.ExceedMax:
                    # if the int value exceed int's max value, there's no normal code validation,
                    # API will throw int exceed error directly
                    if max_value is not None:
                        field_value = max_value + 1
                    else:
                        field_value = 2147483647  # 2147483647 is int's maxvalue
                elif field_value_type == FieldValueType.Valid:
                    if min_value is None:
                        min_value = 1
                    if max_value is None:
                        max_value = 100
                    field_value = random.randint(min_value, max_value)
                elif field_value_type == FieldValueType.Max:
                    if max_value is not None:
                        field_value = max_value
                    else:
                        field_value = 2147483647  # 2147483647 is int's maxvalue
                elif field_value_type == FieldValueType.Min:
                    if min_value is not None:
                        field_value = min_value
                    else:
                        field_value = 0
        elif field_template.field_type == FieldType.TypeString:
            if field_value_type == FieldValueType.BelowMin:
                if field_template.content_format is not None:
                    not_allowable_format = string.punctuation + string.whitespace
                    not_allowable_format.replace('|', '')
                    not_allowable_format.replace('-', '')
                    field_value = ''.join(random.sample(not_allowable_format, 10))
            elif field_value_type == FieldValueType.ExceedMax:
                if field_template.content_format is not None:
                    field_value = ''.join(random.choices(string.ascii_letters + string.digits + '|-', k=field_template.max_value + 1))
                else:
                    field_value = ''.join(random.choices(string.printable, k=field_template.max_value + 1))
            else:
                if field_value_type == FieldValueType.Valid:
                    content_len = random.randint(field_template.min_value, field_template.max_value)
                elif field_value_type == FieldValueType.Max:
                    content_len = field_template.max_value
                elif field_value_type == FieldValueType.Min:
                    content_len = field_template.min_value

                if content_len is not None and content_len > 0:
                    if field_template.content_format is not None:
                        field_value = ''.join(
                            random.choices(string.ascii_letters + string.digits + '|-', k=content_len))
                    else:
                        field_value = ''.join(random.choices(string.printable, k=content_len))
        elif field_template.field_type == FieldType.TypeDate:
            if field_value_type in (FieldValueType.Valid, FieldValueType.Max, FieldValueType.Min):
                field_value = datetime.datetime.now().strftime(field_template.content_format)
                index = field_value.rindex('.')
                field_value = field_value[:index + 1] + field_value[index + 1:index + 4] + 'Z'
        elif field_template.field_type == FieldType.TypeUUID:
            if field_value_type == FieldValueType.BelowMin or field_value_type == FieldValueType.ExceedMax:
                # planSystemKey is different than other UUID fields, it's actually String type in DB, but other UUID fields is UUID in DB
                if field_template.field_name == 'planSystemKey':
                    field_value = ''.join(random.sample(string.ascii_letters, 5))
            elif field_value_type in (FieldValueType.Valid, FieldValueType.Max, FieldValueType.Min):
                field_value = uuid.uuid1()
        elif field_template.field_type == FieldType.TypeObject:
            if field_value_type == FieldValueType.BelowMin:
                value_empty_dict = {}
                value_empty_list = []
                value_empty_list_with_empty_dict = [{}, {}]
                field_value = random.choice([value_empty_dict, value_empty_list, value_empty_list_with_empty_dict])
            elif field_value_type in (FieldValueType.Valid, FieldValueType.Max, FieldValueType.Min):
                value_str = ''.join(random.sample(string.ascii_letters, 10))
                value_int = random.randint(-1000, 1000)
                value_float = random.uniform(2, 10)
                value_boolean = random.choice([True, False])
                value_list = [value_str, value_int, value_float, value_boolean]
                value_json_dict1 = {}
                value_json_dict1['testRevision'] = random.randint(1, 10)
                value_json_dict1['testTitle'] = ''.join(random.sample(string.ascii_letters, 5))
                value_json_dict1['testBoolean'] = value_boolean

                value_sub_field_dict1 = {}
                value_sub_field_dict1['testSubRevision'] = random.randint(1, 10)
                value_sub_field_dict1['testSubType'] = ''.join(random.sample(string.ascii_letters, 5))
                value_sub_field_dict1['testSubList'] = value_list

                value_sub_field_dict2 = {}
                value_sub_field_dict2['testSubRevision'] = random.randint(1, 10)
                value_sub_field_dict2['testSubType'] = ''.join(random.sample(string.ascii_letters, 5))
                value_sub_field_dict2['testSubTitle'] = ''.join(random.sample(string.ascii_letters, 10))

                value_json_dict1['testList'] = [value_sub_field_dict1, value_sub_field_dict2]

                value_json_dict2 = {}
                value_json_dict2['testRevision'] = random.randint(1, 10)
                value_json_dict2['testTitle'] = ''.join(random.sample(string.ascii_letters, 5))
                value_json_dict2['testBoolean'] = value_boolean
                value_json_dict2['testInt'] = value_int

                value_json_dict3 = {}
                value_json_dict3['testRevision'] = random.randint(1, 10)
                value_json_dict3['testTitle'] = ''.join(random.sample(string.ascii_letters, 5))
                value_json_dict3['testBoolean'] = value_boolean
                value_json_dict3['testInt'] = value_int
                value_json_dict3['testList'] = value_list

                value_json_list = [value_json_dict1, value_json_dict2, value_json_dict3]

                # json field value randomly choose from each type, includes primitive type and json with dict or list types
                field_value = random.choice([value_str, value_int, value_float, value_boolean, value_list,
                                             value_json_dict1, value_json_list])

        return field_value

    # as now service change all the input/output to use camelCase format, so, make the change
    @staticmethod
    def convert_name_from_lower_case_to_camel_case(field_name):
        while field_name.find('_') > 0:
            under_score_index = field_name.find('_')
            under_score_next_char = field_name[under_score_index+1:under_score_index+2]
            char_need_be_replaced = field_name[under_score_index:under_score_index+2]
            field_name = field_name.replace(char_need_be_replaced, under_score_next_char.upper())
        return field_name

    @staticmethod
    def convert_name_from_camel_case_to_lower_case(field_name):
        to_be_replaced_name = field_name
        for i in range(len(field_name)):
            char = field_name[i:i+1]
            if char.isupper():
                to_be_replaced_name = to_be_replaced_name.replace(char, '_'+char.lower())

        return to_be_replaced_name

    @staticmethod
    def get_field_template_by_name(field_name, field_templates):
        for field_template in field_templates:
            if field_template.field_name.lower() == field_name.replace('_', ''):
                return field_template

    @staticmethod
    def verify_result_with_entity(actual_result_json, expected_learning_entity):
        error_message = ''
        entity_class_name = expected_learning_entity.__class__.__name__
        for key in actual_result_json.keys():
            actual_key_value = actual_result_json[key]
            # as the API change the lower case to camelcase,
            # in order not to change the most of the code, use this function to convert
            lower_case_key = LearningCommonUtils.convert_name_from_camel_case_to_lower_case(key)
            entity_private_field_name = '_' + entity_class_name + '__' + lower_case_key

            is_field_exist = False
            expected_field_value = None
            if hasattr(expected_learning_entity, entity_private_field_name):
                is_field_exist = True
                expected_field_value = getattr(expected_learning_entity, entity_private_field_name)
                if 'Time' in key and actual_key_value == '':
                    actual_key_value = None

            if entity_class_name == 'LearningResultEntity' and key == 'details':
                if len(actual_key_value) != len(expected_field_value):
                    error_message = error_message + "the actual detail list length return from result insert API not as expected!"
                else:
                    # for details field, it can call recursive fuction
                    for i in range(len(actual_key_value)):
                        actual_detail_dict = actual_key_value[i]
                        expected_detail_dict = expected_field_value[i]
                        error_message = error_message + \
                                        LearningCommonUtils.verify_result_with_entity(actual_detail_dict,
                                                                                      expected_detail_dict)
            elif entity_class_name == 'LearningPlanEntity' and key == 'systemkey' and expected_field_value is None:
                if actual_key_value is None or actual_key_value == '':
                    error_message = error_message + " The learning plan's system_key value should not be null"
            elif entity_class_name == 'LearningResultEntity' and key == 'resultKey' and expected_field_value is None:
                if actual_key_value is None or actual_key_value == '':
                    error_message = error_message + " The learning result's resultKey value should not be null"
            else:
                is_value_same = False
                # some times, the actual time don't have 0 in the end, while there's 0 in expected time, e.g.
                # The actual value is:2019-08-26 16:05:31.82, but the expected value is:2019-08-26 16:05:31.820
                if 'Time' in key and expected_field_value is not None:
                    time_format = '%Y-%m-%dT%H:%M:%S.%fZ'
                    actual_time = datetime.datetime.strptime(str(actual_key_value), time_format)
                    expected_time = datetime.datetime.strptime(str(expected_field_value), time_format)
                    if is_field_exist and actual_time == expected_time:
                        is_value_same = True
                else:
                    if isinstance(actual_key_value, float):
                        expected_field_value = float(expected_field_value)
                    if is_field_exist and str(actual_key_value) == str(expected_field_value):
                        is_value_same = True

                if not is_value_same:
                    error_message = error_message + " key:" + key + "'s value in API not as expected in learning svc." \
                                                                    "The actual value is:" + str(actual_key_value) \
                                    + ", but the expected value is:" + expected_field_value
        return error_message

    # verify learning plan/result get API result with DB data
    @staticmethod
    def verify_learning_get_api_data_with_db(actual_learning_get_api_json, expected_db_learning_list):
        error_message = ''

        if len(actual_learning_get_api_json) != len(expected_db_learning_list):
            error_message = "the actual list length return from API not as expected!"

        for i in range(len(actual_learning_get_api_json)):
            actual_api_learning = actual_learning_get_api_json[i]
            expected_db_learning = expected_db_learning_list[i]

            for key in actual_api_learning.keys():
                actual_value = actual_api_learning[key]
                expected_value = expected_db_learning[key.lower()]

                # some learning result's fields is object type, it can store any type of data
                if isinstance(expected_value, str) and key in ('route', 'extension', 'answer'):
                    expected_value = json.loads(expected_value)

                is_value_same = False
                if 'Time' in key and actual_value is not None:
                    api_time_format = '%Y-%m-%dT%H:%M:%S.%fZ'
                    actual_time = datetime.datetime.strptime(str(actual_value), api_time_format)
                    db_time_format = '%Y-%m-%d %H:%M:%S.%f'
                    try:
                        expected_time = datetime.datetime.strptime(str(expected_value), db_time_format)
                    except:
                        db_time_format = '%Y-%m-%d %H:%M:%S'
                        expected_time = datetime.datetime.strptime(str(expected_value), db_time_format)

                    if actual_time == expected_time:
                        is_value_same = True
                elif key == 'details':
                    error_message = error_message + \
                                    LearningCommonUtils.verify_learning_get_api_data_with_db(actual_value,
                                                                                             expected_value)
                elif str(actual_value) == str(expected_value):
                    is_value_same = True

                if key != 'details' and not is_value_same:
                    error_message = error_message + " key:" + key + "'s value in get API not as expected in DB." \
                                                                    "The actual value is:" + str(actual_value) \
                                    + ", but the expected value is:" + expected_value

        return error_message

    @staticmethod
    def get_expected_learning_error_entity_by_template(field_value, field_template, request_index, is_field_details):
        error_code = None
        if field_template.field_type == FieldType.TypeInt:
            if field_value is None or field_value == '':
                if field_template.is_required:
                    error_code = field_template.min_error_code
                    rejected_value = 0
            else:
                if field_template.content_format is not None:
                    if field_value not in field_template.content_format:
                        error_code = field_template.min_error_code
                        rejected_value = field_value
                else:
                    if field_template.min_value is not None and field_value < field_template.min_value:
                        error_code = field_template.min_error_code
                        rejected_value = field_value
                    elif field_template.max_value is not None and field_value > field_template.max_value:
                        error_code = field_template.max_error_code
                        rejected_value = field_value
        elif field_template.field_type == FieldType.TypeString:
            is_exist_error = False
            if field_value is None or field_value == '':
                if field_template.is_required:
                    is_exist_error = True
            else:
                if field_template.content_format is not None:
                    is_fit_format = re.search(field_template.content_format,
                                              field_value)
                    if is_fit_format:
                        if len(field_value) > field_template.max_value:
                            is_exist_error = True
                    else:
                        is_exist_error = True

                if not is_exist_error and len(field_value) > field_template.max_value:
                    is_exist_error = True

            if is_exist_error:
                error_code = field_template.min_error_code
                rejected_value = field_value
        elif field_template.field_type == FieldType.TypeDate:
            time_format = '%Y-%m-%dT%H:%M:%S.%fZ'
            if field_value is not None and field_value != '':
                try:
                    datetime.datetime.strptime(str(field_value), time_format)
                except:
                    error_code = field_template.min_error_code
                    rejected_value = field_value
        elif field_template.field_type == FieldType.TypeObject:
            if field_template.is_required:
                if field_value is None or len(field_value) == 0:
                    error_code = field_template.min_error_code
                    rejected_value = field_value
        elif field_template.field_type == FieldType.TypeUUID:
            if field_template.is_required:
                if field_value is None or field_value == '':
                    error_code = field_template.min_error_code
                    rejected_value = field_value
                    # planSystemKey is different than other UUID fields,
                    # it's actually String type in DB, but other UUID fields is UUID in DB
                    if field_template.field_name != 'planSystemKey':
                        rejected_value = None
                else:
                    if field_template.field_name == 'planSystemKey':
                        is_fit_format = \
                            re.search('[A-Fa-f0-9]{8}-[A-Fa-f0-9]{4}-[A-Fa-f0-9]{4}-[A-Fa-f0-9]{4}-[A-Fa-f0-9]{12}',
                                      field_value)

                        if not is_fit_format:
                            error_code = field_template.min_error_code
                            rejected_value = field_value

        if error_code is not None:
            field_name = field_template.field_name
            if request_index is not None:
                if is_field_details:
                    pre_text = 'details'
                else:
                    pre_text = 'requests'
                field_name = pre_text + '[' + str(request_index) + '].' + field_name
            learning_plan_error_entity = LearningErrorEntity(field_name, error_code, rejected_value)
            return learning_plan_error_entity

    # verify error messages for insert/batch insert/put API
    @staticmethod
    def verify_insert_put_error_messages(api_response_json, expected_error_entity_list):
        error_message = ''

        errors_in_api_response = api_response_json['errors']
        if len(errors_in_api_response) != len(expected_error_entity_list):
            error_message = "the actual list length return from API not as expected!"

        for expected_error_entity in expected_error_entity_list:
            actual_error_dict = jmespath.search("[?field == '{0}'] | [0]".format(expected_error_entity.field_name),
                                                errors_in_api_response)
            if actual_error_dict is None or actual_error_dict['defaultMessage'] != expected_error_entity.error_code \
                    or str(actual_error_dict['rejectedValue']) != str(expected_error_entity.rejected_value):
                error_message = error_message + " The field:" + expected_error_entity.field_name \
                                + "'s error message not as expected!"
        return error_message

    @staticmethod
    def get_expected_learning_data_from_db_by_limit_page(learning_list_from_db, limit, page):
        # default limit value is 50
        if limit is None or limit == '':
            limit = 50

        if page is None:
            page = 1

        list_size = len(learning_list_from_db)

        from_index = (page - 1) * limit
        # if the from index greater than list size, then, there should be empty return list
        if from_index >= list_size:
            return []
        # if the end index greater than list size, then, the end index should be the list size
        end_index = page * limit
        if end_index > list_size:
            end_index = list_size

        return learning_list_from_db[from_index:end_index]


