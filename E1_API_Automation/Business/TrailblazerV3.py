from ..Lib.Moutai import Moutai, Token
import jmespath
from ..Lib.ResetGPGradeTool import ResetGPGradeTool


class TrailbazerService():
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
        return self.mou_tai.set_request_context("post", user_info, "/api/v2/Authentication/TBV3/")

    def get_student_profile(self):
        return self.mou_tai.get("/api/v2/TBV3/")

    def query_school_info(self):
        body ={
            "Key": "aa17e532-4585-449a-8e1f-b30deef07e27",
            "Region": 0,
            "Name": "Name String",
            "Code": "Code String",
            "CityName": "City Name String",
            "ContactPhoneNumber": "Contact Phone Number String",
            "ContactEmail": "Contact Email String",
            "Latitude": 1.5,
            "Longitude": 1.5,
            "CountryISO3Code": "Country IS O3 Code String",
            "DistrictName": "District Name String",
            "OmniId": "Omni Id String",
            "BusinessUnit": "Business Unit String"
            }
        return self.mou_tai.post("/api/v2/SchoolInfo/", json=body)

    def get_all_books(self):
        return self.mou_tai.get("/api/v2/AllBook")

    def course_node_synchronize(self, book_key, course_play_key,amount_num):
        body ={
            {"BookKey": book_key,
             "CoursePlanKey": course_play_key,
             "ProductCode": "TBV3",
             "LastSynchronizedStamp": None,
             "LastSynchronizedKey": None,
             "UpsertsOnly": False,
             "Amount": amount_num
             }
        }
        return self.mou_tai.post("/api/v2/CourseNode/Synchronize", json=body)

    def course_unlock(self,key):
        return self.mou_tai.get("/api/v2/CourseUnlock/TB%s") % key

    def get_homework_motivation_task_info(self, key):
        return self.mou_tai.get("/api/v2/HomeworkMotivationTaskInfo/%s" % key)

    def query_motivation_reward_summary(self, scope_key):
        body ={
            "ScopeKey" : scope_key
        }
        return self.mou_tai.post("/api/v2/MotivationRewardSummary/", json = body
                                 )

    def query_motivation_point_audit(self, scope_key):
        body = {
            "ScopeKey": scope_key
        }
        return self.mou_tai.post("/api/v2/MotivationPointAudit", json=body
                                 )

    def progress_assessment__report_by_unit(self, unit_key):
        return self.mou_tai.get("/api/v2/ProgressAssessmentReport/ByUnit/%s" % unit_key)

    def acitivity_entity_web(self, list):
        return self.mou_tai.post("/api/v2/ActivityEntity/Web", json=list)

    def lesson_score_summary(self, lesson_key_list):
        return self.mou_tai.post("/api/v2/lessonScoreSummary", json=lesson_key_list)

    def homework_lesson_correction(self, course_key, correct_amount):
        body = {"CourseKey": course_key,
                "MistakeAmount": 27,
                "CorrectedAmount": correct_amount}

        return self.mou_tai.post("/api/v2/HomeworkLessonCorrection",json = body)

    def digital_interaction_info(self, book_key):
        return self.mou_tai.get("/DigitalInteractionInfo/ByBook/%s" % book_key)

    def sign_out(self):
        return self.mou_tai.delete(url="/api/v2/Token/")



