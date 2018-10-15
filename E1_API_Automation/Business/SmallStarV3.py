from E1_API_Automation.Business.SchoolCourse import CourseBook
from ..Lib.Moutai import Moutai, Token


class SmallStarService():
    def __init__(self, host):
        self.host = host
        self.mou_tai = Moutai(host=self.host, token=Token("X-BA-TOKEN", "Token"))

    def login(self, user_name, password):
        user_info = {
            "UserName": user_name,
            "Password": password,
            "DeviceId": "",
            "DeviceType": "",
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
            "Amount": amount
        }
        return self.mou_tai.post("/api/v2/BinaryData/Synchronize/", json=body)

    def synchronize_course_node(self, book_key, course_plan_key, product_code, upserts_only=True, amount=123):
        body = {
            "BookKey": book_key,
            "CoursePlanKey": course_plan_key,
            "ProductCode": product_code,
            "UpsertsOnly": upserts_only,
            "Amount": amount
        }
        return self.mou_tai.post("/api/v2/CourseNode/Synchronize/", json=body)

    def synchronize_activity(self, book_key, course_plan_key, product_code, upserts_only=True, amount=123):
        body = {
            "BookKey": book_key,
            "CoursePlanKey": course_plan_key,
            "ProductCode": product_code,
            "UpsertsOnly": upserts_only,
            "Amount": amount
        }
        return self.mou_tai.post("/api/v2/Activity/Synchronize/", json=body)

    def synchronize_digital_article(self, book_key, course_plan_key, product_code, upserts_only=True, amount=123):
        body = {
            "BookKey": book_key,
            "CoursePlanKey": course_plan_key,
            "ProductCode": product_code,
            "UpsertsOnly": upserts_only,
            "Amount": amount
        }
        return self.mou_tai.post("/api/v2/DigitalArticle/Synchronize/", json=body)

    def synchronize_small_star_student_activity_answer(self, book_key, course_plan_key, product_code, upserts_only=True,
                                                       amount=123):
        body = {
            "BookKey": book_key,
            "CoursePlanKey": course_plan_key,
            "ProductCode": product_code,
            "UpsertsOnly": upserts_only,
            "Amount": amount
        }
        return self.mou_tai.post("/api/v2/HistoricalActivityAnswer/SynchronizeAll/", json=body)

    def get_binary_storage_by_resource_id(self, resource_id):
        return self.mou_tai.get("/api/v2/BinaryData/ResourceId/{}".format(resource_id))

    def get_small_star_unlock_course_keys(self, book_key):
        return self.mou_tai.get("/api/v2/CourseUnlock/{}".format(book_key))

    def submit_small_star_student_answers(self, product_key, group_id, book_key, lesson_key, course_plan_key, user_id):
        book_content = CourseBook(self.mou_tai, product_key, book_key, course_plan_key)
        body = self.generate_activity_submit_content_by_lesson_key(book_content, lesson_key)
        body["StudentId"] = user_id
        body["GroupId"] = group_id
        return self.mou_tai.post("/api/v2/ActivityAnswer/SmallStar/", json=body)

    def generate_activity_submit_content_by_lesson_key(self, book_content, lesson_key, activity_index=0, pass_activity=True):
        activities = book_content.get_child_nodes_by_parent_key(lesson_key)
        return book_content.generate_activity_submit_answer(activities[activity_index], pass_activity)

    def fetch_content_update_summary(self, body):
        return self.mou_tai.post("/api/v2/Content/", json=body)

    def batch_resource(self, resource_id):
        return self.mou_tai.get("/Resource/Batch/{}".format(resource_id))

    def batch_resources(self, resource_id_list: list):
        parameter = ','.join(resource_id_list)
        return self.mou_tai.get("/Resource/Batch/{}".format(parameter))
