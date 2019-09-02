from E1_API_Automation.Business.NGPlatform.LearningPlan import LearningPlan
from E1_API_Automation.Business.NGPlatform.LearningPlanErrorEntity import LearningPlanErrorEntity
from E1_API_Automation.Business.NGPlatform.LearningPlanFieldTemplate import LearningPlanFieldTemplate, FieldType, FieldValueType
import random
import string
import datetime
import jmespath
import re


class LearningPlanUtils:
    @staticmethod
    def construct_valid_learning_plan_based_on_entity(fixed_learning_plan, is_need_not_required):
        if fixed_learning_plan is not None:
            product_id = fixed_learning_plan.product_id
            plan_business_key = fixed_learning_plan.plan_business_key
            bucket_id = fixed_learning_plan.bucket_id
            student_key = fixed_learning_plan.student_key
        else:
            product_id = random.randint(1, 512)
            plan_business_key = 'PlanBusinessKeyTest|' \
                                + ''.join(random.sample(string.ascii_letters + string.digits + '|-', 5))
            bucket_id = random.randint(1, 2147483647 - 1)  # 2147483647 is int's maxvalue
            student_key = 'StudentKeyTest|' + ''.join(random.sample(string.ascii_letters + string.digits + '|-', 5))

        # when fixed_learning_plan is not null, student_key might be None
        if student_key is None:
            student_key = 'StudentKeyTest|' + ''.join(random.sample(string.ascii_letters + string.digits + '|-', 5))

        plan_type = random.randint(1, 512)
        state = random.randint(0, 10)
        learning_plan = LearningPlan(product_id, plan_business_key, bucket_id, student_key)
        learning_plan.plan_type = plan_type
        learning_plan.state = state

        if fixed_learning_plan is not None and fixed_learning_plan.system_key is not None:
            learning_plan.system_key = fixed_learning_plan.system_key

        if is_need_not_required:
            learning_plan.route = 'route_test' + ''.join(random.sample(string.printable, 10))
            learning_plan.learning_unit = 'learning_unit_test' + ''.join(random.sample(string.printable, 10))
            learning_plan.created_by = 'created_by_test' + ''.join(random.sample(string.printable, 10))
            learning_plan.last_updated_by = 'last_updated_by_test' + ''.join(random.sample(string.printable, 10))

            time_format = '%Y-%m-%d %H:%M:%S.%f'
            # time_format = '%Y-%m-%d %H:%M:%S'
            learning_plan.created_time = datetime.datetime.now().strftime(time_format)[:-3]
            learning_plan.last_updated_time = datetime.datetime.now().strftime(time_format)[:-3]
            learning_plan.start_time = datetime.datetime.now().strftime(time_format)[:-3]
            learning_plan.end_time = datetime.datetime.now().strftime(time_format)[:-3]
        return learning_plan

    @staticmethod
    def construct_field_value(field_template, field_value_type):
        field_value = None
        if field_template.field_type == FieldType.TypeInt:
            if field_value_type == FieldValueType.BelowMin:
                if field_template.min_value is not None:
                    field_value = field_template.min_value - 1
                else:
                    field_value = -1
            elif field_value_type == FieldValueType.ExceedMax:
                field_value = field_template.max_value + 1
        if field_template.field_type == FieldType.TypeString:
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
        if field_template.field_type == FieldType.TypeDate:
            # for date field, if want to construct invalid data, random choose the year or characters
            if field_value_type == FieldValueType.BelowMin or field_value_type == FieldValueType.ExceedMax:
                value_str = ''.join(random.sample(string.ascii_letters, 5))
                value_year = datetime.datetime.now().year
                field_value = random.choice([value_str, value_year])
        return field_value

    @staticmethod
    def construct_learning_plan_with_invalid_value(field_value_type):
        field_templates = LearningPlanUtils.get_learning_plan_field_templates()
        learning_plan = LearningPlan(None, None, None, None)
        student_plan_items = learning_plan.__dict__
        for item_key in student_plan_items.keys():
            field_name = item_key[len('_' + learning_plan.__class__.__name__ + '__'):]

            if field_name != 'system_key':
                field_template = LearningPlanUtils.get_field_template_by_name(field_name, field_templates)
                field_value = LearningPlanUtils.construct_field_value(field_template, field_value_type)
                setattr(learning_plan, item_key, field_value)

        return learning_plan

    @staticmethod
    def construct_random_valid_learning_plan(is_need_not_required):
        return LearningPlanUtils.construct_valid_learning_plan_based_on_entity(None, is_need_not_required)

    @staticmethod
    def construct_multiple_valid_learning_plans(fixed_learning_plan, number):
        learning_plan_list = []
        for i in range(number):
            learning_plan = LearningPlanUtils.construct_valid_learning_plan_based_on_entity(fixed_learning_plan, True)
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
        learning_plan = LearningPlan('', '', '', '')
        learning_plan.plan_type = ''
        learning_plan.state = ''
        learning_plan.route = ''
        learning_plan.learning_unit = ''
        learning_plan.created_time = ''
        learning_plan.created_by = ''
        learning_plan.last_updated_time = ''
        learning_plan.last_updated_by = ''
        learning_plan.start_time = ''
        learning_plan.end_time = ''
        return learning_plan

    @staticmethod
    def construct_learning_plan_dict(learning_plan):
        learning_plan_dict = {}
        student_plan_items = learning_plan.__dict__
        for item_key in student_plan_items.keys():
            item_value = student_plan_items[item_key]
            learning_plan_key = item_key[len('_' + learning_plan.__class__.__name__ + '__'):]
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
    def verify_learning_plan_data(actual_learning_plan_json, expected_learning_plan):
        error_message = ''
        for key in actual_learning_plan_json.keys():
            actual_key_value = actual_learning_plan_json[key]
            learning_plan_private_field_name = '_LearningPlan__' + key

            is_field_exist = False
            if hasattr(expected_learning_plan, learning_plan_private_field_name):
                is_field_exist = True
                expected_field_value = getattr(expected_learning_plan, learning_plan_private_field_name)
                if '_time' in key and actual_key_value == '':
                    actual_key_value = None

            if key == 'system_key' and expected_field_value is None:
                if actual_key_value is None or actual_key_value == '':
                    error_message = error_message + " The system_key's value should not be null"
            else:
                is_value_same = True
                # some times, the actual time don't have 0 in the end, while there's 0 in expected time, e.g.
                # The actual value is:2019-08-26 16:05:31.82, but the expected value is:2019-08-26 16:05:31.820
                if '_time' in key and expected_field_value is not None:
                    time_format = '%Y-%m-%d %H:%M:%S.%f'
                    actual_time = datetime.datetime.strptime(str(actual_key_value), time_format)
                    expected_time = datetime.datetime.strptime(str(expected_field_value), time_format)
                    if not is_field_exist or not actual_time == expected_time:
                        is_value_same = False
                else:
                    if not is_field_exist or str(actual_key_value) != str(expected_field_value):
                        is_value_same = False

                if not is_value_same:
                    error_message = error_message + " key:" + key + "'s value in API not as expected in learning plan." \
                                                                    "The actual value is:" + str(actual_key_value) \
                                    + ", but the expected value is:" + expected_field_value
        return error_message

    @staticmethod
    def verify_learning_plan_batch_insert_data(actual_learning_plan_batch_insert_json, expected_learning_plan_list):
        error_message = ''

        if len(actual_learning_plan_batch_insert_json) != len(expected_learning_plan_list):
            error_message = "the actual list length return from batch insert API not as expected!"

        for i in range(len(expected_learning_plan_list)):
            actual_learning_plan = actual_learning_plan_batch_insert_json[i]
            expected_learning_plan = expected_learning_plan_list[i]
            error_message = error_message + LearningPlanUtils.verify_learning_plan_data(actual_learning_plan,
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
                jmespath.search("[?system_key == '{0}'] | [0]".format(expected_learning_plan.system_key), actual_learning_plan_get_json)

            error_message = error_message + LearningPlanUtils.verify_learning_plan_data(actual_learning_plan,
                                                                                        expected_learning_plan)
        return error_message

    # get learning plan system key, construct into the entity
    @staticmethod
    def get_learning_plan_system_key(learning_plan_insert_json, learning_plans):
        if isinstance(learning_plans, list):
            for i in range(len(learning_plans)):
                learning_plan = learning_plans[i]
                system_key = learning_plan_insert_json[i]['system_key']
                learning_plan.system_key = system_key
        else:
            system_key = learning_plan_insert_json['system_key']
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

    # verify learning plan get API result with DB data
    @staticmethod
    def verify_learning_plan_get_api_data_with_db(actual_learning_plan_get_api_json, expected_db_learning_plan_list):
        error_message = ''

        if len(actual_learning_plan_get_api_json) != len(expected_db_learning_plan_list):
            error_message = "the actual list length return from API not as expected!"

        for i in range(len(actual_learning_plan_get_api_json)):
            actual_learning_plan = actual_learning_plan_get_api_json[i]
            expected_db_learning_plan = expected_db_learning_plan_list[i]

            for key in actual_learning_plan.keys():
                actual_value = actual_learning_plan[key]
                expected_value = expected_db_learning_plan[key.replace('_', '')]

                is_value_same = True
                if '_time' in key and actual_value is not None:
                    time_format = '%Y-%m-%d %H:%M:%S.%f'
                    actual_time = datetime.datetime.strptime(str(actual_value), time_format)
                    expected_time = datetime.datetime.strptime(str(expected_value), time_format)

                    if not actual_time == expected_time:
                        is_value_same = False
                elif str(actual_value) != str(expected_value):
                    is_value_same = False

                if not is_value_same:
                    error_message = error_message + " key:" + key + "'s value in get API not as expected in DB." \
                                                                    "The actual value is:" + str(actual_value) \
                                    + ", but the expected value is:" + expected_value

        return error_message

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
                field_template = LearningPlanUtils.get_field_template_by_name(field_name, field_templates)
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
        plan_type_field_tempalte.min_value = 1
        plan_type_field_tempalte.min_error_code = '4405'
        plan_type_field_tempalte.max_value = 512
        plan_type_field_tempalte.max_error_code = '4406'

        route_field_tempalte = LearningPlanFieldTemplate('route', FieldType.TypeString, False)
        route_field_tempalte.min_value = 1
        route_field_tempalte.min_error_code = '4407'
        route_field_tempalte.max_value = 512

        state_field_tempalte = LearningPlanFieldTemplate('state', FieldType.TypeInt, True)
        state_field_tempalte.max_value = 10
        state_field_tempalte.max_error_code = '4408'

        learning_unit_field_tempalte = LearningPlanFieldTemplate('learningUnit', FieldType.TypeString, False)
        learning_unit_field_tempalte.min_value = 1
        learning_unit_field_tempalte.min_error_code = '4416'
        learning_unit_field_tempalte.max_value = 1024

        created_by_field_tempalte = LearningPlanFieldTemplate('createdBy', FieldType.TypeString, False)
        created_by_field_tempalte.min_value = 1
        created_by_field_tempalte.min_error_code = '4414'
        created_by_field_tempalte.max_value = 128

        last_updated_by_field_tempalte = LearningPlanFieldTemplate('lastUpdatedBy', FieldType.TypeString, False)
        last_updated_by_field_tempalte.min_value = 1
        last_updated_by_field_tempalte.min_error_code = '4415'
        last_updated_by_field_tempalte.max_value = 128

        created_time_field_tempalte = LearningPlanFieldTemplate('createdTime', FieldType.TypeDate, False)
        created_time_field_tempalte.min_error_code = '4410'

        last_updated_time_field_tempalte = LearningPlanFieldTemplate('lastupdatedTime', FieldType.TypeDate, False)
        last_updated_time_field_tempalte.min_error_code = '4411'

        start_time_field_tempalte = LearningPlanFieldTemplate('startTime', FieldType.TypeDate, False)
        start_time_field_tempalte.min_error_code = '4412'

        end_time_field_tempalte = LearningPlanFieldTemplate('endTime', FieldType.TypeDate, False)
        end_time_field_tempalte.min_error_code = '4413'

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
    def get_field_template_by_name(field_name, field_templates):
        for field_template in field_templates:
            if field_template.field_name.lower() == field_name.replace('_', ''):
                return field_template

    @staticmethod
    def get_expected_learning_plan_error_entity_by_template(field_value, learning_plan_field_template, request_index):
        error_code = None
        if learning_plan_field_template.field_type == FieldType.TypeInt:
            if field_value is None or field_value == '':
                if learning_plan_field_template.is_required:
                    error_code = learning_plan_field_template.min_error_code
                    rejected_value = 0
            elif learning_plan_field_template.min_value is not None and field_value < learning_plan_field_template.min_value:
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
            time_format = '%Y-%m-%d %H:%M:%S.%f'
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

