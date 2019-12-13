import json
from hamcrest import assert_that, equal_to, contains_string
from ptest.decorator import TestClass, Test

from E1_API_Automation.Business.NGPlatform.ContentRepoService import ContentRepoService
from E1_API_Automation.Business.NGPlatform.HomeworkService import HomeworkService
from E1_API_Automation.Business.NGPlatform.LearningPlanEntity import LearningPlanEntity
from E1_API_Automation.Business.NGPlatform.LearningResultEntity import LearningResultEntity
from E1_API_Automation.Business.NGPlatform.LearningResultDetailEntity import LearningResultDetailEntity
from E1_API_Automation.Business.NGPlatform.NGPlatformUtils.ContentRepoCommonData import ContentRepoCommonData
from E1_API_Automation.Settings import env_key, HOMEWORK_ENVIRONMENT, CONTENT_REPO_ENVIRONMENT
from E1_API_Automation.Test.HighFlyerV35.HfBffTestBase import HfBffTestBase
from E1_API_Automation.Test_Data.BffData import BffUsers
from E1_API_Automation.Business.HighFlyer35.HighFlyerUtils.Hf35BffCommonData import Hf35BffCommonData
from E1_API_Automation.Lib.HamcrestMatcher import match_to

import jmespath


@TestClass()
class HighFlyer(HfBffTestBase):

   
    @Test(tags='qa', data_provider=["no_uuid"])
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

    @Test(tags='qa', data_provider=[1, 3, 10])
    def test_post_homework_activity(self, items):
        content_repo_data = ContentRepoCommonData(items)
        # insert content
        content_repo_service = ContentRepoService(CONTENT_REPO_ENVIRONMENT)
        content_json_body = content_repo_data.get_activity_content()
        content_repo_response = content_repo_service.post_content(content_json_body)
        assert_that(content_repo_response.status_code == 200)
        content_activities_response = content_repo_service.get_activities(content_repo_response.json()["savedItems"])
        # bff post
        bff_activity_response = self.bff_service.get_homework_activities(content_repo_response.json()["savedItems"])
        assert_that(bff_activity_response.status_code == 200)
        bff_activity_json = bff_activity_response.json()
        assert_that(bff_activity_json, equal_to(content_activities_response.json()))

    @Test(tags='qa', data_provider=[(3, "activity"), (3, "asset"), (2, "activity_and_asset")])
    def test_get_homework_activity_group(self, number, activity_or_asset):
        content_repo_data = ContentRepoCommonData(number, activity_or_asset)
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
        query_content_group_json_body["parentContentRevision"] = query_content_group_json_body.pop("contentRevision")
        query_content_group_json_body["parentSchemaVersion"] = query_content_group_json_body.pop("schemaVersion")
        content_group_activities_response = content_repo_service.get_activities_group(query_content_group_json_body)
        # bff get activity group
        bff_activity_response = self.bff_service.get_homework_activity_asset_group(
            query_content_group_json_body["parentContentRevision"],
            query_content_group_json_body["parentContentId"])
        assert_that(bff_activity_response.status_code == 200)
        bff_activity_json = bff_activity_response.json()
        if (activity_or_asset == "activity"):
            assert_that(bff_activity_json["activityGroups"], equal_to(content_group_activities_response.json()))
        elif (activity_or_asset == "asset"):
            assert_that(bff_activity_json["assetGroups"], equal_to(content_group_activities_response.json()))

    @Test(tags='qa', data_provider=["", "invalid", "noToken"])
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
        print("Bff get book response is : %s" % (json.dumps(bff_invalid_response.json(), indent=4)))
        if negative_token == ("noToken"):
            assert_that(bff_invalid_response.status_code, equal_to(400))
            assert_that((bff_invalid_response.json()['error'] == "Bad Request"))
        else:
            assert_that(bff_invalid_response.status_code, equal_to(401))
            assert_that((bff_invalid_response.json()['error'] == "Unauthorized"))

    @Test(tags='qa', data_provider=[{"contentId": ""}, {"contentId": None}, {"contentRevision": ""},
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

    @Test(tags='qa', data_provider=[{"contentId": "f3417c1a-cf92-4257-9cec-3efa911b46da"}])
    def test_post_homework_activity_with_mismatch_para(self, negative_parameter):
        content_repo_data = ContentRepoCommonData()
        # insert content
        content_repo_service = ContentRepoService(CONTENT_REPO_ENVIRONMENT)
        content_json_body = content_repo_data.get_activity_content()
        content_repo_response = content_repo_service.post_content(content_json_body)
        assert_that(content_repo_response.status_code == 200)
        content_activities_response = content_repo_service.get_activities(content_repo_response.json()["savedItems"])
        bff_mismatch_json_body = self.update_content_negative_body(negative_parameter,
                                                                   content_activities_response.json(), True)
        bff_mismatch_response = self.bff_service.get_homework_activities(bff_mismatch_json_body)
        assert_that(bff_mismatch_response.status_code == 200)
        print(json.dumps(bff_mismatch_response.json(), indent=4))
        expected_result = content_activities_response.json()
        del expected_result[0]
        assert_that(bff_mismatch_response.json(), equal_to(expected_result))

    @Test(tags='qa', data_provider=["", "invalid", "noToken"])
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
        if negative_token == ("noToken"):
            assert_that(bff_invalid_response.status_code, equal_to(400))
            assert_that((bff_invalid_response.json()['error'] == "Bad Request"))
        else:
            assert_that(bff_invalid_response.status_code, equal_to(401))
            assert_that((bff_invalid_response.json()['error'] == "Unauthorized"))

    @Test(tags='qa', data_provider=[("", ""), (None, None), ("testRevision", "non-uuid")])
    def test_post_homework_activity_group_with_negative_parameter(self, negative_content_revision, negative_content_id):
        bff_activity_response = self.bff_service.get_homework_activity_asset_group(negative_content_revision,
                                                                                   negative_content_id)
        assert_that(bff_activity_response.status_code == 400)
        assert_that((bff_activity_response.json()['error'] == "Bad Request"))

    @Test(tags='qa', data_provider=[("test_content_revision", "5f99af36-cad7-4a45-b811-02c9076f47f1")])
    def test_post_homework_activity_asset_group_with_mismatch_para(self, negative_content_revision,
                                                                   negative_content_id):
        bff_mismatch_response = self.bff_service.get_homework_activity_asset_group(negative_content_revision,
                                                                                   negative_content_id)
        assert_that(bff_mismatch_response.status_code == 200)
        expected_result = {
            "activityGroups": [],
            "assetGroups": []
        }
        assert_that(bff_mismatch_response.json(), equal_to(expected_result))

    @Test(tags='qa')
    def test_bootstrap_controller_status(self):
        response = self.bff_service.get_bootstrap_controller(platform=2)
        assert_that(response.status_code == 200)
        assert_that(response.json(), match_to("provision"))
        assert_that(response.json(), match_to("userContext.availableBooks"))
        assert_that(response.json(), match_to("userContext.currentBook"))

    @Test(tags='qa')
    def test_bootstrap_controller_with_wrong_platform_number(self):
        response = self.bff_service.get_bootstrap_controller(platform=None)
        assert_that(response.status_code == 400)

    @Test(tags='qa')
    def test_bootstrap_controller_ios_platform(self):
        response = self.bff_service.get_bootstrap_controller(platform='ios')
        assert_that(jmespath.search('provision.name', response.json()), contains_string('iOS'))

    @Test(tags='qa')
    def test_bootstrap_controller_android_platform(self):
        response = self.bff_service.get_bootstrap_controller(platform='android')
        assert_that(jmespath.search('provision.name', response.json()), contains_string('andriod'))

    @Test(tags='qa')
    def test_get_unlock_progress(self):
        current_book = jmespath.search('userContext.currentBook',
                                       self.bff_service.get_bootstrap_controller('ios').json())
        print(current_book)
        response = self.bff_service.get_unlock_progress_controller(current_book)
        assert_that(response.status_code == 200)


