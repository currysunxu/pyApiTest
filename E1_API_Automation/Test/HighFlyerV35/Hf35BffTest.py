import datetime
import json
import random
import uuid

import jmespath
from hamcrest import assert_that, equal_to
from ptest.decorator import TestClass, Test

from E1_API_Automation.Business.HighFlyer35.Hf35BffWordAttemptEntity import Hf35BffWordAttemptEntity
from E1_API_Automation.Business.HighFlyer35.HighFlyerUtils.Hf35BffCommonData import Hf35BffCommonData
from E1_API_Automation.Business.HighFlyer35.HighFlyerUtils.Hf35BffUtils import Hf35BffUtils
from E1_API_Automation.Business.KSDInternalService import KSDInternalService
from E1_API_Automation.Business.KidsEVC import KidsEVCService
from E1_API_Automation.Business.NGPlatform.ContentRepoService import ContentRepoService
from E1_API_Automation.Business.NGPlatform.CourseGroupService import CourseGroupService
from E1_API_Automation.Business.NGPlatform.HomeworkService import HomeworkService
from E1_API_Automation.Business.NGPlatform.LearningResultDetailEntity import LearningResultDetailEntity
from E1_API_Automation.Business.NGPlatform.LearningResultEntity import LearningResultEntity
from E1_API_Automation.Business.NGPlatform.NGPlatformUtils.ContentRepoCommonData import ContentRepoCommonData
from E1_API_Automation.Business.ProvisioningService import ProvisioningService
from E1_API_Automation.Business.UpsPrivacyService import UpsPrivacyService
from E1_API_Automation.Business.Utils.EnvUtils import EnvUtils
from E1_API_Automation.Lib.HamcrestMatcher import match_to
from E1_API_Automation.Settings import *
from E1_API_Automation.Test.HighFlyerV35.HfBffTestBase import HfBffTestBase
from E1_API_Automation.Test_Data.BffData import BffUsers, HF35DependService, BffProduct
from E1_API_Automation.Business.NGPlatform.NGPlatformUtils.ContentRepoEnum import ContentRepoContentType, \
    ContentRepoGroupType
from E1_API_Automation.Business.HighFlyer35.HighFlyerUtils.HF35BffEnum import OnlineScope
from E1_API_Automation.Business.Utils.EVCUtils import EVCUtils


