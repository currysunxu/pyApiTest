from datetime import datetime
from datetime import timedelta

import jmespath
from hamcrest import assert_that
from ptest.decorator import TestClass, Test

from E1_API_Automation.Business.NGPlatform.ContentMapQueryEntity import ContentMapQueryEntity
from E1_API_Automation.Business.NGPlatform.ContentMapService import ContentMapService
from E1_API_Automation.Business.NGPlatform.ContentRepoService import ContentRepoService
from E1_API_Automation.Business.NGPlatform.NGPlatformUtils.ContentRepoEnum import ContentRepoContentType, \
    ContentRepoGroupType
from E1_API_Automation.Business.StoryBlok.StoryBlokReleaseService import StoryBlokReleaseService
from E1_API_Automation.Business.StoryBlok.StoryBlokService import StoryBlokService
from E1_API_Automation.Business.StoryBlok.StoryBlokUtils.StoryBlokUtils import StoryBlokUtils
from E1_API_Automation.Business.Utils.EnvUtils import EnvUtils
from E1_API_Automation.Settings import CONTENT_REPO_ENVIRONMENT, CONTENT_MAP_ENVIRONMENT, STORYBLOK_RELEASE_ENVIRONMENT
from E1_API_Automation.Test_Data.StoryblokData import StoryBlokData, StoryblokReleaseProgram


