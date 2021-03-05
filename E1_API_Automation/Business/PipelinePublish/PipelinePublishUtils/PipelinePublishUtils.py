import copy

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
    def get_expected_content_metadata(course, content_type):
        expected_metadata = {}
        expected_metadata['program'] = course
        expected_metadata['domainType'] = content_type.value
        if content_type in (ContentRepoContentType.TypeHomework, ContentRepoContentType.TypeQuiz, ContentRepoContentType.TypeQuestionBank):
            expected_metadata['entityType'] = 'ACTIVITY'
        elif content_type in (ContentRepoContentType.TypeHandout, ContentRepoContentType.TypeFlashcard):
            expected_metadata['entityType'] = 'ECA'
        return expected_metadata
