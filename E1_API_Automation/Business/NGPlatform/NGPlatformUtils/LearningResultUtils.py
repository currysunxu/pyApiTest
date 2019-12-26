from E1_API_Automation.Business.NGPlatform.LearningResultEntity import LearningResultEntity
from E1_API_Automation.Business.NGPlatform.LearningResultDetailEntity import LearningResultDetailEntity
from E1_API_Automation.Business.NGPlatform.LearningFieldTemplate import LearningFieldTemplate, FieldType, FieldValueType
from E1_API_Automation.Business.NGPlatform.NGPlatformUtils.LearningCommonUtils import LearningCommonUtils
from enum import Enum
import random
import string
import uuid


class LearningResultUtils:
    @staticmethod
    def construct_learning_result_valid(details_number):
        return LearningResultUtils.construct_learning_result_valid_by_is_only_required(details_number, False)

    @staticmethod
    def construct_learning_result_valid_by_template(learning_result_template, details_number):
        return LearningResultUtils.construct_learning_result_by_template_and_is_only_required(learning_result_template,
                                                                                              details_number,
                                                                                              FieldValueType.Valid,
                                                                                              False)

    @staticmethod
    def construct_learning_result_valid_by_is_only_required(details_number, is_only_required):
        return LearningResultUtils.construct_learning_result_by_template_and_is_only_required(None, details_number,
                                                                                              FieldValueType.Valid,
                                                                                              is_only_required)

    @staticmethod
    def construct_learning_result_by_value_type(details_number, field_value_type):
        return LearningResultUtils.\
            construct_learning_result_by_template_and_is_only_required(None, details_number, field_value_type, False)

    @staticmethod
    def construct_learning_result_by_template_and_is_only_required(learning_result_template, details_number,
                                                                   field_value_type, is_only_required):
        field_templates = LearningResultUtils.get_learning_result_field_templates()
        learning_result = LearningResultEntity(None, None, None)
        student_result_items = learning_result.__dict__
        for item_key in student_result_items.keys():
            field_name = item_key[len('_' + learning_result.__class__.__name__ + '__'):]

            if field_name != 'details':
                is_copy_from_template = False
                # for these three fields, if template already have value, then, copy them from template,
                # otherwise, randomly generate value
                if field_name in ('product', 'student_key', 'product_module', 'business_key'):
                    if learning_result_template is not None:
                        field_value = getattr(learning_result_template, item_key)
                        if field_value is not None:
                            is_copy_from_template = True

                if not is_copy_from_template:
                    field_template = LearningCommonUtils.get_field_template_by_name(field_name, field_templates)
                    field_value = LearningCommonUtils.construct_field_value_by_is_only_required(field_template,
                                                                                                field_value_type,
                                                                                                is_only_required)
            else:
                field_value = \
                    LearningResultUtils.construct_learning_result_details_by_is_only_required(details_number,
                                                                                              field_value_type,
                                                                                              is_only_required)
            setattr(learning_result, item_key, field_value)

        return learning_result

    @staticmethod
    def construct_learning_result_details_by_is_only_required(details_number, field_value_type, is_only_required):
        detail_field_templates = LearningResultUtils.get_learning_result_detail_field_templates()
        detail_entity_list = []

        # if you want to set empty details, it return empty list
        if details_number is None or details_number == 0:
            return detail_entity_list

        for i in range(details_number):
            learning_result_detail_entity = LearningResultDetailEntity(None)
            result_detail_items = learning_result_detail_entity.__dict__
            for item_key in result_detail_items.keys():
                field_name = item_key[len('_' + learning_result_detail_entity.__class__.__name__ + '__'):]
                field_template = LearningCommonUtils.get_field_template_by_name(field_name, detail_field_templates)
                field_value = LearningCommonUtils.construct_field_value_by_is_only_required(field_template,
                                                                                            field_value_type,
                                                                                            is_only_required)
                setattr(learning_result_detail_entity, item_key, field_value)

            detail_entity_list.append(learning_result_detail_entity)

        return detail_entity_list

    @staticmethod
    def construct_learning_result_template(learning_result_query_type):
        product = random.choice([1, 2, 4, 8, 16, 32, 64])
        student_key = 'resultInsert|StudentKeyTest|' + ''.join(
            random.sample(string.ascii_letters + string.digits + '|-', 5))

        product_module = None
        business_key = None
        if learning_result_query_type != LearningResultQueryType.TypeGetPartition:
            # plan_business_key = 'resultInsert|BusinessKeyTest|' \
            #                     + ''.join(random.sample(string.ascii_letters + string.digits + '|-', 5))
            product_module = random.choice([1, 2, 4, 8, 16, 32])

            if learning_result_query_type == LearningResultQueryType.TypeGetSpecific:
                business_key = 'resultInsert|BusinessKeyTest|' \
                                        + ''.join(random.sample(string.ascii_letters + string.digits + '|-', 5))

        learning_result_template = LearningResultEntity(product, student_key, product_module)
        learning_result_template.business_key = business_key
        return learning_result_template

    @staticmethod
    def construct_learning_result_details_dict(learning_result_details):
        if learning_result_details is not None:
            learning_result_dict_list = []
            for i in range(len(learning_result_details)):
                learning_result_detail = learning_result_details[i]
                learning_result_detail_dict = {}
                learning_result_detail_items = learning_result_detail.__dict__
                for item_key in learning_result_detail_items.keys():
                    learning_result_detail_field_name = item_key[len('_' + learning_result_detail.__class__.__name__ + '__'):]
                    item_value = learning_result_detail_items[item_key]
                    learning_result_detail_field_name = \
                        LearningCommonUtils.convert_name_from_lower_case_to_camel_case(learning_result_detail_field_name)
                    learning_result_detail_dict[learning_result_detail_field_name] = item_value
                learning_result_dict_list.append(learning_result_detail_dict)
            return learning_result_dict_list
        else:
            return None

    @staticmethod
    def construct_learning_result_dict(learning_result):
        learning_result_dict = {}
        learning_result_items = learning_result.__dict__
        for item_key in learning_result_items.keys():
            learning_result_field_name = item_key[len('_' + learning_result.__class__.__name__ + '__'):]
            item_value = learning_result_items[item_key]

            if learning_result_field_name != 'details':
                if learning_result_field_name in ('plan_system_key', 'trace_key'):
                    if item_value is not None:
                        item_value = str(item_value)
                learning_result_field_name = \
                    LearningCommonUtils.convert_name_from_lower_case_to_camel_case(learning_result_field_name)
                learning_result_dict[learning_result_field_name] = item_value
            else:
                detail_dict_list = LearningResultUtils.construct_learning_result_details_dict(item_value)
                learning_result_dict[learning_result_field_name] = detail_dict_list

        return learning_result_dict

    @staticmethod
    def get_learning_result_field_templates():
        learning_result_field_templates = []

        product_id_field_tempalte = LearningFieldTemplate('product', FieldType.TypeInt, True)
        # product_id_field_tempalte.min_value = 1
        product_id_field_tempalte.min_error_code = '4402'
        # product_id_field_tempalte.max_value = 512
        # product_id_field_tempalte.max_error_code = '4403'
        product_id_field_tempalte.content_format = [1, 2, 4, 8, 16, 32, 64]

        regular_expression = '^[A-Za-z0-9|-]+$'
        plan_business_key_field_tempalte = LearningFieldTemplate('businessKey', FieldType.TypeString, True)
        plan_business_key_field_tempalte.min_value = 1
        plan_business_key_field_tempalte.min_error_code = '4404'
        plan_business_key_field_tempalte.max_value = 512
        plan_business_key_field_tempalte.content_format = regular_expression

        # plan_system_key_field_tempalte = LearningFieldTemplate('planSystemKey', FieldType.TypeUUID, True)
        # plan_system_key_field_tempalte.min_error_code = '4419'

        student_key_field_tempalte = LearningFieldTemplate('studentKey', FieldType.TypeString, True)
        student_key_field_tempalte.min_value = 1
        student_key_field_tempalte.min_error_code = '4401'
        student_key_field_tempalte.max_value = 128
        student_key_field_tempalte.content_format = regular_expression

        plan_type_field_tempalte = LearningFieldTemplate('productModule', FieldType.TypeInt, True)
        # plan_type_field_tempalte.min_value = 1
        plan_type_field_tempalte.min_error_code = '4405'
        # plan_type_field_tempalte.max_value = 512
        # plan_type_field_tempalte.max_error_code = '4406'
        plan_type_field_tempalte.content_format = [1, 2, 4, 8, 16, 32]

        # trace_key_field_tempalte = LearningFieldTemplate('traceKey', FieldType.TypeUUID, True)
        # trace_key_field_tempalte.min_error_code = '4423'

        route_field_tempalte = LearningFieldTemplate('route', FieldType.TypeObject, False)
        # route_field_tempalte.min_value = 1
        # route_field_tempalte.min_error_code = '4407'
        # route_field_tempalte.max_value = 512

        # atomic_key_field_tempalte = LearningFieldTemplate('atomicKey', FieldType.TypeString, False)
        # atomic_key_field_tempalte.min_value = 1
        # atomic_key_field_tempalte.min_error_code = '4422'
        # atomic_key_field_tempalte.max_value = 512
        # atomic_key_field_tempalte.content_format = regular_expression

        expected_score_field_tempalte = LearningFieldTemplate('expectedScore', FieldType.TypeInt, False)

        actual_score_field_tempalte = LearningFieldTemplate('actualScore', FieldType.TypeInt, False)

        created_by_field_tempalte = LearningFieldTemplate('createdBy', FieldType.TypeString, False)
        created_by_field_tempalte.min_value = 1
        created_by_field_tempalte.min_error_code = '4414'
        created_by_field_tempalte.max_value = 128

        extension_field_tempalte = LearningFieldTemplate('extension', FieldType.TypeObject, False)

        details_field_tempalte = LearningFieldTemplate('details', FieldType.TypeObject, True)
        details_field_tempalte.min_value = 1
        details_field_tempalte.min_error_code = '4425'

        duration_field_tempalte = LearningFieldTemplate('duration', FieldType.TypeInt, False)

        time_format_expression = '%Y-%m-%dT%H:%M:%S.%fZ'
        start_time_field_tempalte = LearningFieldTemplate('startTime', FieldType.TypeDate, False)
        start_time_field_tempalte.content_format = time_format_expression

        end_time_field_tempalte = LearningFieldTemplate('endTime', FieldType.TypeDate, False)
        end_time_field_tempalte.content_format = time_format_expression

        learning_result_field_templates.append(product_id_field_tempalte)
        learning_result_field_templates.append(plan_business_key_field_tempalte)
        # learning_result_field_templates.append(plan_system_key_field_tempalte)
        learning_result_field_templates.append(student_key_field_tempalte)
        learning_result_field_templates.append(plan_type_field_tempalte)
        # learning_result_field_templates.append(trace_key_field_tempalte)
        learning_result_field_templates.append(route_field_tempalte)
        # learning_result_field_templates.append(atomic_key_field_tempalte)
        learning_result_field_templates.append(expected_score_field_tempalte)
        learning_result_field_templates.append(actual_score_field_tempalte)
        learning_result_field_templates.append(created_by_field_tempalte)
        learning_result_field_templates.append(extension_field_tempalte)
        learning_result_field_templates.append(details_field_tempalte)
        learning_result_field_templates.append(duration_field_tempalte)
        learning_result_field_templates.append(start_time_field_tempalte)
        learning_result_field_templates.append(end_time_field_tempalte)

        return learning_result_field_templates

    @staticmethod
    def get_learning_result_detail_field_templates():
        learning_result_detail_field_templates = []

        regular_expression = '^[A-Za-z0-9|-]+$'
        activity_key_field_tempalte = LearningFieldTemplate('activityKey', FieldType.TypeString, True)
        activity_key_field_tempalte.min_value = 1
        activity_key_field_tempalte.min_error_code = '4420'
        activity_key_field_tempalte.max_value = 128
        activity_key_field_tempalte.content_format = regular_expression

        activity_version_field_tempalte = LearningFieldTemplate('activityVersion', FieldType.TypeString, False)
        activity_version_field_tempalte.min_value = 0
        activity_version_field_tempalte.min_error_code = '4426'
        activity_version_field_tempalte.max_value = 256

        question_key_field_tempalte = LearningFieldTemplate('questionKey', FieldType.TypeString, False)
        question_key_field_tempalte.min_value = 1
        question_key_field_tempalte.min_error_code = '4421'
        question_key_field_tempalte.max_value = 512
        # question_key_field_tempalte.content_format = regular_expression

        question_version_field_tempalte = LearningFieldTemplate('questionVersion', FieldType.TypeString, False)
        question_version_field_tempalte.min_value = 0
        question_version_field_tempalte.min_error_code = '4427'
        question_version_field_tempalte.max_value = 256

        answer_field_tempalte = LearningFieldTemplate('answer', FieldType.TypeObject, False)
        # answer_field_tempalte.min_value = 1
        # answer_field_tempalte.min_error_code = '4424'
        # answer_field_tempalte.max_value = 1024

        extension_field_tempalte = LearningFieldTemplate('extension', FieldType.TypeObject, False)

        expected_score_field_tempalte = LearningFieldTemplate('expectedScore', FieldType.TypeInt, False)

        actual_score_field_tempalte = LearningFieldTemplate('actualScore', FieldType.TypeInt, False)

        duration_field_tempalte = LearningFieldTemplate('duration', FieldType.TypeInt, False)

        time_format_expression = '%Y-%m-%dT%H:%M:%S.%fZ'
        start_time_field_tempalte = LearningFieldTemplate('startTime', FieldType.TypeDate, False)
        start_time_field_tempalte.content_format = time_format_expression

        end_time_field_tempalte = LearningFieldTemplate('endTime', FieldType.TypeDate, False)
        end_time_field_tempalte.content_format = time_format_expression

        learning_result_detail_field_templates.append(activity_key_field_tempalte)
        learning_result_detail_field_templates.append(activity_version_field_tempalte)
        learning_result_detail_field_templates.append(question_key_field_tempalte)
        learning_result_detail_field_templates.append(question_version_field_tempalte)
        learning_result_detail_field_templates.append(answer_field_tempalte)
        learning_result_detail_field_templates.append(extension_field_tempalte)
        learning_result_detail_field_templates.append(expected_score_field_tempalte)
        learning_result_detail_field_templates.append(actual_score_field_tempalte)
        learning_result_detail_field_templates.append(duration_field_tempalte)
        learning_result_detail_field_templates.append(start_time_field_tempalte)
        learning_result_detail_field_templates.append(end_time_field_tempalte)

        return learning_result_detail_field_templates

    @staticmethod
    def get_expected_learning_result_error_list_by_entity(learning_entity, field_templates, request_index,
                                                          is_field_details):
        learning_result_field_error_entity_list = []
        entity_items = learning_entity.__dict__
        for item_key in entity_items.keys():
            field_value = entity_items[item_key]
            field_name = item_key[len('_' + learning_entity.__class__.__name__ + '__'):]

            # for non details fields or detail field and field value as None or empty, it will check the field directly
            if field_name != 'details' or (field_name == 'details' and (field_value is None or len(field_value) == 0)):
                field_template = LearningCommonUtils.get_field_template_by_name(field_name, field_templates)
                field_error_entity = \
                    LearningCommonUtils.get_expected_learning_error_entity_by_template(field_value,
                                                                                       field_template,
                                                                                       request_index,
                                                                                       is_field_details)
                if field_error_entity is not None:
                    learning_result_field_error_entity_list.append(field_error_entity)
            else:
                # for details field, check each field in the details list
                detail_field_templates = LearningResultUtils.get_learning_result_detail_field_templates()
                for i in range(len(field_value)):
                    detail_entity = field_value[i]
                    field_error_entity_list = LearningResultUtils.get_expected_learning_result_error_list_by_entity(
                        detail_entity, detail_field_templates, i, True)
                    learning_result_field_error_entity_list = \
                        learning_result_field_error_entity_list + field_error_entity_list

        return learning_result_field_error_entity_list

    @staticmethod
    def get_expected_learning_result_error_list(learning_result_entity):
        field_templates = LearningResultUtils.get_learning_result_field_templates()
        error_entity_list = \
            LearningResultUtils.get_expected_learning_result_error_list_by_entity(learning_result_entity,
                                                                                  field_templates, None, False)
        return error_entity_list

    @staticmethod
    def verify_result_insert_error_messages(api_response_json, learning_result):
        expected_error_entity_list = LearningResultUtils.get_expected_learning_result_error_list(learning_result)
        return LearningCommonUtils.verify_insert_put_error_messages(api_response_json, expected_error_entity_list)


class LearningResultQueryType(Enum):
    TypeGetPartition = 'GetPartitionResults'
    TypeGetUser = 'GetUserResults'
    TypeGetSpecific = 'GetSpecificResult'