@TestClass()
class StoryBlokTestCases:

    # test reader release, also support incremental release verification
    @Test(tags="qa")
    def test_reader_release(self):
        expected_release_revision = self.test_storyblok_release(StoryblokReleaseProgram.READERS)

        # verify reader tree and reader level content groups
        story_blok_service = StoryBlokService(StoryBlokData.StoryBlokService['host'])
        get_storyblok_reader_level_response = story_blok_service.get_storyblok_reader_levels()
        assert_that(get_storyblok_reader_level_response.status_code == 200)
        storyblok_reader_level_list = jmespath.search('stories', get_storyblok_reader_level_response.json())

        content_map_service = ContentMapService(CONTENT_MAP_ENVIRONMENT)
        content_map_entity = ContentMapQueryEntity('READERS_10')
        reader_tree_response = content_map_service.post_content_map_query_tree(content_map_entity)
        assert_that(reader_tree_response.status_code == 200)
        content_map_reader_level_list = reader_tree_response.json()['children']

        # verify content revision should be all same
        assert_that(reader_tree_response.json()['contentRevision'] == expected_release_revision,
                    'content revision in reader tree root not as expected! release revision should be:' + expected_release_revision)

        content_revision_list = jmespath.search('[].contentRevision', content_map_reader_level_list)
        content_revision_list = list(set(content_revision_list))

        assert_that(len(content_revision_list) == 1, 'reader tree children should have same content revision')
        assert_that(content_revision_list[0] == expected_release_revision,
                    'content revision in reader children list not as expected! release revision should be:' + expected_release_revision)

        error_message = StoryBlokUtils.verify_storyblok_reader_levels(storyblok_reader_level_list,
                                                                      content_map_reader_level_list)
        assert_that(len(error_message) == 0, error_message)

    # test vocab release, also support incremental release verification
    @Test(tags="qa")
    def test_vocab_release(self):
        self.test_storyblok_release(StoryblokReleaseProgram.VOCABULARIES)

    # test storyblok reader/vocab release
    def test_storyblok_release(self, release_type):
        storyblok_release_service = StoryBlokReleaseService(STORYBLOK_RELEASE_ENVIRONMENT)

        date_time_format = '%Y-%m-%d %H:%M:%S'
        # storyblok release support incremental release, so, need to find out increased stories from last completed release time
        release_history_response = storyblok_release_service.get_storyblok_release_history(release_type.value)
        release_history_list = jmespath.search('releaseHistory[?status==\'COMPLETED\']',
                                               release_history_response.json())
        expected_release_revision = release_history_list[0]['releaseRevision']
        if len(release_history_list) >= 2:
            published_at_start_date = release_history_list[1]['maxContentTime']
            if published_at_start_date is None:
                published_at_start_date = '1970-01-01'
            else:
                # published_at will start from 1 seconds later than the last maxContentTime
                published_at_start_date = datetime.strptime(published_at_start_date, date_time_format)
                published_at_start_date = (published_at_start_date + timedelta(seconds=1)).strftime(date_time_format)

            published_at_end_date = release_history_list[0]['startAt']
        else:
            published_at_start_date = ''
            published_at_end_date = ''
        storyblok_service = StoryBlokService(StoryBlokData.StoryBlokService['host'])
        page_number = 1
        page_size = 100
        total_count = 0
        while True:
            if release_type == StoryblokReleaseProgram.READERS:
                get_storyblok_stories_response = storyblok_service.get_storyblok_readers(page_number, page_size,
                                                                                         published_at_start_date,
                                                                                         published_at_end_date)
            elif release_type == StoryblokReleaseProgram.VOCABULARIES:
                get_storyblok_stories_response = storyblok_service.get_storyblok_vocabs(page_number, page_size,
                                                                                        published_at_start_date,
                                                                                        published_at_end_date)
            else:
                get_storyblok_stories_response = storyblok_service.get_storyblok_mocktest(page_number, page_size,
                                                                                          published_at_start_date,
                                                                                          published_at_end_date)
            assert_that(get_storyblok_stories_response.status_code == 200)
            content_id_list = jmespath.search('stories[].uuid', get_storyblok_stories_response.json())
            storyblok_story_list = jmespath.search('stories', get_storyblok_stories_response.json())
            if len(storyblok_story_list) == 0:
                if page_number == 1:
                    assert_that(False, 'There\'s no reader/vocab story to be verified!')
                break

            content_repo_service = ContentRepoService(CONTENT_REPO_ENVIRONMENT)
            if release_type == StoryblokReleaseProgram.MOCKTEST:
                latest_content_response = content_repo_service.get_latest_activities(content_id_list)
            else:
                latest_content_response = content_repo_service.get_latest_ecas(content_id_list)
            assert_that(latest_content_response.status_code == 200)
            error_message = StoryBlokUtils.verify_storyblok_stories(storyblok_story_list,
                                                                    latest_content_response.json(),
                                                                    expected_release_revision, release_type)
            assert_that(len(error_message) == 0, error_message)
            total_count = total_count + len(storyblok_story_list)
            # if content fetched list less than page_size, then end the loop
            if len(storyblok_story_list) < page_size:
                break
            else:
                page_number = page_number + 1
        print('-------------verified total number is:{0}-----------------'.format(str(total_count)))
        return expected_release_revision

    '''
    There's two ways of verification, one is to verify the latest course history, it may be any course. e.g. test_latest_course_release()
    The other way is to specify the release type, run this specific course release directly, e.g. test_highflyers_release()
    '''
    # test the latest course release
    @Test()
    def test_latest_course_release(self):
        storyblok_release_service = StoryBlokReleaseService(STORYBLOK_RELEASE_ENVIRONMENT)

        # fetch out all the release history
        release_history_response = storyblok_release_service.get_storyblok_release_history()
        # filter out the latest course release history, it can be any course
        release_history_list = jmespath.search('releaseHistory[?status==\'COMPLETED\' && program != \'{0}\' && program != \'{1}\' && program != \'{2}\']'
                                               .format(StoryblokReleaseProgram.READERS.value, StoryblokReleaseProgram.VOCABULARIES.value, StoryblokReleaseProgram.MOCKTEST.value),
                                               release_history_response.json())
        release_scope = release_history_list[0]['scope']
        region_achs = release_history_list[0]['regionAchs']
        release_program = release_history_list[0]['program']
        self.test_course_release_by_scope([release_scope], region_achs, release_program)

    @Test()
    def test_highflyers_release(self):
        if EnvUtils.is_env_qa():
            release_type = StoryblokReleaseProgram.HIGHFLYERS_35
        else:
            # for staging and live, the storyblok release program haven't been changed, so, still using the old name
            release_type = StoryblokReleaseProgram.HIGHFLYERS

        self.test_course_release_by_type(release_type)

    @Test()
    def test_smallstars_30_release(self):
        self.test_course_release_by_type(StoryblokReleaseProgram.SMALLSTARS_30)

    @Test()
    def test_smallstars_35_release(self):
        self.test_course_release_by_type(StoryblokReleaseProgram.SMALLSTARS_35)

    # test the course release by type
    def test_course_release_by_type(self, release_type):
        storyblok_release_service = StoryBlokReleaseService(STORYBLOK_RELEASE_ENVIRONMENT)

        release_history_response = storyblok_release_service.get_storyblok_release_history(
            release_type.value)
        release_history_list = jmespath.search('releaseHistory[?status==\'COMPLETED\']',
                                               release_history_response.json())
        release_scope = release_history_list[0]['scope']
        region_achs = release_history_list[0]['regionAchs']
        release_program = release_history_list[0]['program']
        self.test_course_release_by_scope([release_scope], region_achs, release_program)

    # test course release by release scope
    @Test(data_provider=(
    ["book-c", "book-d", "book-e", "book-f", "book-g", "book-h", "book-i", "book-j"], ["cn-3", "cn-3-144"], 'Highflyers35'))
    def test_course_release_by_scope(self, release_scopes, region_achs, release_program):
        course_config_path = StoryBlokData.StoryBlokProgram[release_program]['course-config-path']
        course_source_name = StoryBlokData.StoryBlokProgram[release_program]['source-name']
        target_program = StoryBlokData.StoryBlokProgram[release_program]['target-name']

        for release_scope in release_scopes:
            for region_ach in region_achs:
                print('release_program:{0}, release_scope:{1}, region_ach:{2}'.format(release_program, release_scope, region_ach))
                storyblok_service = StoryBlokService(StoryBlokData.StoryBlokService['host'])
                get_book_story_response = storyblok_service.get_storyblok_book_by_scope(course_config_path, release_scope)
                assert_that(get_book_story_response.status_code == 200)
                storyblok_book_story = jmespath.search('stories|[0]', get_book_story_response.json())
                storyblok_correlation_path = storyblok_book_story['content']['correlation_path']
                # correlation_path in storyblok is like "highflyers/book-7", need to add region into it to become: highflyers/cn-3/book-7
                storyblok_correlation_path_with_region = StoryBlokUtils.get_storyblok_correlation_path_wth_region(
                    storyblok_correlation_path, course_source_name, region_ach)
                storyblok_default_reader_level = storyblok_book_story['content']['default_reader_level']

                content_map_service = ContentMapService(CONTENT_MAP_ENVIRONMENT)
                content_map_entity = ContentMapQueryEntity(target_program, region_ach=region_ach)
                course_map_tree_response = content_map_service.post_content_map_query_tree(content_map_entity)
                book_in_content_map = jmespath.search(
                    'children[?contentPath == \'{0}\'] | [0]'.format(storyblok_correlation_path_with_region),
                    course_map_tree_response.json())

                assert_that(book_in_content_map['default_reader_level'] == storyblok_default_reader_level,
                            'default_reader_level value not consistent between content map and storyblok for contentPath:'
                            + storyblok_correlation_path)

                content_repo_service = ContentRepoService(CONTENT_REPO_ENVIRONMENT)

                book_reader_content_groups = \
                    content_repo_service.get_content_groups_by_param(ContentRepoContentType.TypeReader.value,
                                                                     ContentRepoGroupType.TypeECAGroup.value,
                                                                     book_in_content_map['contentId'],
                                                                     book_in_content_map['contentRevision'],
                                                                     book_in_content_map['schemaVersion']).json()

                # verify reader in this book
                storyblok_reader_configs_response = storyblok_service.get_storyblok_reader_configs(course_config_path, release_scope).json()
                storyblok_reader_configs_with_order = sorted(storyblok_reader_configs_response['stories'],
                                                             key=lambda k: k['full_slug'])
                error_message = StoryBlokUtils.verify_reader_after_course_release(book_in_content_map,
                                                                                  storyblok_reader_configs_with_order,
                                                                                  book_reader_content_groups)
                assert_that(len(error_message) == 0, error_message)

                # verify vocab in this book
                book_vocab_content_groups = \
                    content_repo_service.get_content_groups_by_param(ContentRepoContentType.TypeVocab.value,
                                                                     None,
                                                                     book_in_content_map['contentId'],
                                                                     book_in_content_map['contentRevision'],
                                                                     book_in_content_map['schemaVersion']).json()

                storyblok_vocab_configs_response = storyblok_service.get_storyblok_vocab_configs(course_config_path, release_scope).json()
                storyblok_vocab_configs_with_order = sorted(storyblok_vocab_configs_response['stories'],
                                                            key=lambda k: k['full_slug'])
                error_message = StoryBlokUtils.verify_vocab_after_course_release(book_in_content_map,
                                                                                 storyblok_vocab_configs_with_order,
                                                                                 book_vocab_content_groups)
                assert_that(len(error_message) == 0, error_message)

    @Test(tags="qa")
    def test_mocktest_release(self):
        self.test_storyblok_release(StoryblokReleaseProgram.MOCKTEST)
