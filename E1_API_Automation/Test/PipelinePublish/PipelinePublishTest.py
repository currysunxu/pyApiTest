import json
import os

import jmespath
import requests
from hamcrest import assert_that
from jsonschema import validate
from ptest.decorator import TestClass, Test

from E1_API_Automation.Business.NGPlatform.ContentBuilderService import ContentBuilderService
from E1_API_Automation.Business.NGPlatform.ContentMapQueryEntity import ContentMapQueryEntity
from E1_API_Automation.Business.NGPlatform.ContentMapService import ContentMapService
from E1_API_Automation.Business.NGPlatform.ContentRepoService import ContentRepoService
from E1_API_Automation.Business.NGPlatform.NGPlatformUtils.ContentRepoEnum import ContentRepoContentType, \
    ContentRepoGroupType
from E1_API_Automation.Business.PipelinePublish.AEMService import AEMService
from E1_API_Automation.Business.PipelinePublish.PipelinePublishUtils.PipelinePublishConstants import \
    PipelinePublishConstants
from E1_API_Automation.Business.PipelinePublish.PipelinePublishVerifyService import PipelinePublishVerifyService
from E1_API_Automation.Settings import CONTENT_MAP_ENVIRONMENT, CONTENT_BUILDER_ENVIRONMENT, CONTENT_REPO_ENVIRONMENT
from E1_API_Automation.Test_Data.PipelinePublishData import AEMData


