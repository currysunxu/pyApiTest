import json

import jmespath
import json_tools
import requests
from hamcrest import assert_that

from E1_API_Automation.Business.HighFlyer35.OneAppBffService import OneAppBffService
from E1_API_Automation.Business.HighFlyer35.Hf35MediaService import Hf35MediaService
from E1_API_Automation.Business.NGPlatform.ContentRepoService import ContentRepoService
from E1_API_Automation.Business.NGPlatform.NGPlatformUtils.ContentRepoEnum import ContentRepoContentType
from E1_API_Automation.Business.PipelinePublish.PipelinePublishUtils.PipelinePublishConstants import \
    PipelinePublishConstants
from E1_API_Automation.Business.PipelinePublish.PipelinePublishUtils.PipelinePublishUtils import PipelinePublishUtils
from E1_API_Automation.Business.Utils.CommonUtils import CommonUtils
from E1_API_Automation.Settings import CONTENT_REPO_ENVIRONMENT, BFF_ENVIRONMENT, env_key, MEDIA_ENVIRONMENT
from E1_API_Automation.Test_Data.BffData import BffProduct, BffUsers


class PipelinePublishVerifyService:
    def __init__(self):
        self.bff_service = OneAppBffService(BFF_ENVIRONMENT)
        key = BffProduct.HFV35.value
        user_name = BffUsers.BffUserPw[env_key][key][0]['username']
        password = BffUsers.BffUserPw[env_key][key][0]['password']
        self.bff_service.login(user_name, password)
        self.media_service = Hf35MediaService(MEDIA_ENVIRONMENT, self.bff_service.access_token)
        self.content_repo_service = ContentRepoService(CONTENT_REPO_ENVIRONMENT)

    def verify_content_after_release(self, aem_book_tree, content_map_book_tree, expected_release_revision):
        region_ach = content_map_book_tree['regionAch']
        content_revision_list = []
        content_revision_list.append(jmespath.search('contentRevision', content_map_book_tree))
        content_revision_list.extend(jmespath.search('children[].contentRevision', content_map_book_tree))
        content_revision_list.extend(jmespath.search('children[].children[].contentRevision', content_map_book_tree))
        content_revision_list = list(set(content_revision_list))

        error_message = []
        if len(content_revision_list) != 1:
            error_message.append('content map book tree should have same content revision in all the nodes!')
            return error_message

        if content_revision_list[0] != expected_release_revision:
            error_message.append(
                'content revision not as expected! release revision should be:' + expected_release_revision)
            return error_message

        error_message.extend(self.verify_aem_fields_with_content_map(aem_book_tree,
                                                                     content_map_book_tree))

        aem_units_dict = aem_book_tree['units']
        content_map_unit_list = content_map_book_tree[PipelinePublishConstants.FIELD_CHILDREN]

        if len(aem_units_dict) != len(content_map_unit_list):
            error_message.append('AEM unit list size not same as content map unit list size!')
            return error_message

        for i in range(len(content_map_unit_list)):
            print("--------------------start verify unit" + str(i + 1))
            # for each unit, init the service as the expire time is too short in QA
            self.__init__()

            # for small star, it have Unit 0, but the id is unit-11 for Unit 0
            content_map_unit_dict = content_map_unit_list[i]
            aem_path = content_map_unit_dict['originID']
            # aem_unit_dict = aem_unit_list['unit-' + str(i + 1)]
            aem_unit_dict = PipelinePublishUtils.get_expected_aem_unit_by_path(aem_units_dict, aem_path)

            aem_unit_title = aem_unit_dict[PipelinePublishConstants.FIELD_TITLE]

            error_message.extend(self.verify_aem_fields_with_content_map(aem_unit_dict,
                                                                         content_map_unit_dict))

            # unit title should not include unit character for highflyers
            if 'unit' in aem_unit_title.lower() and content_map_book_tree['contentPath'].startswith('highflyers'):
                error_message.append(" unit title should not include unit character!")

            # verify unit handouts
            error_message.extend(self.verify_unit_handouts(aem_unit_dict,
                                                           content_map_unit_dict))

            # verify unit flashcards
            error_message.extend(self.verify_unit_flashcard(aem_unit_dict,
                                                            content_map_unit_dict))

            # verify unit quiz
            error_message.extend(self.verify_unit_quiz(aem_unit_dict, content_map_unit_dict))

            # verify unit question bank
            error_message.extend(self.verify_unit_question_bank(aem_unit_dict, content_map_unit_dict))

            # verify lesson by unit structure
            aem_lesson_by_unit_list = aem_unit_dict[PipelinePublishConstants.FIELD_REGION_LESSONS][region_ach][
                PipelinePublishConstants.FIELD_LESSONS]
            content_map_lesson_by_unit_list = content_map_unit_dict[PipelinePublishConstants.FIELD_CHILDREN]

            if len(aem_lesson_by_unit_list) != len(content_map_lesson_by_unit_list):
                error_message.append(
                    'AEM lesson list size under unit: {0} not same as content map lesson list size!'.format(
                        aem_unit_title))
                return error_message

            for j in range(len(aem_lesson_by_unit_list)):
                print("--start verify lesson" + str(j + 1))
                aem_lesson_by_unit = aem_lesson_by_unit_list['assignment-' + str(j + 1)]
                content_map_lesson_by_unit = content_map_lesson_by_unit_list[j]

                error_message.extend(self.verify_aem_fields_with_content_map(aem_lesson_by_unit,
                                                                             content_map_lesson_by_unit))

                # verify lesson homework
                # # for small star, not verify homework for now, as lite not need these, and content-repo have issue: CP-254
                # if not content_map_book_tree['contentPath'].startswith('small'):
                #     error_message.extend(self.verify_lesson_homework(aem_lesson_by_unit,
                #                                                      content_map_lesson_by_unit))
                error_message.extend(self.verify_lesson_homework(aem_lesson_by_unit,
                                                                 content_map_lesson_by_unit))
                print("--end of verify lesson" + str(j + 1))
        print("--------------------end of verify unit" + str(i + 1))
        return error_message

    def verify_aem_fields_with_content_map(self, aem_dict, content_map_dict):
        error_message = []
        title = aem_dict[PipelinePublishConstants.FIELD_TITLE]
        path = aem_dict[PipelinePublishConstants.FIELD_PATH]
        if title != content_map_dict[PipelinePublishConstants.FIELD_TITLE]:
            error_message.append("title {0} not consistent between AEM and Content_Map!".format(title))

        if path != content_map_dict[PipelinePublishConstants.FIELD_ORIGINID]:
            error_message.append("path {0} not consistent between AEM and Content_Map!".format(path))
        return error_message

    def verify_unit_handouts(self, aem_unit_dict, content_map_unit_dict):
        return self.verify_unit_handouts_flashcard(aem_unit_dict, content_map_unit_dict,
                                                   ContentRepoContentType.TypeHandout)

    def verify_unit_flashcard(self, aem_unit_dict, content_map_unit_dict):
        return self.verify_unit_handouts_flashcard(aem_unit_dict, content_map_unit_dict,
                                                   ContentRepoContentType.TypeFlashcard)

    def verify_unit_handouts_flashcard(self, aem_unit_dict, content_map_unit_dict, content_type):
        error_message = []

        if not 'resources' in aem_unit_dict.keys():
            return error_message

        aem_handouts_url = aem_unit_dict['resources']
        aem_handouts_response = requests.get(aem_handouts_url)
        assert_that(aem_handouts_response.status_code == 200)

        expected_path = 'handouts.assets'
        if content_type == ContentRepoContentType.TypeFlashcard:
            expected_path = 'flashcards.assets'

        aem_handouts_assets = jmespath.search(expected_path, aem_handouts_response.json())

        unit_content_id = content_map_unit_dict[PipelinePublishConstants.FIELD_CONTENT_ID]
        course = content_map_unit_dict[PipelinePublishConstants.FIELD_COURSE]
        region_ach = content_map_unit_dict[PipelinePublishConstants.FIELD_REGION_ACH]

        unit_handout_content_group = \
            self.content_repo_service.get_content_groups_by_param(content_type.value,
                                                                  None,
                                                                  unit_content_id,
                                                                  content_map_unit_dict[
                                                                      PipelinePublishConstants.FIELD_CONTENT_REVISION],
                                                                  content_map_unit_dict[
                                                                      PipelinePublishConstants.FIELD_SCHEMA_REVISION]).json()

        if aem_handouts_assets is None or len(aem_handouts_assets) == 0:
            if len(unit_handout_content_group) != 0:
                error_message.append('There should be no {0} Content group created as AEM unit:{1} don\'t have any {0}!'
                                     .format(content_type.value, unit_content_id))
                return error_message
        else:
            unit_handout_eca_group = jmespath.search('[?groupType==\'ECA_GROUP\']|[0]', unit_handout_content_group)
            unit_handout_asset_group = jmespath.search('[?groupType==\'ASSET_GROUP\']|[0]', unit_handout_content_group)

            unit_handout_eca_metadata_list = unit_handout_eca_group[PipelinePublishConstants.FIELD_CHILDREFS]

            unit_handout_ecas = self.content_repo_service.get_ecas(unit_handout_eca_metadata_list).json()

            if len(aem_handouts_assets) != len(unit_handout_eca_metadata_list):
                error_message.append(
                    'AEM unit handout asset list size not same as content repo unit handout eca list size!')
                return error_message

            for i in range(len(aem_handouts_assets)):
                aem_handout_asset = aem_handouts_assets[i]
                unit_handout_eca_metadata = unit_handout_eca_metadata_list[i]
                unit_handout_eca = jmespath.search(
                    "[?contentId == '{0}'] | [0]".format(
                        unit_handout_eca_metadata[PipelinePublishConstants.FIELD_CONTENT_ID]),
                    unit_handout_ecas)
                error_message.extend(self.verify_handout_homework_fields(aem_handout_asset,
                                                                         unit_handout_eca,
                                                                         content_type,
                                                                         course,
                                                                         region_ach))

            # verify handout eca asset list with asset group
            error_message.extend(self.verify_handout_eca_assets_with_asset_group(unit_handout_ecas,
                                                                                 unit_handout_asset_group))

        return error_message

    # verify unit quiz
    def verify_unit_quiz(self, aem_unit_dict, content_map_unit_dict):
        error_message = []
        aem_unit_quiz_list = []
        if PipelinePublishConstants.FIELD_QUIZ in aem_unit_dict.keys():
            aem_unit_quiz_list = aem_unit_dict[PipelinePublishConstants.FIELD_QUIZ]

        # there will be only one quiz if the list is not empty
        if len(aem_unit_quiz_list) > 0:
            aem_unit_quiz = aem_unit_quiz_list[0]

        unit_content_id = content_map_unit_dict[PipelinePublishConstants.FIELD_CONTENT_ID]
        course = content_map_unit_dict[PipelinePublishConstants.FIELD_COURSE]
        region_ach = content_map_unit_dict[PipelinePublishConstants.FIELD_REGION_ACH]

        unit_quiz_content_groups = \
            self.content_repo_service.get_content_groups_by_param(ContentRepoContentType.TypeQuiz.value,
                                                                  None,
                                                                  unit_content_id,
                                                                  content_map_unit_dict[
                                                                      PipelinePublishConstants.FIELD_CONTENT_REVISION],
                                                                  content_map_unit_dict[
                                                                      PipelinePublishConstants.FIELD_SCHEMA_REVISION]).json()

        if len(aem_unit_quiz_list) == 0:
            if len(unit_quiz_content_groups) != 0:
                error_message.append(
                    'There should be no QUIZ Content group created as AEM unit:{0} don\'t have any quiz!'.format(
                        unit_content_id))
                return error_message
        else:
            aem_unit_quiz_skillset_localizations = aem_unit_quiz[PipelinePublishConstants.FIELD_SKILLSET_LOCALIZATION]
            aem_unit_quiz_activities = aem_unit_quiz['activities']

            unit_quiz_activity_group = jmespath.search('[?groupType==\'ACTIVITY_GROUP\']|[0]', unit_quiz_content_groups)
            unit_quiz_asset_group_list = jmespath.search('[?groupType==\'ASSET_GROUP\']', unit_quiz_content_groups)

            content_group_unit_quiz_activity_entity_list = unit_quiz_activity_group[
                PipelinePublishConstants.FIELD_CHILDREFS]
            content_repo_unit_quiz_activity_list = self.content_repo_service.get_activities(
                content_group_unit_quiz_activity_entity_list).json()

            # verify the localization for this unit quiz
            expected_skill_set_localizations = PipelinePublishUtils.get_expected_unit_quiz_localizations(
                content_group_unit_quiz_activity_entity_list,
                content_repo_unit_quiz_activity_list,
                aem_unit_quiz_skillset_localizations)

            # check with the skillsetLocalization field
            diff_list = json_tools.diff(expected_skill_set_localizations,
                                        unit_quiz_activity_group['metadata']['parts'])
            if len(diff_list) != 0:
                error_message.append(
                    'skillsetLocalization value in content group not consistent with the value in AEM, diff is:' \
                    + str(diff_list))

            if len(aem_unit_quiz_activities) != len(content_group_unit_quiz_activity_entity_list):
                error_message.append(
                    'AEM unit quiz activity list size not same as content repo unit quiz activity list size!')
                return error_message

            for i in range(len(aem_unit_quiz_activities)):
                aem_unit_quiz_activity = aem_unit_quiz_activities[i]
                content_group_unit_quiz_activity_entity = content_group_unit_quiz_activity_entity_list[i]
                content_repo_unit_quiz_activity = jmespath.search(
                    "[?contentId == '{0}'] | [0]".format(
                        content_group_unit_quiz_activity_entity[PipelinePublishConstants.FIELD_CONTENT_ID]),
                    content_repo_unit_quiz_activity_list)
                error_message.extend(self.verify_aem_homework_with_content_repo_activity(
                    aem_unit_quiz_activity, content_repo_unit_quiz_activity, ContentRepoContentType.TypeQuiz, course, region_ach))

            # verify the asset_group with the asset exit in the activity list
            error_message.extend(self.verify_activity_assets_with_asset_group(
                content_repo_unit_quiz_activity_list, unit_quiz_asset_group_list))

        return error_message

    # verify unit question bank field
    def verify_unit_question_bank(self, aem_unit_dict, content_map_unit_dict):
        error_message = []
        aem_unit_question_bank_list = []
        if PipelinePublishConstants.FIELD_QUESTION_BANK in aem_unit_dict.keys():
            aem_unit_question_bank_list = aem_unit_dict[PipelinePublishConstants.FIELD_QUESTION_BANK]

        unit_content_id = content_map_unit_dict[PipelinePublishConstants.FIELD_CONTENT_ID]
        course = content_map_unit_dict[PipelinePublishConstants.FIELD_COURSE]
        region_ach = content_map_unit_dict[PipelinePublishConstants.FIELD_REGION_ACH]

        unit_question_bank_content_groups = \
            self.content_repo_service.get_content_groups_by_param(ContentRepoContentType.TypeQuestionBank.value,
                                                                  None,
                                                                  unit_content_id,
                                                                  content_map_unit_dict[
                                                                      PipelinePublishConstants.FIELD_CONTENT_REVISION],
                                                                  content_map_unit_dict[
                                                                      PipelinePublishConstants.FIELD_SCHEMA_REVISION]).json()

        if len(aem_unit_question_bank_list) == 0:
            if len(unit_question_bank_content_groups) != 0:
                error_message.append(
                    'There should be no Question Bank Content group created as AEM unit:{0} don\'t have any questionBank!'.format(
                        unit_content_id))
                return error_message
        else:
            unit_question_bank_activity_group = jmespath.search('[?groupType==\'ACTIVITY_GROUP\']|[0]',
                                                                unit_question_bank_content_groups)
            unit_question_bank_asset_group_list = jmespath.search('[?groupType==\'ASSET_GROUP\']',
                                                                  unit_question_bank_content_groups)

            content_group_unit_question_bank_activity_entity_list = \
                unit_question_bank_activity_group[PipelinePublishConstants.FIELD_CHILDREFS]
            content_repo_unit_question_bank_activity_list = \
                self.content_repo_service.get_activities(content_group_unit_question_bank_activity_entity_list).json()

            if len(aem_unit_question_bank_list) != len(content_group_unit_question_bank_activity_entity_list):
                error_message.append(
                    'AEM unit question bank activity list size not same as content repo unit question bank activity list size!')
                return error_message

            for i in range(len(aem_unit_question_bank_list)):
                aem_unit_question_bank_activity = aem_unit_question_bank_list[i]
                content_group_unit_question_bank_activity_entity = \
                content_group_unit_question_bank_activity_entity_list[i]
                content_repo_unit_question_bank_activity = jmespath.search(
                    "[?contentId == '{0}'] | [0]".format(
                        content_group_unit_question_bank_activity_entity[PipelinePublishConstants.FIELD_CONTENT_ID]),
                    content_repo_unit_question_bank_activity_list)
                error_message.extend(self.verify_aem_homework_with_content_repo_activity(
                    aem_unit_question_bank_activity, content_repo_unit_question_bank_activity,
                    ContentRepoContentType.TypeQuestionBank, course, region_ach))

            # verify the asset_group with the asset exit in the activity list
            error_message.extend(self.verify_activity_assets_with_asset_group(
                content_repo_unit_question_bank_activity_list, unit_question_bank_asset_group_list))

        return error_message

    def verify_handout_eca_assets_with_asset_group(self, eca_list, asset_group):
        error_message = []
        # verify asset_group assets are same as it exits in the eca list
        expected_asset_list = PipelinePublishUtils.get_expected_asset_list(eca_list)

        expected_asset_list = sorted(expected_asset_list, key=lambda k: k[PipelinePublishConstants.FIELD_URL])
        actual_asset_group_childrefs = sorted(asset_group[PipelinePublishConstants.FIELD_CHILDREFS],
                                              key=lambda k: k[PipelinePublishConstants.FIELD_URL])
        diff_list = json_tools.diff(actual_asset_group_childrefs, expected_asset_list)
        if len(diff_list) != 0:
            error_message.append('asset_group childref not as expected for unit contentid: {0}, diff:{1}'.format(
                asset_group['parentRef'][PipelinePublishConstants.FIELD_CONTENT_ID], str(diff_list)))
        return error_message

    def verify_handout_homework_fields(self, aem_handout_homework, content_repo_eca_activity, activity_type, course, region_ach):
        error_message = []

        expected_metadata = PipelinePublishUtils.get_expected_content_metadata(course, activity_type, region_ach)
        actual_metadata = content_repo_eca_activity[PipelinePublishConstants.FIELD_METADATA]
        diff_list = json_tools.diff(actual_metadata, expected_metadata)
        if len(diff_list) != 0:
            error_message.append("metadata {0} not as expect"
                                 "ed for activity/eca:{1}, expected metadata is:{2}".format(actual_metadata,
                                                                                            content_repo_eca_activity[PipelinePublishConstants.FIELD_CONTENT_ID],
                                                                                                                      expected_metadata))

        content_repo_eca_activity_data = content_repo_eca_activity[PipelinePublishConstants.FIELD_DATA]
        for key in aem_handout_homework.keys():
            content_repo_key = key
            # # for lesson homework activity, field name which in the same level with "questions", will be capitalized in content_repo
            # if activity_type == ContentRepoContentType.TypeHomework and 'questions' in aem_handout_homework.keys():
            #     content_repo_key = content_repo_key.capitalize()
            error_message.extend(self
                                 .verify_aem_fields_with_content_repo(key, aem_handout_homework[key],
                                                                      content_repo_eca_activity_data[content_repo_key]))
        return error_message

    def verify_aem_fields_with_content_repo(self, key, aem_value, content_repo_value):
        error_message = []

        if key == PipelinePublishConstants.FIELD_URL:
            error_message.extend(self.verify_aem_asset_with_content_repo(aem_value, content_repo_value))
        else:
            if isinstance(aem_value, list):
                for i in range(len(aem_value)):
                    aem_list_item = aem_value[i]
                    content_repo_list_item = content_repo_value[i]
                    error_message.extend(self.verify_aem_fields_with_content_repo(key, aem_list_item,
                                                                                  content_repo_list_item))

            elif isinstance(aem_value, dict):
                # if it's asset, remove id from aem dict, as we don't need to verify this
                if PipelinePublishConstants.FIELD_MIME_TYPE in aem_value.keys():
                    aem_value.pop(PipelinePublishConstants.FIELD_ID)
                    # some asset have title field, not been stored to content_repo
                    if PipelinePublishConstants.FIELD_TITLE in aem_value.keys():
                        aem_value.pop(PipelinePublishConstants.FIELD_TITLE)
                for key in aem_value.keys():
                    aem_field_value = aem_value[key]
                    # print("verify key:" + key)
                    # need to check with leon, there's theme in the activity body
                    if key != 'theme' and key != 'tags':
                        content_repo_field_value = content_repo_value[key]
                        error_message.extend(self.verify_aem_fields_with_content_repo(key, aem_field_value,
                                                                                      content_repo_field_value))
            else:
                if str(aem_value) != str(content_repo_value):
                    error_message.append(" key:" + key + "'s value in aem not equal to the value in content-repo." \
                                                         "The aem value is:" + str(aem_value) \
                                         + ", but the value in content-repo is:" + str(content_repo_value))

        return error_message

    def verify_aem_asset_with_content_repo(self, aem_asset_url, content_repo_asset_url):
        print("start verify url:" + aem_asset_url)
        error_message = []
        # aem_asset_response = requests.get(aem_asset_url)
        # assert_that(aem_asset_response.status_code == 200,
        #             'aem asset response status is not 200:' + aem_asset_url)
        # aem_asset_sha1 = PipelinePublishUtils.get_asset_sha1(aem_asset_response.content)
        sha1_start_index = aem_asset_url.rfind('v=') + 2
        sha1_end_index = aem_asset_url.rfind('&')

        # some TB asset url is like this: http://10.163.8.4:4503/apps/e1commons/image.view/content/adam/courses/tb16/book-1/unit-2/activities/homework/multipleselectimage-vocabulary-coloursanddescriptions-activity21-/vocabulary--colours-and-descriptions--activity-21--q4-/_jcr_content/stimulus?v=6fe66efc5af10aee9479b595b9fccfe90ce3dafa&compressToJpeg=true
        if sha1_end_index != -1 and sha1_end_index > sha1_start_index:
            aem_asset_sha1 = aem_asset_url[sha1_start_index:sha1_end_index]
        else:
            aem_asset_sha1 = aem_asset_url[sha1_start_index:]

        print("start get media for content asset:" + content_repo_asset_url)
        content_repo_asset_response = self.media_service.get_media(content_repo_asset_url)
        assert_that(content_repo_asset_response.status_code == 200,
                    'content asset response status is {0}, not 200 for url: {1}'
                    .format(content_repo_asset_response.status_code, content_repo_asset_url))
        print("end of get media for content asset:" + content_repo_asset_url)
        content_repo_asset_sha1 = CommonUtils.get_asset_sha1(content_repo_asset_response.content)

        if aem_asset_sha1 != content_repo_asset_sha1:
            error_message.append(
                "asset in AEM not consistent with content-repo, aem asset url is:{0}, content asset url is:{1}, sha1 is:{2}".format(
                    aem_asset_url, content_repo_asset_url, content_repo_asset_sha1))
        print("enf of verify url:" + aem_asset_url)
        return error_message

    def verify_lesson_homework(self, aem_lesson_by_unit_dict, content_map_lesson_by_unit_dict):
        error_message = []
        aem_homework_list = aem_lesson_by_unit_dict['homework']

        lesson_content_id = content_map_lesson_by_unit_dict[PipelinePublishConstants.FIELD_CONTENT_ID]
        course = content_map_lesson_by_unit_dict[PipelinePublishConstants.FIELD_COURSE]
        region_ach = content_map_lesson_by_unit_dict[PipelinePublishConstants.FIELD_REGION_ACH]

        lesson_homework_content_group = \
            self.content_repo_service.get_content_groups_by_param(ContentRepoContentType.TypeHomework.value,
                                                                  None,
                                                                  lesson_content_id,
                                                                  content_map_lesson_by_unit_dict[
                                                                      PipelinePublishConstants.FIELD_CONTENT_REVISION],
                                                                  content_map_lesson_by_unit_dict[
                                                                      PipelinePublishConstants.FIELD_SCHEMA_REVISION]).json()
        # for cn-3-144, there's no homework under some lesson, also check if this lesson don't have any content group
        if len(aem_homework_list) == 0:
            if len(lesson_homework_content_group) != 0:
                error_message.append(
                    'This lesson {0} should not have any content group as AEM don\'t have any homework under this lesson!'.format(
                        lesson_content_id))
                return error_message
        else:
            lesson_activity_group = jmespath.search('[?groupType==\'ACTIVITY_GROUP\']|[0]',
                                                    lesson_homework_content_group)
            lesson_asset_group_list = jmespath.search('[?groupType==\'ASSET_GROUP\']', lesson_homework_content_group)

            lesson_activity_metadata_list = lesson_activity_group[PipelinePublishConstants.FIELD_CHILDREFS]
            lesson_activity_list = self.content_repo_service.get_activities(lesson_activity_metadata_list).json()

            if len(aem_homework_list) != len(lesson_activity_metadata_list):
                error_message.append(
                    'AEM lesson homework list size not same as content repo lesson activity list size!')
                return error_message

            for i in range(len(aem_homework_list)):
                aem_homework = aem_homework_list[i]
                lesson_activity_metadata = lesson_activity_metadata_list[i]
                lesson_activity = jmespath.search(
                    "[?contentId == '{0}'] | [0]".format(
                        lesson_activity_metadata[PipelinePublishConstants.FIELD_CONTENT_ID]),
                    lesson_activity_list)
                error_message.extend(self.verify_aem_homework_with_content_repo_activity(
                    aem_homework, lesson_activity, ContentRepoContentType.TypeHomework, course, region_ach))

            # verify the asset_group with the asset exit in the activity list
            error_message.extend(self.verify_activity_assets_with_asset_group(
                lesson_activity_list, lesson_asset_group_list))

        return error_message

    def verify_aem_homework_with_content_repo_activity(self, aem_homework, lesson_activity, activity_type, course, region_ach):
        error_message = []
        aem_homework_detail_url = aem_homework[PipelinePublishConstants.FIELD_URL]
        aem_homework_detail_response = requests.get(aem_homework_detail_url)
        assert_that(aem_homework_detail_response.status_code == 200)
        aem_homework_detail = aem_homework_detail_response.json()

        homework_title = aem_homework[PipelinePublishConstants.FIELD_TITLE]
        if homework_title != lesson_activity[PipelinePublishConstants.FIELD_TITLE]:
            error_message.append("title {0} not consistent between AEM homework and activity!".format(
                homework_title))

        if aem_homework['id'] != lesson_activity['extra']['com-ef-kt']['sourceID']:
            error_message.append("id {0} not consistent between AEM homework and activity!".format(
                aem_homework['id']))

        if aem_homework['path'] != lesson_activity['extra']['com-ef-kt']['sourcePath']:
            error_message.append(" path {0} not consistent between AEM homework and activity!".format(
                aem_homework['path']))

        if aem_homework_detail['Key'] != lesson_activity['originID']:
            error_message.append(" Key {0} not consistent between AEM homework and activity!".format(
                aem_homework_detail['Key']))

        error_message.extend(self.verify_handout_homework_fields(aem_homework_detail,
                                                                 lesson_activity, activity_type, course,
                                                                 region_ach))
        return error_message

    def verify_activity_assets_with_asset_group(self, activity_list, asset_group_list):
        error_message = []

        # some activities don't have any asset
        for activity in activity_list:
            activity_content_id = activity['contentId']
            asset_in_activity_list = PipelinePublishUtils.get_expected_asset_list([activity])
            asset_group_for_activity = jmespath.search(
                "[?parentRef.contentId == \'{0}\']".format(activity_content_id), asset_group_list)
            if len(asset_in_activity_list) == 0:
                if len(asset_group_for_activity) != 0:
                    error_message.append(
                        'asset group should not present for activity: {0}, as this activity don\'t have any asset!'.format(
                            activity_content_id))
            else:
                if len(asset_group_for_activity) == 0:
                    error_message.append(
                        'asset group should be present for activity: {0}, as this activity have some assets!'.format(
                            activity_content_id))

        for asset_group in asset_group_list:
            expected_activity_contentid = asset_group['parentRef']['contentId']
            expected_activity = jmespath.search(
                "[?contentId == '{0}'] | [0]".format(expected_activity_contentid), activity_list)

            expected_asset_list = PipelinePublishUtils.get_expected_asset_list([expected_activity])

            expected_asset_list = sorted(expected_asset_list, key=lambda k: k[PipelinePublishConstants.FIELD_URL])
            actual_asset_list = jmespath.search('childRefs[]', asset_group)
            actual_asset_list = PipelinePublishUtils.remove_duplicate_asset(actual_asset_list)
            actual_asset_list = sorted(actual_asset_list, key=lambda k: k[PipelinePublishConstants.FIELD_URL])
            diff_list = json_tools.diff(actual_asset_list, expected_asset_list)
            if len(diff_list) != 0:
                error_message.append(
                    'asset list in asset_group for activity: {0} not as expected for asset exist in activity list, diff is: {1}'.format(
                        expected_activity, str(diff_list)))
        return error_message
