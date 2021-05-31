from hamcrest import assert_that, equal_to, not_none, is_not
from ptest.decorator import TestClass, Test, BeforeClass

from E1_API_Automation.Business.EVC.EVCContentService import EVCContentService
from E1_API_Automation.Lib.HamcrestExister import exist
from E1_API_Automation.Test_Data.EVCData import EVCLayoutCode, EVCContentMaterialType


def get_testcase_params(topic_type: EVCLayoutCode.Kids_PL):
    yield from list(EVCContentService.get_topic_ids(topic_type).json().keys())[0:10]


@TestClass(run_mode="parallel")
class EVCContentTest:

    @BeforeClass()
    def before_method(self):
        self.evc_content_service = EVCContentService()

    @Test(tags="stg, live")
    def test_get_kids_pl_topics(self):
        response = self.evc_content_service.get_topic_ids(EVCContentMaterialType.FM_Kids_PL)

        # check response status is 200 and returned topic list is not empty
        assert_that(response.status_code, equal_to(200))
        topic_list = response.json()
        assert_that(len(topic_list), is_not(0))

        # check each topic has id and value
        for item in topic_list:
            assert_that(item, not_none())
            assert_that(topic_list[item], not_none())

    @Test(tags="stg, live", data_provider=get_testcase_params(EVCLayoutCode.Kids_PL))
    def test_kids_pl_material(self, topic_id):
        response = self.evc_content_service.get_lesson_by_id(topic_id)

        # check response status is 200, and only one material returns
        assert_that(response.status_code, equal_to(200))
        assert_that(len(response.json()), equal_to(1))

        # check material structure is correct
        material_info = response.json()[0]
        assert_that(material_info, exist("TopicId"))
        assert_that(material_info, exist("Title"))
        assert_that(material_info, exist("Description"))
        assert_that(material_info, exist("HtmlMaterialFilePath"))
        assert_that(material_info, exist("Metatag"))
        assert_that(material_info, exist("AudioFile"))
