import random
import time
import uuid

import jmespath
import json_tools
from hamcrest import assert_that, equal_to
from ptest.decorator import TestClass, Test

from E1_API_Automation.Business.HighFlyer35.Hf35BffWordAttemptEntity import Hf35BffWordAttemptEntity
from E1_API_Automation.Business.HighFlyer35.HF35BffReaderAttemptEntity import Hf35BffReaderAttemptEntity
from E1_API_Automation.Business.HighFlyer35.HighFlyerUtils.HF35BffEnum import OnlineScope
from E1_API_Automation.Business.HighFlyer35.HighFlyerUtils.Hf35BffCommonData import Hf35BffCommonData
from E1_API_Automation.Business.HighFlyer35.HighFlyerUtils.Hf35BffUtils import Hf35BffUtils
from E1_API_Automation.Business.NGPlatform.ContentRepoService import ContentRepoService
from E1_API_Automation.Business.NGPlatform.CourseGroupService import CourseGroupService
from E1_API_Automation.Business.NGPlatform.HomeworkService import HomeworkService
from E1_API_Automation.Business.NGPlatform.LearningResultDetailEntity import LearningResultDetailEntity
from E1_API_Automation.Business.NGPlatform.LearningResultEntity import LearningResultEntity
from E1_API_Automation.Business.NGPlatform.StudyPlanEntity import StudyPlanEntity
from E1_API_Automation.Business.NGPlatform.NGPlatformUtils.ContentRepoCommonData import ContentRepoCommonData
from E1_API_Automation.Business.NGPlatform.NGPlatformUtils.ContentRepoEnum import ContentRepoContentType, \
    ContentRepoGroupType
from E1_API_Automation.Business.NGPlatform.NGPlatformUtils.LearningEnum import LearningResultProduct, \
    LearningResultProductModule
