#!/usr/bin/env python
#-*-coding:utf-8-*-

#author:Curry
#date:2019/10/14

import datetime
import json

from E1_API_Automation.Business.NGPlatform.HomeworkService import HomeworkService
from E1_API_Automation.Business.NGPlatform.LearningPlanEntity import LearningPlanEntity
from E1_API_Automation.Business.NGPlatform.LearningResultEntity import LearningResultEntity
from E1_API_Automation.Business.NGPlatform.LearningResultDetailEntity import LearningResultDetailEntity
from E1_API_Automation.Settings import env_key,HOMEWORK_ENVIRONMENT
from E1_API_Automation.Test.HighFlyerV35.HfBffTestBase import HfBffTestBase
from E1_API_Automation.Test_Data.BffData import BffUsers
from E1_API_Automation.Business.HighFlyer35.HighFlyerUtils.Hf35BffCommonData import Hf35BffCommonData
from hamcrest import assert_that, equal_to
from ptest.decorator import TestClass, Test



@TestClass()
class Hf35BffTest(HfBffTestBase):

    @Test(tag='qa')
    def test_bff_auth_login_valid_username(self):
        product_keys = BffUsers.BffUserPw[env_key].keys()
        for key in product_keys:
            user_name = BffUsers.BffUserPw[env_key][key][0]['username']
            password = BffUsers.BffUserPw[env_key][key][0]['password']
            if key.__contains__('HF'):
                print("HF user is : %s"%(user_name))
                response = self.bff_service.login(user_name, password)
                print("Bff login response is : %s"%(response.__str__()))
                id_token = self.bff_service.get_auth_token()
                print("Bff login Token is : %s"%(id_token))
                assert_that((not id_token.__eq__("")) and id_token.__str__() is not None)

    @Test(tag='qa')
    def test_bff_auth_login_invalid_username(self):
        user_name = BffUsers.BffUserPw[env_key][self.key][0]['password']
        password = BffUsers.BffUserPw[env_key][self.key][0]['password']
        response = self.bff_service.login(user_name,password)
        print("Bff login response is : %s"%(response.__str__()))
        assert_that(response.status_code, equal_to(404))

    @Test(tag='qa')
    def test_bff_auth_login_not_HF_username(self):
        product_keys = BffUsers.BffUserPw[env_key].keys()
        for key in product_keys:
            user_name = BffUsers.BffUserPw[env_key][key][0]['username']
            password = BffUsers.BffUserPw[env_key][key][0]['password']
            response = self.bff_service.login(user_name, password)
            print(
                "Product:" + key + ";UserName:" + user_name )
            if not key.__contains__('HF'):
                print("status: %s, message: %s"%(str(response.json()['status']),response.json()['message']))
                assert_that(response.status_code, equal_to(401))
                assert_that((response.json()['error'].__eq__("Unauthorized")))


    @Test(tag='qa',data_provider=[("noToken")])
    def test_submit_new_attempt_without_auth_token(self,negative_para):
        bff_data_obj = Hf35BffCommonData()
        response = self.bff_service.submit_new_attempt_with_negative_auth_token(bff_data_obj.get_attempt_body(),negative_para)
        print("Bff login response is : %s" % (response.__str__()))
        assert_that(response.status_code, equal_to(400))
        assert_that((response.json()['error'].__eq__("Bad Request")))

    @Test(tag='qa',data_provider=[(""),("invalid")])
    def test_submit_new_attempt_with_invalid_auth_token(self,negative_para):
        bff_data_obj = Hf35BffCommonData()
        response = self.bff_service.submit_new_attempt_with_negative_auth_token(bff_data_obj.get_attempt_body(),negative_para)
        print("Bff login response is : %s" % (response.__str__()))
        assert_that(response.status_code, equal_to(401))
        assert_that((response.json()['error'].__eq__("Unauthorized")))

    @Test(tag='qa',data_provider=[(1,1), (2,4), (4,2),(10,10)])
    def test_submit_new_attempt_with_valid_body(self,activity_num,detail_num):
        bff_data_obj = Hf35BffCommonData(activity_num,detail_num)
        submit_response = self.bff_service.submit_new_attempt(bff_data_obj.get_attempt_body())
        print("Bff submit response is : %s" % (submit_response.__str__()))
        print("Bff submit response is : %s" % (submit_response.text))
        assert_that(submit_response.status_code,equal_to(200))
        assert_that((not submit_response.text.__eq__("")))
        # check learning plan
        learning_plan_entity = LearningPlanEntity(None,None,None,None)
        self.setter_learning_plan(learning_plan_entity,bff_data_obj)
        plan_response = self.get_learning_plan_response(learning_plan_entity)
        plan_system = plan_response.json()[0]["systemKey"]
        print("Bff submit response %s should be same with plan system key : %s" %(submit_response.text,plan_system))
        assert_that(submit_response.text[1:-1], equal_to(plan_system))
        self.check_bff_compare_learning_plan(plan_response,learning_plan_entity)
        # check learning result
        learning_result_entity = LearningResultEntity(None,None,None)
        self.setter_learning_result(learning_result_entity,bff_data_obj,plan_system)
        result_response = self.get_learning_result_response(learning_result_entity)
        assert_that(result_response.status_code,equal_to(200))
        learning_details_entity = LearningResultDetailEntity(None)
        self.setter_learning_result_details(learning_details_entity,bff_data_obj)
        self.check_bff_compare_learning_result(result_response,learning_result_entity,learning_details_entity)

    @Test(tag='qa',data_provider=[(1,1), (2,4), (4,2),(10,10)])
    def test_submit_best_attempt(self,activity_num,detail_num):
        bff_data_obj = Hf35BffCommonData(activity_num,detail_num)
        submit_response = self.bff_service.submit_new_attempt(bff_data_obj.get_attempt_body())
        print("Bff submit response is : %s" % (submit_response.__str__()))
        print("Bff submit response is : %s" % (submit_response.text))
        assert_that(submit_response.status_code,equal_to(200))
        bff_data_obj.set_best_attempt()
        submit_best_response = self.bff_service.submit_new_attempt(bff_data_obj.previous_attempt)
        assert_that(submit_best_response.status_code,equal_to(200))
        student_key = bff_data_obj.get_attempt_body()["studentId"]
        book_content_id = bff_data_obj.get_attempt_body()["bookContentId"]
        best_submit_response = self.bff_service.get_the_best_attempt(student_key,book_content_id)
        # check bff get best attempt
        bff_best_total_score = sum(Hf35BffCommonData.get_value_by_json_path(best_submit_response.json()[0], "$.activities..totalScore"))
        expected_total_score = sum(Hf35BffCommonData.get_value_by_json_path(bff_data_obj.attempt_json,"$..totalScore"))
        bff_best_score = sum(Hf35BffCommonData.get_value_by_json_path(best_submit_response.json()[0], "$.activities..score"))
        expected_score = sum(Hf35BffCommonData.get_value_by_json_path(bff_data_obj.attempt_json,"$..score"))
        assert_that(bff_best_total_score,equal_to(expected_total_score))
        assert_that(bff_best_score,equal_to(expected_score))
        # check homework service best attempt
        homework_service = HomeworkService(HOMEWORK_ENVIRONMENT)
        homework_best_attempt_response = homework_service.get_the_best_attempt(student_key,book_content_id)
        homework_best_total_score = sum(Hf35BffCommonData.get_value_by_json_path(homework_best_attempt_response.json()[0],"$.activities..totalScore"))
        homework_best_score = sum(Hf35BffCommonData.get_value_by_json_path(homework_best_attempt_response.json()[0],"$.activities..score"))
        assert_that(homework_best_total_score,equal_to(bff_best_total_score))
        assert_that(homework_best_score,equal_to(bff_best_score))
        assert_that(best_submit_response.json(),equal_to(homework_best_attempt_response.json()))

    @Test(tag='qa',data_provider=[("HIGH_FLYERS_35","1")])
    def test_get_course_structure(self,course,scheme_version):
        bff_course_response = self.bff_service.get_course_structure()
        print("Bff get course response is : %s"%(json.dumps(bff_course_response.json(),indent=4)))
        assert_that(bff_course_response.status_code,equal_to(200))
        json_body = {
          "childTypes":["COURSE","BOOK"] ,
          "contentId": None,
          "regionAch": "cn-3",
          "treeRevision": None
        }
        content_map_response = self.get_course_from_content_map(course,scheme_version,json_body)
        assert_that(bff_course_response.json(),equal_to(content_map_response.json()))

    @Test(tag='qa',data_provider=[("HIGH_FLYERS_35","1")])
    def test_get_book_structure(self,course,scheme_version):
        json_body = {
          "childTypes":["COURSE","BOOK","UNIT","LESSON"] ,
          "contentId": None,
          "regionAch": "cn-3",
          "treeRevision": None
        }
        content_map_response = self.get_course_from_content_map(course,scheme_version,json_body)
        content_id_from_content_map = content_map_response.json()["contentId"]
        tree_revision_from_content_map = content_map_response.json()["treeRevision"]
        bff_book_response = self.bff_service.get_book_structure(content_id_from_content_map,tree_revision_from_content_map)
        print("Bff get course response is : %s"%(json.dumps(bff_book_response.json(),indent=4)))
        assert_that(bff_book_response.status_code,equal_to(200))
        assert_that(bff_book_response.json(),equal_to(content_map_response.json()))

    @Test(tag='qa',data_provider=[(""),("invalid"),("noToken")])
    def test_get_course_structure_with_invalid_token(self,invalid):
        bff_course_response = self.bff_service.get_course_structure_with_negative_token(invalid)
        print("Bff get course response is : %s"%(json.dumps(bff_course_response.json(),indent=4)))
        print("Bff get course response : %s" % (bff_course_response.__str__()))
        if invalid.__eq__("noToken"):
            assert_that(bff_course_response.status_code, equal_to(400))
            assert_that((bff_course_response.json()['error'].__eq__("Bad Request")))
        else:
            assert_that(bff_course_response.status_code, equal_to(401))
            assert_that((bff_course_response.json()['error'].__eq__("Unauthorized")))


    @Test(tag='qa',data_provider=[(""),("invalid"),("noToken")])
    def test_get_book_structure_with_invalid_token(self,invalid):
        json_body = {
          "childTypes":["COURSE","BOOK","UNIT","LESSON"] ,
          "contentId": None,
          "regionAch": "cn-3",
          "treeRevision": None
        }
        content_map_response = self.get_course_from_content_map("HIGH_FLYERS_35","1",json_body)
        content_id_from_content_map = content_map_response.json()["contentId"]
        tree_revision_from_content_map = content_map_response.json()["treeRevision"]
        bff_book_response = self.bff_service.get_book_structure_with_negative_token(content_id_from_content_map,
                                                                                      tree_revision_from_content_map,invalid)
        print("Bff get book response is : %s"%(json.dumps(bff_book_response.json(),indent=4)))
        print("Bff get book response : %s" % (bff_book_response.__str__()))
        if invalid.__eq__("noToken"):
            assert_that(bff_book_response.status_code, equal_to(400))
            assert_that((bff_book_response.json()['error'].__eq__("Bad Request")))
        else:
            assert_that(bff_book_response.status_code, equal_to(401))
            assert_that((bff_book_response.json()['error'].__eq__("Unauthorized")))

    @Test(tag='qa', data_provider=[("no_content_id"), ("no_tree_revision")])
    def test_get_book_structure_without_contentId_or_treeRevision(self, invalid):
        json_body = {
            "childTypes": ["COURSE", "BOOK", "UNIT", "LESSON"],
            "contentId": None,
            "regionAch": "cn-3",
            "treeRevision": None
        }
        content_map_response = self.get_course_from_content_map("HIGH_FLYERS_35", "1", json_body)
        if invalid.__eq__("no_content_id"):
            content_id_from_content_map = ""
        else:
            content_id_from_content_map = content_map_response.json()["contentId"]
        if invalid.__eq__("no_tree_revision"):
            tree_revision_from_content_map = ""
        else:
            tree_revision_from_content_map = content_map_response.json()["treeRevision"]

        bff_book_response = self.bff_service.get_book_structure(content_id_from_content_map,tree_revision_from_content_map)
        print("Bff get book response is : %s" % (json.dumps(bff_book_response.json(), indent=4)))
        print("Bff get book response : %s" % (bff_book_response.__str__()))
        assert_that(bff_book_response.status_code, equal_to(404))
        assert_that((bff_book_response.json()['error'].__eq__("Not Found")))

    @Test(tag='qa', data_provider=[("no_uuid")])
    def test_get_book_structure_with_invalid_contentId(self, invalid):
        json_body = {
            "childTypes": ["COURSE", "BOOK", "UNIT", "LESSON"],
            "contentId": None,
            "regionAch": "cn-3",
            "treeRevision": None
        }
        content_map_response = self.get_course_from_content_map("HIGH_FLYERS_35", "1", json_body)
        if invalid.__eq__("no_uuid"):
            content_id_from_content_map = "5ba2a7066356aaa"
        tree_revision_from_content_map = content_map_response.json()["treeRevision"]

        bff_book_response = self.bff_service.get_book_structure(content_id_from_content_map,tree_revision_from_content_map)
        print("Bff get book response is : %s" % (json.dumps(bff_book_response.json(), indent=4)))
        print("Bff get book response : %s" % (bff_book_response.__str__()))
        assert_that(bff_book_response.status_code, equal_to(400))
        assert_that((bff_book_response.json()['error'].__eq__("Bad Request")))
