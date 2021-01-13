from ptest.decorator import TestClass, Test, BeforeClass

from E1_API_Automation.Business.EVC.EVCContentService import EVCContentService
from E1_API_Automation.Settings import EVC_CONTENT_ENVIRONMENT
from E1_API_Automation.Test_Data.EVCData import EVCLayoutCode, EVCContentMaterialType


def get_testcase_params(topic_type: EVCLayoutCode.FM_Kids_PL):
    yield from EVCContentService.get_topic_ids(EVC_CONTENT_ENVIRONMENT, topic_type)


@TestClass(run_mode="parallel")
class EVCContentTest:

    @BeforeClass()
    def before_method(self):
        self.evc_content_service = EVCContentService(EVC_CONTENT_ENVIRONMENT)

    @Test(tags="qa, stg, live")
    def test_get_kids_pl_topics(self):
        topic_list = self.evc_content_service.get_topics_by_topic_type(EVC_CONTENT_ENVIRONMENT,
                                                                       EVCContentMaterialType.FM_Kids_PL)
        self.evc_content_service.check_topic_details(topic_list)

    @Test(tags="qa, stg, live", data_provider=get_testcase_params(EVCLayoutCode.FM_Kids_PL))
    def test_kids_pl_material(self, topic_id):
        response = self.evc_content_service.get_lesson_by_id(topic_id)
        self.evc_content_service.check_topic_structure(response)
