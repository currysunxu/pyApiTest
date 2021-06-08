import datetime
import time
import random
import jmespath
import jsonpath
from hamcrest import assert_that, equal_to
import uuid

from E1_API_Automation.Business.HighFlyer35.OneAppBffService import OneAppBffService
from E1_API_Automation.Business.HighFlyer35.HighFlyerUtils.Hf35BffCommonData import Hf35BffCommonData
from E1_API_Automation.Business.NGPlatform.ContentMapService import ContentMapService
from E1_API_Automation.Business.NGPlatform.GeneralTestService import GeneralTestService
from E1_API_Automation.Business.NGPlatform.StudyPlanService import StudyPlanService
from E1_API_Automation.Business.NGPlatform.ContentMapQueryEntity import ContentMapQueryEntity
from E1_API_Automation.Business.NGPlatform.LearningResultService import LearningResultService
from E1_API_Automation.Business.NGPlatform.NGPlatformUtils.LearningEnum import LearningResultProduct, \
    LearningResultProductModule
from E1_API_Automation.Business.NGPlatform.CourseGroupService import CourseGroupService
from E1_API_Automation.Business.OMNIService import OMNIService
from E1_API_Automation.Business.RemediationService import RemediationService
from E1_API_Automation.Business.Utils.CommonUtils import CommonUtils
from E1_API_Automation.Settings import *
from ptest.decorator import BeforeMethod,BeforeClass
from E1_API_Automation.Test_Data.SSUnitQuizData import SSUnitQuizData


from E1_API_Automation.Test_Data.BffData import BffProduct, BffUsers, BusinessData
from E1_API_Automation.Business.AuthService import Auth2Service
from E1_API_Automation.Test_Data.RemediationData import RemediationData


def check_bff_compare_learning_plan(plan_response, leanring_plan_entity):
    assert_that(plan_response.json()[0]["planBusinessKey"], equal_to(leanring_plan_entity.business_key))
    assert_that(int(plan_response.json()[0]["studentKey"]), equal_to(int(leanring_plan_entity.student_key)))
    assert_that(plan_response.json()[0]["bucketId"], equal_to(leanring_plan_entity.bucket_id))
    assert_that(plan_response.json()[0]["productId"], equal_to(leanring_plan_entity.product))
    assert_that(plan_response.json()[0]["state"], equal_to(leanring_plan_entity.state))
    assert_that(plan_response.json()[0]["learningUnit"], equal_to(leanring_plan_entity.learning_unit))
    assert_that(plan_response.json()[0]["route"], equal_to(leanring_plan_entity.route))
    assert_that(plan_response.json()[0]["startTime"], equal_to(leanring_plan_entity.start_time))
    assert_that(plan_response.json()[0]["endTime"], equal_to(leanring_plan_entity.end_time))


