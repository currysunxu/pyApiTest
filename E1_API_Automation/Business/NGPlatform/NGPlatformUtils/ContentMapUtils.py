from E1_API_Automation.Business.NGPlatform.ContentMapNodeEntity import ContentMapNodeEntity
from E1_API_Automation.Business.NGPlatform.NGPlatformUtils.LearningEnum import ContentMapNodeType
import uuid
import random
import datetime


class ContentMapUtils:
    @staticmethod
    def construct_content_map_tree_entity():
        course_content_id = uuid.uuid1()
        time_format = '%Y-%m-%d'
        date_value = datetime.datetime.now().strftime(time_format)
        random_value = random.randint(1, 1000)
        course_content_revision = date_value + "-" + str(random_value)
        content_map_course = ContentMapNodeEntity(ContentMapNodeType.Course, course_content_id, course_content_revision)

