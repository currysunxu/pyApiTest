#!/usr/bin/env python
#-*-coding:utf-8-*-

#author:Curry
#date:2019/10/29
import json
import random
import string
import time
import uuid

import jsonpath

from E1_API_Automation.Business.HighFlyer35.HighFlyerUtils.Hf35BffUtils import Hf35BffUtils


class Hf35BffCommonData:

    attempt_json = {}
    plan_business = []
    previous_attempt = {}
    score = 0

    def __init__(self,activity_num=2,detail_num=3):
        """
        initialize json data for submitting an attempt
        :param activity_num: default activity is 2
        :param detail_num: default details is 3
        """
        self.attempt_json = self.create_attempt_json_body(activity_num,detail_num)
        self.business_key = self.get_business_key()
        self.previous_attempt = self.attempt_json

    def create_attempt_json_body(self,activity_num,detail_num):
        """
        dynamically create json body for submitting an attempt
        :param activity_num: default activity is 2
        :param detail_num: default details is 3
        :return:
        """
        answer_list = Hf35BffUtils.construct_answer_obj(detail_num)
        details_list = Hf35BffUtils.construct_detail_obj(answer_list)
        activity_list = Hf35BffUtils.construct_activity_obj(activity_num,details_list)
        bff_entity_dict = Hf35BffUtils.construct_bff_entity(activity_list)
        return bff_entity_dict

    def get_business_key(self):
        """
        join bussiness key
        :return: bussiness key
        """
        courseContentId = self.get_attempt_body()["courseContentId"]
        bookContentId = self.get_attempt_body()["bookContentId"]
        unitContentId = self.get_attempt_body()["unitContentId"]
        lessonContentId = self.get_attempt_body()["lessonContentId"]
        learningUnitContentId = self.get_attempt_body()["learningUnitContentId"]
        business_keys = []
        business_keys.append(courseContentId)
        business_keys.append(bookContentId)
        business_keys.append(unitContentId)
        business_keys.append(lessonContentId)
        business_keys.append(learningUnitContentId)
        return business_keys

    def get_attempt_body(self):
        return self.attempt_json

    def set_best_attempt(self):
        """
        set best attempt score as actual score * 3, expected score * 2 to make sure best score
        1. read activity node at first
        2. add total score and score in each details node
        """
        for act_index in range(len(jsonpath.jsonpath(json.loads(json.dumps(self.previous_attempt)), '$..activities[*]'))):
            for details_index in range(len(jsonpath.jsonpath(json.loads(json.dumps(self.previous_attempt)), '$.activities.[0].details'))):
                self.previous_attempt["activities"][act_index]["details"][details_index]["totalScore"] *= 2
                self.previous_attempt["activities"][act_index]["details"][details_index]["score"] *= 3

    @staticmethod
    def get_value_by_json_path(json_body, expression):
        """
        encapuslate jsonpath to special expression parse,like $..{field}
        :param json_body:
        :param expression:
        :return:
        """
        return jsonpath.jsonpath(json.loads(json.dumps(json_body)), expression)