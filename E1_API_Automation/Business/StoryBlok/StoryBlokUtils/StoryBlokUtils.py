import json

import jmespath
import json_tools
import re
from tkinter.filedialog import askopenfilename
import zipfile

from hamcrest import assert_that

from E1_API_Automation.Business.NGPlatform.ContentRepoService import ContentRepoService
from E1_API_Automation.Business.NGPlatform.NGPlatformUtils.ContentRepoEnum import ContentRepoContentType, \
    ContentRepoGroupType
from E1_API_Automation.Business.PipelinePublish.MediaService import MediaService
from E1_API_Automation.Business.StoryBlok.StoryBlokImportService import StoryBlokImportService
from E1_API_Automation.Business.StoryBlok.StoryBlokUtils.StoryBlokConstants import StoryBlokConstants
from E1_API_Automation.Business.Utils.CommonUtils import CommonUtils
from E1_API_Automation.Business.Utils.EnvUtils import EnvUtils
from E1_API_Automation.Settings import env_key
from E1_API_Automation.Test_Data.PipelinePublishData import AEMData
from E1_API_Automation.Test_Data.StoryblokData import StoryBlokVersion, StoryblokReleaseProgram


class StoryBlokUtils:
    @staticmethod
    def get_storyblok_version_by_env():
        if EnvUtils.is_env_qa():
            return StoryBlokVersion.DRAFT.value
        else:
            return StoryBlokVersion.PUBLISHED.value

    @staticmethod
    def verify_storyblok_stories(storyblok_story_list, content_repo_content_list, expected_release_revision,
                                 release_type=None):
        content_revision_list = jmespath.search('[].contentRevision', content_repo_content_list)
        content_revision_list = list(set(content_revision_list))

        error_message = []
        if len(content_revision_list) != 1:
            error_message.append('ecas in content repo should have same content revision!')
            return error_message

        if content_revision_list[0] != expected_release_revision:
            error_message.append(
                'content revision not as expected! release revision should be:' + expected_release_revision)
            return error_message

        if len(storyblok_story_list) != len(content_repo_content_list):
            error_message.append('storyblok story list size not same as content repo eca list size!')
            return error_message

        for storyblok_story in storyblok_story_list:
            content_id = storyblok_story['uuid']
            content_repo_content = jmespath.search('[?contentId == \'{0}\']|[0]'.format(content_id),
                                                   content_repo_content_list)
            error_message.extend(StoryBlokUtils.verify_storyblok_story_with_contentrepo(storyblok_story,
                                                                                        content_repo_content,
                                                                                        release_type))
        return error_message

    @staticmethod
    def get_reader_cover_thumbnail(cover_image_file_name, cover_thumbnail_resolution):
        indicator = cover_image_file_name.find('/f/')
        cover_thumbnail_file_name = '{0}/{1}/{2}'.format(StoryBlokConstants.STORYBLOK_COVER_THUMBNAIL_HOST,
                                                         cover_thumbnail_resolution,
                                                         cover_image_file_name[indicator + 1:])
        cover_thumbnail_dict = {}
        cover_thumbnail_dict['filename'] = cover_thumbnail_file_name
        cover_thumbnail_dict['fieldtype'] = 'asset'
        return cover_thumbnail_dict

    @staticmethod
    def verify_storyblok_story_with_contentrepo(storyblok_story, content_repo_content, release_type=None):
        error_message = []
        print('start verify storyblok story:' + storyblok_story['name'])

        component = ''
        latest_activity_list = None
        expected_metadata = {}
        if release_type == StoryblokReleaseProgram.MOCKTEST:
            expected_metadata['domainType'] = 'MT'
            component = storyblok_story['content']['component']
            if component == 'paper':
                expected_metadata['entityType'] = 'PAPER'
                # for paper, the activity will be converted to latest activity in content-repo
                content_repo_service = ContentRepoService()
                paper_activity_id_list = jmespath.search("content.parts[].sections[].activities[].activity",
                                                         storyblok_story)
                latest_activity_list = content_repo_service.get_latest_activities(paper_activity_id_list).json()
                expected_paper_question_count = len(jmespath.search("content.parts[].sections[].activities[]", storyblok_story))
            else:
                expected_metadata['entityType'] = 'ACTIVITY'
        elif release_type == StoryblokReleaseProgram.READERS:
            expected_metadata['domainType'] = 'READER'
            expected_metadata['entityType'] = 'ECA'

            #if it's reader release, there will be a cover_thumbnail field added if reader's cover_image have value
            storyblok_content = storyblok_story['content']
            if 'cover_image' in storyblok_content.keys():
                cover_image_dict = storyblok_content['cover_image']
                if 'filename' in cover_image_dict.keys() and len(cover_image_dict['filename']) != 0:
                    cover_image_file_name = cover_image_dict['filename']

                    cover_thumbnail_dict_1 = StoryBlokUtils.get_reader_cover_thumbnail(cover_image_file_name, StoryBlokConstants.STORYBLOK_COVER_THUMBNAIL_RESOLUTION_1)
                    cover_thumbnail_dict_2 = StoryBlokUtils.get_reader_cover_thumbnail(cover_image_file_name,
                                                                                       StoryBlokConstants.STORYBLOK_COVER_THUMBNAIL_RESOLUTION_2)
                    cover_thumbnail_dict_3 = StoryBlokUtils.get_reader_cover_thumbnail(cover_image_file_name,
                                                                                       StoryBlokConstants.STORYBLOK_COVER_THUMBNAIL_RESOLUTION_3)
                    storyblok_content['cover_thumbnail'] = cover_thumbnail_dict_1
                    storyblok_content['cover_thumbnail2'] = cover_thumbnail_dict_2
                    storyblok_content['cover_thumbnail3'] = cover_thumbnail_dict_3
        elif release_type == StoryblokReleaseProgram.VOCABULARIES:
            expected_metadata['domainType'] = 'VOCAB'
            expected_metadata['entityType'] = 'ECA'

        diff_list = json_tools.diff(json.dumps(content_repo_content['metadata']), json.dumps(expected_metadata))
        # if str(content_repo_content['metadata']) != str(expected_metadata):
        if len(diff_list) != 0:
            error_message.append(
                '{0} story\'s metadata in content-repo not equal as expected {1}'.format(content_repo_content['contentId'],
                                                                                         str(expected_metadata)))
            return error_message

        content_repo_content_data = content_repo_content['data']
        # content repo source field should be storyblok
        if content_repo_content_data['source'] != 'storyblok':
            error_message.append(
                'reader/vocab eca or mocktest activity field \'source\' in content-repo not equal to storyblok')
            return error_message

        # for paper, it will generate questionCount in content repo
        if component == 'paper':
            key = 'questionCount'
            content_repo_question_count = content_repo_content_data[key]
            error_message.extend(StoryBlokUtils.
                                 verify_paper_fields_with_contentrepo(key, expected_paper_question_count,
                                                                      content_repo_question_count))

        for key in storyblok_story.keys():
            if key not in (
                    '_uid', '_editable', 'alternates', 'default_full_slug', 'sort_by_date', 'position', 'tag_list',
                    'is_startpage',
                    'meta_data', 'group_id', 'first_published_at', 'release_id', 'lang', 'path', 'translated_slugs',
                    'parent_id'):
                storyblock_value = storyblok_story[key]

                if key == 'uuid':
                    content_repo_value = content_repo_content['contentId']
                elif key == 'id':
                    content_repo_value = content_repo_content_data['originID']
                else:
                    content_repo_value = content_repo_content_data[key]

                if component == 'paper':
                    error_message.extend(StoryBlokUtils.
                                         verify_paper_fields_with_contentrepo(key, storyblock_value, content_repo_value,
                                                                              latest_activity_list))
                else:
                    error_message.extend(StoryBlokUtils.
                                         verify_storyblok_fields_with_contentrepo(key, storyblock_value,
                                                                                  content_repo_value,
                                                                                  release_type))
            else:
                # otherwise those key should not present in content_repo
                if key in content_repo_content_data.keys():
                    error_message.append(' key:{0} should not exist in content-repo.')
        if len(error_message) != 0:
            print(error_message)
        return error_message

    @staticmethod
    def verify_mt_question_resources(storyblock_value, content_repo_value):
        error_message = []
        # for mt question resources filed, only url will be changed(upload to AWS), other fields will not be converted
        for key in storyblock_value.keys():
            if key not in ('id', 'url'):
                storyblock_field_value = storyblock_value[key]
                content_repo_field_value = content_repo_value[key]

                if str(storyblock_field_value) != str(content_repo_field_value):
                    error_message.append(" key:" + key + "'s value in storyblok mt question resource not equal to the value in content-repo." \
                                                         "The storyblok value is:" + str(storyblock_field_value)
                                         + ", but the value in content-repo is:" + str(content_repo_field_value))
            elif key == 'url':
                # check the asset sha1 between storyblok and aws s3
                error_message.extend(StoryBlokUtils.verify_content_repo_asset_field(key,
                                                                                    content_repo_value[key],
                                                                                    storyblock_value[key]))
            else:
                # otherwise those key should not present in content_repo
                if key in content_repo_value.keys():
                    error_message.append(' mt question resources\' key:{0} should not exist in content-repo.')
        return error_message

    @staticmethod
    def verify_storyblok_fields_with_contentrepo(key, storyblock_value, content_repo_value, release_type=None, is_mt_question_resource=False):
        error_message = []

        ''' 
        if it's mock test question, and key in specific list, it's customized plugin in storyblok, the value is storyblok_story[key][key]
        e.g.
        "body": {
                 "body": {
                        "mappings": []
                        },
                        "plugin": "body"
                }
        '''
        if release_type == StoryblokReleaseProgram.MOCKTEST and key in (
                'body', 'tags', 'stimulus', 'questions', 'resources', 'explanation'):
            if isinstance(storyblock_value, dict) and 'plugin' in storyblock_value.keys():
                storyblock_value = storyblock_value[key]
                if key == 'resources':
                    is_mt_question_resource = True

        if isinstance(storyblock_value, list):
            if len(storyblock_value) != len(content_repo_value):
                error_message.append(
                    'length for key:{0} not consistent between storyblok and content_repo'.format(key))
            else:
                for i in range(len(storyblock_value)):
                    storyblok_list_item = storyblock_value[i]
                    content_repo_list_item = content_repo_value[i]
                    error_message.extend(StoryBlokUtils.
                                         verify_storyblok_fields_with_contentrepo(key,
                                                                                  storyblok_list_item,
                                                                                  content_repo_list_item,
                                                                                  release_type,
                                                                                  is_mt_question_resource))
        elif isinstance(storyblock_value, dict):
            # for mt question resource, valdiate differently
            if is_mt_question_resource:
                error_message.extend(StoryBlokUtils.verify_mt_question_resources(storyblock_value,
                                                                                 content_repo_value))
            else:
                # if it's asset dict
                if 'fieldtype' in storyblock_value.keys() and storyblock_value['fieldtype'] == 'asset':
                    error_message.extend(StoryBlokUtils.verify_content_repo_asset(storyblock_value,
                                                                                  content_repo_value))
                else:
                    for key in storyblock_value.keys():
                        if key not in (
                                '_uid', '_editable'):
                            storyblock_field_value = storyblock_value[key]
                            content_repo_field_value = content_repo_value[key]

                            error_message.extend(StoryBlokUtils.
                                                 verify_storyblok_fields_with_contentrepo(key, storyblock_field_value,
                                                                                          content_repo_field_value,
                                                                                          release_type))
                        else:
                            # otherwise those key should not present in content_repo
                            if key in content_repo_value.keys():
                                error_message.append(' key:{0} should not exist in content-repo.')
        else:
            if str(storyblock_value) != str(content_repo_value):
                error_message.append(" key:" + key + "'s value in storyblok not equal to the value in content-repo." \
                                                     "The storyblok value is:" + str(storyblock_value)
                                     + ", but the value in content-repo is:" + str(content_repo_value))

        return error_message

    @staticmethod
    def verify_paper_activities_with_contentrepo(paper_activities, content_repo_activities, latest_activity_list):
        error_message = []
        if len(paper_activities) != len(content_repo_activities):
            error_message.append('length for activities not consistent between storyblok and content_repo')
        else:
            for i in range(len(paper_activities)):
                storyblok_activity = paper_activities[i]
                content_repo_activity = content_repo_activities[i]

                if content_repo_activity['activitySequence'] != (i + 1):
                    error_message.append('activitySequence not as expected as {0}'.format(str(i + 1)))

                for key in storyblok_activity.keys():
                    if key not in ('_uid', 'component'):
                        storyblok_activity_value = storyblok_activity[key]
                        if key == 'activity':
                            # activity field in storyblok will be converted to latest activity's contentId, contentRevision, schemaVersion
                            expected_latest_activity = jmespath.search(
                                "[?contentId == '{0}'] | [0]".format(storyblok_activity_value),
                                latest_activity_list)
                            expected_content_revision = expected_latest_activity['contentRevision']
                            expected_schema_revision = expected_latest_activity['schemaVersion']
                            if content_repo_activity['contentId'] != storyblok_activity_value:
                                error_message.append(
                                    ' contentId in content-repo not as expected:' + storyblok_activity_value)

                            if content_repo_activity['contentRevision'] != expected_content_revision:
                                error_message.append(
                                    ' contentRevision in content-repo not as expected:' + expected_content_revision)

                            if content_repo_activity['schemaVersion'] != expected_schema_revision:
                                error_message.append(
                                    ' schemaRevision in content-repo not as expected:' + expected_schema_revision)
                        else:
                            content_repo_activity_value = content_repo_activity[key]
                            if str(storyblok_activity_value) != str(content_repo_activity_value):
                                error_message.append(
                                    " key:" + key + "'s value in storyblok not equal to the value in content-repo." \
                                                    "The storyblok value is:" + str(
                                        storyblok_activity_value) \
                                    + ", but the value in content-repo is:" + str(content_repo_activity_value))
                    else:
                        # otherwise those key should not present in content_repo
                        if key in content_repo_activity.keys():
                            error_message.append(' key:{0} should not exist in content-repo activity')
        return error_message

    @staticmethod
    def verify_paper_sections_with_contentrepo(paper_sections, content_repo_sections, latest_activity_list):
        error_message = []
        if len(paper_sections) != len(content_repo_sections):
            error_message.append('length for sections not consistent between storyblok and content_repo')
        else:
            for i in range(len(paper_sections)):
                storyblok_section = paper_sections[i]
                content_repo_section = content_repo_sections[i]

                if content_repo_section['sectionSequence'] != (i + 1):
                    error_message.append(' sectionSequence not as expected as {0}'.format(str(i + 1)))

                for key in storyblok_section.keys():
                    #storyblok section's id will not be released to content repo, content repo's id value will be released with storyblok's _uid value
                    if key == 'id':
                        continue
                    storyblok_section_value = storyblok_section[key]
                    if key == 'activities':
                        expected_content_repo_value = content_repo_section[key]
                        error_message.extend(StoryBlokUtils.verify_paper_activities_with_contentrepo(
                            storyblok_section_value, expected_content_repo_value, latest_activity_list))
                    else:
                        # paper section's _uid will be converted to id into content-repo
                        if key == '_uid':
                            expected_content_repo_value = content_repo_section['id']
                        else:
                            expected_content_repo_value = content_repo_section[key]
                        if str(storyblok_section_value) != str(expected_content_repo_value):
                            error_message.append(
                                " key:" + key + "'s value in storyblok not equal to the value in content-repo." \
                                                "The storyblok value is:" + str(
                                    storyblok_section_value) \
                                + ", but the value in content-repo is:" + str(
                                    expected_content_repo_value))
        return error_message

    @staticmethod
    def verify_paper_fields_with_contentrepo(key, storyblock_value, content_repo_value, latest_activity_list=None):
        error_message = []

        if key == 'resource':
            error_message.extend(StoryBlokUtils.verify_content_repo_asset(storyblock_value,
                                                                          content_repo_value))
        elif key == 'sections':
            error_message.extend(StoryBlokUtils.verify_paper_sections_with_contentrepo(storyblock_value,
                                                                                       content_repo_value,
                                                                                       latest_activity_list))
        else:
            if isinstance(storyblock_value, list):
                if len(storyblock_value) != len(content_repo_value):
                    error_message.append('length for key:{0} not consistent between storyblok and content_repo'.format(
                        key))
                else:
                    for i in range(len(storyblock_value)):
                        storyblok_list_item = storyblock_value[i]
                        content_repo_list_item = content_repo_value[i]
                        error_message.extend(StoryBlokUtils. \
                                             verify_paper_fields_with_contentrepo(key, storyblok_list_item,
                                                                                  content_repo_list_item,
                                                                                  latest_activity_list))
            elif isinstance(storyblock_value, dict):
                for key in storyblock_value.keys():
                    if key not in (
                            '_uid', '_editable'):
                        storyblock_field_value = storyblock_value[key]
                        content_repo_field_value = content_repo_value[key]
                        error_message.extend(StoryBlokUtils. \
                                             verify_paper_fields_with_contentrepo(key, storyblock_field_value,
                                                                                  content_repo_field_value,
                                                                                  latest_activity_list))
                    else:
                        # otherwise those key should not present in content_repo
                        if key in content_repo_value.keys():
                            error_message.append(' key:{0} should not exist in content-repo.')
            else:
                if str(storyblock_value) != str(content_repo_value):
                    error_message.append(" key:" + key + "'s value in storyblok not equal to the value in content-repo." \
                                                         "The storyblok value is:" + str(
                        storyblock_value) \
                                         + ", but the value in content-repo is:" + str(content_repo_value))

        return error_message

    @staticmethod
    def verify_content_repo_asset(storyblok_asset_dict, content_repo_asset_dict):
        error_message = []

        if isinstance(storyblok_asset_dict, str):
            if len(storyblok_asset_dict) == 0 and len(content_repo_asset_dict) == 0:
                return []
            elif len(storyblok_asset_dict) == 0 and len(content_repo_asset_dict) != 0:
                error_message.append("asset section in content repo should be empty")
                return error_message

        storyblok_file_name = storyblok_asset_dict['filename']
        if storyblok_file_name is None or len(storyblok_file_name) == 0:
            expected_filed_list = ['sha1', 'size', 'mimeType', 'url']

            for key in content_repo_asset_dict.keys():
                if key not in expected_filed_list:
                    error_message.append(' {0} is not a expected field in content repo asset section'.format(key))

            if len(error_message) != 0:
                return error_message

            for key in expected_filed_list:
                if key == 'size':
                    expected_value = 0
                else:
                    expected_value = ''
                error_message.extend(StoryBlokUtils.verify_content_repo_asset_field(key,
                                                                                    content_repo_asset_dict[key],
                                                                                    expected_value))
        else:
            expected_url = storyblok_file_name
            sha1_end_index = expected_url.rfind('/')
            sha1_start_index = expected_url.rfind('/', 0, sha1_end_index)
            expected_sha1 = expected_url[sha1_start_index + 1:sha1_end_index]
            asset_name = storyblok_file_name[sha1_end_index+1:]

            expected_mime_type = ''
            if expected_url.lower().endswith('.png'):
                expected_mime_type = 'image/png'
            elif expected_url.lower().endswith('.mp3'):
                expected_mime_type = 'audio/mpeg'
            elif expected_url.lower().endswith('.jpg') or expected_url.lower().endswith('.jpeg'):
                expected_mime_type = 'image/jpeg'

            aws_s3_subfolder = expected_mime_type[:expected_mime_type.find('/')]

            # if storyblok file name starts with https://storyblok-image.ef.com.cn/unsafe, the asset is for cover_thumbnail
            if storyblok_file_name.startswith(StoryBlokConstants.STORYBLOK_COVER_THUMBNAIL_HOST):
                thumbnail_resolution_start_index = len(StoryBlokConstants.STORYBLOK_COVER_THUMBNAIL_HOST) + 1
                thumbnail_resolution_end_index = storyblok_file_name.find('/', thumbnail_resolution_start_index)
                thumbnail_resolution = storyblok_file_name[thumbnail_resolution_start_index:thumbnail_resolution_end_index]
                suffix_index = asset_name.rfind('.')
                asset_name = asset_name[:suffix_index] + '_' + thumbnail_resolution + asset_name[suffix_index:]

            # url in content repo is different from storyblok, the asset will be uploaded to aws s3
            expected_asset_name_in_content = '{0}_{1}'.format(expected_sha1, asset_name)
            expected_url_value = 'org/com-ef-kt/{0}/{1}'.format(aws_s3_subfolder, expected_asset_name_in_content)
            # check the content_repo url value
            error_message.extend(StoryBlokUtils.verify_content_repo_asset_field('url_value',
                                                                                content_repo_asset_dict[
                                                                                    'url'],
                                                                                expected_url_value))

            # check the asset sha1 between storyblok and aws s3
            compare_key = 'url'
            error_message.extend(StoryBlokUtils.verify_content_repo_asset_field(compare_key,
                                                                                content_repo_asset_dict[
                                                                                    compare_key],
                                                                                expected_url))

            if storyblok_file_name.startswith(StoryBlokConstants.STORYBLOK_COVER_THUMBNAIL_HOST):
                expected_sha1 = '{0}_{1}'.format(expected_sha1, thumbnail_resolution)

            compare_key = 'sha1'
            error_message.extend(StoryBlokUtils.verify_content_repo_asset_field(compare_key,
                                                                                content_repo_asset_dict[
                                                                                    compare_key],
                                                                                expected_sha1))

            # this value is set harcoded
            compare_key = 'size'
            error_message.extend(StoryBlokUtils.verify_content_repo_asset_field(compare_key,
                                                                                content_repo_asset_dict[
                                                                                    compare_key],
                                                                                1024))

            compare_key = 'mimeType'
            error_message.extend(StoryBlokUtils.verify_content_repo_asset_field(compare_key,
                                                                                content_repo_asset_dict[
                                                                                    compare_key],
                                                                                expected_mime_type))

            if expected_mime_type == 'audio/mpeg':
                is_asset_image = False
            else:
                is_asset_image = True

            if is_asset_image:
                # thumbnail have fixed width and height
                if storyblok_file_name.startswith(StoryBlokConstants.STORYBLOK_COVER_THUMBNAIL_HOST):
                    # expected_width_value = StoryBlokConstants.STORYBLOK_COVER_THUMBNAIL_WIDTH_221
                    # expected_height_value = StoryBlokConstants.STORYBLOK_COVER_THUMBNAIL_HEIGHT
                    indicator = thumbnail_resolution.find('x')
                    expected_width_value = thumbnail_resolution[:indicator]
                    expected_height_value = thumbnail_resolution[indicator+1:]
                else:
                    image_size_end_index = sha1_start_index
                    image_size_start_index = expected_url.rfind('/', 0, image_size_end_index)
                    image_size = expected_url[image_size_start_index + 1:image_size_end_index]
                    split_index = image_size.rfind('x')
                    expected_width_value = image_size[:split_index]
                    expected_height_value = image_size[split_index + 1:]

                compare_key = 'width'
                error_message.extend(StoryBlokUtils.verify_content_repo_asset_field(compare_key,
                                                                                    content_repo_asset_dict[
                                                                                        compare_key],
                                                                                    expected_width_value))

                compare_key = 'height'
                error_message.extend(StoryBlokUtils.verify_content_repo_asset_field(compare_key,
                                                                                    content_repo_asset_dict[
                                                                                        compare_key],
                                                                                    expected_height_value))
            else:
                # for audio, there's no width and height, but have duration field
                compare_key = 'duration'
                error_message.extend(StoryBlokUtils.verify_content_repo_asset_field(compare_key,
                                                                                    content_repo_asset_dict[
                                                                                        compare_key],
                                                                                    0))
        return error_message

    @staticmethod
    def verify_content_repo_asset_field(field_name, content_repo_value, expected_value):
        error_message = []
        # storyblok resources were uploaded to AWS S3, need to compare storyblok resource sha1 with content repo resource sha1
        if field_name == 'url' and len(expected_value) != 0:
            storyblok_resource_response = StoryBlokImportService.get_storyblok_resource(expected_value)
            assert_that(storyblok_resource_response.status_code == 200,
                        'storyblok resource response status is {0}, not 200 for url: {1}'
                        .format(storyblok_resource_response.status_code, expected_value))
            storyblok_resource_sha1 = CommonUtils.get_asset_sha1(storyblok_resource_response.content)

            media_host = AEMData.CSEMediaService[env_key]['host']
            media_api_key = AEMData.CSEMediaService[env_key]['x-api-key']
            cse_media_service = MediaService(media_host, media_api_key)
            cse_media_service_response = cse_media_service.get_media(content_repo_value)
            assert_that(cse_media_service_response.status_code == 200,
                        'cse media service resource response status is {0} not 200 for url: {1}'
                        .format(cse_media_service_response.status_code, content_repo_value))
            media_resource_sha1 = CommonUtils.get_asset_sha1(cse_media_service_response.content)

            # not compare resource sha1 for cover_thumbnail because of CP-237
            if not expected_value.startswith(StoryBlokConstants.STORYBLOK_COVER_THUMBNAIL_HOST):
                if storyblok_resource_sha1 != media_resource_sha1:
                    error_message.append(
                        "resource in content repo not consistent with Storyblok, content repo resource url is:{0}, storyblok resource url is:{1}, sha1 is:{2}".format(
                            content_repo_value, expected_value, storyblok_resource_sha1))
        else:
            if str(content_repo_value) != str(expected_value):
                error_message.append("asset field:" + field_name + "'s value in content repo not as expected." \
                                                                   "The content_repo_value value is:" + str(
                    content_repo_value) \
                                     + ", but expected value is:" + str(expected_value))
        return error_message

    @staticmethod
    def verify_storyblok_reader_levels(storyblok_reader_level_list, content_map_reader_level_list):
        content_revision_list = jmespath.search('[].contentRevision', content_map_reader_level_list)
        content_revision_list = list(set(content_revision_list))

        content_repo_service = ContentRepoService()

        error_message = []
        if len(content_revision_list) != 1:
            error_message.append('reader levels in content map should have same content revision!')
            return error_message

        if len(storyblok_reader_level_list) != len(content_map_reader_level_list):
            error_message.append('storyblok reader level list size not same as content map reader level list size!')
            return error_message

        for i in range(len(content_map_reader_level_list)):
            content_map_reader_level = content_map_reader_level_list[i]
            storyblok_reader_level = storyblok_reader_level_list[i]

            # reader level verification
            expected_reader_level = {}
            expected_reader_level['type'] = 'LEVEL'
            expected_reader_level['contentPath'] = storyblok_reader_level['full_slug'].replace('course-config/', '')
            expected_reader_level['course'] = 'READERS_10'
            expected_reader_level['originID'] = storyblok_reader_level['id']
            expected_reader_level['code'] =int(storyblok_reader_level['content']['code'])
            expected_reader_level['source'] = 'storyblok'
            expected_reader_level['title'] = storyblok_reader_level['name']
            expected_reader_level['level_up_threshold'] = storyblok_reader_level['content']['level_up_threshold']

            for key in expected_reader_level.keys():
                if expected_reader_level[key] != content_map_reader_level[key]:
                    error_message.append(
                        'key:{0} value not consistent between expected and content map for reader level {1}' \
                            .format(key, expected_reader_level['title']))

            # verify unassigned readers under reader level
            storyblok_unassigned_readers = storyblok_reader_level['content']['unassigned_readers']
            storyblok_unassigned_reader_uuid_list = jmespath.search('[].reader', storyblok_unassigned_readers)
            unassigned_reader_latest_eca_response = content_repo_service.get_latest_ecas(
                storyblok_unassigned_reader_uuid_list)
            unassigned_reader_latest_eca_list = unassigned_reader_latest_eca_response.json()

            reader_eca_group_response = \
                content_repo_service.get_content_groups_by_param(ContentRepoContentType.TypeReader.value,
                                                                 ContentRepoGroupType.TypeECAGroup.value,
                                                                 content_map_reader_level['contentId'],
                                                                 content_map_reader_level['contentRevision'],
                                                                 content_map_reader_level['schemaVersion'])
            content_group_reader_metadata_list = reader_eca_group_response.json()[0]['childRefs']

            error_message.extend(StoryBlokUtils. \
                                 verify_reader_vocab_content_groups(storyblok_unassigned_reader_uuid_list,
                                                                    unassigned_reader_latest_eca_list,
                                                                    content_group_reader_metadata_list,
                                                                    StoryblokReleaseProgram.READERS))

        return error_message

    # verify reader's unassigned/assigned/ef readers and vocabs between stoyblok and content service
    @staticmethod
    def verify_reader_vocab_content_groups(storyblok_reader_vocab_uuid_list, latest_eca_list,
                                           content_group_childref_list, type):
        error_message = []

        if len(storyblok_reader_vocab_uuid_list) != len(content_group_childref_list):
            error_message.append('storyblok reader/vocab list size not same as content repo childref list size!')
            return error_message

        for i in range(len(storyblok_reader_vocab_uuid_list)):
            reader_vocab_uuid = storyblok_reader_vocab_uuid_list[i]
            latest_eca = jmespath.search("[?contentId == '{0}'] | [0]".format(reader_vocab_uuid),
                                         latest_eca_list)
            actual_content_group_childref = content_group_childref_list[i]

            expected_content_group_childref = {}
            expected_content_group_childref['contentId'] = latest_eca['contentId']
            expected_content_group_childref['contentRevision'] = latest_eca['contentRevision']
            expected_content_group_childref['schemaVersion'] = latest_eca['schemaVersion']
            expected_content_group_childref['nodeType'] = "ECA"

            expected_reader_metadata = {}
            if type == StoryblokReleaseProgram.VOCABULARIES:
                expected_content_group_childref['type'] = "Vocabulary"
                expected_reader_metadata['word'] = latest_eca['data']['content']['word']
            else:
                expected_content_group_childref['type'] = "Reader"
                expected_reader_metadata['title'] = latest_eca['data']['content']['title']
                expected_reader_metadata['cover_image'] = latest_eca['data']['content']['cover_thumbnail']
                if 'cover_thumbnail2' in latest_eca['data']['content'].keys():
                    expected_reader_metadata['cover_image2'] = latest_eca['data']['content']['cover_thumbnail2']
                else:
                    expected_reader_metadata['cover_image2'] = None

                if 'cover_thumbnail3' in latest_eca['data']['content'].keys():
                    expected_reader_metadata['cover_image3'] = latest_eca['data']['content']['cover_thumbnail3']
                else:
                    expected_reader_metadata['cover_image3'] = None

                expected_reader_metadata['reader_provider'] = latest_eca['data']['content']['reader_provider']
            expected_content_group_childref['metadata'] = expected_reader_metadata

            for key in actual_content_group_childref.keys():
                if str(actual_content_group_childref[key]) != str(expected_content_group_childref[key]):
                    error_message.append('key:{0} value not consistent between expected and content repo for reader {1}' \
                                         .format(key, reader_vocab_uuid))
        return error_message

    @staticmethod
    def verify_reader_after_course_release(book_in_content_map, storyblok_reader_config_list,
                                           book_reader_content_group_list):
        error_message = []
        region_ach = book_in_content_map['regionAch']
        book_content_path = book_in_content_map['contentPath']
        course_source_name = book_content_path[:book_content_path.index('/')]
        content_repo_service = ContentRepoService()

        if len(storyblok_reader_config_list) != len(book_reader_content_group_list):
            error_message.append(
                'storyblok reader config list size not same as book\'s reader content group list size!')
            return error_message

        unit_content_path_list_in_content_map = jmespath.search('children[].contentPath', book_in_content_map)

        # reader config list have been sorted by full_slug, the order should be consistent with content group searched by book
        for i in range(len(storyblok_reader_config_list)):
            storyblok_reader_config = storyblok_reader_config_list[i]

            storyblok_correlation_path = storyblok_reader_config['content']['parent']['content']['correlation_path']
            storyblok_correlation_path = StoryBlokUtils.get_storyblok_correlation_path_wth_region(
                storyblok_correlation_path, course_source_name, region_ach)
            unit_in_content_map = jmespath.search(
                'children[?contentPath == \'{0}\'] | [0]'.format(storyblok_correlation_path),
                book_in_content_map)

            # for small star, it have unit 10, so the order can not guarantee the book_reader_content_group
            unit_content_id = unit_in_content_map['contentId']
            book_reader_content_group = jmespath.search(
                '[?parentRef.contentId == \'{0}\'] | [0]'.format(unit_content_id), book_reader_content_group_list)

            expected_content_group_parent_ref = {}
            expected_content_group_parent_ref['type'] = 'UNIT'
            expected_content_group_parent_ref['contentId'] = unit_content_id
            expected_content_group_parent_ref['contentRevision'] = unit_in_content_map['contentRevision']
            expected_content_group_parent_ref['schemaVersion'] = unit_in_content_map['schemaVersion']
            expected_content_group_parent_ref['contentIndex'] = \
                unit_content_path_list_in_content_map.index(storyblok_correlation_path) + 1

            actual_eca_group_parent_ref = book_reader_content_group['parentRef']

            # verify the eca group's parentRef
            diff_list = json_tools.diff(actual_eca_group_parent_ref, expected_content_group_parent_ref)
            if len(diff_list) != 0:
                error_message.append('eca_group parentref not as expected, diff:' + str(diff_list))

            # verfiy all the assigned readers and ef readers in storyblok consistent with content group
            storyblok_assigned_reader_uuid_list = jmespath.search('content.assigned_readers[].reader',
                                                                  storyblok_reader_config)
            ef_reader_uuid_list = jmespath.search('content.ef_readers[].reader', storyblok_reader_config)
            reader_uuid_list = storyblok_assigned_reader_uuid_list + ef_reader_uuid_list

            reader_latest_eca_list = content_repo_service.get_latest_ecas(reader_uuid_list).json()
            error_message.extend(
                StoryBlokUtils.verify_reader_vocab_content_groups(reader_uuid_list, reader_latest_eca_list,
                                                                  book_reader_content_group['childRefs'],
                                                                  StoryblokReleaseProgram.READERS))

            # check ef_reader's reader_provider is EF
            for ef_reader_uuid in ef_reader_uuid_list:
                ef_reader_in_content_group = jmespath.search('childRefs[?contentId == \'{0}\'] | [0]'
                                                             .format(ef_reader_uuid), book_reader_content_group)

                if ef_reader_in_content_group['metadata']['reader_provider'] != 'EF':
                    error_message.append('ef reader:{0} \'s reader_provider is not EF!')
        return error_message

    @staticmethod
    def verify_vocab_after_course_release(book_in_content_map, storyblok_vocab_config_list,
                                          book_vocab_content_group_list):
        error_message = []
        region_ach = book_in_content_map['regionAch']
        book_content_path = book_in_content_map['contentPath']
        course_source_name = book_content_path[:book_content_path.index('/')]
        content_repo_service = ContentRepoService()

        vocab_eca_group_list = jmespath.search('[?groupType==\'ECA_GROUP\']', book_vocab_content_group_list)
        vocab_asset_group_list = jmespath.search('[?groupType==\'ASSET_GROUP\']', book_vocab_content_group_list)

        if len(storyblok_vocab_config_list) != len(vocab_eca_group_list):
            error_message.append('storyblok vocab config list size not same as book\'s vocab eca group list size!')
            return error_message

        unit_content_path_list_in_content_map = jmespath.search('children[].contentPath', book_in_content_map)

        # vocab config list have been sorted by full_slug, the order should be consistent with content group searched by book
        for i in range(len(storyblok_vocab_config_list)):
            storyblok_vocab_config = storyblok_vocab_config_list[i]
            # vocab_eca_group = vocab_eca_group_list[i]
            # vocab_asset_group = vocab_asset_group_list[i]

            storyblok_correlation_path = storyblok_vocab_config['content']['parent']['content']['correlation_path']
            storyblok_correlation_path = StoryBlokUtils.get_storyblok_correlation_path_wth_region(
                storyblok_correlation_path, course_source_name, region_ach)
            unit_in_content_map = jmespath.search(
                'children[?contentPath == \'{0}\'] | [0]'.format(storyblok_correlation_path),
                book_in_content_map)
            unit_content_index = unit_content_path_list_in_content_map.index(storyblok_correlation_path) + 1

            vocab_eca_group = jmespath.search(
                '[? parentRef.contentIndex == `{0}`]| [0]'.format(unit_content_index), vocab_eca_group_list)
            vocab_asset_group = jmespath.search(
                '[? parentRef.contentIndex == `{0}`]| [0]'.format(unit_content_index), vocab_asset_group_list)

            expected_content_group_parent_ref = {}
            expected_content_group_parent_ref['type'] = 'UNIT'
            expected_content_group_parent_ref['contentId'] = unit_in_content_map['contentId']
            expected_content_group_parent_ref['contentRevision'] = unit_in_content_map['contentRevision']
            expected_content_group_parent_ref['schemaVersion'] = unit_in_content_map['schemaVersion']
            expected_content_group_parent_ref['contentIndex'] = unit_content_index

            actual_eca_group_parent_ref = vocab_eca_group['parentRef']

            # verify the eca group's parentRef
            diff_list = json_tools.diff(actual_eca_group_parent_ref, expected_content_group_parent_ref)
            if len(diff_list) != 0:
                error_message.append('eca_group parentref not as expected, diff:' + str(diff_list))

            actual_asset_group_parent_ref = vocab_asset_group['parentRef']
            # verify the asset group's parentRef
            diff_list = json_tools.diff(actual_asset_group_parent_ref, expected_content_group_parent_ref)
            if len(diff_list) != 0:
                error_message.append('asset_group parentref not as expected, diff:' + str(diff_list))

            # verfiy related vocabs in storyblok consistent with content group
            storyblok_vocab_uuid_list = jmespath.search('content.vocabularies[]', storyblok_vocab_config)

            vocab_latest_eca_list = content_repo_service.get_latest_ecas(storyblok_vocab_uuid_list).json()
            error_message.extend(StoryBlokUtils.verify_reader_vocab_content_groups(storyblok_vocab_uuid_list,
                                                                                   vocab_latest_eca_list,
                                                                                   vocab_eca_group['childRefs'],
                                                                                   StoryblokReleaseProgram.VOCABULARIES))

            expected_asset_list = jmespath.search('[].data.content.image',
                                                  vocab_latest_eca_list) + jmespath.search('[].data.content.audio',
                                                                                           vocab_latest_eca_list)
            for asset_dict in expected_asset_list:
                asset_dict['nodeType'] = 'ASSET'

            expected_asset_list = sorted(expected_asset_list, key=lambda k: k['url'])
            actual_asset_group_childrefs = sorted(vocab_asset_group['childRefs'], key=lambda k: k['url'])
            diff_list = json_tools.diff(actual_asset_group_childrefs, expected_asset_list)
            if len(diff_list) != 0:
                error_message.append('asset_group childref not as expected, diff:' + str(diff_list))

        return error_message

    @staticmethod
    def get_zip_file():
        zip_name = askopenfilename()
        if '.zip' not in zip_name:
            print("Not a zip file")
            exit()
        zip_file = zipfile.ZipFile(zip_name, 'r')
        return zip_file

    @staticmethod
    def convert_asset_name(asset_name):
        if len(asset_name.rsplit('.', 1)) == 2:
            asset_name = re.sub(r'\W', "-", asset_name.rsplit('.', 1)[0]).rstrip('-') + "." + asset_name.rsplit('.', 1)[
                1]
            new_asset_name = [""]
            for str in asset_name:
                if str != new_asset_name[-1] or str != '-':
                    new_asset_name.append(str)
            convert_name = ''.join(new_asset_name).lower()
            return convert_name
        return None

    @staticmethod
    def get_storyblok_correlation_path_wth_region(storyblok_correlation_path, course_source_name, region_ach):
        slash_index = storyblok_correlation_path.index('/')
        # correlation_path in storyblok is like "highflyers/book-7", need to add region into it to become: highflyers/cn-3/book-7
        # return storyblok_correlation_path[:slash_index] + '/' + region_ach + storyblok_correlation_path[slash_index:]
        return course_source_name + '/' + region_ach + storyblok_correlation_path[slash_index:]

    def convert_n_bytes(self, n, b):
        bits = b * 8
        return (n + 2 ** (bits - 1)) % 2 ** bits - 2 ** (bits - 1)

    def convert_4_bytes(self, n):
        return self.convert_n_bytes(n, 4)

    # inorder to generate hashcode value same as JAVA's string.hashcode()
    @classmethod
    def getHashCode(cls, s):
        h = 0
        n = len(s)
        for i, c in enumerate(s):
            h = h + ord(c) * 31 ** (n - 1 - i)
        return cls().convert_4_bytes(h)

    @staticmethod
    def get_folder_slug(folder_name):
        pattern = re.compile(r'[A-Za-z0-9]+', re.I)

        folder_slug = pattern.search(folder_name)
        # for chinese name folder, feature will convert it into hashcode value
        if folder_slug is None:
            return StoryBlokUtils.getHashCode(folder_name)
        else:
            return folder_slug.group().lower()

    @staticmethod
    def verify_mt_activity_with_storyblok_question(mt_activity, storyblok_question):
        mt_tpl_data = mt_activity['tpl_data']
        mt_tpl_data = json.loads(mt_tpl_data)

        error_message = []
        if str(storyblok_question['slug']) != str(mt_activity['id']):
            error_message.append('question slug not expected as:' + mt_activity['id'])

        storyblok_question_content = storyblok_question['content']

        if storyblok_question_content['component'] != 'mt_activity':
            error_message.append('question component should be mt_activity for question: {0}'.format(mt_activity['id']))

        for key in mt_tpl_data.keys():
            error_message.extend(StoryBlokUtils.verify_mt_fields_with_storyblok_question(key, mt_tpl_data[key],
                                                                                         storyblok_question_content[
                                                                                             key]))
        return error_message

    @staticmethod
    def verify_mt_fields_with_storyblok_question(key, mt_acvitity_value, storyblok_question_value):
        error_message = []

        '''for those keys, in storyblok, it have been configured as plugin, so, the actual value is storyblok_question_value[key]
        e.g.
            "body": {
                "body": {
                    "mappings": []
                },
                "plugin": "body"
            }
        '''
        if key in ('body', 'tags', 'stimulus', 'questions', 'resources', 'explanation'):
            # only when storyblok value is dict and there's plugin field exist, then do this logic, otherwise, it's normal field
            if isinstance(storyblok_question_value, dict) and 'plugin' in storyblok_question_value.keys():
                if key != 'questions':
                    if storyblok_question_value['plugin'] != key:
                        error_message.append('{0}\'s plugin value not expected as {1}'.format(key, key))
                else:
                    # questions field's plugin value is mt-questions
                    if storyblok_question_value['plugin'] != 'mt-questions':
                        error_message.append('{0}\'s plugin value not expected as mt-questions'.format(key))

                storyblok_question_value = storyblok_question_value[key]

        if key == 'url':
            error_message.extend(
                StoryBlokUtils.verify_mt_resource_with_storyblok(mt_acvitity_value, storyblok_question_value))
        else:
            if isinstance(mt_acvitity_value, list):
                # if it's empty list for mt, then it should be empty list for storyblok too
                if len(mt_acvitity_value) != len(storyblok_question_value):
                    error_message.append('length for key:{0} not consistent between mt and storyblok'.format(key))
                else:
                    for i in range(len(mt_acvitity_value)):
                        mt_list_item = mt_acvitity_value[i]
                        storyblok_list_item = storyblok_question_value[i]
                        error_message.extend(StoryBlokUtils.verify_mt_fields_with_storyblok_question(key, mt_list_item,
                                                                                                     storyblok_list_item))

            elif isinstance(mt_acvitity_value, dict):
                for key in mt_acvitity_value.keys():
                    mt_field_value = mt_acvitity_value[key]
                    # print("verify key:" + key)
                    storyblok_field_value = storyblok_question_value[key]
                    error_message.extend(StoryBlokUtils.verify_mt_fields_with_storyblok_question(key, mt_field_value,
                                                                                                 storyblok_field_value))
            else:
                if str(mt_acvitity_value) != str(storyblok_question_value):
                    error_message.append(
                        " key:" + key + "'s value in mt_activity not equal to the value in storyblok question." \
                                        "The aem value is:" + str(mt_acvitity_value) \
                        + ", but the value in storyblok question is:" + str(storyblok_question_value))

        return error_message

    @staticmethod
    def verify_mt_resource_with_storyblok(mt_resource_url, storyblok_resource_url):
        print("start verify url:" + mt_resource_url)
        error_message = []
        mt_resource_response = StoryBlokImportService.get_mt_resource(mt_resource_url)
        assert_that(mt_resource_response.status_code == 200,
                    'mt resource response status is not 200:' + mt_resource_url)
        mt_resource_sha1 = CommonUtils.get_asset_sha1(mt_resource_response.content)

        storyblok_resource_response = StoryBlokImportService.get_storyblok_resource(storyblok_resource_url)
        assert_that(storyblok_resource_response.status_code == 200,
                    'storyblok resource response status is {0}, not 200 for url: {1}'
                    .format(storyblok_resource_response.status_code, storyblok_resource_url))
        storyblok_resource_sha1 = CommonUtils.get_asset_sha1(storyblok_resource_response.content)

        if mt_resource_sha1 != storyblok_resource_sha1:
            error_message.append(
                "resource in MT not consistent with Storyblok, MT resource url is:{0}, storyblok resource url is:{1}, sha1 is:{2}".format(
                    mt_resource_url, storyblok_resource_url, storyblok_resource_sha1))
        print("enf of verify url:" + mt_resource_url)
        return error_message