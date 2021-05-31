from typing import List
import requests

from E1_API_Automation.Business.BaseService import BaseService
from E1_API_Automation.Test_Data.EVCData import EVCContentMaterialType


class EVCContentService(BaseService):

    def get_topic_ids(self, topic_type) -> List[str]:
        request_url = self.host + "/services/api/evccontent/topiclist?topictype={0}".format(topic_type)
        response = requests.get(request_url)
        return response

    def get_lesson_by_id(self, content_id):
        request_url = self.host + "/services/api/evccontent/lesson?topicId={0}&lessontype={1}".format(content_id,
                                                                                                      EVCContentMaterialType.FM_Kids_PL)
        response = requests.get(request_url)
        return response
