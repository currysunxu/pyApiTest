import copy

import jmespath

from E1_API_Automation.Business.NGPlatform.NGPlatformUtils.ContentRepoEnum import ContentRepoContentType
from E1_API_Automation.Business.PipelinePublish.PipelinePublishUtils.PipelinePublishConstants import \
    PipelinePublishConstants


class PipelinePublishUtils:

    @staticmethod
    def remove_duplicate_asset(asset_list):
        # remove the duplicate assets
        asset_url_dict = {}

        for asset in asset_list:
            asset_url = asset[PipelinePublishConstants.FIELD_URL]
            if not asset_url in asset_url_dict.keys():
                asset_url_dict[asset_url] = asset

        return list(asset_url_dict.values())

    @staticmethod
    def get_expected_asset_list(content_list):
        expected_asset_list = []
        for content in content_list:
            for key in content.keys():
                expected_asset_list.extend(PipelinePublishUtils.get_expected_asset_list_by_indicator(content[key]))

        expected_asset_list = PipelinePublishUtils.remove_duplicate_asset(expected_asset_list)

        for asset_dict in expected_asset_list:
            asset_dict['nodeType'] = 'ASSET'
        return expected_asset_list

    @staticmethod
    def get_expected_asset_list_by_indicator(content_value):
        expected_asset_list = []

        if isinstance(content_value, list):
            for i in range(len(content_value)):
                content_list_item = content_value[i]
                expected_asset_list.extend(PipelinePublishUtils.get_expected_asset_list_by_indicator(content_list_item))
        elif isinstance(content_value, dict):
            # if there's mimeType, indicate it's asset
            if PipelinePublishConstants.FIELD_MIME_TYPE in content_value.keys():
                content_value_copy = copy.deepcopy(content_value)
                expected_asset_list.append(content_value_copy)

            # video asset have thumbnails, it's also an asset
            for key in content_value.keys():
                expected_asset_list.extend(
                    PipelinePublishUtils.get_expected_asset_list_by_indicator(content_value[key]))

        return expected_asset_list

    @staticmethod
    def get_expected_aem_unit_by_path(aem_units_dict, expected_aem_path):
        for key in aem_units_dict.keys():
            aem_unit_dict = aem_units_dict[key]
            path = aem_unit_dict['path']
            if path == expected_aem_path:
                return aem_unit_dict

    @staticmethod
    def get_expected_content_metadata(course, content_type, region_ach):
        expected_metadata = {}
        expected_metadata['program'] = course
        expected_metadata['domainType'] = content_type.value
        if content_type in (ContentRepoContentType.TypeHomework, ContentRepoContentType.TypeQuiz, ContentRepoContentType.TypeQuestionBank):
            expected_metadata['entityType'] = 'ACTIVITY'
        elif content_type in (ContentRepoContentType.TypeHandout, ContentRepoContentType.TypeFlashcard):
            expected_metadata['entityType'] = 'ECA'

        if region_ach:
            expected_metadata['regionAch'] = region_ach.upper()
        return expected_metadata

    @staticmethod
    def get_expected_unit_quiz_localizations(content_group_unit_quiz_activity_entity_list,
                                             content_repo_unit_quiz_activity_list,
                                             aem_unit_quiz_skillset_localizations):
        activity_skill_set_map = {}
        for content_group_unit_quiz_activity_entity in content_group_unit_quiz_activity_entity_list:
            content_repo_unit_quiz_activity = jmespath.search(
                "[?contentId == '{0}'] | [0]".format(
                    content_group_unit_quiz_activity_entity[PipelinePublishConstants.FIELD_CONTENT_ID]),
                content_repo_unit_quiz_activity_list)
            activity_skill_set = content_repo_unit_quiz_activity['data']['Body']['tags']['skillType']
            activity_dict = {}
            activity_dict[PipelinePublishConstants.FIELD_CONTENT_ID] = content_group_unit_quiz_activity_entity[
                PipelinePublishConstants.FIELD_CONTENT_ID]
            activity_dict[PipelinePublishConstants.FIELD_CONTENT_REVISION] = content_group_unit_quiz_activity_entity[
                PipelinePublishConstants.FIELD_CONTENT_REVISION]
            activity_dict[PipelinePublishConstants.FIELD_SCHEMA_REVISION] = content_group_unit_quiz_activity_entity[
                PipelinePublishConstants.FIELD_SCHEMA_REVISION]
            if activity_skill_set in activity_skill_set_map.keys():
                categorized_activity_list = activity_skill_set_map[activity_skill_set]
                activity_dict = len(categorized_activity_list) + 1
                categorized_activity_list.append(activity_dict)
            else:
                activity_dict['sequence'] = 1
                activity_skill_set_map[activity_skill_set] = [activity_dict]

        expected_skill_set_localizations = []
        for aem_skill_set_localization in aem_unit_quiz_skillset_localizations:
            expected_skill_set_localization = {}
            aem_skill_set = aem_skill_set_localization['skillset']
            expected_skill_set_localization['code'] = aem_skill_set
            expected_localization_desc_list = []
            for aem_localization_desc in aem_skill_set_localization['localizations']:
                expected_localization_desc = {}
                expected_localization_desc['text'] = aem_localization_desc['description']
                expected_localization_desc['language'] = aem_localization_desc['language']
                expected_localization_desc_list.append(expected_localization_desc)
            expected_skill_set_localization['title'] = expected_localization_desc_list
            expected_skill_set_localization['activityRefs'] = activity_skill_set_map[aem_skill_set]
            expected_skill_set_localizations.append(expected_skill_set_localization)
        return expected_skill_set_localizations
