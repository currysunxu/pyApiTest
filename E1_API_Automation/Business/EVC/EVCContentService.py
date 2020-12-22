from typing import List

import requests

from E1_API_Automation.Lib.Moutai import Moutai
from E1_API_Automation.Settings import EVC_CONTENT_ENVIRONMENT


def get_material_ids(material_type) -> List[str]:
    response = requests.get(EVC_CONTENT_ENVIRONMENT + "/services/api/evccontent/topiclist", params={"topictype": material_type})

    if response.status_code != 200:
        raise Exception(
            "Failed to get material ids, status code: %s, response content: %s" % (response.status_code, response.content.decode("utf-8")))

    return list(response.json().keys())


class EVCContentService:
    def __init__(self, host):
        self.host = host
        self.mou_tai = Moutai(host=self.host)

    def get_topic_ids(self, topic_type) -> List[str]:
        response = self.mou_tai.get("/services/api/evccontent/topiclist?topictype={0}".format(topic_type))
        if response.status_code != 200:
            raise Exception(
                "Failed to get topic ids, status code: %s, response content: %s" % (
                    response.status_code, response.content.decode("utf-8")))

        return list(response.json().keys())

    def get_lesson_by_id(self, content_id):
        response = self.mou_tai.get(
            "/services/api/evccontent/lesson?topicId={0}&lessontype={1}".format(content_id, 'Kids_PL'))

        if response.status_code != 200:
            raise Exception(
                "Failed to get material info, status code: %s, response content: %s" % (
                    response.status_code, response.content.decode("utf-8")))

        return response.json()
