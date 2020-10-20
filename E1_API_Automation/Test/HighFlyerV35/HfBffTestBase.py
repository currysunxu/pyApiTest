import datetime
import time
import random
import jmespath
from hamcrest import assert_that, equal_to
import uuid

from E1_API_Automation.Business.HighFlyer35.Hf35BffService import Hf35BffService
from E1_API_Automation.Business.HighFlyer35.HighFlyerUtils.Hf35BffCommonData import Hf35BffCommonData
from E1_API_Automation.Business.NGPlatform.ContentMapService import ContentMapService
from E1_API_Automation.Business.NGPlatform.StudyPlanService import StudyPlanService
from E1_API_Automation.Business.NGPlatform.ContentMapQueryEntity import ContentMapQueryEntity
from E1_API_Automation.Business.NGPlatform.LearningResultService import LearningResultService
from E1_API_Automation.Business.NGPlatform.NGPlatformUtils.LearningEnum import LearningResultProduct, \
    LearningResultProductModule
from E1_API_Automation.Business.OMNIService import OMNIService
from E1_API_Automation.Settings import *
from ptest.decorator import BeforeMethod

from E1_API_Automation.Test_Data.BffData import BffProduct, BffUsers





class HfBffTestBase:

    @BeforeMethod()
    def setup(self):
        self.bff_service = Hf35BffService(BFF_ENVIRONMENT)
        self.cm_service = ContentMapService(CONTENT_MAP_ENVIRONMENT)
        self.sp_service = StudyPlanService(STUDY_TIME_ENVIRONMENT)
        self.key = BffProduct.HFV35.value
        self.user_name = BffUsers.BffUserPw[env_key][self.key][0]['username']
        self.password = BffUsers.BffUserPw[env_key][self.key][0]['password']
        self.bff_service.login(self.user_name, self.password)
        self.omni_service = OMNIService(OMNI_ENVIRONMENT)
        try:
            self.customer_id = BffUsers.BffUserPw[env_key][self.key][0]['userid']
        except:
            self.customer_id = self.omni_service.get_customer_id(self.user_name, self.password)

    def check_bff_compare_learning_plan(self, plan_response, leanring_plan_entity):
        assert_that(plan_response.json()[0]["planBusinessKey"], equal_to(leanring_plan_entity.business_key))
        assert_that(int(plan_response.json()[0]["studentKey"]), equal_to(int(leanring_plan_entity.student_key)))
        assert_that(plan_response.json()[0]["bucketId"], equal_to(leanring_plan_entity.bucket_id))
        assert_that(plan_response.json()[0]["productId"], equal_to(leanring_plan_entity.product))
        assert_that(plan_response.json()[0]["state"], equal_to(leanring_plan_entity.state))
        assert_that(plan_response.json()[0]["learningUnit"], equal_to(leanring_plan_entity.learning_unit))
        assert_that(plan_response.json()[0]["route"], equal_to(leanring_plan_entity.route))
        assert_that(plan_response.json()[0]["startTime"], equal_to(leanring_plan_entity.start_time))
        assert_that(plan_response.json()[0]["endTime"], equal_to(leanring_plan_entity.end_time))

    def check_bff_compare_learning_result(self, result_response, learning_result_entity, learning_details_entity):
        assert_that(result_response.json()[0]["product"], equal_to(learning_result_entity.product))
        assert_that(result_response.json()[0]["productModule"], equal_to(learning_result_entity.product_module))
        assert_that(int(result_response.json()[0]["studentKey"]), equal_to(int(learning_result_entity.student_key)))
        assert_that(result_response.json()[0]["businessKey"], equal_to(learning_result_entity.business_key))
        assert_that(result_response.json()[0]["expectedScore"], equal_to(learning_result_entity.expected_score))
        assert_that(result_response.json()[0]["actualScore"], equal_to(learning_result_entity.actual_score))
        assert_that(result_response.json()[0]["startTime"], equal_to(learning_result_entity.start_time))
        assert_that(result_response.json()[0]["endTime"], equal_to(learning_result_entity.end_time))
        assert_that(result_response.json()[0]["route"], equal_to(learning_result_entity.route))
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
        self.extend_activity_obj(learning_result_entity, learning_details_entity)
        assert_that(Hf35BffCommonData.get_value_by_json_path(result_response.json()[0], "$..activityKey"),
                    equal_to(learning_details_entity.activity_key))
        assert_that(Hf35BffCommonData.get_value_by_json_path(result_response.json()[0], "$..activityVersion"),
                    equal_to(learning_details_entity.activity_version))

    def extend_activity_obj(self, learning_result_entity, learning_details_entity):
        """extend activity_key and activity_version by details numbers
        :param learning_details_entity:
        learning_details_entity.activity_key and activity_version are both list type
        For example: activity_key = {c,a,d} and details number = 4
        1.The first element 'c' will be extend 3 times , {c,c,c,c,a,d}
        2.insert_index will indicate to last index.
        3.The following element will be extend by logic above.
        """
        activity_field_tuple = [learning_details_entity.activity_key, learning_details_entity.activity_version]
        for activity_field in activity_field_tuple:
            activity_copy = activity_field.copy()
            insert_index = 0
            for element in activity_copy:
                for index in range(len(learning_result_entity.details[0]) - 1):
                    activity_field.insert(insert_index, element)
                insert_index += len(learning_result_entity.details[0])

    def get_learning_result_response(self, learning_result_entity):
        learning_result_service = LearningResultService(LEARNING_RESULT_ENVIRONMENT)
        result_response = learning_result_service.get_specific_result(learning_result_entity)
        return result_response

    def setter_learning_plan(self, learning_plan_entity, bff_data_obj):
        """
        set all fields in learning_plan_entity
        :param learning_plan_entity:
        :param bff_data_obj: test data object
        :return:
        """
        learning_plan_entity.business_key = '|'.join(bff_data_obj.plan_business)
        learning_plan_entity.student_key = self.customer_id
        learning_plan_entity.bucket_id = datetime.datetime.now().year
        learning_plan_entity.product = 2
        learning_plan_entity.state = 4
        learning_plan_entity.learning_unit = bff_data_obj.get_attempt_body()["learningUnitContentId"]
        learning_plan_entity.start_time = bff_data_obj.get_attempt_body()["startTimeUtc"]
        learning_plan_entity.end_time = bff_data_obj.get_attempt_body()["endTimeUtc"]
        # Todo need to refactor dynamicly for groupId after add corresponding api in Homework Service
        learning_plan_entity.route = "treeRevision=%s|%s" % (
            bff_data_obj.get_attempt_body()["treeRevision"], "groupId=null")

    def setter_learning_result(self, learning_result_entity, bff_data_obj):
        """set all fields in learning_result_entity
        :param learning_result_entity: all_question_expected_scores and all_question_actual_scores are both list type
        :param bff_data_obj: json test data object
        :param plan_system: from learning plan response
        learning_result_entity.product_module = 1 means 'homework'
        learning_result_entity.product = 2 means 'high flyers'
        """
        all_question_expected_scores = sum(
            Hf35BffCommonData.get_value_by_json_path(bff_data_obj.get_attempt_body(), '$..totalScore'))
        all_question_actual_scores = sum(
            Hf35BffCommonData.get_value_by_json_path(bff_data_obj.get_attempt_body(), '$..score'))
        all_details = Hf35BffCommonData.get_value_by_json_path(bff_data_obj.get_attempt_body(), '$..details')
        learning_result_entity.product_module = LearningResultProductModule.HOMEWORK.value
        learning_result_entity.product = LearningResultProduct.HIGHFLYER.value
        learning_result_entity.business_key = '|'.join(bff_data_obj.get_business_key())
        learning_result_entity.student_key = int(self.customer_id)
        learning_result_entity.expected_score = all_question_expected_scores
        learning_result_entity.actual_score = all_question_actual_scores
        learning_result_entity.details = all_details
        learning_result_entity.start_time = bff_data_obj.get_attempt_body()["startTime"]
        learning_result_entity.end_time = bff_data_obj.get_attempt_body()["endTime"]
        route = {}
        route['course'] = 'HIGH_FLYERS_35'
        route['regionAch'] = 'cn-3'
        route['treeRevision'] = bff_data_obj.get_attempt_body()["treeRevision"]
        route['schemaVersion'] = bff_data_obj.get_attempt_body()["schemaVersion"]
        route['courseContentId'] = bff_data_obj.get_attempt_body()["courseContentId"]
        route['courseContentRevision'] = bff_data_obj.get_attempt_body()["courseContentRevision"]
        route['bookContentId'] = bff_data_obj.get_attempt_body()["bookContentId"]
        route['bookContentRevision'] = bff_data_obj.get_attempt_body()["bookContentRevision"]
        route['unitContentId'] = bff_data_obj.get_attempt_body()["unitContentId"]
        route['unitContentRevision'] = bff_data_obj.get_attempt_body()["unitContentRevision"]
        route['lessonContentId'] = bff_data_obj.get_attempt_body()["lessonContentId"]
        route['lessonContentRevision'] = bff_data_obj.get_attempt_body()["lessonContentRevision"]
        route['learningUnitContentId'] = bff_data_obj.get_attempt_body()["learningUnitContentId"]
        route['learningUnitContentRevision'] = bff_data_obj.get_attempt_body()["learningUnitContentRevision"]
        route['parentContentPath'] = bff_data_obj.get_attempt_body()["parentContentPath"]
        learning_result_entity.route = route

    def setter_learning_result_details(self, learning_details_entity, bff_data_obj):
        """
        set all fields in learning_plan_details_entity
        :param learning_details_entity: all variable are list type
        :param bff_data_obj: json test data object
        :return:
        """
        detail_act_keys = Hf35BffCommonData.get_value_by_json_path(bff_data_obj.get_attempt_body(),
                                                                   '$..activityContentId')
        detail_act_versions = Hf35BffCommonData.get_value_by_json_path(bff_data_obj.get_attempt_body(),
                                                                       '$..activityContentRevision')
        detail_question_keys = Hf35BffCommonData.get_value_by_json_path(bff_data_obj.get_attempt_body(),
                                                                        '$..questionId')
        detail_answers = Hf35BffCommonData.get_value_by_json_path(bff_data_obj.get_attempt_body(), '$..answer')
        detail_expected_scores = Hf35BffCommonData.get_value_by_json_path(bff_data_obj.get_attempt_body(),
                                                                          '$..totalScore')
        detail_actual_scores = Hf35BffCommonData.get_value_by_json_path(bff_data_obj.get_attempt_body(), '$..score')
        learning_details_entity.activity_key = detail_act_keys
        learning_details_entity.activity_version = detail_act_versions
        learning_details_entity.question_key = detail_question_keys
        learning_details_entity.answer = detail_answers
        learning_details_entity.expected_score = detail_expected_scores
        learning_details_entity.actual_score = detail_actual_scores

    def get_course_from_content_map(self, course, schema_version, json_body_dict):
        """
        get course response from content map service
        :param course:
        :param schema_version:
        :param json_body_dict: json body
        :return: get course structure from content map
        """
        content_map_service = ContentMapService(CONTENT_MAP_ENVIRONMENT)
        content_map_entity = ContentMapQueryEntity(course, schema_version)
        self.__setter_content_map_entity(content_map_entity, json_body_dict)
        return content_map_service.post_content_map_query_tree(content_map_entity)

    def __setter_content_map_entity(self, content_map_entity, json_body_dict):
        content_map_entity.child_types = json_body_dict["childTypes"]
        content_map_entity.content_id = json_body_dict["contentId"]
        content_map_entity.region_ach = json_body_dict["regionAch"]
        content_map_entity.tree_revision = json_body_dict["treeRevision"]

    def update_content_negative_body(self, negative_dict, content_body, is_mismatch=False):
        keys = list(negative_dict.keys())
        values = list(negative_dict.values())
        for dict in content_body:
            dict[keys[0]] = negative_dict[keys[0]]
            if is_mismatch:
                break
        return content_body

    def get_current_book_from_bootstrap(self):
        response = self.bff_service.get_bootstrap_controller(platform='ios')
        current_book = jmespath.search('userContext.currentBook', response.json())
        return current_book

    def get_tree_revision_from_course_structure(self):
        response = self.bff_service.get_course_structure()
        tree_revision = response.json()['treeRevision']
        return tree_revision

    def get_reader_default_level_from_course_structure(self):
        current_book = self.get_current_book_from_bootstrap()
        course_structure = self.bff_service.get_course_structure()
        course_structure_json = course_structure.json()
        index = 0
        while 1:
            content_id_path = 'children[%s].contentId' % index
            default_level_path = 'children[%s].default_reader_level' % index

            book_content_id = jmespath.search(content_id_path, course_structure_json)
            if book_content_id == current_book:
                default_level_id = jmespath.search(default_level_path, course_structure_json)
                break
            index += 1
        return default_level_id

    def get_current_unassigned_level(self):
        default_level_id = self.get_reader_default_level_from_course_structure()
        level_focused_response = self.bff_service.get_reader_level_focused(self.customer_id, default_level_id)
        level_focused_json = level_focused_response.json()

        current_level = jmespath.search("currentLevel", level_focused_json)
        index = 0
        while 1:
            level_code_path = "currentLevel[%s].code" % index
            code = jmespath.search(level_code_path, level_focused_json)
            if code == current_level:
                current_level_id = jmespath.search("currentLevel[%s].contentId" % index, level_focused_json)
                current_level_content_revision = jmespath.search("currentLevel[%s].contentRevision" % index, \
                                                                 level_focused_json)
                break
        return current_level_id, current_level_content_revision

    def get_random_date(self, earliest):
        start_time = earliest
        end_time = start_time + 5184000
        t = random.randint(int(start_time), int(end_time))
        t = datetime.datetime.fromtimestamp(t)
        t = datetime.datetime.strftime(t, "%Y-%m-%dT%H:%M:%S.%jZ")
        return t


    def setter_study_plan_entity(self, study_plan_entity, content_path, check_type):
        product_module = [1, 256, 512]
        study_plan_entity.student_id = 1071
        study_plan_entity.product = 2
        if check_type == 0:
            study_plan_entity.product_module = product_module[random.randint(0, 2)]
        else:
            study_plan_entity.product_module = 16
        study_plan_entity.ref_id = "c84b8137-0de5-4f8b-8a16-4ed6d576e063"
        study_plan_entity.ref_content_path = content_path
        ch = chr(random.randrange(ord('A'), ord('Z') + 1))
        session_purpose = ""
        session_purpose += ch
        for i in range(8):
            ch = chr(random.randrange(ord('a'), ord('z') + 1))
            session_purpose += ch
        session_type = ""
        for i in range(6):
            ch = chr(random.randrange(ord('A'), ord('Z') + 1))
            session_type += ch
        study_plan_entity.ref_props = {'sessionPurpose': session_purpose, 'totalAccuracy': str(random.randint(0, 100)),
                                       'sessionType': session_type}
        study_plan_entity.effect_at = self.get_random_date(int(time.mktime(time.strptime(time.strftime("%Y-%m-%dT%H:%M"
                                                                                                       ":%S.%jZ",
                                                                                                       time.localtime()),
                                                                                         "%Y-%m-%dT%H:%M:%S.%jZ"))) - 2592000)
        study_plan_entity.expire_at = self.get_random_date(int(time.mktime(time.strptime(study_plan_entity.effect_at,"%Y-%m-%dT%H:%M:%S.%jZ"))))
        tem = random.randint(0, 1)
        if tem == 0:
            study_plan_entity.start_at = None
            study_plan_entity.complete_at = None
        else:
            study_plan_entity.start_at = self.get_random_date(int(time.mktime(time.strptime(time.strftime("%Y-%m-%dT%H:%M"
                                                                                                       ":%S.%jZ",
                                                                                                       time.localtime()),
                                                                                         "%Y-%m-%dT%H:%M:%S.%jZ"))) - 2592000)
            tem1 = random.randint(0, 1)
            if tem1 == 0:
                study_plan_entity.complete_at = None
            else:
                study_plan_entity.complete_at = self.get_random_date(int(time.mktime(time.strptime(study_plan_entity.start_at,"%Y-%m-%dT%H:%M:%S.%jZ"))))
