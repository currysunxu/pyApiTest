#!/usr/bin/env python
#-*-coding:utf-8-*-

#author:Curry
#date:2019/10/31
import json
import random
import re
import string
import time
import uuid

from E1_API_Automation.Business.HighFlyer35.Hf35BffActivityEntity import Hf35BffActivityEntity
from E1_API_Automation.Business.HighFlyer35.Hf35BffDetailsEntity import Hf35BffDetailsEntity
from E1_API_Automation.Business.HighFlyer35.Hf35BffAttemptEntity import Hf35BffAttemptEntity


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
		total_score and score are double.
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
		bff_entity = Hf35BffAttemptEntity(learning_content_id,activity_list)
		bff_entity.start_time_utc =random_date_time
		bff_entity.end_time_utc =random_date_time
		bff_entity.book_content_id = uuid.uuid4().__str__()
		bff_entity.course_content_id = uuid.uuid4().__str__()
		bff_entity.unit_content_id = uuid.uuid4().__str__()
		bff_entity.lesson_content_id = uuid.uuid4().__str__()
		bff_entity.tree_revision = "TestRevision%s"%(random.randint(1,10))
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