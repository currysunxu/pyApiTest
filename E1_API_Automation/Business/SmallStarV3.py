import uuid
import arrow

from E1_API_Automation.Business.BaseService import BaseService
from E1_API_Automation.Business.SchoolCourse import CourseBook
from ..Lib.Moutai import Moutai, Token


class SmallStarService(BaseService):
    def __init__(self):
        super().__init__("Environment", {}, Token("X-BA-TOKEN", "Token"))

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

    def get_student_privacy_policy_content_for_mobile(self, culture_code):
        return self.mou_tai.get(
            "/api/v2/PrivacyPolicy/StudentPrivacyPolicyAgreementForMobile/?product=3&cultureCode={}&platformType=ios".format(culture_code))

    def get_student_privacy_policy_content_newapi(self, culture_code):
        return self.mou_tai.get(
            "/api/v2/PrivacyPolicy/PrivacyPolicyDocuments/?Product=3&CultureCode={}".format(culture_code))

    def save_student_privacy_policy_content(self, privacy_document_id):
        body = {
            "privacyDocumentId": privacy_document_id,
            "product": 3
        }
        return self.mou_tai.post("/api/v2/PrivacyPolicy/StudentPrivacyPolicyAgreement/", json=body)

    def sign_out(self):
        return self.mou_tai.delete(url="/api/v2/Token/")

    def synchronize_binary_data(self, book_key, course_plan_key, upserts_only=True, amount=1230000,
                                last_synchronized_key=None, last_Synchronized_Stamp=None):
        body = {
            "BookKey": book_key,
            "CoursePlanKey": course_plan_key,
            #"ProductCode": product_code,
            "UpsertsOnly": upserts_only,
            "Amount": amount
        }
        if last_synchronized_key and last_synchronized_key is not None:
            body['LastSynchronizedStamp'] = last_Synchronized_Stamp
            body['LastSynchronizeKey'] = last_synchronized_key
        return self.mou_tai.post("/api/v2/BinaryData/Synchronize/", json=body)

    def synchronize_course_node(self, book_key, course_plan_key,  upserts_only=True, amount=1230000,
                                last_synchronized_key=None, last_Synchronized_Stamp=None):
        body = {
            "BookKey": book_key,
            "CoursePlanKey": course_plan_key,
            #"ProductCode": product_code,
            "UpsertsOnly": upserts_only,
            "Amount": amount
        }
        if last_synchronized_key and last_synchronized_key is not None:
            body['LastSynchronizedStamp'] = last_Synchronized_Stamp
            body['LastSynchronizeKey'] = last_synchronized_key
        return self.mou_tai.post("/api/v2/CourseNode/Synchronize/", json=body)

    def synchronize_activity(self, book_key, course_plan_key, upserts_only=True, amount=1230000,
                             last_synchronized_key=None, last_Synchronized_Stamp=None):
        body = {
            "BookKey": book_key,
            "CoursePlanKey": course_plan_key,
            #"ProductCode": product_code,
            "UpsertsOnly": upserts_only,
            "Amount": amount
        }
        if last_synchronized_key and last_synchronized_key is not None:
            body['LastSynchronizedStamp'] = last_Synchronized_Stamp
            body['LastSynchronizeKey'] = last_synchronized_key
        return self.mou_tai.post("/api/v2/Activity/Synchronize/", json=body)

    def synchronize_digital_article(self, book_key, course_plan_key, upserts_only=True, amount=1230000,
                                    last_synchronized_key=None, last_Synchronized_Stamp=None):
        body = {
            "BookKey": book_key,
            "CoursePlanKey": course_plan_key,
            #"ProductCode": product_code,
            "UpsertsOnly": upserts_only,
            "Amount": amount
        }
        if last_synchronized_key and last_synchronized_key is not None:
            body['LastSynchronizedStamp'] = last_Synchronized_Stamp
            body['LastSynchronizeKey'] = last_synchronized_key
        return self.mou_tai.post("/api/v2/DigitalArticle/Synchronize/", json=body)

    def synchronize_small_star_student_unit_quiz_answer(self, book_key, course_plan_key, upserts_only=True,
                                                       amount=12300000, last_Synchronized_Stamp=None, last_synchronized_key=None):

        body = {
            "BookKey": book_key,
            "CoursePlanKey": course_plan_key,
            "UpsertsOnly": upserts_only,
            "Amount": amount
        }
        if last_synchronized_key and last_synchronized_key is not None:
            body['LastSynchronizedStamp'] = last_Synchronized_Stamp
            body['LastSynchronizeKey'] = last_synchronized_key
        return self.mou_tai.post("/api/v2/HistoricalUnitQuizAnswer/SynchronizeAll", json=body)

    def synchronize_small_star_student_activity_answer(self, book_key, course_plan_key, upserts_only=True,
                                                       amount=12300000, last_Synchronized_Stamp=None, last_synchronized_key=None):
        body = {
            "BookKey": book_key,
            "CoursePlanKey": course_plan_key,
            "UpsertsOnly": upserts_only,
            "Amount": amount
        }

        if last_synchronized_key and last_synchronized_key is not None:
            body['LastSynchronizedStamp'] = last_Synchronized_Stamp
            body['LastSynchronizeKey'] = last_synchronized_key
        return self.mou_tai.post("/api/v2/HistoricalActivityAnswer/SynchronizeAll/", json=body)

    def synchronize_small_star_student_activity_answer_newapi(self, book_key, course_plan_key, upserts_only=True,
                                                              amount=1230000, last_Synchronized_Stamp=None, last_synchronized_key=None):
        body = {
            "BookKey": book_key,
            "CoursePlanKey": course_plan_key,
            "UpsertsOnly": upserts_only,
            "Amount": amount
        }

        if last_synchronized_key and last_synchronized_key is not None:
            body['LastSynchronizedStamp'] = last_Synchronized_Stamp
            body['LastSynchronizeKey'] = last_synchronized_key
        return self.mou_tai.post("/api/v2/HistoricalActivityAnswer/SynchronizeBestOnly/", json=body)

    def get_binary_storage_by_resource_id(self, resource_id):
        return self.mou_tai.get("/api/v2/BinaryData/ResourceId/{}".format(resource_id))

    def get_small_star_unlock_course_keys(self, book_key):
        return self.mou_tai.get("/api/v2/CourseUnlock/SmallStar/{}".format(book_key))

    def submit_small_star_student_answers(self, product_key, group_id, book_key, lesson_key, course_plan_key, user_id, pass_activity=True):
        book_content = CourseBook(self.mou_tai, product_key, book_key, course_plan_key)
        body, submit_activity_key = self.generate_activity_submit_content_by_lesson_key(book_content, lesson_key, pass_activity=pass_activity)
        body["StudentId"] = user_id
        body["GroupId"] = group_id
        return self.mou_tai.post("/api/v2/ActivityAnswer", json=body), submit_activity_key

    def submit_small_star_student_answers_newapi(self, product_key, group_id, book_key, lesson_key, course_plan_key, user_id, pass_activity=True):
        book_content = CourseBook(self.mou_tai, product_key, book_key, course_plan_key)
        body, submit_activity_key = self.generate_activity_submit_content_by_lesson_key(book_content, lesson_key, pass_activity=pass_activity)
        body["StudentId"] = user_id
        body["GroupId"] = group_id
        return self.mou_tai.post("/api/v2/ActivityAnswer/SmallStar/", json=body), submit_activity_key

    def submit_small_star_unit_quiz_answers(self, product_key, group_id, book_key, lesson_key, course_plan_key,
                                            user_id, pass_activity=True):
        book_content = CourseBook(self.mou_tai, product_key, book_key, course_plan_key)
        body, submit_activity_key = self.generate_activity_submit_content_by_lesson_key(book_content, lesson_key,
                                                                                        pass_activity=pass_activity)
        body["StudentId"] = user_id
        body["GroupId"] = group_id
        body["BatchDateTime"] = arrow.utcnow().format('YYYY-MM-DDTHH:mm:ssZZ')
        body["BatchId"] = str(uuid.uuid1())
        return self.mou_tai.post("/api/v2/UnitQuizAnswer/SmallStar/", json=body), submit_activity_key

    def generate_activity_submit_content_by_lesson_key(self, book_content, lesson_key, pass_activity, activity_index=0):
        activities = book_content.get_child_nodes_by_parent_key(lesson_key)
        return book_content.generate_activity_submit_answer(activities[activity_index], pass_activity), activities[activity_index]['ActivityKeys']

    def fetch_content_update_summary(self, body):
        return self.mou_tai.post("/api/v2/Content/", json=body)

    def batch_resource(self, resource_id):
        return self.mou_tai.get("/Resource/Batch/{}".format(resource_id))

    def batch_resources(self, resource_id_list: list):
        parameter = ','.join(resource_id_list)
        return self.mou_tai.get("/Resource/Batch/{}".format(parameter))
