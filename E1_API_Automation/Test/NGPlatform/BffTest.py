#!/usr/bin/env python
#-*-coding:utf-8-*-

#author:Curry
#date:2019/10/14

import datetime

from E1_API_Automation.Business.NGPlatform.BffService import BffService
from E1_API_Automation.Business.NGPlatform.HomeworkService import HomeworkService
from E1_API_Automation.Business.NGPlatform.LearningPlanEntity import LearningPlanEntity
from E1_API_Automation.Business.NGPlatform.LearningPlanService import LearningPlanService
from E1_API_Automation.Business.NGPlatform.LearningResultEntity import LearningResultEntity
from E1_API_Automation.Business.NGPlatform.LearningResultService import LearningResultService
from E1_API_Automation.Business.NGPlatform.LearningResultDetailEntity import LearningResultDetailEntity
from E1_API_Automation.Settings import BFF_ENVIRONMENT, env_key, AUTH_ENVIRONMENT, LEARNING_RESULT_ENVIRONMENT, \
    LEARNING_PLAN_ENVIRONMENT,HOMEWORK_ENVIRONMENT
from E1_API_Automation.Test_Data.BffData import BffUsers, BffProduct, BffCommonData, BffUtil
from hamcrest import assert_that, equal_to
from ptest.decorator import TestClass, Test



