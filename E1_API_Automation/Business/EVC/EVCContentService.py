import requests

from typing import List
from hamcrest import assert_that, equal_to, contains_string, not_none

from E1_API_Automation.Lib.HamcrestExister import exist
from E1_API_Automation.Test_Data.EVCData import TOPIC_AMOUNT, EVCContentMaterialType


class EVCContentService:
    def __init__(self, host):
        self.host = host

    @staticmethod
    def get_topic_ids(host_url, topic_type) -> List[str]:
        request_url = host_url + "/services/api/evccontent/topiclist?topictype={0}".format(topic_type)
        response = requests.get(request_url)
        assert_that(response.status_code, equal_to(200))

        return list(response.json().keys())

    def get_lesson_by_id(self, content_id):
        request_url = self.host + "/services/api/evccontent/lesson?topicId={0}&lessontype={1}".format(content_id,
                                                                                                      EVCContentMaterialType.FM_Kids_PL)
        response = requests.get(request_url)
        assert_that(response.status_code, equal_to(200))
        assert_that(len(response.json()), equal_to(1))
        return response.json()[0]

    def get_topics_by_topic_type(self, host_url, topic_type):
        request_url = host_url + "/services/api/evccontent/topiclist?topictype={0}".format(topic_type)
        response = requests.get(request_url)
        assert_that(response.status_code, equal_to(200))

        return response.json()

    def check_topic_details(self, topic_list):
        for item in topic_list:
            assert_that(item, not_none())
            assert_that(topic_list[item], not_none())

    def check_topic_structure(self, response):
        assert_that(response, exist("TopicId"))
        assert_that(response, exist("Title"))
        assert_that(response, exist("Description"))
        assert_that(response, exist("HtmlMaterialFilePath"))
        assert_that(response, exist("Metatag"))
        assert_that(response, exist("AudioFile"))