@TestClass()
class Hf35BffTest(HfBffTestBase):

    @Test(tags="qa, stg, live")
    def test_bff_auth_login_valid_username(self):
        product_keys = BffUsers.BffUserPw[env_key].keys()
        for key in product_keys:
            user_name = BffUsers.BffUserPw[env_key][key][0]['username']
            password = BffUsers.BffUserPw[env_key][key][0]['password']
            # all type users can login with auth2 successfully
            response = self.bff_service.login(user_name, password)
            assert_that(response.status_code, equal_to(200))
            id_token = jmespath.search('idToken', response.json())
            access_token = jmespath.search('accessToken', response.json())
            refresh_token = jmespath.search('refreshToken', response.json())
            assert_that((not id_token == "" and id_token.__str__() is not None))
            assert_that((not access_token == "" and access_token.__str__() is not None))
            assert_that((not refresh_token == "" and refresh_token.__str__() is not None))


    @Test(tags="qa, stg, live")
    def test_bff_auth_login_invalid_username(self):
        user_name = "invalidUserName%s" % (random.randint(1, 100))
        password = "invalidPassword"
        response = self.bff_service.login(user_name, password)
        print("Bff login response is : %s" % (response.__str__()))
        # as QA using mock omni, so the behavior is little different
        if EnvUtils.is_env_qa():
            assert_that(response.status_code, equal_to(404))
        else:
            assert_that(response.status_code, equal_to(401))

    # only HFV2, HFV3Plus user can call bff apis successfully, other users can't call bff apis, will return 401
    @Test(tags="qa, stg, live")
    def test_auth2_authorization(self):
        product_keys = BffUsers.BffUserPw[env_key].keys()
        for key in product_keys:
            user_name = BffUsers.BffUserPw[env_key][key][0]['username']
            password = BffUsers.BffUserPw[env_key][key][0]['password']
            # all type users can login successfully
            response = self.bff_service.login(user_name, password)
            assert_that(response.status_code, equal_to(200))

            # only HFV2, HFV3Plus users can call bff apis, others can't
            response = self.bff_service.get_bootstrap_controller('ios')
            if key in (BffProduct.HFV2.value, BffProduct.HFV3.value, BffProduct.HFV35.value):
                assert_that(response.status_code, equal_to(200))
                assert_that(response.json(), match_to("provision"))
                assert_that(response.json(), match_to("userContext.availableBooks"))
                assert_that(response.json(), match_to("userContext.currentBook"))
            else:
                assert_that(response.status_code, equal_to(401))
                assert_that((response.json()['error'] == "Unauthorized"))
                assert_that((response.json()['message'] == "Unauthorized program."))

    @Test(tags="qa, stg, live", data_provider=["noToken"])
    def test_submit_new_attempt_without_auth_token(self, negative_para):
        bff_data_obj = Hf35BffCommonData()
        response = self.bff_service.submit_new_attempt_with_negative_auth_token(bff_data_obj.get_attempt_body(),
                                                                                negative_para)
        print("Bff login response is : %s" % (response.__str__()))
        assert_that(response.status_code, equal_to(400))
        assert_that((response.json()['error'] == "Bad Request"))

    @Test(tags="qa, stg, live", data_provider=["", "invalid", "noToken", "expired"])
    def test_submit_new_attempt_with_invalid_auth_token(self, negative_para):
        bff_data_obj = Hf35BffCommonData()
        response = self.bff_service.submit_new_attempt_with_negative_auth_token(bff_data_obj.get_attempt_body(),
                                                                                negative_para)
        self.verify_bff_api_response_with_invalid_token(negative_para, response)

    @Test(tags="qa, stg, live", data_provider=[(1, 1), (2, 4), (4, 2)])
    def test_submit_new_attempt_with_valid_body(self, activity_num, detail_num):
        bff_data_obj = Hf35BffCommonData(activity_num, detail_num)
        submit_response = self.bff_service.submit_new_attempt(bff_data_obj.get_attempt_body())
        print("Bff submit response is : %s" % (submit_response.__str__()))
        print("Bff submit response is : %s" % (submit_response.text))
        assert_that(submit_response.status_code, equal_to(200))
        assert_that(not submit_response.text == "")
        # check learning result
        learning_result_entity = LearningResultEntity(None, None, None)
        self.setter_learning_result(learning_result_entity, bff_data_obj)
        result_response = self.get_learning_result_response(learning_result_entity)
        assert_that(result_response.status_code, equal_to(200))
        assert_that(submit_response.text[1:-1], equal_to(result_response.json()[0]["resultKey"]))
        learning_details_entity = LearningResultDetailEntity(None)
        self.setter_learning_result_details(learning_details_entity, bff_data_obj)
        self.check_bff_compare_learning_result(result_response, learning_result_entity, learning_details_entity)

    @Test(tags="qa, stg, live", data_provider=[(1, 1), (4, 2)])
    def test_submit_best_attempt(self, activity_num, detail_num):
        bff_data_obj = Hf35BffCommonData(activity_num, detail_num)
        submit_response = self.bff_service.submit_new_attempt(bff_data_obj.get_attempt_body())
        print("Bff submit response is : %s" % (submit_response.__str__()))
        print("Bff submit response is : %s" % (submit_response.text))
        assert_that(submit_response.status_code, equal_to(200))
        bff_data_obj.set_best_attempt()
        submit_best_response = self.bff_service.submit_new_attempt(bff_data_obj.previous_attempt)
        assert_that(submit_best_response.status_code, equal_to(200))
        book_content_id = bff_data_obj.get_attempt_body()["bookContentId"]
        best_submit_response = self.bff_service.get_the_best_attempt(book_content_id)
        # check bff get best attempt
        bff_best_total_score = sum(
            Hf35BffCommonData.get_value_by_json_path(best_submit_response.json()[0], "$.activities..totalScore"))
        expected_total_score = sum(Hf35BffCommonData.get_value_by_json_path(bff_data_obj.attempt_json, "$..totalScore"))
        bff_best_score = sum(
            Hf35BffCommonData.get_value_by_json_path(best_submit_response.json()[0], "$.activities..score"))
        expected_score = sum(Hf35BffCommonData.get_value_by_json_path(bff_data_obj.attempt_json, "$..score"))
        print("Expected result is : %s" % (bff_data_obj.attempt_json))
        print("Actual result is : %s" % (best_submit_response.json()[0]))
        assert_that(bff_best_total_score, equal_to(expected_total_score))
        assert_that(bff_best_score, equal_to(expected_score))

        # following two fields are hardcoded
        course = Hf35BffCommonData.get_value_by_json_path(best_submit_response.json()[0], "$.course")
        region_ach = Hf35BffCommonData.get_value_by_json_path(best_submit_response.json()[0], "$.regionAch")
        assert_that(course[0], equal_to('HIGH_FLYERS_35'))
        assert_that(region_ach[0], equal_to('cn-3'))

        # check homework service best attempt
        homework_service = HomeworkService(HOMEWORK_ENVIRONMENT)
        homework_best_attempt_response = homework_service.get_the_best_attempt(self.customer_id, book_content_id)
        homework_best_total_score = sum(
            Hf35BffCommonData.get_value_by_json_path(homework_best_attempt_response.json()[0],
                                                     "$.activities..totalScore"))
        homework_best_score = sum(
            Hf35BffCommonData.get_value_by_json_path(homework_best_attempt_response.json()[0], "$.activities..score"))
        assert_that(homework_best_total_score, equal_to(bff_best_total_score))
        assert_that(homework_best_score, equal_to(bff_best_score))
        assert_that(best_submit_response.json(), equal_to(homework_best_attempt_response.json()))

    @Test(tags="qa, stg, live", data_provider=[("HIGH_FLYERS_35", "1")])
    def test_get_course_structure(self, course, scheme_version):
        bff_course_response = self.bff_service.get_course_structure()
        print("Bff get course response is : %s" % (json.dumps(bff_course_response.json(), indent=4)))
        assert_that(bff_course_response.status_code, equal_to(200))
        json_body = {
            "childTypes": ["COURSE", "BOOK"],
            "contentId": None,
            "regionAch": "cn-3",
            "treeRevision": None
        }
        content_map_response = self.get_course_from_content_map(course, scheme_version, json_body)
        assert_that(bff_course_response.json(), equal_to(content_map_response.json()))

    @Test(tags="qa, stg, live", data_provider=[("HIGH_FLYERS_35", "1")])
    def test_get_book_structure(self, course, scheme_version):
        json_body = {
            "childTypes": ["COURSE", "BOOK", "UNIT", "LESSON"],
            "contentId": None,
            "regionAch": "cn-3",
            "treeRevision": None
        }
        content_map_response = self.get_course_from_content_map(course, scheme_version, json_body)
        assert_that(content_map_response.status_code == 200)
        content_id_from_content_map = content_map_response.json()["contentId"]
        tree_revision_from_content_map = content_map_response.json()["treeRevision"]
        bff_book_response = self.bff_service.get_book_structure(content_id_from_content_map,
                                                                tree_revision_from_content_map)
        print("Bff get course response is : %s" % (json.dumps(bff_book_response.json(), indent=4)))
        assert_that(bff_book_response.status_code, equal_to(200))
        assert_that(bff_book_response.json(), equal_to(content_map_response.json()))

    def verify_bff_api_response_with_invalid_token(self, invalid_type, api_response):
        if invalid_type in ("noToken", ""):
            assert_that(api_response.status_code, equal_to(400))
            assert_that((api_response.json()['error'] == "Bad Request"))
            assert_that((api_response.json()['message'] == "token required"))
        elif invalid_type == "expired":
            # in stg, live, as we have hotfix, for expire token, the status become 401
            assert_that(api_response.status_code, equal_to(401))
            assert_that((api_response.json()['error'] == "Unauthorized"))
            assert_that((api_response.json()['message'] == "token expired"))
        else:
            assert_that(api_response.status_code, equal_to(403))
            assert_that((api_response.json()['error'] == "Forbidden"))
            assert_that((api_response.json()['message'] == "invalid token"))

    @Test(tags="qa, stg, live", data_provider=["", "invalid", "noToken", "expired"])
    def test_get_course_structure_with_invalid_token(self, invalid):
        bff_course_response = self.bff_service.get_course_structure_with_negative_token(invalid)
        print("Bff get course response is : %s" % (json.dumps(bff_course_response.json(), indent=4)))
        print("Bff get course response : %s" % (bff_course_response.__str__()))
        self.verify_bff_api_response_with_invalid_token(invalid, bff_course_response)

    @Test(tags="qa, stg, live", data_provider=["", "invalid", "noToken", "expired"])
    def test_get_book_structure_with_invalid_token(self, invalid):
        json_body = {
            "childTypes": ["COURSE", "BOOK", "UNIT", "LESSON"],
            "contentId": None,
            "regionAch": "cn-3",
            "treeRevision": None
        }
        content_map_response = self.get_course_from_content_map("HIGH_FLYERS_35", "1", json_body)
        content_id_from_content_map = content_map_response.json()["contentId"]
        tree_revision_from_content_map = content_map_response.json()["treeRevision"]
        bff_book_response = self.bff_service.get_book_structure_with_negative_token(content_id_from_content_map,
                                                                                    tree_revision_from_content_map,
                                                                                    invalid)
        self.verify_bff_api_response_with_invalid_token(invalid, bff_book_response)

    @Test(tags="qa, stg, live", data_provider=["no_content_id", "no_tree_revision"])
    def test_get_book_structure_without_contentId_or_treeRevision(self, invalid):
        json_body = {
            "childTypes": ["COURSE", "BOOK", "UNIT", "LESSON"],
            "contentId": None,
            "regionAch": "cn-3",
            "treeRevision": None
        }
        content_map_response = self.get_course_from_content_map("HIGH_FLYERS_35", "1", json_body)
        if invalid == "no_content_id":
            content_id_from_content_map = ""
        else:
            content_id_from_content_map = content_map_response.json()["contentId"]
        if invalid == "no_tree_revision":
            tree_revision_from_content_map = ""
        else:
            tree_revision_from_content_map = content_map_response.json()["treeRevision"]

        bff_book_response = self.bff_service.get_book_structure(content_id_from_content_map,
                                                                tree_revision_from_content_map)
        print("Bff get book response is : %s" % (json.dumps(bff_book_response.json(), indent=4)))
        print("Bff get book response : %s" % (bff_book_response.__str__()))
        if invalid == "no_content_id":
            assert_that(bff_book_response.status_code, equal_to(404))
            assert_that((bff_book_response.json()['error'] == ("Not Found")))
        elif invalid == "no_tree_revision":
            assert_that(bff_book_response.status_code, equal_to(400))
            assert_that((bff_book_response.json()['error'] == ("Bad Request")))
            assert_that((bff_book_response.json()['message'] == ("getBookStructure.treeRevision: must not be empty")))

    @Test(tags="qa, stg, live", data_provider=["no_uuid"])
    def test_get_book_structure_with_invalid_contentId(self, invalid):
        json_body = {
            "childTypes": ["COURSE", "BOOK", "UNIT", "LESSON"],
            "contentId": None,
            "regionAch": "cn-3",
            "treeRevision": None
        }
        content_map_response = self.get_course_from_content_map("HIGH_FLYERS_35", "1", json_body)
        if invalid == "no_uuid":
            content_id_from_content_map = "5ba2a7066356aaa"
        tree_revision_from_content_map = content_map_response.json()["treeRevision"]

        bff_book_response = self.bff_service.get_book_structure(content_id_from_content_map,
                                                                tree_revision_from_content_map)
        print("Bff get book response is : %s" % (json.dumps(bff_book_response.json(), indent=4)))
        print("Bff get book response : %s" % (bff_book_response.__str__()))
        assert_that(bff_book_response.status_code, equal_to(400))
        assert_that((bff_book_response.json()['error'] == "Bad Request"))

    @Test(tags="qa, stg, live", data_provider=["", "invalid", "noToken", "expired"])
    def test_post_homework_activity_with_negative_token(self, negative_token):
        content_repo_data = ContentRepoCommonData()
        # insert content
        content_repo_service = ContentRepoService(CONTENT_REPO_ENVIRONMENT)
        content_json_body = content_repo_data.get_activity_content()
        content_repo_response = content_repo_service.post_content(content_json_body)
        assert_that(content_repo_response.status_code == 200)
        content_activities_response = content_repo_service.get_activities(content_repo_response.json()["savedItems"])
        bff_invalid_response = self.bff_service.get_homework_activities_with_negative_token(
            content_activities_response.json(), negative_token)
        self.verify_bff_api_response_with_invalid_token(negative_token, bff_invalid_response)

    @Test(tags="qa, stg, live", data_provider=[{"contentId": ""}, {"contentId": None}, {"contentRevision": ""},
                                    {"contentId": "test_neg"}, {"contentRevision": None},
                                    {"schemaVersion": ""}, {"schemaVersion": None}, {"schemaVersion": "c"}])
    def test_post_homework_activity_with_negative_parameter(self, negative_parameter):
        content_repo_data = ContentRepoCommonData()
        # insert content
        content_repo_service = ContentRepoService(CONTENT_REPO_ENVIRONMENT)
        content_json_body = content_repo_data.get_activity_content()
        content_repo_response = content_repo_service.post_content(content_json_body)
        assert_that(content_repo_response.status_code == 200)
        content_activities_response = content_repo_service.get_activities(content_repo_response.json()["savedItems"])
        bff_negative_json = self.update_content_negative_body(negative_parameter, content_activities_response.json())
        bff_invalid_response = self.bff_service.get_homework_activities(bff_negative_json)
        assert_that(bff_invalid_response.status_code, equal_to(400))
        assert_that((bff_invalid_response.json()['error'] == "Bad Request"))

    @Test(tags="qa, stg, live", data_provider=["", "invalid", "noToken", "expired"])
    def test_post_homework_activity_group_with_negative_token(self, negative_token):
        content_repo_data = ContentRepoCommonData()
        # insert content
        content_repo_service = ContentRepoService(CONTENT_REPO_ENVIRONMENT)
        content_json_body = content_repo_data.get_activity_content()
        content_repo_response = content_repo_service.post_content(content_json_body)
        assert_that(content_repo_response.status_code == 200)
        # insert content group
        content_group_json_body = content_repo_data.get_activity_or_asset_content_group()
        content_group_repo_response = content_repo_service.post_content_group(content_group_json_body)
        assert_that(content_group_repo_response.status_code == 200)
        query_content_group_json_body = content_group_repo_response.json()["savedItems"][0].copy()
        query_content_group_json_body.pop("savedContentType")
        query_content_group_json_body["parentContentId"] = query_content_group_json_body.pop("contentId")
        query_content_group_json_body["parentContentRevision"] = query_content_group_json_body.pop(
            "contentRevision")
        query_content_group_json_body["parentSchemaVersion"] = query_content_group_json_body.pop("schemaVersion")
        # bff get activity group
        bff_invalid_response = self.bff_service.get_homework_activities_group_with_negative_token(
            query_content_group_json_body["parentContentRevision"],
            query_content_group_json_body["parentContentId"],
            negative_token)
        self.verify_bff_api_response_with_invalid_token(negative_token, bff_invalid_response)

    @Test(tags="qa, stg, live", data_provider=[("", "5f99af36-cad7-4a45-b811-02c9076f47f1", 1),
                                    ("test_content_revision", "", 1),
                                    ("test_content_revision", "5f99af36-cad7-4a45-b811-02c9076f47f1", ""),
                                    ("testRevision", "non-uuid", 1),
                                    ("test_content_revision", "5f99af36-cad7-4a45-b811-02c9076f47f1", "ss")])
    def test_post_homework_activity_group_with_negative_parameter(self, negative_content_revision, negative_content_id,
                                                                  negative_schema_version):
        bff_activity_response = self.bff_service.get_homework_activity_asset_group(negative_content_revision,
                                                                                   negative_content_id,
                                                                                   negative_schema_version)
        assert_that(bff_activity_response.status_code == 400)
        assert_that((bff_activity_response.json()['error'] == "Bad Request"))

    @Test(tags="qa, stg, live", data_provider=[("test_content_revision", "5f99af36-cad7-4a45-b811-02c9076f47f1", 1)])
    def test_post_homework_activity_asset_group_with_mismatch_para(self, negative_content_revision,
                                                                   negative_content_id, negative_schema_version):
        bff_mismatch_response = self.bff_service.get_homework_activity_asset_group(negative_content_revision,
                                                                                   negative_content_id,
                                                                                   negative_schema_version)
        assert_that(bff_mismatch_response.status_code == 200)
        expected_result = {
            "activityGroups": [],
            "assetGroups": []
        }
        assert_that(bff_mismatch_response.json(), equal_to(expected_result))

    @Test(tags="qa, stg, live")
    def test_bootstrap_controller_with_wrong_platform_number(self):
        response = self.bff_service.get_bootstrap_controller(platform=None)
        assert_that(response.status_code == 400)

        response = self.bff_service.get_bootstrap_controller(platform=2)
        assert_that(response.status_code == 409)

    def test_bootstrap_controller_by_platform(self, platform):
        response = self.bff_service.get_bootstrap_controller(platform=platform)
        assert_that(response.json(), match_to("provision"))
        assert_that(response.json(), match_to("userContext.availableBooks"))
        assert_that(response.json(), match_to("userContext.currentBook"))
        # assert_that(jmespath.search('provision.name', response.json()), contains_string('iOS APP'))
        if platform == 'ios':
            platform_type = 1
        else:
            platform_type = 2

        assert_that(jmespath.search('provision.platformType', response.json()), equal_to(platform_type))
        provisioning_service = ProvisioningService(HF35DependService.provisioning_service[env_key]['host'])
        platform_key = HF35DependService.provisioning_service[env_key][platform + '-app-key']
        provisioning_response = provisioning_service.get_app_version_by_platform_key(platform_key)
        Hf35BffUtils.verify_bootstrap_provision(response.json()['provision'], provisioning_response.json())

        ksd_internal_service = KSDInternalService(HF35DependService.ksd_internal_service[env_key]['host'])
        ksd_oc_context_response = ksd_internal_service.get_ksd_oc_context(self.customer_id, platform)
        expected_oc_context = ksd_oc_context_response.json()

        assert_that(json.dumps(response.json()['ocContext']), equal_to(json.dumps(expected_oc_context)))

    @Test(tags="qa, stg, live")
    def test_bootstrap_controller_ios_platform(self):
        self.test_bootstrap_controller_by_platform('ios')


    @Test(tags="qa, stg, live")
    def test_bootstrap_controller_android_platform(self):
        self.test_bootstrap_controller_by_platform('android')

    @Test(tags="qa, stg, live")
    def test_get_unlock_progress(self):
        current_book = self.get_current_book_from_bootstrap()
        print(current_book)
        bff_unlock_response = self.bff_service.get_unlock_progress_controller(current_book)
        assert_that(bff_unlock_response.status_code == 200)

        course_group_service = CourseGroupService(COURSE_GROUP_ENVIRONMENT)
        course_group_unlock_response = course_group_service.get_unlock_progress(self.customer_id, current_book)
        assert_that(course_group_unlock_response.status_code == 200)

        assert_that(bff_unlock_response.json(), equal_to(course_group_unlock_response.json()))

    @Test(tags="qa, stg, live")
    def test_get_homework_content_groups(self):
        current_book = self.get_current_book_from_bootstrap()
        tree_revision = self.get_tree_revision_from_course_structure()
        book_structure_response = self.bff_service.get_book_structure(current_book, tree_revision)
        unit_content_id = jmespath.search('children[0].contentId', book_structure_response.json())
        unit_content_revision = jmespath.search('children[0].contentRevision', book_structure_response.json())
        unit_schema_version = jmespath.search('children[0].schemaVersion', book_structure_response.json())
        bff_homework_content_group_response = self.bff_service.get_homework_activity_asset_group(unit_content_revision,
                                                                                                 unit_content_id,
                                                                                                 unit_schema_version)
        assert_that(bff_homework_content_group_response.status_code == 200)

        content_repo_service = ContentRepoService(CONTENT_REPO_ENVIRONMENT)
        homework_activity_group_response = \
            content_repo_service.get_content_groups_by_param(ContentRepoContentType.TypeHomework.value,
                                                             ContentRepoGroupType.TypeActivityGroup.value,
                                                             unit_content_id, unit_content_revision,
                                                             unit_schema_version)
        assert_that(homework_activity_group_response.status_code == 200)

        homework_asset_group_response = \
            content_repo_service.get_content_groups_by_param(ContentRepoContentType.TypeHomework.value,
                                                             ContentRepoGroupType.TypeAssetGroup.value,
                                                             unit_content_id, unit_content_revision,
                                                             unit_schema_version)
        assert_that(homework_asset_group_response.status_code == 200)

        assert_that(bff_homework_content_group_response.json()["activityGroups"],
                    equal_to(homework_activity_group_response.json()))
        assert_that(bff_homework_content_group_response.json()["assetGroups"],
                    equal_to(homework_asset_group_response.json()))

    @Test(tags="qa, stg, live")
    def test_get_handout_content_groups(self):
        book_content_id = self.get_current_book_from_bootstrap()
        course_structure_response = self.bff_service.get_course_structure()

        book_content_revision = jmespath.search('children[?contentId==\'%s\'].contentRevision| [0]' % (book_content_id),
                                                course_structure_response.json())
        book_schema_version = jmespath.search('children[?contentId==\'%s\'].schemaVersion| [0]' % (book_content_id),
                                              course_structure_response.json())

        bff_handout_content_group_response = \
            self.bff_service.get_handout_content_groups(book_content_id, book_content_revision, book_schema_version)
        assert_that(bff_handout_content_group_response.status_code == 200)

        content_repo_service = ContentRepoService(CONTENT_REPO_ENVIRONMENT)
        handout_eca_group_response = \
            content_repo_service.get_content_groups_by_param(ContentRepoContentType.TypeHandout.value,
                                                             ContentRepoGroupType.TypeECAGroup.value,
                                                             book_content_id, book_content_revision,
                                                             book_schema_version)
        assert_that(handout_eca_group_response.status_code == 200)

        handout_asset_group_response = \
            content_repo_service.get_content_groups_by_param(ContentRepoContentType.TypeHandout.value,
                                                             ContentRepoGroupType.TypeAssetGroup.value,
                                                             book_content_id, book_content_revision,
                                                             book_schema_version)
        assert_that(handout_asset_group_response.status_code == 200)

        assert_that(bff_handout_content_group_response.json()["ecaGroups"],
                    equal_to(handout_eca_group_response.json()))
        assert_that(bff_handout_content_group_response.json()["assetGroups"],
                    equal_to(handout_asset_group_response.json()))

    @Test(tags="qa, stg, live")
    def test_get_homework_activities(self):
        current_book = self.get_current_book_from_bootstrap()
        tree_revision = self.get_tree_revision_from_course_structure()
        book_structure_response = self.bff_service.get_book_structure(current_book, tree_revision)
        unit_content_id = jmespath.search('children[0].contentId', book_structure_response.json())
        unit_content_revision = jmespath.search('children[0].contentRevision', book_structure_response.json())
        unit_schema_version = jmespath.search('children[0].schemaVersion', book_structure_response.json())
        bff_homework_content_group_response = self.bff_service.get_homework_activity_asset_group(unit_content_revision,
                                                                                                 unit_content_id,
                                                                                                 unit_schema_version)
        assert_that(bff_homework_content_group_response.status_code == 200)
        # get two activity items from activity group
        activity_filter_body = jmespath.search(
            'activityGroups[0].childRefs[:2].{schemaVersion:schemaVersion,contentId:contentId, contentRevision:contentRevision}',
            bff_homework_content_group_response.json())
        bff_activity_response = self.bff_service.get_homework_activities(activity_filter_body)
        assert_that(bff_activity_response.status_code == 200)

        content_repo_service = ContentRepoService(CONTENT_REPO_ENVIRONMENT)
        content_repo_activity_response = content_repo_service.get_activities(activity_filter_body)
        assert_that(content_repo_activity_response.status_code == 200)
        # check the bff activity api response will be same to what you get from content repo, order by id
        assert_that(bff_activity_response.json().sort(key=lambda k:(k.get('id',0))), equal_to(content_repo_activity_response.json().sort(key=lambda k:(k.get('id',0)))))

    @Test(tags="qa, stg, live")
    def test_get_handout_eca(self):
        book_content_id = self.get_current_book_from_bootstrap()
        course_structure_response = self.bff_service.get_course_structure()

        book_content_revision = jmespath.search('children[?contentId==\'%s\'].contentRevision| [0]' % (book_content_id),
                                                course_structure_response.json())
        book_schema_version = jmespath.search('children[?contentId==\'%s\'].schemaVersion| [0]' % (book_content_id),
                                              course_structure_response.json())

        bff_handout_content_group_response = \
            self.bff_service.get_handout_content_groups(book_content_id, book_content_revision, book_schema_version)
        assert_that(bff_handout_content_group_response.status_code == 200)

        # get two eca items from eca group
        eca_filter_body = jmespath.search(
            'ecaGroups[0].childRefs[:2].{schemaVersion:schemaVersion,contentId:contentId, contentRevision:contentRevision}',
            bff_handout_content_group_response.json())
        bff_eca_response = self.bff_service.get_handout_ecas(eca_filter_body)
        assert_that(bff_eca_response.status_code == 200)

        content_repo_service = ContentRepoService(CONTENT_REPO_ENVIRONMENT)
        content_repo_eca_response = content_repo_service.get_ecas(eca_filter_body)
        assert_that(content_repo_eca_response.status_code == 200)
        # check the bff eca api response will be same to what you get from content repo
        assert_that(bff_eca_response.json(), equal_to(content_repo_eca_response.json()))

    # test get online class for ksd
    @Test(tags="qa, stg, live")
    def test_get_online_pl_class_ksd(self):
        bff_online_ksd_response = self.bff_service.get_online_pl_class(OnlineScope.KSD.value)
        assert_that(bff_online_ksd_response.status_code == 200)
        local_time_utc = datetime.datetime.utcnow()
        # if there's no data found, need to create ksd online class first
        if len(bff_online_ksd_response.json()) == 0 and not EnvUtils.is_env_live():
            #schedule a pl class base on current date
            schedule_pl = EVCUtils.schedule_evc_pl(self.bff_service.id_token,local_time_utc,"HFV3Plus")

            # after insert online data, get hf35 bff data again
            bff_online_ksd_response = self.bff_service.get_online_pl_class(OnlineScope.KSD.value)
            assert_that(bff_online_ksd_response.status_code == 200)
            #assert new schedule PL in bff online api
            assert_that(jmespath.search('axisClassId', schedule_pl) in jmespath.search('[].classId',bff_online_ksd_response.json()))


        evc_service = KidsEVCService(KSD_ENVIRONMENT)
        evc_service.mou_tai.headers['X-EF-TOKEN'] = self.bff_service.id_token
        date_time_format = "%Y-%m-%dT%H:%M:%S.%fZ"

        # start time is 3 hours before current utc time, end time is 4 weeks after current utc time
        start_time_utc = (local_time_utc - datetime.timedelta(hours=3)).strftime(date_time_format)
        end_time_utc = (local_time_utc + datetime.timedelta(days=28)).strftime(date_time_format)

        evc_student_online_class_response = evc_service.get_hfv3plus_student_online_class(start_time_utc, end_time_utc)
        # code will filter out endDateTimeUtc greater than current utc time data, and classStatus in ("Booked", "Ongoing", "Attended")
        evc_student_online_class_expected = jmespath.search(
            '[?endDateTimeUtc>\'' + local_time_utc.strftime(date_time_format)
            + '\' && (classStatus == \'Booked\' || classStatus == \'Ongoing\' || classStatus == \'Attended\')]',
            evc_student_online_class_response.json())
        teacher_id_set = set(jmespath.search('[].teacherId', evc_student_online_class_expected))

        evc_teacher_info_response = evc_service.get_teacher_info(teacher_id_set)

        error_message = Hf35BffUtils.verify_ksd_online_pl_class(bff_online_ksd_response.json(),
                                                                evc_student_online_class_expected,
                                                                evc_teacher_info_response.json())
        assert_that(error_message == '', error_message)

    @Test(tags="qa, stg, live")
    def test_get_online_pl_class_osd(self):
        bff_online_osd_response = self.bff_service.get_online_pl_class(OnlineScope.OSD.value)
        assert_that(bff_online_osd_response.status_code == 200)

    @Test(tags="qa, stg, live")
    def test_get_online_gl_class(self):
        bff_online_gl_response = self.bff_service.get_online_gl_class()
        assert_that(bff_online_gl_response.status_code == 200)

        evc_service = KidsEVCService(KSD_ENVIRONMENT)
        evc_service.mou_tai.headers['X-EF-TOKEN'] = self.bff_service.id_token
        evc_group_class_response = evc_service.get_offline_classes()
        assert_that(evc_group_class_response.status_code == 200)

        error_message = Hf35BffUtils.verify_online_gl_class(bff_online_gl_response.json(),
                                                                evc_group_class_response.json())
        assert_that(error_message == '', error_message)

    @Test(tags="qa, stg, live")
    def test_get_privacy_policy_document(self):
        bff_privacy_policy_document_response = self.bff_service.get_privacy_policy_document()
        assert_that(bff_privacy_policy_document_response.status_code == 200)

        ups_service = UpsPrivacyService(HF35DependService.ups_service[env_key]['host'])
        ups_pp_document_response = ups_service.get_privacy_policy_document_hf35()
        assert_that(ups_pp_document_response.status_code == 200)

        assert_that(bff_privacy_policy_document_response.json()['id'] == ups_pp_document_response.json()['id'])
        assert_that(bff_privacy_policy_document_response.json()['url'] == ups_pp_document_response.json()['url'])
        # currently, this value will be same for all the environment
        assert_that(bff_privacy_policy_document_response.json()['termsConditionUrl'] == 'https://study.ef.cn/content/terms-and-conditions.htm')

    @Test(tags="qa, stg, live")
    def test_post_privacy_policy_agreement(self):
        bff_privacy_policy_document_response = self.bff_service.get_privacy_policy_document()
        assert_that(bff_privacy_policy_document_response.status_code == 200)
        privacy_policy_document_id = bff_privacy_policy_document_response.json()['id']

        bff_privacy_policy_agreement_response = self.bff_service.post_privacy_policy_agreement(privacy_policy_document_id)
        assert_that(bff_privacy_policy_agreement_response.status_code == 200)

        ups_service = UpsPrivacyService(HF35DependService.ups_service[env_key]['host'])
        ups_pp_agreement_response = ups_service.get_privacy_policy_agreement_hf35(self.customer_id)
        assert_that(ups_pp_agreement_response.status_code == 200)

        assert_that(str(ups_pp_agreement_response.json()['studentId']) == str(self.customer_id))
        assert_that(ups_pp_agreement_response.json()['latestPrivacyPolicyDocumentResult']['id'] == privacy_policy_document_id)
        assert_that(ups_pp_agreement_response.json()['latestPrivacyPolicyDocumentResult']['signed'] == True)

    @Test(tags="qa, stg, live")
    def test_get_vocab_content_groups(self):
        book_content_id = self.get_current_book_from_bootstrap()
        course_structure_response = self.bff_service.get_course_structure()

        book_content_revision = jmespath.search('children[?contentId==\'%s\'].contentRevision| [0]' % (book_content_id),
                                                course_structure_response.json())
        book_schema_version = jmespath.search('children[?contentId==\'%s\'].schemaVersion| [0]' % (book_content_id),
                                              course_structure_response.json())

        bff_vocab_content_group_response = \
            self.bff_service.get_vocab_content_groups(book_content_id, book_content_revision, book_schema_version)
        assert_that(bff_vocab_content_group_response.status_code == 200)

        content_repo_service = ContentRepoService(CONTENT_REPO_ENVIRONMENT)
        vocab_eca_group_response = \
            content_repo_service.get_content_groups_by_param(ContentRepoContentType.TypeVocab.value,
                                                             ContentRepoGroupType.TypeECAGroup.value,
                                                             book_content_id, book_content_revision,
                                                             book_schema_version)
        assert_that(vocab_eca_group_response.status_code == 200)

        vocab_asset_group_response = \
            content_repo_service.get_content_groups_by_param(ContentRepoContentType.TypeVocab.value,
                                                             ContentRepoGroupType.TypeAssetGroup.value,
                                                             book_content_id, book_content_revision,
                                                             book_schema_version)
        assert_that(vocab_asset_group_response.status_code == 200)

        assert_that(bff_vocab_content_group_response.json()["ecaGroups"],
                    equal_to(vocab_eca_group_response.json()))
        assert_that(bff_vocab_content_group_response.json()["assetGroups"],
                    equal_to(vocab_asset_group_response.json()))

    @Test(tags="qa, stg, live")
    def test_submit_vocab_progress(self):
        word_attempt_template = Hf35BffWordAttemptEntity(str(uuid.uuid1()), str(uuid.uuid1()))
        word_attempt_list = Hf35BffUtils.construct_vocab_progress_list(word_attempt_template, 2)
        # submit vocab progress
        submit_response = self.bff_service.post_vocab_progress(word_attempt_list)
        assert_that(submit_response.status_code, equal_to(200))

        # get vocab progress
        vocab_progress_response = self.bff_service.get_vocab_progress(word_attempt_template.book_content_id)
        assert_that(vocab_progress_response.status_code, equal_to(200))

        assert_that(len(vocab_progress_response.json()), equal_to(len(word_attempt_list)))

        # check vocab progress response
        for i in range(len(vocab_progress_response.json())):
            actual_vocab_progress = vocab_progress_response.json()[i]
            expected_word_attempt = word_attempt_list[i]

            assert_that(actual_vocab_progress, match_to('id'))
            assert_that(actual_vocab_progress['studentId'], equal_to(int(self.customer_id)))
            assert_that(actual_vocab_progress['courseContentId'], equal_to(expected_word_attempt.course_content_id))
            assert_that(actual_vocab_progress['bookContentId'], equal_to(expected_word_attempt.book_content_id))
            assert_that(actual_vocab_progress['unitContentId'], equal_to(expected_word_attempt.unit_content_id))
            assert_that(actual_vocab_progress['wordContentId'], equal_to(expected_word_attempt.word_content_id))
            assert_that(actual_vocab_progress['currentLevel'], equal_to(expected_word_attempt.detail.current_level))
            assert_that(actual_vocab_progress['parentContentPath'], equal_to(expected_word_attempt.parent_content_path))
            assert_that(actual_vocab_progress['lastStudyAt'], equal_to(expected_word_attempt.detail.last_study_time))
            assert_that(actual_vocab_progress, match_to('createdAt'))
            assert_that(actual_vocab_progress, match_to('lastUpdatedAt'))
            assert_that(actual_vocab_progress['createdAt'], equal_to(actual_vocab_progress['lastUpdatedAt']))

        # check learning result
        learning_result_entity = LearningResultEntity(None, None, None)
        learning_result_entity.product_module = 1
        learning_result_entity.product = 2
        learning_result_entity.student_key = int(self.customer_id)

        for i in range(len(word_attempt_list)):
            expected_word_attempt = word_attempt_list[i]
            Hf35BffUtils.construct_expected_learning_result_by_word_attempt(learning_result_entity, expected_word_attempt)

            result_response = self.get_learning_result_response(learning_result_entity)
            assert_that(result_response.status_code, equal_to(200))

            assert_that(result_response.json()[0]["product"], equal_to(learning_result_entity.product))
            assert_that(result_response.json()[0]["productModule"], equal_to(learning_result_entity.product_module))
            assert_that(int(result_response.json()[0]["studentKey"]), equal_to(int(learning_result_entity.student_key)))
            assert_that(result_response.json()[0]["businessKey"], equal_to(learning_result_entity.business_key))
            assert_that(result_response.json()[0]["route"], equal_to(learning_result_entity.route))
            assert_that(result_response.json()[0]["details"][0]["activityKey"], expected_word_attempt.word_content_id)
            assert_that(result_response.json()[0]["extension"], equal_to(learning_result_entity.extension))

    @Test(tags="qa, stg, live")
    def test_get_vocab_progress(self):
        course_content_id = str(uuid.uuid1())
        book_content_id = str(uuid.uuid1())
        word_attempt_template = Hf35BffWordAttemptEntity(course_content_id, book_content_id)
        word_attempt_list = Hf35BffUtils.construct_vocab_progress_list(word_attempt_template, 3)
        # submit vocab progress
        vocab_submit_response = self.bff_service.post_vocab_progress(word_attempt_list)
        assert_that(vocab_submit_response.status_code, equal_to(200))

        # get vocab progress
        vocab_progress_response = self.bff_service.get_vocab_progress(word_attempt_template.book_content_id)
        assert_that(vocab_progress_response.status_code, equal_to(200))

        # check with homework service
        homework_service = HomeworkService(HOMEWORK_ENVIRONMENT)
        homework_vocab_progress_response = homework_service.get_vocab_progress(self.customer_id, book_content_id)
        assert_that(homework_vocab_progress_response.status_code, equal_to(200))
        assert_that(vocab_progress_response.json(), equal_to(homework_vocab_progress_response.json()))