@TestClass()
class BffTest:

    @Test(tag='qa')
    def test_bff_auth_login_valid_username(self):
        bff_service = BffService(BFF_ENVIRONMENT)
        product_keys = BffUsers.BffUserPw[env_key].keys()
        for key in product_keys:
            user_name = BffUsers.BffUserPw[env_key][key][0]['username']
            password = BffUsers.BffUserPw[env_key][key][0]['password']
            if key.__contains__('HF'):
                print("HF user is : %s"%(user_name))
                response = bff_service.login(user_name, password)
                print("Bff login response is : %s"%(response.__str__()))
                id_token = bff_service.get_auth_token()
                print("Bff login Token is : %s"%(id_token))
                assert_that((not id_token.__eq__("")) and id_token.__str__() is not None)

    @Test(tag='qa')
    def test_bff_auth_login_invalid_username(self):
        bff_service = BffService(BFF_ENVIRONMENT)
        key = BffProduct.HFV35.value
        user_name = BffUsers.BffUserPw[env_key][key][0]['password']
        password = BffUsers.BffUserPw[env_key][key][0]['password']
        response = bff_service.login(user_name,password)
        print("Bff login response is : %s"%(response.__str__()))
        assert_that(response.status_code, equal_to(404))

    @Test(tag='qa')
    def test_bff_auth_login_not_HF_username(self):
        bff_service = BffService(BFF_ENVIRONMENT)
        product_keys = BffUsers.BffUserPw[env_key].keys()
        for key in product_keys:
            user_name = BffUsers.BffUserPw[env_key][key][0]['username']
            password = BffUsers.BffUserPw[env_key][key][0]['password']
            response = bff_service.login(user_name, password)
            print(
                "Product:" + key + ";UserName:" + user_name )
            if not key.__contains__('HF'):
                print("status: %s, message: %s"%(str(response.json()['status']),response.json()['message']))
                assert_that(response.status_code, equal_to(401))
                assert_that((response.json()['error'].__eq__("Unauthorized")))


    @Test(tag='qa')
    def test_submit_new_attempt_without_auth_token(self):
        bff_service = BffService(BFF_ENVIRONMENT)
        response=bff_service.submit_new_attempt_with_negative_auth_token()
        print("Bff login response is : %s" % (response.__str__()))
        assert_that(response.status_code, equal_to(400))
        assert_that((response.json()['error'].__eq__("Bad Request")))

    @Test(tag='qa')
    def test_submit_new_attempt_with_invalid_auth_token(self):
        bff_service = BffService(BFF_ENVIRONMENT)
        response=bff_service.submit_new_attempt_with_negative_auth_token("invalid")
        print("Bff login response is : %s" % (response.__str__()))
        assert_that(response.status_code, equal_to(401))
        assert_that((response.json()['error'].__eq__("Unauthorized")))

    @Test(tag='qa')
    def test_submit_new_attempt_with_valid_body(self):
        bff_service = BffService(BFF_ENVIRONMENT)
        key = BffProduct.HFV35.value
        user_name = BffUsers.BffUserPw[env_key][key][0]['username']
        password = BffUsers.BffUserPw[env_key][key][0]['password']
        bff_data_obj = BffCommonData()
        submit_response = bff_service.submit_new_attempt(user_name,password,bff_data_obj.get_attempt_body())
        print("Bff submit response is : %s" % (submit_response.__str__()))
        print("Bff submit response is : %s" % (submit_response.text))
        assert_that(submit_response.status_code,equal_to(200))
        assert_that((not submit_response.text.__eq__("")))
        bucket_id = datetime.datetime.now().year
        product_id = 2
        plan_busniess_tuple = bff_data_obj.plan_business
        student_key = bff_data_obj.get_attempt_body()["studentId"]
        plan_busniess = '|'.join(plan_busniess_tuple)
        learning_unit = bff_data_obj.get_attempt_body()["learningUnitContentId"]
        start_time= bff_data_obj.get_attempt_body()["startTimeUtc"]
        end_time= bff_data_obj.get_attempt_body()["endTimeUtc"]
        tree_revision= bff_data_obj.get_attempt_body()["treeRevision"]
        learning_plan_entity = LearningPlanEntity(product_id, plan_busniess, bucket_id, student_key)
        plan_response = self.get_learning_plan_response(learning_plan_entity)
        plan_system = plan_response.json()[0]["systemKey"]
        print("Bff submit response %s should be same with plan system key : %s" %(submit_response.text,plan_system))
        assert_that(submit_response.text[1:-1], equal_to(plan_system))
        learning_plan_entity.state = 4
        learning_plan_entity.learning_unit = learning_unit
        learning_plan_entity.start_time = start_time
        learning_plan_entity.end_time = end_time
        learning_plan_entity.route = tree_revision
        self.check_bff_compare_learning_plan(plan_response,learning_plan_entity)
        learning_result_entity = LearningResultEntity(product_id, plan_busniess, int(student_key))
        result_response = self.get_learning_result_response(learning_result_entity)
        atomic_key = learning_unit
        all_question_expected_score = sum(BffUtil.get_value_by_json_path(bff_data_obj.get_attempt_body(),'$..totalScore'))
        all_question_actual_score = sum(BffUtil.get_value_by_json_path(bff_data_obj.get_attempt_body(),'$..score'))
        all_details = BffUtil.get_value_by_json_path(bff_data_obj.get_attempt_body(), '$..details')
        learning_result_entity.plan_type = 1
        learning_result_entity.atomic_key = atomic_key
        learning_result_entity.plan_business_key = plan_busniess
        learning_result_entity.plan_system_key = plan_system
        learning_result_entity.expected_score = all_question_expected_score
        learning_result_entity.actual_score = all_question_actual_score
        learning_result_entity.details = all_details
        detail_act_key = BffUtil.get_value_by_json_path(bff_data_obj.get_attempt_body(), '$..activityContentId')
        detail_act_version = BffUtil.get_value_by_json_path(bff_data_obj.get_attempt_body(), '$..activityContentRevision')
        detail_question_key = BffUtil.get_value_by_json_path(bff_data_obj.get_attempt_body(),'$..questionId')
        detail_answer = BffUtil.get_value_by_json_path(bff_data_obj.get_attempt_body(),'$..answer')
        detail_expected_score = BffUtil.get_value_by_json_path(bff_data_obj.get_attempt_body(),'$..totalScore')
        detail_actual_score = BffUtil.get_value_by_json_path(bff_data_obj.get_attempt_body(),'$..score')
        learning_details_entity = LearningResultDetailEntity(detail_act_key)
        learning_details_entity.activity_version = detail_act_version
        learning_details_entity.question_key = detail_question_key
        learning_details_entity.answer = detail_answer
        learning_details_entity.expected_score = detail_expected_score
        learning_details_entity.actual_score = detail_actual_score
        self.check_bff_compare_learning_result(result_response,learning_result_entity,learning_details_entity)

    @Test(tag='qa')
    def test_submit_best_attempt(self):
        bff_service = BffService(BFF_ENVIRONMENT)
        key = BffProduct.HFV35.value
        user_name = BffUsers.BffUserPw[env_key][key][0]['username']
        password = BffUsers.BffUserPw[env_key][key][0]['password']
        bff_data_obj = BffCommonData()
        submit_response = bff_service.submit_new_attempt(user_name,password,bff_data_obj.get_attempt_body())
        print("Bff submit response is : %s" % (submit_response.__str__()))
        print("Bff submit response is : %s" % (submit_response.text))
        assert_that(submit_response.status_code,equal_to(200))
        bff_data_obj.set_best_attempt()
        submit_best_response = bff_service.submit_new_attempt(user_name,password,bff_data_obj.previous_attempt)
        assert_that(submit_best_response.status_code,equal_to(200))
        student_key = bff_data_obj.get_attempt_body()["studentId"]
        book_content_id = bff_data_obj.get_attempt_body()["bookContentId"]
        best_submit_response = bff_service.get_the_best_attempt(student_key,book_content_id)
        # check bff get best attempt
        bff_best_total_score = sum(BffUtil.get_value_by_json_path(best_submit_response.json()[0], "$..totalScore"))
        expected_total_score = sum(BffUtil.get_value_by_json_path(bff_data_obj.attempt_json,"$..totalScore"))
        bff_best_score = sum(BffUtil.get_value_by_json_path(best_submit_response.json()[0], "$..score"))
        expected_score = sum(BffUtil.get_value_by_json_path(bff_data_obj.attempt_json,"$..score"))
        assert_that(bff_best_total_score,equal_to(expected_total_score))
        assert_that(bff_best_score,equal_to(expected_score))
        # check homework service best attempt
        homework_service = HomeworkService(HOMEWORK_ENVIRONMENT)
        homework_best_attempt_response = homework_service.get_the_best_attempt(student_key,book_content_id)
        homework_best_total_score = sum(BffUtil.get_value_by_json_path(homework_best_attempt_response.json()[0],"$..totalScore"))
        homework_best_score = sum(BffUtil.get_value_by_json_path(homework_best_attempt_response.json()[0],"$..score"))
        assert_that(homework_best_total_score,equal_to(bff_best_total_score))
        assert_that(homework_best_score,equal_to(bff_best_score))


    def check_bff_compare_learning_plan(self, plan_response, leanring_plan_entity):
        assert_that(plan_response.json()[0]["planBusinessKey"], equal_to(leanring_plan_entity.plan_business_key))
        assert_that(int(plan_response.json()[0]["studentKey"]), equal_to(int(leanring_plan_entity.student_key)))
        assert_that(plan_response.json()[0]["bucketId"], equal_to(leanring_plan_entity.bucket_id))
        assert_that(plan_response.json()[0]["productId"], equal_to(leanring_plan_entity.product_id))
        assert_that(plan_response.json()[0]["state"],equal_to(leanring_plan_entity.state))
        assert_that(plan_response.json()[0]["learningUnit"], equal_to(leanring_plan_entity.learning_unit))
        assert_that(plan_response.json()[0]["route"], equal_to(leanring_plan_entity.route))
        assert_that(plan_response.json()[0]["startTime"], equal_to(leanring_plan_entity.start_time))
        assert_that(plan_response.json()[0]["endTime"], equal_to(leanring_plan_entity.end_time))

    def check_bff_compare_learning_result(self,result_response,learning_result_entity,learning_details_entity):
        assert_that(result_response.json()[0]["productId"], equal_to(learning_result_entity.product_id))
        assert_that(result_response.json()[0]["planType"], equal_to(learning_result_entity.plan_type))
        assert_that(int(result_response.json()[0]["studentKey"]), equal_to(int(learning_result_entity.student_key)))
        assert_that(result_response.json()[0]["atomicKey"], equal_to(learning_result_entity.atomic_key))
        assert_that(result_response.json()[0]["planBusinessKey"],equal_to(learning_result_entity.plan_business_key))
        assert_that(result_response.json()[0]["planSystemKey"], equal_to(learning_result_entity.plan_system_key))
        assert_that(result_response.json()[0]["expectedScore"], equal_to(learning_result_entity.expected_score))
        assert_that(result_response.json()[0]["actualScore"], equal_to(learning_result_entity.actual_score))
        # check details object
        index = 0
        for details in learning_result_entity.details:
            for detail in details:
                assert_that(result_response.json()[0]["details"][index]["questionKey"],equal_to(detail["questionId"]))
                assert_that(result_response.json()[0]["details"][index]["expectedScore"],equal_to(detail["totalScore"]))
                assert_that(result_response.json()[0]["details"][index]["actualScore"],equal_to(detail["score"]))
                assert_that(result_response.json()[0]["details"][index]["answer"],equal_to(detail["answer"]))
                index+=1
        # check activity object
        self.extend_activity_obj(learning_details_entity)
        assert_that(BffUtil.get_value_by_json_path(result_response.json()[0],"$..activityKey"), equal_to(learning_details_entity.activity_key))
        assert_that(BffUtil.get_value_by_json_path(result_response.json()[0],"$..activityVersion"), equal_to(learning_details_entity.activity_version))

    def extend_activity_obj(self, learning_details_entity):
        activity_field_tuple =  [learning_details_entity.activity_key,learning_details_entity.activity_version]
        for activity_field in activity_field_tuple:
            activity_copy = activity_field.copy()
            key_index = 0
            for insert_index in range(len(activity_copy)):
                activity_field.insert(key_index, activity_copy[insert_index])
                key_index += 2

    def get_learning_plan_response(self,learning_plan_entity):
        learning_plan_service = LearningPlanService(LEARNING_PLAN_ENVIRONMENT)
        plan_response = learning_plan_service.get_partition_plan_without_limit_page(learning_plan_entity)
        print("learining plan response is : "+plan_response.text)
        return plan_response

    def get_learning_result_response(self,learning_result_entity):
        learning_result_service = LearningResultService(LEARNING_RESULT_ENVIRONMENT)
        result_response = learning_result_service.get_user_result_without_limit(learning_result_entity)
        print(result_response.json())
        return result_response



