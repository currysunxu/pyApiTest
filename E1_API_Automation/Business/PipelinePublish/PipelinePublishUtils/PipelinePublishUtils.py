import copy
import hashlib
from enum import Enum

from E1_API_Automation.Business.PipelinePublish.PipelinePublishUtils.PipelinePublishConstants import \
    PipelinePublishConstants


class ContentMapCourse(Enum):
    highflyers = 'HIGH_FLYERS_35'


class PipelinePublishUtils:
    @staticmethod
    def get_content_map_course(course_enum_name):
        for content_map_course in ContentMapCourse:
            if content_map_course.name == course_enum_name:
                return content_map_course.value

    @staticmethod
    def get_asset_sha1(asset_encode):
        s1 = hashlib.sha1()
        s1.update(asset_encode)
        return s1.hexdigest()

    @staticmethod
    def remove_duplicate_asset(asset_list):
        # remove the duplicate assets
        asset_url_dict = {}
        for asset in asset_list:
            asset_url_dict[asset[PipelinePublishConstants.FIELD_URL]] = asset

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