@TestClass()
class PipelinePublishTestCases:
    '''
    This case is for the verification after PP release from AEM to content service. 
    It will verify the structure, detail homework/handout contents compared with AEM, 
    and also verify the content asset download, and calculate the asset's sha1 to compare with AEM
    
    source_aem_env: indicate the release source, choose with LIVE or STG
    course: indicate the course name in AEM, currently it's: highflyers
    release_book: indicate the book you want to release from AEM
    region_ach: indicate the region_ach you will verify in content service
    '''

    # @Test(data_provider=[("LIVE", "Highflyers35",
    #                       ["book-2", "book-3", "book-4", "book-5", "book-6", "book-7", "book-8"], "cn-3")])
    @Test(data_provider=[("LIVE", "Smallstars35",
                          ["book-1"], "cn-3")])
    # @Test(data_provider=[("LIVE", "Highflyers35",
    #                       ["book-5"], "cn-3-144")])
    def test_pp_release(self, source_aem_env, release_program, release_book_list, region_ach):
        for release_book in release_book_list:
            print('-------------------------Start verify book: {0}'.format(release_book))
            release_as_program = None
            if 'release-as' in AEMData.CourseData[release_program].keys():
                release_as_program = AEMData.CourseData[release_program]['release-as']

            if release_as_program is not None:
                release_course = AEMData.CourseData[release_as_program]['source-name']
            else:
                release_course = AEMData.CourseData[release_program]['source-name']

            book_content_path = '{0}/{1}/{2}'.format(release_course, region_ach, release_book)

            aem_service = AEMService(AEMData.AEMHost[source_aem_env])
            source_course = AEMData.CourseData[release_program]['source-name']
            aem_book_response = aem_service.get_aem_book(source_course, release_book)

            content_map_service = ContentMapService(CONTENT_MAP_ENVIRONMENT)

            if release_as_program is not None:
                content_map_course = AEMData.CourseData[release_as_program]['target-name']
            else:
                content_map_course = AEMData.CourseData[release_program]['target-name']
            content_map_entity = ContentMapQueryEntity(content_map_course, region_ach=region_ach)
            content_map_tree_response = content_map_service.post_content_map_query_tree(content_map_entity)
            assert_that(content_map_tree_response.status_code == 200)
            content_map_book_tree = jmespath.search('children[? contentPath == \'{0}\']|[0]'.format(book_content_path),
                                                    content_map_tree_response.json())
            book_content_id = content_map_book_tree['contentId']

            content_builder_service = ContentBuilderService(CONTENT_BUILDER_ENVIRONMENT)
            content_builder_processed_status_response = content_builder_service.get_release_by_status()
            release_url_list = jmespath.search('[*].url', content_builder_processed_status_response.json())
            latest_book_release_url = jmespath.search('[? contains(@, \'{0}\')]|[0]'.format(book_content_id),
                                                      release_url_list)
            revision_start_index = latest_book_release_url.rfind('=')
            release_revision = latest_book_release_url[revision_start_index + 1:]

            pipeline_publish_service = PipelinePublishVerifyService()
            error_message = pipeline_publish_service.verify_content_after_release(aem_book_response.json(),
                                                                                  content_map_book_tree,
                                                                                  release_revision)
            assert_that(len(error_message) == 0, error_message)
            print('-------------------------End of verify book: {0}'.format(release_book))

        # verify activities templates after release for highflyer
        if release_program == 'Highflyers35':
            self.test_book_activity_templates(release_program, region_ach, release_book_list)

    '''
    validate all the book's activities after release, to check if the structure align with the templates
    '''
    @Test(data_provider=[
        ("Highflyers35", "cn-3", ["book-1", "book-2", "book-3", "book-4", "book-5", "book-6", "book-7", "book-8"])])
    def test_book_activity_templates(self, release_program, region_ach, book_list):
        # get the pre-defined templates
        path = 'E1_API_Automation/Test_Data/ActivityTemplate/'
        dir_files = os.listdir(path)

        activity_template_dict = {}
        for template_file in dir_files:
            if template_file != '__init__.py':
                with open(path + template_file, 'r') as f:
                    activity_template = json.load(f)
                    template_name = template_file[:template_file.rfind('.')]
                    activity_template_dict[template_name] = activity_template

        content_map_service = ContentMapService(CONTENT_MAP_ENVIRONMENT)
        content_repo_service = ContentRepoService(CONTENT_REPO_ENVIRONMENT)
        for book in book_list:
            print('-------------------------Start verify activities for book: {0}'.format(book))
            source_course = AEMData.CourseData[release_program]['source-name']
            book_content_path = '{0}/{1}/{2}'.format(source_course, region_ach, book)

            content_map_course = AEMData.CourseData[release_program]['target-name']
            content_map_entity = ContentMapQueryEntity(content_map_course, region_ach=region_ach)
            content_map_tree_response = content_map_service.post_content_map_query_tree(content_map_entity)
            assert_that(content_map_tree_response.status_code == 200)
            content_map_book_tree = jmespath.search('children[? contentPath == \'{0}\']|[0]'.format(book_content_path),
                                                    content_map_tree_response.json())
            book_content_id = content_map_book_tree['contentId']
            book_content_revision = content_map_book_tree['contentRevision']
            book_content_schema_version = content_map_book_tree['schemaVersion']

            activity_group_content_groups = \
                content_repo_service.get_content_groups_by_param(ContentRepoContentType.TypeHomework.value,
                                                                 ContentRepoGroupType.TypeActivityGroup.value,
                                                                 book_content_id,
                                                                 book_content_revision,
                                                                 book_content_schema_version).json()

            content_list = jmespath.search(
                '[].childRefs[].{contentId: contentId, contentRevision: contentRevision, schemaVersion: schemaVersion}',
                activity_group_content_groups)

            activity_list = content_repo_service.get_activities(content_list).json()

            non_defined_templates = []
            for activity in activity_list:
                activity_type = activity['data']['Type']
                if activity_type in activity_template_dict.keys():
                    print("----start verify activity:{0}, activity_type is: {1}".format(activity['contentId'],
                                                                                        activity_type))
                    activity_template = activity_template_dict[activity_type]
                    validate(activity, schema=activity_template)
                else:
                    non_defined_templates.append(activity_type)

            assert_that(len(non_defined_templates) == 0,
                        "There's non defined templates:{0}  for book:{1}".format(str(non_defined_templates), book))
