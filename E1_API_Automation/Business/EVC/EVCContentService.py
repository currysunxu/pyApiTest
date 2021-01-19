from typing import List
import requests

from E1_API_Automation.Test_Data.EVCData import EVCContentMaterialType


class EVCContentService:
    def __init__(self, host):
        self.host = host

    @staticmethod
    def get_topic_ids(host_url, topic_type) -> List[str]:
        request_url = host_url + "/services/api/evccontent/topiclist?topictype={0}".format(topic_type)
        response = requests.get(request_url)
        return response

    def get_lesson_by_id(self, content_id):
        request_url = self.host + "/services/api/evccontent/lesson?topicId={0}&lessontype={1}".format(content_id,
                                                                                                      EVCContentMaterialType.FM_Kids_PL)
        response = requests.get(request_url)
        return response
