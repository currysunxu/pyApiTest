from hamcrest import assert_that
from ptest.decorator import TestClass, Test, BeforeClass

from E1_API_Automation.Business.EVC.EVCContentService import EVCContentService, get_material_ids
from E1_API_Automation.Settings import EVC_CONTENT_ENVIRONMENT
from E1_API_Automation.Test_Data.EVCData import ContentMaterialType


def get_testcase_params(topic_type: ContentMaterialType.FM_Kids_PL):
    yield from get_material_ids(topic_type)


@TestClass(run_mode="parallel")
class EVCContentTest:

    @BeforeClass()
    def before_method(self):
        self.evc_content_service = EVCContentService(EVC_CONTENT_ENVIRONMENT)

    @Test(tags="qa, stg, live")
    def test_get_kids_pl_topics(self):
        topic_list = self.evc_content_service.get_topic_ids(ContentMaterialType.FM_Kids_PL)
        assert_that(len(topic_list))

    @Test(tags="qa, stg, live", data_provider=get_testcase_params(ContentMaterialType.FM_Kids_PL))
    def test_kids_pl_material(self, topic_id):
        response = self.evc_content_service.get_lesson_by_id(topic_id)
        assert_that(response)
