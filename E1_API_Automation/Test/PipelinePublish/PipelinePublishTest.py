import jmespath
from hamcrest import assert_that
from ptest.decorator import TestClass, Test

from E1_API_Automation.Business.NGPlatform.ContentBuilderService import ContentBuilderService
from E1_API_Automation.Business.NGPlatform.ContentMapQueryEntity import ContentMapQueryEntity
from E1_API_Automation.Business.NGPlatform.ContentMapService import ContentMapService
from E1_API_Automation.Business.PipelinePublish.AEMService import AEMService
from E1_API_Automation.Business.PipelinePublish.PipelinePublishUtils.PipelinePublishUtils import PipelinePublishUtils
from E1_API_Automation.Business.PipelinePublish.PipelinePublishVerifyService import PipelinePublishVerifyService
from E1_API_Automation.Settings import CONTENT_MAP_ENVIRONMENT, CONTENT_BUILDER_ENVIRONMENT
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
    @Test(data_provider=[("LIVE", "highflyers", ["book-5", "book-6", "book-7", "book-8"], "cn-3")])
    def test_pp_release(self, source_aem_env, course, release_book_list, region_ach):
        for release_book in release_book_list:
            print('-------------------------Start verify book: {0}'.format(release_book))
            book_content_path = '{0}/{1}/{2}'.format(course, region_ach, release_book)

            aem_service = AEMService(AEMData.AEMHost[source_aem_env])
            aem_book_response = aem_service.get_aem_book(course, release_book)

            content_map_service = ContentMapService(CONTENT_MAP_ENVIRONMENT)

            content_map_course = PipelinePublishUtils.get_content_map_course(course)
            content_map_entity = ContentMapQueryEntity(content_map_course, region_ach=region_ach)
            content_map_tree_response = content_map_service.post_content_map_query_tree(content_map_entity)
            assert_that(content_map_tree_response.status_code == 200)
            content_map_book_tree = jmespath.search('children[? contentPath == \'{0}\']|[0]'.format(book_content_path),
                                                    content_map_tree_response.json())
            book_content_id = content_map_book_tree['contentId']

            content_builder_service = ContentBuilderService(CONTENT_BUILDER_ENVIRONMENT)
            content_builder_processed_status_response = content_builder_service.get_release_by_status()
            release_url_list = jmespath.search('[*].url', content_builder_processed_status_response.json())
            latest_book_release_url = jmespath.search('[? contains(@, \'{0}\')]|[-1]'.format(book_content_id),
                                                      release_url_list)
            revision_start_index = latest_book_release_url.rfind('=')
            release_revision = latest_book_release_url[revision_start_index + 1:]

            pipeline_publish_service = PipelinePublishVerifyService()
            error_message = pipeline_publish_service.verify_content_after_release(aem_book_response.json(),
                                                                                  content_map_book_tree,
                                                                                  release_revision)
            assert_that(len(error_message) == 0, error_message)
            print('-------------------------End of verify book: {0}'.format(release_book))
