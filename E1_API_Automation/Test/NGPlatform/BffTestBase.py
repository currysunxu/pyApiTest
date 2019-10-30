#!/usr/bin/env python
#-*-coding:utf-8-*-

#author:Curry
#date:2019/10/29
from hamcrest import assert_that, equal_to

from E1_API_Automation.Business.NGPlatform.BffService import BffService
from E1_API_Automation.Business.NGPlatform.NGPlatformUtils.BffCommonData import BffCommonData
from E1_API_Automation.Business.NGPlatform.LearningPlanService import LearningPlanService
from E1_API_Automation.Business.NGPlatform.LearningResultService import LearningResultService
from E1_API_Automation.Settings import LEARNING_PLAN_ENVIRONMENT, LEARNING_RESULT_ENVIRONMENT, BFF_ENVIRONMENT, env_key
from ptest.decorator import BeforeMethod

from E1_API_Automation.Test_Data.BffData import BffProduct, BffUsers


class BffTestBase:

	@BeforeMethod()
	def setup(self):
		self.bff_service = BffService(BFF_ENVIRONMENT)
		self.key = BffProduct.HFV35.value
		self.user_name = BffUsers.BffUserPw[env_key][self.key][0]['username']
		self.password = BffUsers.BffUserPw[env_key][self.key][0]['password']
		self.bff_service.login(self.user_name,self.password)


	def check_bff_compare_learning_plan(self, plan_response, leanring_plan_entity):
		assert_that(plan_response.json()[0]["planBusinessKey"], equal_to(leanring_plan_entity.plan_business_key))
		assert_that(int(plan_response.json()[0]["studentKey"]), equal_to(int(leanring_plan_entity.student_key)))
		assert_that(plan_response.json()[0]["bucketId"], equal_to(leanring_plan_entity.bucket_id))
		assert_that(plan_response.json()[0]["productId"], equal_to(leanring_plan_entity.product_id))
		assert_that(plan_response.json()[0]["state"], equal_to(leanring_plan_entity.state))
		assert_that(plan_response.json()[0]["learningUnit"], equal_to(leanring_plan_entity.learning_unit))
		assert_that(plan_response.json()[0]["route"], equal_to(leanring_plan_entity.route))
		assert_that(plan_response.json()[0]["startTime"], equal_to(leanring_plan_entity.start_time))
		assert_that(plan_response.json()[0]["endTime"], equal_to(leanring_plan_entity.end_time))

	def check_bff_compare_learning_result(self, result_response, learning_result_entity, learning_details_entity):
		assert_that(result_response.json()[0]["productId"], equal_to(learning_result_entity.product_id))
		assert_that(result_response.json()[0]["planType"], equal_to(learning_result_entity.plan_type))
		assert_that(int(result_response.json()[0]["studentKey"]), equal_to(int(learning_result_entity.student_key)))
		assert_that(result_response.json()[0]["atomicKey"], equal_to(learning_result_entity.atomic_key))
		assert_that(result_response.json()[0]["planBusinessKey"], equal_to(learning_result_entity.plan_business_key))
		assert_that(result_response.json()[0]["planSystemKey"], equal_to(learning_result_entity.plan_system_key))
		assert_that(result_response.json()[0]["expectedScore"], equal_to(learning_result_entity.expected_score))
		assert_that(result_response.json()[0]["actualScore"], equal_to(learning_result_entity.actual_score))
		# check details object
		index = 0
		for details in learning_result_entity.details:
			for detail in details:
				assert_that(result_response.json()[0]["details"][index]["questionKey"], equal_to(detail["questionId"]))
				assert_that(result_response.json()[0]["details"][index]["expectedScore"],
							equal_to(detail["totalScore"]))
				assert_that(result_response.json()[0]["details"][index]["actualScore"], equal_to(detail["score"]))
				assert_that(result_response.json()[0]["details"][index]["answer"], equal_to(detail["answer"]))
				index += 1
		# check activity object
		self.extend_activity_obj(learning_details_entity)
		assert_that(BffCommonData.get_value_by_json_path(result_response.json()[0], "$..activityKey"),
					equal_to(learning_details_entity.activity_key))
		assert_that(BffCommonData.get_value_by_json_path(result_response.json()[0], "$..activityVersion"),
					equal_to(learning_details_entity.activity_version))

	def extend_activity_obj(self, learning_details_entity):
		activity_field_tuple = [learning_details_entity.activity_key, learning_details_entity.activity_version]
		for activity_field in activity_field_tuple:
			activity_copy = activity_field.copy()
			key_index = 0
			for insert_index in range(len(activity_copy)):
				activity_field.insert(key_index, activity_copy[insert_index])
				key_index += 2

	def get_learning_plan_response(self, learning_plan_entity):
		learning_plan_service = LearningPlanService(LEARNING_PLAN_ENVIRONMENT)
		plan_response = learning_plan_service.get_partition_plan_without_limit_page(learning_plan_entity)
		print("learining plan response is : " + plan_response.text)
		return plan_response

	def get_learning_result_response(self, learning_result_entity):
		learning_result_service = LearningResultService(LEARNING_RESULT_ENVIRONMENT)
		result_response = learning_result_service.get_user_result_without_limit(learning_result_entity)
		print(result_response.json())
		return result_response

	def setter_learning_plan(self,learning_plan_entity,bff_data_obj):
		learning_plan_entity.state = 4
		learning_plan_entity.learning_unit = bff_data_obj.get_attempt_body()["learningUnitContentId"]
		learning_plan_entity.start_time = bff_data_obj.get_attempt_body()["startTimeUtc"]
		learning_plan_entity.end_time = bff_data_obj.get_attempt_body()["endTimeUtc"]
		learning_plan_entity.route = bff_data_obj.get_attempt_body()["treeRevision"]


	def setter_learning_result(self,learning_result_entity,bff_data_obj,plan_system):
		all_question_expected_score = sum(
			BffCommonData().get_value_by_json_path(bff_data_obj.get_attempt_body(), '$..totalScore'))
		all_question_actual_score = sum(
			BffCommonData().get_value_by_json_path(bff_data_obj.get_attempt_body(), '$..score'))
		all_details = BffCommonData().get_value_by_json_path(bff_data_obj.get_attempt_body(), '$..details')
		learning_result_entity.plan_type = 1
		learning_result_entity.atomic_key = bff_data_obj.get_attempt_body()["learningUnitContentId"]
		learning_result_entity.plan_system_key = plan_system
		learning_result_entity.expected_score = all_question_expected_score
		learning_result_entity.actual_score = all_question_actual_score
		learning_result_entity.details = all_details

	def setter_learning_result_details(self,learning_details_entity,bff_data_obj):
		detail_act_version = BffCommonData().get_value_by_json_path(bff_data_obj.get_attempt_body(),'$..activityContentRevision')
		detail_question_key = BffCommonData().get_value_by_json_path(bff_data_obj.get_attempt_body(), '$..questionId')
		detail_answer = BffCommonData().get_value_by_json_path(bff_data_obj.get_attempt_body(), '$..answer')
		detail_expected_score = BffCommonData().get_value_by_json_path(bff_data_obj.get_attempt_body(), '$..totalScore')
		detail_actual_score = BffCommonData().get_value_by_json_path(bff_data_obj.get_attempt_body(), '$..score')
		learning_details_entity.activity_version = detail_act_version
		learning_details_entity.question_key = detail_question_key
		learning_details_entity.answer = detail_answer
		learning_details_entity.expected_score = detail_expected_score
		learning_details_entity.actual_score = detail_actual_score
