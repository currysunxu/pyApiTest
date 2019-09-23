from E1_API_Automation.Business.NGPlatform.LearningPlan import LearningPlan
from E1_API_Automation.Business.NGPlatform.LearningPlanErrorEntity import LearningPlanErrorEntity
from E1_API_Automation.Business.NGPlatform.LearningPlanFieldTemplate import LearningPlanFieldTemplate, FieldType, FieldValueType
from E1_API_Automation.Business.NGPlatform.NGPlatformUtils.LearningCommonUtils import LearningCommonUtils
import random
import string
import datetime
import jmespath
import re


class LearningPlanUtils:
    @staticmethod
    def construct_learning_plan_by_template(learning_plan_template, field_value_type):
        return LearningPlanUtils.\
            construct_learning_plan_by_template_and_is_only_required(learning_plan_template, field_value_type, False)

    @staticmethod
    def construct_learning_plan_with_invalid_value(field_value_type):
        return LearningPlanUtils.construct_learning_plan_by_template(None, field_value_type)

    @staticmethod
    def construct_learning_plan_by_template_and_is_only_required(learning_plan_template, field_value_type, is_need_not_required):
        field_templates = LearningPlanUtils.get_learning_plan_field_templates()
        learning_plan = LearningPlan(None, None, None, None)
        student_plan_items = learning_plan.__dict__
        for item_key in student_plan_items.keys():
            field_name = item_key[len('_' + learning_plan.__class__.__name__ + '__'):]

            is_copy_from_template = False
            field_value = None
            # for these three fields, if template already have value, then, copy them from template,
            # otherwise, randomly generate value
            if field_name in ('product_id', 'plan_business_key', 'bucket_id', 'student_key', 'system_key'):
                if learning_plan_template is not None:
                    field_value = getattr(learning_plan_template, item_key)
                    if field_value is not None:
                        is_copy_from_template = True

            if not is_copy_from_template and field_name != 'system_key':
                field_template = LearningCommonUtils.get_field_template_by_name(field_name, field_templates)
                field_value = LearningCommonUtils.construct_field_value_by_is_only_required(field_template,
                                                                                            field_value_type,
                                                                                            is_need_not_required)
            setattr(learning_plan, item_key, field_value)

        return learning_plan

    @staticmethod
    def construct_random_valid_learning_plan(is_only_required):
        return LearningPlanUtils.construct_learning_plan_by_template_and_is_only_required(None, FieldValueType.Valid,
                                                                                          is_only_required)

    @staticmethod
    def construct_multiple_valid_learning_plans(fixed_learning_plan, number):
        learning_plan_list = []
        for i in range(number):
            learning_plan = LearningPlanUtils.construct_learning_plan_by_template(fixed_learning_plan,
                                                                                  FieldValueType.Valid)
            learning_plan_list.append(learning_plan)

        return learning_plan_list

    @staticmethod
    def construct_learning_plan_template(is_need_student_key):
        product_id = 2
        plan_business_key = 'BatchPlanInsert|BusinessKeyTest|' \
                            + ''.join(random.sample(string.ascii_letters + string.digits + '|-', 5))
        bucket_id = datetime.datetime.now().year

        student_key = None
        if is_need_student_key:
            student_key = 'BatchPlanInsert|StudentKeyTest|' + ''.join(
                random.sample(string.ascii_letters + string.digits + '|-', 5))
        learning_plan_template = LearningPlan(product_id, plan_business_key, bucket_id, student_key)
        return learning_plan_template

    @staticmethod
    def construct_learning_plan_with_empty_fields():
        learning_plan = LearningPlanUtils.construct_learning_plan_by_template(None, FieldValueType.EmptyValue)
        return learning_plan

    @staticmethod
    def construct_learning_plan_dict(learning_plan):
        learning_plan_dict = {}
        student_plan_items = learning_plan.__dict__
        for item_key in student_plan_items.keys():
            item_value = student_plan_items[item_key]
            learning_plan_key = item_key[len('_' + learning_plan.__class__.__name__ + '__'):]
            learning_plan_key = LearningCommonUtils.convert_name_from_lower_case_to_camel_case(learning_plan_key)
            learning_plan_dict[learning_plan_key] = item_value
        return learning_plan_dict

    # construct batch learning plan dict
    @staticmethod
    def construct_batch_learning_plan_dict(learning_plan_list):
        batch_learning_plan_dict = {}
        batch_learning_plan_list = []
        for i in range(len(learning_plan_list)):
            learning_plan = learning_plan_list[i]
            learning_plan_dict = LearningPlanUtils.construct_learning_plan_dict(learning_plan)
            batch_learning_plan_list.append(learning_plan_dict)
        batch_learning_plan_dict['requests'] = batch_learning_plan_list
        return batch_learning_plan_dict

    @staticmethod
    def verify_learning_plan_batch_insert_data(actual_learning_plan_batch_insert_json, expected_learning_plan_list):
        error_message = ''

        if len(actual_learning_plan_batch_insert_json) != len(expected_learning_plan_list):
            error_message = "the actual list length return from batch insert API not as expected!"

        for i in range(len(expected_learning_plan_list)):
            actual_learning_plan = actual_learning_plan_batch_insert_json[i]
            expected_learning_plan = expected_learning_plan_list[i]
            error_message = error_message + LearningCommonUtils.verify_result_with_entity(actual_learning_plan,
                                                                                          expected_learning_plan)
        return error_message

    @staticmethod
    def verify_learning_plan_get_data_with_entity_list(actual_learning_plan_get_json, expected_learning_plan_list):
        error_message = ''

        if len(actual_learning_plan_get_json) != len(expected_learning_plan_list):
            error_message = "the actual list length return using GET API not as expected!"

        for i in range(len(expected_learning_plan_list)):
            expected_learning_plan = expected_learning_plan_list[i]
            actual_learning_plan = \
                jmespath.search("[?systemKey == '{0}'] | [0]".format(expected_learning_plan.system_key), actual_learning_plan_get_json)

            error_message = error_message + LearningCommonUtils.verify_result_with_entity(actual_learning_plan,
                                                                                          expected_learning_plan)
        return error_message

    # get learning plan system key, construct into the entity
    @staticmethod
    def get_learning_plan_system_key(learning_plan_insert_json, learning_plans):
        if isinstance(learning_plans, list):
            for i in range(len(learning_plans)):
                learning_plan = learning_plans[i]
                system_key = learning_plan_insert_json[i]['systemKey']
                learning_plan.system_key = system_key
        else:
            system_key = learning_plan_insert_json['systemKey']
            learning_plans.system_key = system_key
        return learning_plans

    @staticmethod
    def get_expected_learning_plan_from_db_by_limit_page(learning_plan_list_from_db, limit, page):
        # default limit value is 50
        if limit is None:
            limit = 50

        if page is None:
            page = 1

        list_size = len(learning_plan_list_from_db)

        from_index = (page - 1) * limit
        # if the from index greater than list size, then, there should be empty return list
        if from_index >= list_size:
            return []
        # if the end index greater than list size, then, the end index should be the list size
        end_index = page * limit
        if end_index > list_size:
            end_index = list_size

        return learning_plan_list_from_db[from_index:end_index]

    # verify error messages for insert/batch insert/put API
    @staticmethod
    def verify_insert_put_error_messages(api_response_json, learning_plans):
        error_message = ''
        expected_error_entity_list = LearningPlanUtils.get_expected_learning_plan_error_list(learning_plans)

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
    def get_expected_learning_plan_error_list(learning_plans):
        error_entity_list = []
        if isinstance(learning_plans, list):
            for i in range(len(learning_plans)):
                learning_plan = learning_plans[i]
                field_error_entity_list = LearningPlanUtils.get_expected_learning_plan_error_list_by_entity(learning_plan, i)
                error_entity_list = error_entity_list + field_error_entity_list
        else:
            error_entity_list = LearningPlanUtils.get_expected_learning_plan_error_list_by_entity(learning_plans, None)
        return error_entity_list

    @staticmethod
    def get_expected_learning_plan_error_list_by_entity(learning_plan, request_index):
        learning_plan_field_error_entity_list = []
        field_templates = LearningPlanUtils.get_learning_plan_field_templates()
        student_plan_items = learning_plan.__dict__
        for item_key in student_plan_items.keys():
            field_value = student_plan_items[item_key]
            field_name = item_key[len('_' + learning_plan.__class__.__name__ + '__'):]

            if field_name != 'system_key':
                field_template = LearningCommonUtils.get_field_template_by_name(field_name, field_templates)
                field_error_entity = LearningPlanUtils.get_expected_learning_plan_error_entity_by_template(field_value,
                                                                                                           field_template,
                                                                                                           request_index)
                if field_error_entity is not None:
                    learning_plan_field_error_entity_list.append(field_error_entity)
        return learning_plan_field_error_entity_list

    @staticmethod
    def get_learning_plan_field_templates():
        learning_plan_field_templates = []

        product_id_field_tempalte = LearningPlanFieldTemplate('productId', FieldType.TypeInt, True)
        # product_id_field_tempalte.min_value = 1
        product_id_field_tempalte.min_error_code = '4402'
        # product_id_field_tempalte.max_value = 512
        # product_id_field_tempalte.max_error_code = '4403'
        product_id_field_tempalte.content_format = [1, 2, 4, 8, 16, 32, 64]

        regular_expression = '^[A-Za-z0-9|-]+$'
        plan_business_key_field_tempalte = LearningPlanFieldTemplate('planBusinessKey', FieldType.TypeString, True)
        plan_business_key_field_tempalte.min_value = 1
        plan_business_key_field_tempalte.min_error_code = '4404'
        plan_business_key_field_tempalte.max_value = 512
        plan_business_key_field_tempalte.content_format = regular_expression

        bucket_id_field_tempalte = LearningPlanFieldTemplate('bucketId', FieldType.TypeInt, True)
        bucket_id_field_tempalte.min_value = 1
        bucket_id_field_tempalte.min_error_code = '4409'
        bucket_id_field_tempalte.max_value = 2147483647 - 1
        bucket_id_field_tempalte.max_error_code = '4418'

        student_key_field_tempalte = LearningPlanFieldTemplate('studentKey', FieldType.TypeString, True)
        student_key_field_tempalte.min_value = 1
        student_key_field_tempalte.min_error_code = '4401'
        student_key_field_tempalte.max_value = 128
        student_key_field_tempalte.content_format = regular_expression

        plan_type_field_tempalte = LearningPlanFieldTemplate('planType', FieldType.TypeInt, True)
        # plan_type_field_tempalte.min_value = 1
        plan_type_field_tempalte.min_error_code = '4405'
        # plan_type_field_tempalte.max_value = 512
        # plan_type_field_tempalte.max_error_code = '4406'
        plan_type_field_tempalte.content_format = [1, 2, 4, 8, 16, 32]

        route_field_tempalte = LearningPlanFieldTemplate('route', FieldType.TypeString, False)
        route_field_tempalte.min_value = 1
        route_field_tempalte.min_error_code = '4407'
        route_field_tempalte.max_value = 512

        state_field_tempalte = LearningPlanFieldTemplate('state', FieldType.TypeInt, True)
        # state_field_tempalte.max_value = 10
        state_field_tempalte.min_error_code = '4408'
        state_field_tempalte.content_format = [1, 2, 4, 8]

        learning_unit_field_tempalte = LearningPlanFieldTemplate('learningUnit', FieldType.TypeString, False)
        learning_unit_field_tempalte.min_value = 1
        learning_unit_field_tempalte.min_error_code = '4416'
        learning_unit_field_tempalte.max_value = 1024

        created_by_field_tempalte = LearningPlanFieldTemplate('createdBy', FieldType.TypeString, False)
        created_by_field_tempalte.min_value = 0
        created_by_field_tempalte.min_error_code = '4414'
        created_by_field_tempalte.max_value = 128

        last_updated_by_field_tempalte = LearningPlanFieldTemplate('lastUpdatedBy', FieldType.TypeString, False)
        last_updated_by_field_tempalte.min_value = 0
        last_updated_by_field_tempalte.min_error_code = '4415'
        last_updated_by_field_tempalte.max_value = 128

        time_format_expression = '%Y-%m-%dT%H:%M:%S.%fZ'
        created_time_field_tempalte = LearningPlanFieldTemplate('createdTime', FieldType.TypeDate, False)
        # created_time_field_tempalte.min_error_code = '4410'
        created_time_field_tempalte.content_format = time_format_expression

        last_updated_time_field_tempalte = LearningPlanFieldTemplate('lastUpdatedTime', FieldType.TypeDate, False)
        # last_updated_time_field_tempalte.min_error_code = '4411'
        last_updated_time_field_tempalte.content_format = time_format_expression

        start_time_field_tempalte = LearningPlanFieldTemplate('startTime', FieldType.TypeDate, False)
        # start_time_field_tempalte.min_error_code = '4412'
        start_time_field_tempalte.content_format = time_format_expression

        end_time_field_tempalte = LearningPlanFieldTemplate('endTime', FieldType.TypeDate, False)
        # end_time_field_tempalte.min_error_code = '4413'
        end_time_field_tempalte.content_format = time_format_expression

        learning_plan_field_templates.append(product_id_field_tempalte)
        learning_plan_field_templates.append(plan_business_key_field_tempalte)
        learning_plan_field_templates.append(bucket_id_field_tempalte)
        learning_plan_field_templates.append(student_key_field_tempalte)
        learning_plan_field_templates.append(plan_type_field_tempalte)
        learning_plan_field_templates.append(route_field_tempalte)
        learning_plan_field_templates.append(state_field_tempalte)
        learning_plan_field_templates.append(learning_unit_field_tempalte)
        learning_plan_field_templates.append(created_by_field_tempalte)
        learning_plan_field_templates.append(last_updated_by_field_tempalte)
        learning_plan_field_templates.append(created_time_field_tempalte)
        learning_plan_field_templates.append(last_updated_time_field_tempalte)
        learning_plan_field_templates.append(start_time_field_tempalte)
        learning_plan_field_templates.append(end_time_field_tempalte)

        return learning_plan_field_templates

    @staticmethod
    def get_expected_learning_plan_error_entity_by_template(field_value, learning_plan_field_template, request_index):
        error_code = None
        if learning_plan_field_template.field_type == FieldType.TypeInt:
            if field_value is None or field_value == '':
                if learning_plan_field_template.is_required:
                    error_code = learning_plan_field_template.min_error_code
                    rejected_value = 0
            else:
                if learning_plan_field_template.content_format is not None:
                    if field_value not in learning_plan_field_template.content_format:
                        error_code = learning_plan_field_template.min_error_code
                        rejected_value = field_value
                else:
                    if learning_plan_field_template.min_value is not None and field_value < learning_plan_field_template.min_value:
                        error_code = learning_plan_field_template.min_error_code
                        rejected_value = field_value
                    elif field_value > learning_plan_field_template.max_value:
                        error_code = learning_plan_field_template.max_error_code
                        rejected_value = field_value
        elif learning_plan_field_template.field_type == FieldType.TypeString:
            is_exist_error = False
            if field_value is None or field_value == '':
                if learning_plan_field_template.is_required:
                    is_exist_error = True
            else:
                if learning_plan_field_template.content_format is not None:
                    is_fit_format = re.search(learning_plan_field_template.content_format,
                                              field_value)
                    if is_fit_format:
                        if len(field_value) > learning_plan_field_template.max_value:
                            is_exist_error = True
                    else:
                        is_exist_error = True

                if not is_exist_error and len(field_value) > learning_plan_field_template.max_value:
                    is_exist_error = True

            if is_exist_error:
                error_code = learning_plan_field_template.min_error_code
                rejected_value = field_value
        elif learning_plan_field_template.field_type == FieldType.TypeDate:
            time_format = '%Y-%m-%dT%H:%M:%S.%fZ'
            if field_value is not None and field_value != '':
                try:
                    datetime.datetime.strptime(str(field_value), time_format)
                except:
                    error_code = learning_plan_field_template.min_error_code
                    rejected_value = field_value

        if error_code is not None:
            field_name = learning_plan_field_template.field_name
            if request_index is not None:
                field_name = 'requests[' + str(request_index) + '].' + field_name
            learning_plan_error_entity = LearningPlanErrorEntity(field_name, error_code, rejected_value)
            return learning_plan_error_entity

