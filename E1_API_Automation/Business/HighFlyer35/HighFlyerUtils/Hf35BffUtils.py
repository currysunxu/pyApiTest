#!/usr/bin/env python
#-*-coding:utf-8-*-

#author:Curry
#date:2019/10/31
import datetime
import json
import random
import re
import string
import time
import uuid

import jmespath

from E1_API_Automation.Business.HighFlyer35.Hf35BffActivityEntity import Hf35BffActivityEntity
from E1_API_Automation.Business.HighFlyer35.Hf35BffDetailsEntity import Hf35BffDetailsEntity
from E1_API_Automation.Business.HighFlyer35.Hf35BffAttemptEntity import Hf35BffAttemptEntity
from E1_API_Automation.Business.HighFlyer35.Hf35BffWordAttemptEntity import Hf35BffWordAttemptEntity, \
	Hf35BffWordAttemptDetailEntity
from E1_API_Automation.Business.NGPlatform.NGPlatformUtils.LearningCommonUtils import LearningCommonUtils


class Hf35BffUtils:

	@staticmethod
	def construct_answer_obj(detail_num):
		"""
		construct answer object by details
		:param detail_num: dynamically pass from test case level
		:return: a list type which length depends on details number
		"""
		answer_list = []
		for answer_index in range(detail_num):
			answer_obj = {"answer_key": "homeworkSVC_Test_%s"%(str(answer_index)),
			"options": [{"id": "homeworkSVC_TestID_%s"%(str(answer_index))},[random.sample(range(1, 34), 4)]]
						  }
			answer_list.append(answer_obj)
		return answer_list

	@staticmethod
	def construct_detail_obj(answer_list):
		"""
		construct details object by question_id,total_score,score,answer
		total_score and score will be integer or float by answer_size.
		:param answer_list:
		:return: a list include details objects
		"""
		details_list = []
		answer_size = len(answer_list)
		for answer in answer_list:
			question_id = uuid.uuid4().__str__()
			details_entity = Hf35BffDetailsEntity(question_id)
			details_entity.total_score = random.randint(9,10) if (answer_size==1) else random.uniform(9,10)
			details_entity.score = random.randint(1,8) if (answer_size==1) else random.uniform(9,10)
			details_entity.answer = answer
			detail_items = details_entity.__dict__
			detail_items_new = Hf35BffUtils.modify_dict_keys(detail_items)
			details_list.append(detail_items_new)

		return details_list

	@staticmethod
	def construct_activity_obj(activity_num,detail_list):
		"""
		construct activity object
		:param activity_num:
		:param detail_list:
		:return:a list include activity objects
		"""
		activity_list = []
		for activity_index in range(activity_num):
			activity_id = uuid.uuid4().__str__()
			activity_entity = Hf35BffActivityEntity(activity_id,detail_list)
			activity_entity.activity_content_revision = "activityContentRevision"+str(random.randint(1, 10))
			activity_items = activity_entity.__dict__
			activity_items_new = Hf35BffUtils.modify_dict_keys(activity_items)
			activity_list.append(activity_items_new)

		return activity_list

	@staticmethod
	def construct_bff_entity(activity_list):
		"""
		construct bff attempt json data
		:param activity_list:
		:return:  return bff attempt json data
		"""
		random_date_time = time.strftime("%Y-%m-%dT%H:%M:%S.%jZ", time.localtime())
		learning_content_id = uuid.uuid4().__str__()
		bff_entity = Hf35BffAttemptEntity(learning_content_id, activity_list)
		bff_entity.start_time = random_date_time
		bff_entity.end_time = random_date_time
		bff_entity.book_content_id = uuid.uuid4().__str__()
		bff_entity.book_content_revision = "BookContentRevision%s" % (random.randint(1, 100))
		bff_entity.course_content_id = uuid.uuid4().__str__()
		bff_entity.course_content_revision = "CourseContentRevision%s" % (random.randint(1, 100))
		bff_entity.unit_content_id = uuid.uuid4().__str__()
		bff_entity.unit_content_revision = "UnitContentRevision%s" % (random.randint(1, 100))
		bff_entity.lesson_content_id = uuid.uuid4().__str__()
		bff_entity.lesson_content_revision = "LessonContentRevision%s" % (random.randint(1, 100))
		bff_entity.learning_unit_content_revision = "LearningUnitContentRevision%s" % (random.randint(1, 100))
		bff_entity.tree_revision = "TestRevision%s" % (random.randint(1, 10))
		bff_entity.schema_version = random.randint(1, 10)
		bff_dict = bff_entity.__dict__
		bff_dict_new = Hf35BffUtils.modify_dict_keys(bff_dict)
		return bff_dict_new

	@staticmethod
	def last_index_of(my_list, my_value):
		"""
		get last index of specific value
		:param mylist:
		:param myvalue:
		:return: last index of myvalue
		"""
		return len(my_list) - my_list[::-1].index(my_value) - 1

	@staticmethod
	def modify_dict_keys(previous_dict):
		"""
		remove prefix of classname cause by python builtin __dict__
		for example: update "_Hf35BffDetails__score" to "score"
		:param previous_dict: dict_keyname_with_prefix
		:return: list <dict> which keys are clear without prefix of classname and __
		"""
		new_dict = previous_dict.copy()
		for item_key in previous_dict.keys():
			field_name = item_key[Hf35BffUtils.last_index_of(item_key, "__") + 1:]
			field_name = Hf35BffUtils.underline_to_hump(field_name)
			new_dict.update({field_name: new_dict.pop(item_key)})
		return new_dict

	@staticmethod
	def underline_to_hump(underline_str):
		'''
		underline string to hump
		:param underline_str:
		:return: hump str
		'''
		sub = re.sub(r'(_\w)', lambda x: x.group(1)[1].upper(), underline_str)
		return sub

	@staticmethod
	def hump_to_underline(hump_str):
		'''
		hump to underline
		:param hunp_str: hump str
		:return: lower str under line string
		'''
		p = re.compile(r'([a-z]|\d)([A-Z])')
		sub = re.sub(p, r'\1_\2', hump_str).lower()
		return sub

	@staticmethod
	def verify_ksd_online_pl_class(ksd_online_class_list, expected_evc_online_class_list, evc_teacher_info_list):
		error_message = ''

		if len(ksd_online_class_list) != len(expected_evc_online_class_list):
			error_message = "ksd online class size not as expected!"

		for i in range(len(ksd_online_class_list)):
			actual_ksd_online_class = ksd_online_class_list[i]
			expected_evc_online_class = expected_evc_online_class_list[i]

			teacher_id = actual_ksd_online_class['teacherId']
			expected_evc_teacher = {}
			for evc_teacher_info in evc_teacher_info_list:
				if evc_teacher_info['teacherId'] == teacher_id:
					expected_evc_teacher = evc_teacher_info
					break

			for key in actual_ksd_online_class.keys():
				actual_value = actual_ksd_online_class[key]
				if key not in ('teacherName', 'teacherAvatarUrl', 'teacherAccent'):
					expected_value = expected_evc_online_class[key]

					if 'Time' in key:
						actual_value = datetime.datetime.strptime(str(actual_value), '%Y-%m-%dT%H:%M:%S.%fZ')
						expected_value = datetime.datetime.strptime(str(expected_value), '%Y-%m-%dT%H:%M:%SZ')
				elif key == 'teacherName':
					expected_value = expected_evc_teacher['displayName']
				elif key == 'teacherAvatarUrl':
					expected_value = expected_evc_teacher['avatarUrl']
				elif key == 'teacherAccent':
					expected_teacher_english_spoken = expected_evc_teacher['englishSpoken']

					expected_value = ''
					if expected_teacher_english_spoken == '703539':
						expected_value = 'British'
					elif expected_teacher_english_spoken == '703540':
						expected_value = 'American'

				if str(actual_value) != str(expected_value):
					error_message = error_message + " In {0} onlineclass, {1} value not as expected, the actual value is {2}, but expected {3}".format(
						i, key, actual_value, expected_value)

		return error_message

	@staticmethod
	def verify_online_gl_class(actual_gl_online_class_list, expected_gl_online_class_list):
		error_message = ''

		if len(actual_gl_online_class_list) != len(expected_gl_online_class_list):
			error_message = "ksd online class size not as expected!"

		for i in range(len(actual_gl_online_class_list)):
			actual_gl_online_class = actual_gl_online_class_list[i]
			expected_gl_online_class = expected_gl_online_class_list[i]

			for key in actual_gl_online_class.keys():
				actual_value = actual_gl_online_class[key]
				expected_value = expected_gl_online_class[key]
				if 'Time' in key:
					actual_value = datetime.datetime.strptime(str(actual_value), '%Y-%m-%dT%H:%M:%S.%fZ')
					expected_value = datetime.datetime.strptime(str(expected_value), '%Y-%m-%dT%H:%M:%SZ')

				if str(actual_value) != str(expected_value):
					error_message = error_message + " In {0} onlineclass, {1} value not as expected, the actual value is {2}, but expected {3}".format(
						i, key, actual_value, expected_value)

		return error_message

	@staticmethod
	def verify_bootstrap_provision(actual_bootstrap_provision, expected_provision):
		error_message = ''

		# provisioning service's key was capitalized
		for key in actual_bootstrap_provision.keys():
			actual_value = actual_bootstrap_provision[key]
			expected_value = expected_provision['{}{}'.format(key[0].upper(), key[1:])]

			if str(actual_value) != str(expected_value):
				error_message = error_message + " {0} value not as expected, the actual value is {1}, but expected {2}"\
					.format(key, actual_value, expected_value)

		return error_message

	@staticmethod
	def construct_word_attempts_dict(word_attempts):
		if word_attempts is not None:
			word_attempt_dict_list = []
			for i in range(len(word_attempts)):
				word_attempt = word_attempts[i]
				word_attempt_dict = {}
				word_attempt_items = word_attempt.__dict__
				for item_key in word_attempt_items.keys():
					word_attempt_field_name = item_key[
														len('_' + word_attempt.__class__.__name__ + '__'):]
					item_value = word_attempt_items[item_key]

					if word_attempt_field_name != 'detail':
						word_attempt_field_name = \
							LearningCommonUtils.convert_name_from_lower_case_to_camel_case(
								word_attempt_field_name)
						word_attempt_dict[word_attempt_field_name] = item_value
					else:
						detail_dict = Hf35BffUtils.construct_word_attempt_detail(item_value)
						word_attempt_dict[word_attempt_field_name] = detail_dict
				word_attempt_dict_list.append(word_attempt_dict)
			return word_attempt_dict_list
		else:
			return None

	@staticmethod
	def construct_word_attempt_detail(word_attempt_detail):
		word_attempt_detail_dict = {}
		word_attempt_detail_items = word_attempt_detail.__dict__
		for item_key in word_attempt_detail_items.keys():
			word_attempt_detail_field_name = item_key[len('_' + word_attempt_detail.__class__.__name__ + '__'):]
			item_value = word_attempt_detail_items[item_key]

			word_attempt_detail_field_name = \
				LearningCommonUtils.convert_name_from_lower_case_to_camel_case(word_attempt_detail_field_name)
			word_attempt_detail_dict[word_attempt_detail_field_name] = item_value

		return word_attempt_detail_dict

	@staticmethod
	def construct_vocab_progress_list(word_attempt_template, item_num=1):
		word_attempt_list = []
		for index in range(item_num):
			word_attempt_entity = Hf35BffWordAttemptEntity(word_attempt_template.course_content_id, word_attempt_template.book_content_id)
			word_attempt_entity.course_content_revision = "CourseContentRevision%s" % (random.randint(1, 100))
			word_attempt_entity.book_content_revision = "BookContentRevision%s" % (random.randint(1, 100))
			word_attempt_entity.unit_content_id = str(uuid.uuid1())
			word_attempt_entity.unit_content_revision = "UnitContentRevision%s" % (random.randint(1, 100))
			word_attempt_entity.word_content_id = str(uuid.uuid1())
			word_attempt_entity.word_content_revision = "WordContentRevision%s" % (random.randint(1, 100))
			word_attempt_entity.tree_revision = "TestRevision%s" % (random.randint(1, 10))
			word_attempt_entity.schema_version = random.randint(1, 10)

			random_date_time = time.strftime("%Y-%m-%dT%H:%M:%S.%jZ", time.localtime())
			word_attempt_detail_entity = Hf35BffWordAttemptDetailEntity()
			word_attempt_detail_entity.current_level = random.randint(1, 10)
			word_attempt_detail_entity.score = random.uniform(50, 100)
			word_attempt_detail_entity.last_study_time = random_date_time

			word_attempt_entity.detail = word_attempt_detail_entity

			word_attempt_list.append(word_attempt_entity)
		return word_attempt_list

	@staticmethod
	def construct_expected_learning_result_by_word_attempt(learning_result_entity, word_attempt):
		business_keys = []
		business_keys.append(word_attempt.course_content_id)
		business_keys.append(word_attempt.book_content_id)
		business_keys.append(word_attempt.unit_content_id)
		business_keys.append(word_attempt.word_content_id)
		learning_result_entity.business_key = '|'.join(business_keys)

		route = {}
		route['course'] = 'HIGH_FLYERS_35'
		route['regionAch'] = 'CN_3'
		route['treeRevision'] = word_attempt.tree_revision
		route['schemaVersion'] = word_attempt.schema_version
		route['courseContentId'] = word_attempt.course_content_id
		route['courseContentRevision'] = word_attempt.course_content_revision
		route['bookContentId'] = word_attempt.book_content_id
		route['bookContentRevision'] = word_attempt.book_content_revision
		route['unitContentId'] = word_attempt.unit_content_id
		route['unitContentRevision'] = word_attempt.unit_content_revision
		route['wordContentId'] = word_attempt.word_content_id
		route['wordContentRevision'] = word_attempt.word_content_revision
		learning_result_entity.route = route

		extension = {}
		extension['currentLevel'] = word_attempt.detail.current_level
		extension['score'] = word_attempt.detail.score
		extension['lastStudyTime'] = word_attempt.detail.last_study_time
		learning_result_entity.extension = extension