class OneAppBffTestBase:

    @BeforeClass()
    def setup(self):
        self.bff_service = OneAppBffService(BFF_ENVIRONMENT)
        self.cm_service = ContentMapService(CONTENT_MAP_ENVIRONMENT)
        self.sp_service = StudyPlanService(STUDY_TIME_ENVIRONMENT)
        self.omni_service = OMNIService(OMNI_ENVIRONMENT)
        self.course_group_service = CourseGroupService(COURSE_GROUP_ENVIRONMENT)
        current_test_program = self.__class__.__name__
        self.key = BffProduct.HFV35.value if current_test_program.startswith('HighFlyer') else BffProduct.SSV3.value
        self.user_name = BffUsers.BffUserPw[env_key][self.key][0]['username']
        self.password = BffUsers.BffUserPw[env_key][self.key][0]['password']
        self.customer_id = self.omni_service.get_customer_id(self.user_name, self.password)

    @BeforeMethod()
    def sign_in(self):
        self.bff_service.login(self.user_name, self.password)
        self.auth2_service = Auth2Service(AUTH2_ENVIRONMENT, self.bff_service.mou_tai.headers['EF-Access-Token'])


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
        route['treeRevision'] = bff_data_obj.get_attempt_body()["treeRevision"]
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

    def get_data_from_content_map_course_node(self, content_path, check_field) -> object:
        content_map_service = ContentMapService(CONTENT_MAP_ENVIRONMENT)
        course_node_response = content_map_service.get_content_map_course_node(content_path)
        return course_node_response.json()[check_field]

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

    def get_current_book_content_path_from_bootstrap(self):
        response = self.bff_service.get_student_context()
        finder_current_book = self.find_current_book(response)
        return finder_current_book

    def get_current_book_content_id_from_bootstrap(self):
        response = self.bff_service.get_student_context()
        finder_current_book = self.find_current_book(response)
        current_book_content_id = jmespath.search("availableBooks[?contentPath=='{0}'].contentId".format(finder_current_book), response.json())[0]
        return current_book_content_id

    def get_check_field_from_content_obj_by_content_path(self, content_object, content_path, check_field) -> object:
        # ..children match assignment level, .children match unit level
        try:
            expression = '$..children[?(@.contentPath=="{0}")]' if "assignment" in content_path else '$.children[?(@.contentPath=="{0}")]'
            dict_obj = jsonpath.jsonpath(content_object,expression.format(content_path))[0]
        except Exception as e:
            print(str(e))
            print(content_path)
        return dict_obj[check_field]

    def find_current_book(self, response):
        current_book = jmespath.search('currentBook', response.json())
        availableBooks = jmespath.search('availableBooks', response.json())
        finder_current_book = current_book if current_book != 'unsupported/book' else availableBooks[-1]['contentPath']
        return finder_current_book

    def get_tree_revision_from_course_structure(self):
        response = self.bff_service.get_course_structure()
        tree_revision = response.json()['treeRevision']
        return tree_revision

    def get_reader_default_level_from_course_structure(self):
        current_book = self.get_current_book_content_path_from_bootstrap()
        course_structure = self.bff_service.get_book_structure_v2(current_book)
        course_structure_json = course_structure.json()
        index = 0
        while 1:
            book_content_path = jmespath.search("contentPath", course_structure_json)
            if book_content_path == current_book:
                default_level_id = jmespath.search("default_reader_level", course_structure_json)
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
        product_module = [1, 128, 256, 512]
        study_plan_entity.student_id = self.omni_service.get_customer_id(self.user_name, self.password)
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

    def get_content_path_from_acl(self,acl_response):
        # get core and activated program
        core_and_activated_program = jsonpath.jsonpath(acl_response.json(), "$.[?(@.type == 'CORE' && @.activated == True)].program")[0]
        levels = jsonpath.jsonpath(acl_response.json(), "$.[?(@.program == '{}')].levels".format(core_and_activated_program))
        expect_levels = []
        for level in levels[0]:
            if not level['isSwapped'] and level['state'] == "INPROGRESS" and 'contentPath' in level:
                expect_levels.append(level)
        # if all completed status ,get content path by original levels
        # else get the biggest level by inprogress status
        if len(expect_levels) == 0:
            content_path = levels[0][len(levels[0]) - 1]["contentPath"]
        elif len(expect_levels) >= 0:
            content_path = expect_levels[len(expect_levels)-1]["contentPath"]

        return content_path

    def submit_remediation_best_attempts(self, test_id, test_instance_key,start,end):
        actual_score = CommonUtils.randomFloatToString(start, end)
        remediation_body = RemediationData.build_remediation_activities(test_instance_key, test_id, actual_score)
        bff_remediation_response = self.bff_service.post_best_remediation_attempts(remediation_body)
        return bff_remediation_response

    def verify_bff_best_attempts(self, test_instance_key):
        remediation = RemediationService(REMEDIATION_ENVIRONMENT)
        best_attempts = remediation.get_best_remediation_attempts(self.customer_id, test_instance_key)
        bff_best_attempts = self.bff_service.get_best_remediation_attempts(test_instance_key)
        assert_that(bff_best_attempts.status_code, equal_to(200))
        assert_that(bff_best_attempts.json()[0], equal_to(best_attempts.json()[0]))

    def get_specific_data_from_course_node(self, content_path, field):
        content_map_course_node = self.cm_service.get_content_map_course_node(content_path)
        return content_map_course_node.json()[field]

    def unlock_ss_unit_quiz(self):
        global unlock_response
        course_node_response = self.cm_service.get_content_map_course_node(BusinessData.SS_UNIT_CONTENT_PATH,
                                                                           "WITH_DESCENDANTS").json()
        last_assignment_content_path = course_node_response['children'][course_node_response['childCount'] - 1][
            'contentPath']
        general_test_svc = GeneralTestService(GENERAL_TEST_ENVIRONMENT)
        general_test = general_test_svc.get_test_by_student_and_content_path(self.customer_id,
                                                                             BusinessData.SS_UNIT_CONTENT_PATH)
        if general_test.status_code == 204:
            # 204 mean no unlock for current test
            unlock_response = general_test_svc.put_unlock_unit_quiz(self.customer_id, last_assignment_content_path)
            assert_that(unlock_response.status_code, equal_to(200))
            return general_test, general_test_svc, unlock_response
        return general_test, general_test_svc, None