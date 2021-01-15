import json
from datetime import datetime

import jmespath
from hamcrest import assert_that
from ptest.decorator import TestClass, Test

from E1_API_Automation.Business.StoryBlok.StoryBlokImportService import StoryBlokImportService
from E1_API_Automation.Business.StoryBlok.StoryBlokService import StoryBlokService
from E1_API_Automation.Business.StoryBlok.StoryBlokUtils.StoryBlokUtils import StoryBlokUtils
from E1_API_Automation.Settings import STORYBLOK_IMPORT_ENVIRONMENT
from E1_API_Automation.Test_Data.StoryblokData import StoryBlokData, MockTestData


@TestClass()
class MTActivityImportTest:

    @Test()
    def test_mt_activity_import(self):
        mt_activity_table_name = '21cnjy.activity_for_content'
        storyblok_import_service = StoryBlokImportService(STORYBLOK_IMPORT_ENVIRONMENT)
        activity_import_status_response = storyblok_import_service.get_storyblok_import_status()
        activity_import_status_list = jmespath.search('[?status==\'COMPLETE\']', activity_import_status_response.json())
        if 'specified_uuid' in activity_import_status_list[0].keys():
            # this is the import by uuid history
            valid_activity_list = StoryBlokImportService.get_activity_by_uuid_from_mt_db(mt_activity_table_name,
                                                                                         activity_import_status_list[0]['specified_uuid'])
        else:
            version = activity_import_status_list[0]['min_version']
            valid_activity_list = StoryBlokImportService.get_valid_activities_from_mt_db(mt_activity_table_name,
                                                                                         version)

        storyblok_service = StoryBlokService(StoryBlokData.StoryBlokService['host'], 'MT')
        # logic to get all storyblok questions
        # page_number = 1
        # page_size = 100
        # total_count = 0
        # storyblok_question_list=[]
        # while True:
        #     print('-------------start get storyblok question for page:{0}, start time is:{1}-----------------'
        #           .format(page_number, datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')))
        #     get_storyblok_stories_response = storyblok_service.get_storyblok_questions(page_number, page_size)
        #     assert_that(get_storyblok_stories_response.status_code == 200)
        #     storyblok_story_list = jmespath.search('stories', get_storyblok_stories_response.json())
        #     if len(storyblok_story_list) == 0:
        #         if page_number == 1:
        #             assert_that(False, 'There\'s no reader/vocab story to be verified!')
        #         break
        #     storyblok_question_list.extend(storyblok_story_list)
        #
        #     print('-------------end of get storyblok question for page:{0}, end time is:{1}-----------------'
        #           .format(page_number, datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')))
        #
        #     total_count = total_count + len(storyblok_story_list)
        #     # if content fetched list less than page_size, then end the loop
        #     if len(storyblok_story_list) < page_size:
        #         break
        #     else:
        #         page_number = page_number + 1
        #
        # print('-------------get question total number is:{0}-----------------'.format(str(total_count)))
        count = 0
        for mt_activity in valid_activity_list:
            mt_activity_id = mt_activity['id']
            mt_tpl_data = mt_activity['tpl_data']
            mt_tpl_data = json.loads(mt_tpl_data)
            print('-----------------------Start verify mt_activity:' + str(mt_activity_id))

            # storyblok_question = jmespath.search('[?name == \'{0}\']|[0]'.format(mt_activity_id),
            #                                      storyblok_question_list)

            version = list(mt_tpl_data['tags']['version'].values())[0]
            book = list(mt_tpl_data['tags']['book'].values())[0]
            base_type = list(mt_tpl_data['tags']['baseType'].values())[0]

            storyblok_question_full_slug = 'mt/questions/{0}/{1}/{2}/{3}' \
                .format(StoryBlokUtils.get_folder_slug(version),
                        StoryBlokUtils.get_folder_slug(book),
                        StoryBlokUtils.get_folder_slug(base_type),
                        mt_activity_id)
            storyblok_question_response = storyblok_service.get_storyblok_question_by_full_slug(storyblok_question_full_slug)
            assert_that(storyblok_question_response.status_code == 200)
            storyblok_question = storyblok_question_response.json()['story']
            error_message = StoryBlokUtils.verify_mt_activity_with_storyblok_question(mt_activity, storyblok_question)
            assert_that(len(error_message) == 0, error_message)
            count = count + 1
            print('-----------------------End of verify mt_activity:' + str(mt_activity_id))
        print('----Verified total activity number is:' + str(count))
