from E1_API_Automation.Business.HFV35.LearningPlan import LearningPlan
import random
import string
import datetime


class LearningPlanUtils:
    @staticmethod
    def construct_random_valid_learning_plan(is_need_not_required):
        product_id = random.randint(1, 512)
        plan_business_key = 'PlanBusinessKeyTest|' + ''.join(random.sample(string.ascii_letters + string.digits + '|-', 5))
        bucket_id = random.randint(1, 2147483647 - 1)  #2147483647 is int's maxvalue
        student_key = 'StudentKeyTest|' + ''.join(random.sample(string.ascii_letters + string.digits + '|-', 5))
        plan_type = random.randint(1, 512)
        state = random.randint(0, 10)
        print("product_id:"+str(product_id))
        print("plan_business_key:" + plan_business_key)
        print("bucket_id:" + str(bucket_id))
        print("student_key:" + student_key)
        learning_plan = LearningPlan(product_id, plan_business_key, bucket_id, student_key, plan_type, state)

        if is_need_not_required:
            learning_plan.route = 'route_test' + ''.join(random.sample(string.printable, 10))
            learning_plan.learning_unit = 'learning_unit_test' + ''.join(random.sample(string.printable, 10))
            learning_plan.created_by = 'created_by_test' + ''.join(random.sample(string.printable, 10))
            learning_plan.last_updated_by = 'last_updated_by_test' + ''.join(random.sample(string.printable, 10))

            # time_format = '%Y-%m-%d %H:%M:%S.%f'
            time_format = '%Y-%m-%d %H:%M:%S'
            learning_plan.created_time = datetime.datetime.now().strftime(time_format)
            learning_plan.last_updated_time = datetime.datetime.now().strftime(time_format)
            learning_plan.start_time = datetime.datetime.now().strftime(time_format)
            learning_plan.end_time = datetime.datetime.now().strftime(time_format)
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

    @staticmethod
    def verify_learning_plan_data(actual_learning_plan_json, expected_learning_plan):
        error_message = ''
        for key in actual_learning_plan_json.keys():
            actual_key_value = actual_learning_plan_json[key]
            if key != 'system_key':
                learning_plan_private_field_name = '_LearningPlan__' + key
                is_field_exist = False
                if hasattr(expected_learning_plan, learning_plan_private_field_name):
                    is_field_exist = True
                    expected_field_value = getattr(expected_learning_plan, learning_plan_private_field_name)
                    if '_time' in key and expected_field_value is None:
                        expected_field_value = ''
                if not is_field_exist or str(actual_key_value) != str(expected_field_value):
                    error_message = error_message + " key:" + key + "'s value in API not as expected in learning plan." \
                                                                    "The actual value is:" + str(actual_key_value) \
                                    + ", but the expected value is:" + expected_field_value
            else:
                if actual_key_value is None or actual_key_value == '':
                    error_message = error_message + " The system_key's value should not be null"
        return error_message
