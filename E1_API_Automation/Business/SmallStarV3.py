from ..Lib.Moutai import Moutai, Token
import jmespath
from ..Lib.ResetGPGradeTool import ResetGPGradeTool


class SmallStarService():
    def __init__(self, host):
        self.host = host
        self.mou_tai = Moutai(host=self.host, token=Token("X-BA-TOKEN", "Token"))

    def login(self, user_name, password):
        user_info = {
            "UserName": user_name,  # "jenkin0528tb",
            "Password": password,  # "12345",
            "DeviceId":"",
            "DeviceType":"",
            "Platform": 0
        }
        return self.mou_tai.set_request_context("post", user_info, "/api/v2/Authentication/SS/")

    def get_student_profile(self):
        return self.mou_tai.get("/api/v2/StudentProfile/SS/")

    def sign_out(self):
        return self.mou_tai.delete(url="/api/v2/Token/")

    def synchronize_binary_data(self, book_key, course_plan_key, product_code, upserts_only=True, amount=123):
        body = {
            "BookKey": book_key,
            "CoursePlanKey": course_plan_key,
            "ProductCode": product_code,
            "UpsertsOnly": upserts_only,
            "Amount" : amount
        }
        return self.mou_tai.post("/api/v2/BinaryData/Synchronize/", json=body)


    def synchronize_course_node(self, book_key, course_plan_key, product_code, upserts_only=True, amount=123):
        body = {
            "BookKey": book_key,
            "CoursePlanKey": course_plan_key,
            "ProductCode": product_code,
            "UpsertsOnly": upserts_only,
            "Amount" : amount
        }
        return self.mou_tai.post("/api/v2/CourseNode/Synchronize/", json=body)

    def synchronize_activity(self, book_key, course_plan_key, product_code, upserts_only=True, amount=123):
        body = {
            "BookKey": book_key,
            "CoursePlanKey": course_plan_key,
            "ProductCode": product_code,
            "UpsertsOnly": upserts_only,
            "Amount" : amount
        }
        return self.mou_tai.post("/api/v2/Activity/Synchronize/", json=body)


    def synchronize_digital_article(self, book_key, course_plan_key, product_code, upserts_only=True, amount=123):
        body = {
            "BookKey": book_key,
            "CoursePlanKey": course_plan_key,
            "ProductCode": product_code,
            "UpsertsOnly": upserts_only,
            "Amount" : amount
        }
        return self.mou_tai.post("/api/v2/DigitalArticle/Synchronize/", json=body)


    def synchronize_small_star_student_activity_answer(self, book_key, course_plan_key, product_code, upserts_only=True, amount=123):
        body = {
            "BookKey": book_key,
            "CoursePlanKey": course_plan_key,
            "ProductCode": product_code,
            "UpsertsOnly": upserts_only,
            "Amount" : amount
        }
        return self.mou_tai.post("/api/v2/HistoricalActivityAnswer/SynchronizeAll/", json=body)

    def get_binary_storage_by_resource_id(self, resource_id):
        return self.mou_tai.get("/api/v2/BinaryData/ResourceId/{}".format(resource_id))

    def get_small_star_unlock_course_keys(self, book_key):
        return self.mou_tai.get("/api/v2/CourseUnlock/SmallStar/{}".format(book_key))

    def submit_small_star_student_answers(self, body):
        '''
        body format:
         {
        "ActivityCourseKey": "f1dddbcb-11ac-49c7-9e7a-167f8a53f0e7",
        "ActivityKey": "3f22da06-88bd-45ec-ad35-13ecdbbe31fa",
        "StudentId": "Student Id String",
        "GroupId": "Group Id String",
        "Answers": [
        {
            "Detail": { Any JSON },
            "Key": "0ee7b8a8-a2d7-4f6f-8631-e9833ca5522f",
            "QuestionKey": "4feec5d1-985b-44e5-98ab-651a768275e2",
            "TotalScore": 1.5,
            "Score": 1.5,
            "Attempts": 123,
            "TotalStar": 123,
            "Star": 123,
            "Duration": 123,
            "LocalStartStamp": "2018-08-24T02:38:21.318Z",
            "LocalEndStamp": "2018-08-24T02:38:21.318Z"
        },
        {
            "Detail": { Any JSON },
            "Key": "ac5741cb-da59-4b4a-a13a-ad3b7776a8e4",
            "QuestionKey": "c7cd3c74-489f-4ef9-95ed-16d0d565d47a",
            "TotalScore": 1.5,
            "Score": 1.5,
            "Attempts": 123,
            "TotalStar": 123,
            "Star": 123,
            "Duration": 123,
            "LocalStartStamp": "2018-08-24T02:38:21.318Z",
            "LocalEndStamp": "2018-08-24T02:38:21.318Z"
        }

    ]
}
        '''
        return self.mou_tai.post("/api/v2/ActivityAnswer/SmallStar/", json=body)

    def fetch_content_update_summary(self, body):
        return self.mou_tai.post("/api/v2/Content/", json=body)
