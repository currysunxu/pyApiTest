import jmespath
import json_tools

from E1_API_Automation.Business.NGPlatform.ContentRepoService import ContentRepoService
from E1_API_Automation.Business.NGPlatform.NGPlatformUtils.ContentRepoEnum import ContentRepoContentType, \
    ContentRepoGroupType
from E1_API_Automation.Business.Utils.EnvUtils import EnvUtils
from E1_API_Automation.Settings import CONTENT_REPO_ENVIRONMENT
from E1_API_Automation.Test_Data.StoryblokData import StoryBlokVersion, StoryblokReleaseProgram


class StoryBlokUtils:
    @staticmethod
    def get_storyblok_version_by_env():
        if EnvUtils.is_env_qa():
            return StoryBlokVersion.DRAFT.value
        else:
            return StoryBlokVersion.PUBLISHED.value

    @staticmethod
    def verify_storyblok_stories(storyblok_story_list, content_repo_eca_list, expected_release_revision):
        content_revision_list = jmespath.search('[].contentRevision', content_repo_eca_list)
        content_revision_list = list(set(content_revision_list))

        error_message = ''
        if len(content_revision_list) != 1:
            error_message = 'ecas in content repo should have same content revision!'
            return error_message

        if content_revision_list[0] != expected_release_revision:
            error_message = 'content revision not as expected! release revision should be:' + expected_release_revision
            return error_message

        if len(storyblok_story_list) != len(content_repo_eca_list):
            error_message = 'storyblok story list size not same as content repo eca list size!'
            return error_message

        for storyblok_story in storyblok_story_list:
            content_id = storyblok_story['uuid']
            content_repo_reader = jmespath.search('[?contentId == \'{0}\']|[0]'.format(content_id),
                                                  content_repo_eca_list)
            error_message = error_message + StoryBlokUtils.verify_storyblok_story_with_contentrepo(storyblok_story,
                                                                                                   content_repo_reader)
        return error_message

    @staticmethod
    def verify_storyblok_story_with_contentrepo(storyblok_story, content_repo_eca):
        error_message = ''
        print('start verify storyblok story:' + storyblok_story['name'])
        content_repo_eca_data = content_repo_eca['data']
        # content repo source field should be storyblok
        if content_repo_eca_data['source'] != 'storyblok':
            return 'reader/vocab eca field \'source\' in content-repo not equal to storyblok'

        for key in storyblok_story.keys():
            if key not in (
                    '_uid', '_editable', 'alternates', 'default_full_slug', 'sort_by_date', 'position', 'tag_list',
                    'is_startpage',
                    'meta_data', 'group_id', 'first_published_at', 'release_id', 'lang', 'path', 'translated_slugs',
                    'parent_id'):
                storyblock_value = storyblok_story[key]
                if key == 'uuid':
                    content_repo_value = content_repo_eca['contentId']
                elif key == 'id':
                    content_repo_value = content_repo_eca_data['originID']
                else:
                    content_repo_value = content_repo_eca_data[key]

                error_message = error_message + StoryBlokUtils. \
                    verify_storyblok_fields_with_contentrepo(key, storyblock_value, content_repo_value)
        if len(error_message) != 0:
            print(error_message)
        return error_message

    @staticmethod
    def verify_storyblok_fields_with_contentrepo(key, storyblock_value, content_repo_value):
        error_message = ''

        if key.endswith('image'):
            error_message = error_message + StoryBlokUtils.verify_content_repo_asset(True, storyblock_value,
                                                                                     content_repo_value)
        elif key.endswith('audio'):
            error_message = error_message + StoryBlokUtils.verify_content_repo_asset(False, storyblock_value,
                                                                                     content_repo_value)
        else:
            if isinstance(storyblock_value, list):
                for i in range(len(storyblock_value)):
                    storyblok_list_item = storyblock_value[i]
                    content_repo_list_item = content_repo_value[i]
                    error_message = error_message + StoryBlokUtils. \
                        verify_storyblok_fields_with_contentrepo(key, storyblok_list_item, content_repo_list_item)

            elif isinstance(storyblock_value, dict):
                for key in storyblock_value.keys():
                    if key not in (
                            '_uid', '_editable'):
                        storyblock_field_value = storyblock_value[key]
                        content_repo_field_value = content_repo_value[key]
                        error_message = error_message + StoryBlokUtils. \
                            verify_storyblok_fields_with_contentrepo(key, storyblock_field_value,
                                                                     content_repo_field_value)
            else:
                if str(storyblock_value) != str(content_repo_value):
                    error_message = error_message + " key:" + key + "'s value in storyblok not equal to the value in content-repo." \
                                                                    "The storyblok value is:" + str(
                        storyblock_value) \
                                    + ", but the value in content-repo is:" + str(content_repo_value)

        return error_message

    @staticmethod
    def verify_content_repo_asset(is_asset_image, storyblok_asset_dict, content_repo_asset_dict):
        error_message = ''

        if isinstance(storyblok_asset_dict, str):
            if len(storyblok_asset_dict) == 0 and len(content_repo_asset_dict) == 0:
                return ''
            elif len(storyblok_asset_dict) == 0 and len(content_repo_asset_dict) != 0:
                error_message = "asset section in content repo should be empty, is the asset image?" + str(
                    is_asset_image)
                return error_message

        storyblok_file_name = storyblok_asset_dict['filename']
        if storyblok_file_name is None or len(storyblok_file_name) == 0:
            expected_filed_list = ['sha1', 'size', 'mimeType', 'url']

            for key in content_repo_asset_dict.keys():
                if key not in expected_filed_list:
                    error_message = error_message + ' {0} is not a expected field in content repo asset section'.format(
                        key)

            if len(error_message) != 0:
                return error_message

            for key in expected_filed_list:
                if key == 'size':
                    expected_value = 0
                else:
                    expected_value = ''
                error_message = error_message + StoryBlokUtils.verify_content_repo_asset_field(key,
                                                                                               content_repo_asset_dict[
                                                                                                   key],
                                                                                               expected_value)
        else:
            expected_url = storyblok_file_name
            sha1_end_index = expected_url.rfind('/')
            sha1_start_index = expected_url.rfind('/', 0, sha1_end_index)
            expected_sha1 = expected_url[sha1_start_index + 1:sha1_end_index]

            compare_key = 'url'
            error_message = error_message + StoryBlokUtils.verify_content_repo_asset_field(compare_key,
                                                                                           content_repo_asset_dict[
                                                                                               compare_key],
                                                                                           expected_url)
            compare_key = 'sha1'
            error_message = error_message + StoryBlokUtils.verify_content_repo_asset_field(compare_key,
                                                                                           content_repo_asset_dict[
                                                                                               compare_key],
                                                                                           expected_sha1)

            # this value is set harcoded
            compare_key = 'size'
            error_message = error_message + StoryBlokUtils.verify_content_repo_asset_field(compare_key,
                                                                                           content_repo_asset_dict[
                                                                                               compare_key],
                                                                                           1024)
            if expected_url.endswith('.png'):
                expected_mime_type = 'image/png'
            elif expected_url.endswith('.mp3'):
                expected_mime_type = 'audio/mpeg'
            elif expected_url.endswith('.jpg'):
                expected_mime_type = 'image/jpeg'

            compare_key = 'mimeType'
            error_message = error_message + StoryBlokUtils.verify_content_repo_asset_field(compare_key,
                                                                                           content_repo_asset_dict[
                                                                                               compare_key],
                                                                                           expected_mime_type)

            if is_asset_image:
                image_size_end_index = sha1_start_index
                image_size_start_index = expected_url.rfind('/', 0, image_size_end_index)
                image_size = expected_url[image_size_start_index + 1:image_size_end_index]
                split_index = image_size.find('x')
                expected_width_value = image_size[:split_index]
                expected_height_value = image_size[split_index + 1:]

                compare_key = 'width'
                error_message = error_message + StoryBlokUtils.verify_content_repo_asset_field(compare_key,
                                                                                               content_repo_asset_dict[
                                                                                                   compare_key],
                                                                                               expected_width_value)

                compare_key = 'height'
                error_message = error_message + StoryBlokUtils.verify_content_repo_asset_field(compare_key,
                                                                                               content_repo_asset_dict[
                                                                                                   compare_key],
                                                                                               expected_height_value)
            else:
                # for audio, there's no width and height, but have duration field
                compare_key = 'duration'
                error_message = error_message + StoryBlokUtils.verify_content_repo_asset_field(compare_key,
                                                                                               content_repo_asset_dict[
                                                                                                   compare_key],
                                                                                               0)
        return error_message

    @staticmethod
    def verify_content_repo_asset_field(field_name, content_repo_value, expected_value):
        error_message = ''
        if str(content_repo_value) != str(expected_value):
            error_message = "asset field:" + field_name + "'s value in content repo not as expected." \
                                                          "The content_repo_value value is:" + str(content_repo_value) \
                            + ", but expected value is:" + str(expected_value)
        return error_message

    @staticmethod
    def verify_storyblok_reader_levels(storyblok_reader_level_list, content_map_reader_level_list):
        content_revision_list = jmespath.search('[].contentRevision', content_map_reader_level_list)
        content_revision_list = list(set(content_revision_list))

        content_repo_service = ContentRepoService(CONTENT_REPO_ENVIRONMENT)

        error_message = ''
        if len(content_revision_list) != 1:
            error_message = 'reader levels in content map should have same content revision!'
            return error_message

        if len(storyblok_reader_level_list) != len(content_map_reader_level_list):
            error_message = 'storyblok reader level list size not same as content map reader level list size!'
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
            expected_reader_level['code'] = storyblok_reader_level['content']['code']
            expected_reader_level['source'] = 'storyblok'
            expected_reader_level['title'] = storyblok_reader_level['name']
            expected_reader_level['level_up_threshold'] = storyblok_reader_level['content']['level_up_threshold']

            for key in expected_reader_level.keys():
                if expected_reader_level[key] != content_map_reader_level[key]:
                    error_message = error_message + 'key:{0} value not consistent between expected and content map for reader level {1}' \
                        .format(key, expected_reader_level['title'])

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

            error_message = error_message + StoryBlokUtils. \
                verify_reader_vocab_content_groups(storyblok_unassigned_reader_uuid_list,
                                                   unassigned_reader_latest_eca_list,
                                                   content_group_reader_metadata_list, StoryblokReleaseProgram.READERS)

        return error_message

    # verify reader's unassigned/assigned/ef readers and vocabs between stoyblok and content service
    @staticmethod
    def verify_reader_vocab_content_groups(storyblok_reader_vocab_uuid_list, latest_eca_list,
                                           content_group_childref_list, type):
        error_message = ''

        if len(storyblok_reader_vocab_uuid_list) != len(content_group_childref_list):
            error_message = 'storyblok reader/vocab list size not same as content repo childref list size!'
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
                expected_reader_metadata['cover_image'] = latest_eca['data']['content']['cover_image']
                expected_reader_metadata['reader_provider'] = latest_eca['data']['content']['reader_provider']
            expected_content_group_childref['metadata'] = expected_reader_metadata

            for key in actual_content_group_childref.keys():
                if str(actual_content_group_childref[key]) != str(expected_content_group_childref[key]):
                    error_message = error_message + 'key:{0} value not consistent between expected and content repo for reader {1}' \
                        .format(key, reader_vocab_uuid)
        return error_message

    @staticmethod
    def verify_reader_after_highflyers_release(book_in_content_map, storyblok_reader_config_list,
                                               book_reader_content_group_list):
        error_message = ''
        content_repo_service = ContentRepoService(CONTENT_REPO_ENVIRONMENT)

        if len(storyblok_reader_config_list) != len(book_reader_content_group_list):
            error_message = 'storyblok reader config list size not same as book\'s reader content group list size!'
            return error_message

        unit_content_path_list_in_content_map = jmespath.search('children[].contentPath', book_in_content_map)

        # reader config list have been sorted by full_slug, the order should be consistent with content group searched by book
        for i in range(len(storyblok_reader_config_list)):
            storyblok_reader_config = storyblok_reader_config_list[i]
            book_reader_content_group = book_reader_content_group_list[i]

            storyblok_correlation_path = storyblok_reader_config['content']['parent']['content']['correlation_path']
            unit_in_content_map = jmespath.search(
                'children[?contentPath == \'{0}\'] | [0]'.format(storyblok_correlation_path),
                book_in_content_map)

            expected_content_group_parent_ref = {}
            expected_content_group_parent_ref['type'] = 'UNIT'
            expected_content_group_parent_ref['contentId'] = unit_in_content_map['contentId']
            expected_content_group_parent_ref['contentRevision'] = unit_in_content_map['contentRevision']
            expected_content_group_parent_ref['schemaVersion'] = unit_in_content_map['schemaVersion']
            expected_content_group_parent_ref['contentIndex'] = \
                unit_content_path_list_in_content_map.index(storyblok_correlation_path) + 1

            actual_eca_group_parent_ref = book_reader_content_group['parentRef']

            # verify the eca group's parentRef
            diff_list = json_tools.diff(actual_eca_group_parent_ref, expected_content_group_parent_ref)
            if len(diff_list) != 0:
                error_message = error_message + 'eca_group parentref not as expected, diff:' + str(diff_list)


            # verfiy all the assigned readers and ef readers in storyblok consistent with content group
            storyblok_assigned_reader_uuid_list = jmespath.search('content.assigned_readers[].reader',
                                                                  storyblok_reader_config)
            ef_reader_uuid_list = jmespath.search('content.ef_readers[].reader', storyblok_reader_config)
            reader_uuid_list = storyblok_assigned_reader_uuid_list + ef_reader_uuid_list

            reader_latest_eca_list = content_repo_service.get_latest_ecas(reader_uuid_list).json()
            error_message = error_message + \
                            StoryBlokUtils.verify_reader_vocab_content_groups(reader_uuid_list, reader_latest_eca_list,
                                                                              book_reader_content_group['childRefs'],
                                                                              StoryblokReleaseProgram.READERS)

            # check ef_reader's reader_provider is EF
            for ef_reader_uuid in ef_reader_uuid_list:
                ef_reader_in_content_group = jmespath.search('childRefs[?contentId == \'{0}\'] | [0]'
                                                             .format(ef_reader_uuid), book_reader_content_group)

                if ef_reader_in_content_group['metadata']['reader_provider'] != 'EF':
                    error_message = error_message + 'ef reader:{0} \'s reader_provider is not EF!'
        return error_message

    @staticmethod
    def verify_vocab_after_highflyers_release(book_in_content_map, storyblok_vocab_config_list,
                                              book_vocab_content_group_list):
        error_message = ''
        content_repo_service = ContentRepoService(CONTENT_REPO_ENVIRONMENT)

        vocab_eca_group_list = jmespath.search('[?groupType==\'ECA_GROUP\']', book_vocab_content_group_list)
        vocab_asset_group_list = jmespath.search('[?groupType==\'ASSET_GROUP\']', book_vocab_content_group_list)

        if len(storyblok_vocab_config_list) != len(vocab_eca_group_list):
            error_message = 'storyblok vocab config list size not same as book\'s vocab eca group list size!'
            return error_message

        unit_content_path_list_in_content_map = jmespath.search('children[].contentPath', book_in_content_map)

        # vocab config list have been sorted by full_slug, the order should be consistent with content group searched by book
        for i in range(len(storyblok_vocab_config_list)):
            storyblok_vocab_config = storyblok_vocab_config_list[i]
            vocab_eca_group = vocab_eca_group_list[i]
            vocab_asset_group = vocab_asset_group_list[i]

            storyblok_correlation_path = storyblok_vocab_config['content']['parent']['content']['correlation_path']
            unit_in_content_map = jmespath.search(
                'children[?contentPath == \'{0}\'] | [0]'.format(storyblok_correlation_path),
                book_in_content_map)

            expected_content_group_parent_ref = {}
            expected_content_group_parent_ref['type'] = 'UNIT'
            expected_content_group_parent_ref['contentId'] = unit_in_content_map['contentId']
            expected_content_group_parent_ref['contentRevision'] = unit_in_content_map['contentRevision']
            expected_content_group_parent_ref['schemaVersion'] = unit_in_content_map['schemaVersion']
            expected_content_group_parent_ref['contentIndex'] = \
                unit_content_path_list_in_content_map.index(storyblok_correlation_path) + 1

            actual_eca_group_parent_ref = vocab_eca_group['parentRef']

            # verify the eca group's parentRef
            diff_list = json_tools.diff(actual_eca_group_parent_ref, expected_content_group_parent_ref)
            if len(diff_list) != 0:
                error_message = error_message + 'eca_group parentref not as expected, diff:' + str(diff_list)

            actual_asset_group_parent_ref = vocab_asset_group['parentRef']
            # verify the asset group's parentRef
            diff_list = json_tools.diff(actual_asset_group_parent_ref, expected_content_group_parent_ref)
            if len(diff_list) != 0:
                error_message = error_message + 'asset_group parentref not as expected, diff:' + str(diff_list)

            # verfiy related vocabs in storyblok consistent with content group
            storyblok_vocab_uuid_list = jmespath.search('content.vocabularies[]', storyblok_vocab_config)

            vocab_latest_eca_list = content_repo_service.get_latest_ecas(storyblok_vocab_uuid_list).json()
            error_message = error_message + \
                            StoryBlokUtils.verify_reader_vocab_content_groups(storyblok_vocab_uuid_list,
                                                                              vocab_latest_eca_list,
                                                                              vocab_eca_group['childRefs'],
                                                                              StoryblokReleaseProgram.VOCABULARIES)

            expected_asset_list = jmespath.search('[].data.content.image',
                                                  vocab_latest_eca_list) + jmespath.search('[].data.content.audio',
                                                                                           vocab_latest_eca_list)
            for asset_dict in expected_asset_list:
                asset_dict['nodeType'] = 'ASSET'

            expected_asset_list = sorted(expected_asset_list, key=lambda k: k['url'])
            actual_asset_group_childrefs = sorted(vocab_asset_group['childRefs'], key=lambda k: k['url'])
            diff_list = json_tools.diff(actual_asset_group_childrefs, expected_asset_list)
            if len(diff_list) != 0:
                error_message = error_message + 'asset_group childref not as expected, diff:' + str(diff_list)

        return error_message
