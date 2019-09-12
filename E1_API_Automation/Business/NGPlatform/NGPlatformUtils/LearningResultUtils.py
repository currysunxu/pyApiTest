from E1_API_Automation.Business.NGPlatform.LearningResultEntity import LearningResultEntity
from E1_API_Automation.Business.NGPlatform.LearningResultDetailEntity import LearningResultDetailEntity
from E1_API_Automation.Business.NGPlatform.LearningPlanFieldTemplate import LearningPlanFieldTemplate, FieldType, FieldValueType
import random
import string
import datetime
import uuid
import jmespath
import re


class LearningResultUtils:
    @staticmethod
    def construct_field_value(field_template, field_value_type):
        field_value = None
        if field_template.field_type == FieldType.TypeInt:
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
            if field_value_type == FieldValueType.BelowMin or field_value_type == FieldValueType.ExceedMax:
                value_str = ''.join(random.sample(string.ascii_letters, 5))
                value_year = datetime.datetime.now().year
                field_value = random.choice([value_str, value_year])
            elif field_value_type == FieldValueType.Valid:
                field_value = datetime.datetime.now().strftime(field_template.content_format)[:-4]+'Z'
        elif field_template.field_type == FieldType.TypeUUID:
            if field_value_type == FieldValueType.BelowMin or field_value_type == FieldValueType.ExceedMax:
                field_value = ''.join(random.sample(string.ascii_letters, 5))
            elif field_value_type == FieldValueType.Valid:
                field_value = uuid.uuid1()
        return field_value

    @staticmethod
    def construct_learning_result_valid(details_number):
        field_templates = LearningResultUtils.get_learning_result_field_templates()
        learning_result = LearningResultEntity(None, None, None)
        student_plan_items = learning_result.__dict__
        for item_key in student_plan_items.keys():
            field_name = item_key[len('_' + learning_result.__class__.__name__ + '__'):]

            if field_name != 'details':
                field_template = LearningResultUtils.get_field_template_by_name(field_name, field_templates)
                field_value = LearningResultUtils.construct_field_value(field_template, FieldValueType.Valid)
            else:
                field_value = LearningResultUtils.construct_learning_result_details(FieldValueType.Valid,
                                                                                    details_number)
            setattr(learning_result, item_key, field_value)

        return learning_result

    @staticmethod
    def construct_learning_result_details(field_value_type, details_number):
        detail_field_templates = LearningResultUtils.get_learning_result_detail_field_templates()
        detail_entity_list = []
        for i in range(details_number):
            learning_result_detail_entity = LearningResultDetailEntity(None)
            result_detail_items = learning_result_detail_entity.__dict__
            for item_key in result_detail_items.keys():
                field_name = item_key[len('_' + learning_result_detail_entity.__class__.__name__ + '__'):]
                field_template = LearningResultUtils.get_field_template_by_name(field_name, detail_field_templates)
                field_value = LearningResultUtils.construct_field_value(field_template, field_value_type)
                setattr(learning_result_detail_entity, item_key, field_value)

            detail_entity_list.append(learning_result_detail_entity)

        return detail_entity_list

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
                        LearningResultUtils.convert_name_from_lower_case_to_camel_case(learning_result_detail_field_name)
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
                    LearningResultUtils.convert_name_from_lower_case_to_camel_case(learning_result_field_name)
                learning_result_dict[learning_result_field_name] = item_value
            else:
                detail_dict_list = LearningResultUtils.construct_learning_result_details_dict(item_value)
                learning_result_dict[learning_result_field_name] = detail_dict_list

        return learning_result_dict

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
    def get_learning_result_field_templates():
        learning_result_field_templates = []

        product_id_field_tempalte = LearningPlanFieldTemplate('productId', FieldType.TypeInt, True)
        product_id_field_tempalte.min_value = 1
        product_id_field_tempalte.min_error_code = '4402'
        product_id_field_tempalte.max_value = 512
        product_id_field_tempalte.max_error_code = '4403'

        regular_expression = '^[A-Za-z0-9|-]+$'
        plan_business_key_field_tempalte = LearningPlanFieldTemplate('planBusinessKey', FieldType.TypeString, True)
        plan_business_key_field_tempalte.min_value = 1
        plan_business_key_field_tempalte.min_error_code = '4404'
        plan_business_key_field_tempalte.max_value = 512
        plan_business_key_field_tempalte.content_format = regular_expression

        plan_system_key_field_tempalte = LearningPlanFieldTemplate('planSystemKey', FieldType.TypeUUID, True)
        plan_system_key_field_tempalte.min_error_code = '4419'

        student_key_field_tempalte = LearningPlanFieldTemplate('studentKey', FieldType.TypeString, True)
        student_key_field_tempalte.min_value = 1
        student_key_field_tempalte.min_error_code = '4401'
        student_key_field_tempalte.max_value = 128
        student_key_field_tempalte.content_format = regular_expression

        plan_type_field_tempalte = LearningPlanFieldTemplate('planType', FieldType.TypeInt, True)
        plan_type_field_tempalte.min_value = 1
        plan_type_field_tempalte.min_error_code = '4405'
        plan_type_field_tempalte.max_value = 512
        plan_type_field_tempalte.max_error_code = '4406'

        trace_key_field_tempalte = LearningPlanFieldTemplate('traceKey', FieldType.TypeUUID, True)
        trace_key_field_tempalte.min_error_code = '4423'

        route_field_tempalte = LearningPlanFieldTemplate('route', FieldType.TypeString, False)
        route_field_tempalte.min_value = 1
        route_field_tempalte.min_error_code = '4407'
        route_field_tempalte.max_value = 512

        atomic_key_field_tempalte = LearningPlanFieldTemplate('atomicKey', FieldType.TypeString, False)
        atomic_key_field_tempalte.min_value = 1
        atomic_key_field_tempalte.min_error_code = '4422'
        atomic_key_field_tempalte.max_value = 512
        atomic_key_field_tempalte.content_format = regular_expression

        expected_score_field_tempalte = LearningPlanFieldTemplate('expectedScore', FieldType.TypeInt, False)

        actual_score_field_tempalte = LearningPlanFieldTemplate('actualScore', FieldType.TypeInt, False)

        created_by_field_tempalte = LearningPlanFieldTemplate('createdBy', FieldType.TypeString, False)
        created_by_field_tempalte.min_value = 1
        created_by_field_tempalte.min_error_code = '4414'
        created_by_field_tempalte.max_value = 128

        details_field_tempalte = LearningPlanFieldTemplate('details', FieldType.TypeObject, True)
        details_field_tempalte.min_value = 1
        details_field_tempalte.min_error_code = '4425'

        learning_result_field_templates.append(product_id_field_tempalte)
        learning_result_field_templates.append(plan_business_key_field_tempalte)
        learning_result_field_templates.append(plan_system_key_field_tempalte)
        learning_result_field_templates.append(student_key_field_tempalte)
        learning_result_field_templates.append(plan_type_field_tempalte)
        learning_result_field_templates.append(trace_key_field_tempalte)
        learning_result_field_templates.append(route_field_tempalte)
        learning_result_field_templates.append(atomic_key_field_tempalte)
        learning_result_field_templates.append(expected_score_field_tempalte)
        learning_result_field_templates.append(actual_score_field_tempalte)
        learning_result_field_templates.append(created_by_field_tempalte)
        learning_result_field_templates.append(details_field_tempalte)

        return learning_result_field_templates

    @staticmethod
    def get_learning_result_detail_field_templates():
        learning_result_detail_field_templates = []

        regular_expression = '^[A-Za-z0-9|-]+$'
        activity_key_field_tempalte = LearningPlanFieldTemplate('activityKey', FieldType.TypeString, True)
        activity_key_field_tempalte.min_value = 1
        activity_key_field_tempalte.min_error_code = '4420'
        activity_key_field_tempalte.max_value = 128
        activity_key_field_tempalte.content_format = regular_expression

        activity_version_field_tempalte = LearningPlanFieldTemplate('activityVersion', FieldType.TypeInt, False)

        question_key_field_tempalte = LearningPlanFieldTemplate('questionKey', FieldType.TypeString, False)
        question_key_field_tempalte.min_value = 1
        question_key_field_tempalte.min_error_code = '4421'
        question_key_field_tempalte.max_value = 128
        question_key_field_tempalte.content_format = regular_expression

        question_version_field_tempalte = LearningPlanFieldTemplate('questionVersion', FieldType.TypeInt, False)

        answer_field_tempalte = LearningPlanFieldTemplate('answer', FieldType.TypeString, False)
        answer_field_tempalte.min_value = 1
        answer_field_tempalte.min_error_code = '4424'
        answer_field_tempalte.max_value = 1024

        expected_score_field_tempalte = LearningPlanFieldTemplate('expectedScore', FieldType.TypeInt, False)

        actual_score_field_tempalte = LearningPlanFieldTemplate('actualScore', FieldType.TypeInt, False)

        duration_field_tempalte = LearningPlanFieldTemplate('duration', FieldType.TypeInt, False)

        time_format_expression = '%Y-%m-%dT%H:%M:%S.%fZ'
        start_time_field_tempalte = LearningPlanFieldTemplate('startTime', FieldType.TypeDate, False)
        start_time_field_tempalte.content_format = time_format_expression

        end_time_field_tempalte = LearningPlanFieldTemplate('endTime', FieldType.TypeDate, False)
        end_time_field_tempalte.content_format = time_format_expression

        learning_result_detail_field_templates.append(activity_key_field_tempalte)
        learning_result_detail_field_templates.append(activity_version_field_tempalte)
        learning_result_detail_field_templates.append(question_key_field_tempalte)
        learning_result_detail_field_templates.append(question_version_field_tempalte)
        learning_result_detail_field_templates.append(answer_field_tempalte)
        learning_result_detail_field_templates.append(expected_score_field_tempalte)
        learning_result_detail_field_templates.append(actual_score_field_tempalte)
        learning_result_detail_field_templates.append(duration_field_tempalte)
        learning_result_detail_field_templates.append(start_time_field_tempalte)
        learning_result_detail_field_templates.append(end_time_field_tempalte)

        return learning_result_detail_field_templates

    @staticmethod
    def get_field_template_by_name(field_name, field_templates):
        for field_template in field_templates:
            if field_template.field_name.lower() == field_name.replace('_', ''):
                return field_template