from E1_API_Automation.Business.ProvisioningService import ProvisioningService
from E1_API_Automation.Business.UpsPrivacyService import UpsPrivacyService
from E1_API_Automation.Business.Utils.EnvUtils import EnvUtils
from E1_API_Automation.Lib.HamcrestMatcher import match_to
from E1_API_Automation.Settings import *
from E1_API_Automation.Test.HighFlyerV35.HfBffTestBase import HfBffTestBase
from E1_API_Automation.Test_Data.BffData import BffUsers, HF35DependService, BffProduct
from E1_API_Automation.Lib.HamcrestExister import Exist



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

            # only HFV2, HFV3Plus users' contentscope is Standard, other products, return ONLINE_CLASS
            response = self.bff_service.get_bootstrap_controller('ios')
            if key in (BffProduct.HFV2.value, BffProduct.HFV3.value, BffProduct.HFV35.value):
                assert_that(response.status_code, equal_to(200))
                assert_that(response.json(), match_to("provision"))
                assert_that(response.json(), Exist("userContext.availableBooks"))
                assert_that(response.json(), Exist("userContext.currentBook"))
                assert_that(jmespath.search('userContext.contentScope', response.json()) == "STANDARD")
            elif key == BffProduct.SSV3.value:
                assert_that(response.status_code, equal_to(200))
                assert_that(jmespath.search('userContext.contentScope',response.json()) == "LITE")
            else:
                assert_that(response.status_code, equal_to(200))
                assert_that(jmespath.search('userContext.contentScope',response.json()) == "ONLINE_CLASS")


    @Test(tags="qa, stg, live", data_provider=["noToken"])
    def test_submit_new_attempt_without_auth_token(self, negative_para):
        bff_data_obj = Hf35BffCommonData()
        response = self.bff_service.submit_new_attempt_with_negative_auth_token(bff_data_obj.get_attempt_body(),
                                                                                negative_para)
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
        assert_that(bff_best_total_score, equal_to(expected_total_score))
        assert_that(bff_best_score, equal_to(expected_score))

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

        expected_oc_context = Hf35BffUtils.get_expected_occontext(platform)
        # check json fields
        diff_list = json_tools.diff(response.json()['ocContext'], expected_oc_context)
        assert_that(len(diff_list), equal_to(0))

    @Test(tags="qa, stg, live")
    def test_bootstrap_controller_ios_platform(self):
        self.test_bootstrap_controller_by_platform('ios')

    @Test(tags="qa, stg, live")
    def test_bootstrap_controller_android_platform(self):
        self.test_bootstrap_controller_by_platform('android')

    @Test(tags="qa, stg, live")
    def test_get_unlock_progress(self):
        current_book = self.get_current_book_from_bootstrap()
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
        assert_that(bff_activity_response.json().sort(key=lambda k: (k.get('id', 0))),
                    equal_to(content_repo_activity_response.json().sort(key=lambda k: (k.get('id', 0)))))

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
        assert_that(bff_eca_response.json().sort(key=lambda k: (k.get('id', 0))),
                    equal_to(content_repo_eca_response.json().sort(key=lambda k: (k.get('id', 0)))))

    @Test(tags="qa, stg, live")
    def test_get_online_pl_class_osd(self):
        bff_online_osd_response = self.bff_service.get_online_pl_class(OnlineScope.OSD.value)
        assert_that(bff_online_osd_response.status_code == 200)

    @Test(tags="qa, stg, live")
    def test_get_online_gl_class(self):
        bff_online_gl_response = self.bff_service.get_online_gl_class()
        assert_that(bff_online_gl_response.status_code == 200)

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
        assert_that(bff_privacy_policy_document_response.json()[
                        'termsConditionUrl'] == 'https://study.ef.cn/content/terms-and-conditions.htm')

    @Test(tags="qa, stg, live")
    def test_post_privacy_policy_agreement(self):
        bff_privacy_policy_document_response = self.bff_service.get_privacy_policy_document()
        assert_that(bff_privacy_policy_document_response.status_code == 200)
        privacy_policy_document_id = bff_privacy_policy_document_response.json()['id']

        bff_privacy_policy_agreement_response = self.bff_service.post_privacy_policy_agreement(
            privacy_policy_document_id)
        assert_that(bff_privacy_policy_agreement_response.status_code == 200)

        ups_service = UpsPrivacyService(HF35DependService.ups_service[env_key]['host'])
        ups_pp_agreement_response = ups_service.get_privacy_policy_agreement_hf35(self.customer_id)
        assert_that(ups_pp_agreement_response.status_code == 200)

        assert_that(str(ups_pp_agreement_response.json()['studentId']) == str(self.customer_id))
        assert_that(
            ups_pp_agreement_response.json()['latestPrivacyPolicyDocumentResult']['id'] == privacy_policy_document_id)
        assert_that(ups_pp_agreement_response.json()['latestPrivacyPolicyDocumentResult']['signed'] == True)

    @Test(tags="qa, stg, live")
    def test_get_vocab_content_groups(self):
        current_book = self.get_current_book_from_bootstrap()
        tree_revision = self.get_tree_revision_from_course_structure()
        book_structure_response = self.bff_service.get_book_structure(current_book, tree_revision)
        unit_content_id = jmespath.search('children[0].contentId', book_structure_response.json())
        unit_content_revision = jmespath.search('children[0].contentRevision', book_structure_response.json())
        unit_schema_version = jmespath.search('children[0].schemaVersion', book_structure_response.json())

        bff_vocab_content_group_response = \
            self.bff_service.get_vocab_content_groups(unit_content_id, unit_content_revision, unit_schema_version)
        assert_that(bff_vocab_content_group_response.status_code == 200)

        content_repo_service = ContentRepoService(CONTENT_REPO_ENVIRONMENT)
        vocab_eca_group_response = \
            content_repo_service.get_content_groups_by_param(ContentRepoContentType.TypeVocab.value,
                                                             ContentRepoGroupType.TypeECAGroup.value,
                                                             unit_content_id, unit_content_revision,
                                                             unit_schema_version)
        assert_that(vocab_eca_group_response.status_code == 200)

        vocab_asset_group_response = \
            content_repo_service.get_content_groups_by_param(ContentRepoContentType.TypeVocab.value,
                                                             ContentRepoGroupType.TypeAssetGroup.value,
                                                             unit_content_id, unit_content_revision,
                                                             unit_schema_version)
        assert_that(vocab_asset_group_response.status_code == 200)

        expected_result = vocab_eca_group_response.json()
        assert_that(bff_vocab_content_group_response.json()["ecaGroups"],
                    equal_to(expected_result))
        expected_asset_group_result = vocab_asset_group_response.json()
        assert_that(bff_vocab_content_group_response.json()["assetGroups"],
                    equal_to(expected_asset_group_result))

    @Test(tags="qa, stg, live", data_provider=[1, 2, 4])
    def test_submit_vocab_progress(self, word_attempt_num):
        book_content_id = str(uuid.uuid1())
        word_attempt_list = Hf35BffUtils.construct_vocab_progress_list(book_content_id, word_attempt_num)
        # submit vocab progress
        submit_response = self.bff_service.post_vocab_progress(word_attempt_list)
        assert_that(submit_response.status_code, equal_to(200))
        # assert_that(len(submit_response.json()), equal_to(word_attempt_num))

        # get vocab progress
        vocab_progress_response = self.bff_service.get_vocab_progress(book_content_id)
        assert_that(vocab_progress_response.status_code, equal_to(200))

        assert_that(len(vocab_progress_response.json()), equal_to(word_attempt_num))

        # check vocab progress response
        for i in range(len(vocab_progress_response.json())):
            actual_vocab_progress = vocab_progress_response.json()[i]
            expected_word_attempt = word_attempt_list.activities[i]

            assert_that(actual_vocab_progress, match_to('id'))
            assert_that(actual_vocab_progress['studentId'], equal_to(int(self.customer_id)))
            assert_that(actual_vocab_progress['bookContentId'], equal_to(expected_word_attempt.book_content_id))
            assert_that(actual_vocab_progress['unitContentId'], equal_to(expected_word_attempt.unit_content_id))
            assert_that(actual_vocab_progress['wordContentId'], equal_to(expected_word_attempt.word_content_id))
            assert_that(actual_vocab_progress['currentLevel'], equal_to(expected_word_attempt.detail.current_level))
            assert_that(actual_vocab_progress['parentContentPath'], equal_to(expected_word_attempt.parent_content_path))
            assert_that(actual_vocab_progress['lastStudyAt'], equal_to(expected_word_attempt.detail.last_study_at))
            assert_that(actual_vocab_progress, match_to('createdAt'))
            assert_that(actual_vocab_progress, match_to('lastUpdatedAt'))
            assert_that(actual_vocab_progress['createdAt'], equal_to(actual_vocab_progress['lastUpdatedAt']))

        # check learning result
        learning_result_entity = LearningResultEntity(None, None, None)
        # 128 is for vocab product module
        learning_result_entity.product_module = LearningResultProductModule.VOCABULARY.value
        learning_result_entity.product = LearningResultProduct.HIGHFLYER.value
        learning_result_entity.student_key = int(self.customer_id)
        learning_result_entity.business_key = word_attempt_list.context_lesson_content_id
        Hf35BffUtils.construct_expected_learning_result_by_word_attempt(learning_result_entity,word_attempt_list)

        for i in range(len(word_attempt_list.activities)):
            expected_word_attempt = word_attempt_list.activities[i]
            Hf35BffUtils.construct_expected_learning_result_by_word_attempt(learning_result_entity,
                                                                            expected_word_attempt)

            result_response = self.get_learning_result_response(learning_result_entity)
            assert_that(result_response.status_code, equal_to(200))

            assert_that(result_response.json()[0]["product"], equal_to(learning_result_entity.product))
            assert_that(result_response.json()[0]["productModule"], equal_to(learning_result_entity.product_module))
            assert_that(int(result_response.json()[0]["studentKey"]), equal_to(int(learning_result_entity.student_key)))
            assert_that(result_response.json()[0]["businessKey"], equal_to(learning_result_entity.business_key))
            assert_that(result_response.json()[0]["route"], equal_to(learning_result_entity.route))
            assert_that(result_response.json()[0]["details"][0]["activityKey"], expected_word_attempt.word_content_id)
            assert_that(result_response.json()[0]["details"][0]["extension"], learning_result_entity.details[0]['extension'])
            assert_that(result_response.json()[0]['resultKey'], equal_to(submit_response.json()))

    @Test(tags="qa, stg, live")
    def test_get_vocab_progress(self):
        book_content_id = str(uuid.uuid1())
        word_attempt_list = Hf35BffUtils.construct_vocab_progress_list(book_content_id, 3)
        # submit vocab progress
        vocab_submit_response = self.bff_service.post_vocab_progress(word_attempt_list)
        assert_that(vocab_submit_response.status_code, equal_to(200))

        # get vocab progress
        vocab_progress_response = self.bff_service.get_vocab_progress(book_content_id)
        assert_that(vocab_progress_response.status_code, equal_to(200))

        # check with homework service
        homework_service = HomeworkService(HOMEWORK_ENVIRONMENT)
        homework_vocab_progress_response = homework_service.get_vocab_progress(self.customer_id, book_content_id)
        assert_that(homework_vocab_progress_response.status_code, equal_to(200))
        assert_that(vocab_progress_response.json(), equal_to(homework_vocab_progress_response.json()))

    @Test(tags="qa, stg, live")
    def test_get_reader_content_groups_by_book(self):
        # get current book id and relevant content id
        current_book = self.get_current_book_from_bootstrap()
        tree_revision = self.get_tree_revision_from_course_structure()
        book_structure_response = self.bff_service.get_book_structure(current_book, tree_revision)
        relevant_content_revision = jmespath.search('contentRevision', book_structure_response.json())

        # get content group
        content_group_response = self.bff_service.get_reader_content_groups(current_book, relevant_content_revision)
        assert_that(content_group_response.status_code, equal_to(200))

    @Test(tag="qa, stg, live")
    def test_get_reader_content_group_by_level(self):
        default_level_id = self.get_reader_default_level_from_course_structure()
        level_focused_response = self.bff_service.get_reader_level_focused(self.customer_id, default_level_id)
        assert_that(level_focused_response.status_code, equal_to(200))
        level_focused_json = level_focused_response.json()

        # go through all the levels in the response to get content group
        for level in level_focused_json['levelNodes']:
            relevant_content_id = level['contentId']
            relevant_content_revision = level['contentRevision']
            content_group_response = self.bff_service.get_reader_content_groups(relevant_content_id,
                                                                                relevant_content_revision)
            assert_that(content_group_response.status_code, equal_to(200))

    @Test(tag="qa, stg, live")
    def test_post_reader_progress(self):
        relevant_content_id = str(uuid.uuid1())
        reader_attempt_template = Hf35BffReaderAttemptEntity(relevant_content_id)
        reader_attempt = Hf35BffUtils.construct_reader_attempt(reader_attempt_template)
        reader_attempt_dict = Hf35BffUtils.construct_reader_attempt_dict(reader_attempt)
        # submit reader progress
        attempt_response = self.bff_service.post_reader_progress(reader_attempt_dict)
        assert_that(attempt_response.status_code, equal_to(200))
        # get reader progress
        progress_response = self.bff_service.get_reader_progress(self.customer_id, relevant_content_id)
        assert_that(progress_response.status_code, equal_to(200))

        progress_data = progress_response.json()
        assert_that(progress_data[0]["readerContentId"]), equal_to(reader_attempt_dict["readerContentId"])
        assert_that(progress_data[0]["readerType"]), equal_to(reader_attempt_dict["readerType"])
        assert_that(progress_data[0]["relevantContentId"]), equal_to(reader_attempt_dict["relevantContentId"])
        assert_that(progress_data[0]["parentContentPath"]), equal_to(reader_attempt_dict["parentContentPath"])
        assert_that(progress_data[0]["progress"]), equal_to(reader_attempt_dict["progress"])

    @Test(tag="qa, stg, live")
    def test_get_reader_progress_by_book(self):
        current_book = self.get_current_book_from_bootstrap()
        reader_progress_response = self.bff_service.get_reader_progress(self.customer_id, current_book)
        assert_that(reader_progress_response.status_code, equal_to(200))

    @Test(tag="qa, stg, live")
    def test_get_reader_progress_by_level(self):
        default_level_id = self.get_reader_default_level_from_course_structure()
        level_focused_response = self.bff_service.get_reader_level_focused(self.customer_id, default_level_id)
        assert_that(level_focused_response.status_code, equal_to(200))
        level_focused_json = level_focused_response.json()

        # go through all the levels in the response to get progress
        for level in level_focused_json['levelNodes']:
            relevant_content_id = level['contentId']
            progress_response = self.bff_service.get_reader_progress(self.customer_id, relevant_content_id)
            assert_that(progress_response.status_code, equal_to(200))

    @Test(tags="qa, stg, live")
    def test_get_weekly_plan(self):
        current_book = self.get_current_book_from_bootstrap()
        unlock_response = self.bff_service.get_unlock_progress_controller(current_book)
        assert_that(unlock_response.status_code, equal_to(200))
        unlock_at_str = jmespath.search('[*].unlockedAt', unlock_response.json())
        for unlock_time in unlock_at_str:
            weekly_plan = self.bff_service.get_weekly_plan(unlock_time)
            assert_that(weekly_plan.status_code, equal_to(200))
            for each_plan in weekly_plan.json():
                content_path = each_plan['refContentPath']
                plan_key = each_plan['studentId'], each_plan['product'], each_plan['productModule'], each_plan['refId']
                checkProps = self.bff_service.get_content_path(content_path)
                for each_ref in checkProps.json():
                    content_key = each_ref['studentId'], each_ref['product'], each_ref['productModule'], each_ref[
                        'refId']
                    if content_key == plan_key:
                        assert_that(each_plan, equal_to(each_ref))

    @Test(tags="qa, stg, live")
    def test_empty_weekly_plan(self):
        weekly_plan = self.bff_service.get_weekly_plan("")
        assert_that(weekly_plan.status_code, equal_to(200))

    @Test(tags="qa, stg, live")
    def test_content_path_book(self):
        test_path = "highflyers/cn-3/book-2/unit-1/assignment-1"
        study_plan_entity = StudyPlanEntity(None, None, None)
        self.setter_study_plan_entity(study_plan_entity, test_path, 0)
        self.sp_service.put_study_plan_test_entity(study_plan_entity)
        study_plan_path = study_plan_entity.ref_content_path
        content_path = self.bff_service.get_content_path(study_plan_path)
        assert_that(content_path.status_code, equal_to(200))
        if env_key != 'Live':
            path = content_path.json()[0]
            refProps = path['refProps']
            student_id, product_module = path['studentId'], path['productModule']
            content_map = self.cm_service.get_content_map(study_plan_path).json()
            study_plan = Hf35BffUtils.get_study_plan_by_student_id_from_db(student_id, product_module, study_plan_path)
            assert_that(path['refId'], equal_to(study_plan['ref_id']))
            assert_that(path['effectAt'], equal_to(study_plan['effect_at'].strftime("%Y-%m-%dT%H:%M:%S.000Z")))
            assert_that(path['expireAt'], equal_to(study_plan['expire_at'].strftime("%Y-%m-%dT%H:%M:%S.000Z")))
            if path['startAt'] == None:
                assert_that(path['startAt'], equal_to(study_plan['start_at']))
            else:
                assert_that(path['startAt'], equal_to(study_plan['start_at'].strftime("%Y-%m-%dT%H:%M:%S.000Z")))
            if path['completeAt'] == None:
                assert_that(path['completeAt'], equal_to(study_plan['complete_at']))
            else:
                assert_that(path['completeAt'], equal_to(study_plan['complete_at'].strftime("%Y-%m-%dT%H:%M:%S.000Z")))
            assert_that(refProps['lessonTitle'], equal_to(content_map['title']))
            assert_that(refProps['unitContentId'], equal_to(content_map['parent']['contentId']))
            assert_that(refProps['unitTitle'], equal_to(content_map['parent']['title']))
            assert_that(refProps['bookTitle'], equal_to(content_map['parent']['parent']['title']))

    @Test(tags="qa, stg, live")
    def test_content_path_unit(self):
        test_path = "highflyers/cn-3/book-1/unit-3"
        study_plan_entity = StudyPlanEntity(None, None, None)
        self.setter_study_plan_entity(study_plan_entity, test_path, 1)
        self.sp_service.put_study_plan_test_entity(study_plan_entity)
        study_plan_path = study_plan_entity.ref_content_path
        content_path = self.bff_service.get_content_path(study_plan_path)
        assert_that(content_path.status_code, equal_to(200))
        if env_key != 'Live':
            path = content_path.json()[0]
            student_id, product_module = path['studentId'], path['productModule']
            study_plan = Hf35BffUtils.get_study_plan_by_student_id_from_db(student_id, product_module, study_plan_path)
            assert_that(path['refId'], equal_to(study_plan['ref_id']))
            assert_that(path['effectAt'], equal_to(study_plan['effect_at'].strftime("%Y-%m-%dT%H:%M:%S.000Z")))
            assert_that(path['expireAt'], equal_to(study_plan['expire_at'].strftime("%Y-%m-%dT%H:%M:%S.000Z")))
            if path['startAt'] == None:
                assert_that(path['startAt'], equal_to(study_plan['start_at']))
            else:
                assert_that(path['startAt'], equal_to(study_plan['start_at'].strftime("%Y-%m-%dT%H:%M:%S.000Z")))
            if path['completeAt'] == None:
                assert_that(path['completeAt'], equal_to(study_plan['complete_at']))
            else:
                assert_that(path['completeAt'], equal_to(study_plan['complete_at'].strftime("%Y-%m-%dT%H:%M:%S.000Z")))
            assert_that(path['refProps'], equal_to(eval(study_plan['ref_props'])))

    @Test(tags="qa, stg, live")
    def test_content_state(self):
        test_path = "highflyers/cn-3/book-2/unit-1/assignment-1"
        study_plan_entity = StudyPlanEntity(None, None, None)
        self.setter_study_plan_entity(study_plan_entity, test_path, 0)
        self.sp_service.put_study_plan_test_entity(study_plan_entity)
        study_plan_path = study_plan_entity.ref_content_path
        content_path = self.bff_service.get_content_path(study_plan_path)
        assert_that(content_path.status_code, equal_to(200))
        if env_key != 'Live':
            path = content_path.json()[0]
            if path['startAt'] is None:
                if path['expireAt'] < time.strftime("%Y-%m-%dT%H:%M:%S.%jZ", time.localtime()):
                    assert_that(path['state'], equal_to("ABORTED"))
                else:
                    assert_that(path['state'], equal_to("PLANNED"))
            elif path['completeAt'] is None:
                assert_that(path['state'], equal_to("INPROGRESS"))
            else:
                assert_that(path['state'], equal_to("COMPLETED"))

    @Test(tags="qa, stg,live",data_provider=["unit","lesson"])
    def test_content_path_rewards(self,level):
        if level == 'unit':
            test_path = "highflyers/cn-3/book-2/unit-6"
        else:
            test_path = "highflyers/cn-3/book-2/unit-6/assignment-%s" % (random.randint(1, 10))
        total_rewards = self.bff_service.get_rewards_by_content_path(test_path)
        customer_id = self.omni_service.get_customer_id(self.user_name, self.password)
        assert_that(total_rewards.status_code, equal_to(200))
        if env_key != 'Live':
            completed_study_plan = Hf35BffUtils.get_count_completed_study_plan_by_student_id_from_db(customer_id, test_path)
            assert_that(total_rewards.json(), equal_to(completed_study_plan))

    @Test(tags="qa, stg, live")
    def negative_test_empty_content_path_rewards(self):
        total_rewards = self.bff_service.get_rewards_by_content_path("")
        assert_that(total_rewards.status_code, equal_to(400))
