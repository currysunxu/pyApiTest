from E1_API_Automation.Business.NGPlatform.LearningPlanFieldTemplate import FieldType, FieldValueType
import random
import string
import datetime
import uuid


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
                elif field_value_type == FieldValueType.ExceedMax:
                    field_value = field_template.content_format[-1] + 1
                else:
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
                    if max_value is None:
                        max_value = 2147483647  # 2147483647 is int's maxvalue
                    field_value = max_value + 1
                elif field_value_type == FieldValueType.Valid:
                    if min_value is None:
                        min_value = 1
                    if max_value is None:
                        max_value = 100
                    field_value = random.randint(min_value, max_value)
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
            elif field_value_type == FieldValueType.Valid:
                content_len = random.randint(field_template.min_value, field_template.max_value)
                if field_template.content_format is not None:
                    field_value = ''.join(random.choices(string.ascii_letters + string.digits + '|-', k=content_len))
                else:
                    field_value = ''.join(random.choices(string.printable, k=content_len))
        elif field_template.field_type == FieldType.TypeDate:
            # for date field, if want to construct invalid data, random choose the year or characters
            # if field_value_type == FieldValueType.BelowMin or field_value_type == FieldValueType.ExceedMax:
            #     value_str = ''.join(random.sample(string.ascii_letters, 5))
            #     value_year = datetime.datetime.now().year
            #     field_value = random.choice([value_str, value_year])

            if field_value_type == FieldValueType.Valid:
                field_value = datetime.datetime.now().strftime(field_template.content_format)
                index = field_value.rindex('.')
                field_value = field_value[:index + 1] + field_value[index + 1:index + 4] + 'Z'
        elif field_template.field_type == FieldType.TypeUUID:
            if field_value_type == FieldValueType.BelowMin or field_value_type == FieldValueType.ExceedMax:
                field_value = ''.join(random.sample(string.ascii_letters, 5))
            elif field_value_type == FieldValueType.Valid:
                field_value = uuid.uuid1()
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
            elif entity_class_name == 'LearningPlan' and key == 'systemkey' and expected_field_value is None:
                if actual_key_value is None or actual_key_value == '':
                    error_message = error_message + " The system_key's value should not be null"
            else:
                is_value_same = True
                # some times, the actual time don't have 0 in the end, while there's 0 in expected time, e.g.
                # The actual value is:2019-08-26 16:05:31.82, but the expected value is:2019-08-26 16:05:31.820
                if 'Time' in key and expected_field_value is not None:
                    time_format = '%Y-%m-%dT%H:%M:%S.%fZ'
                    actual_time = datetime.datetime.strptime(str(actual_key_value), time_format)
                    expected_time = datetime.datetime.strptime(str(expected_field_value), time_format)
                    if not is_field_exist or not actual_time == expected_time:
                        is_value_same = False
                else:
                    if not is_field_exist or str(actual_key_value) != str(expected_field_value):
                        is_value_same = False

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

                is_value_same = True
                if 'Time' in key and actual_value is not None:
                    api_time_format = '%Y-%m-%dT%H:%M:%S.%fZ'
                    actual_time = datetime.datetime.strptime(str(actual_value), api_time_format)
                    db_time_format = '%Y-%m-%d %H:%M:%S.%f'
                    expected_time = datetime.datetime.strptime(str(expected_value), db_time_format)

                    if not actual_time == expected_time:
                        is_value_same = False
                elif key == 'details':
                    error_message = error_message + \
                                    LearningCommonUtils.verify_learning_get_api_data_with_db(actual_value,
                                                                                             expected_value)
                elif str(actual_value) != str(expected_value):
                    is_value_same = False

                if key != 'details' and not is_value_same:
                    error_message = error_message + " key:" + key + "'s value in get API not as expected in DB." \
                                                                    "The actual value is:" + str(actual_value) \
                                    + ", but the expected value is:" + expected_value

        return error_message
