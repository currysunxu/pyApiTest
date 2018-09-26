from E1_API_Automation.Business.SchoolCourse import CourseBook
from E1_API_Automation.Business.template.create_acitivty import Activity
from ..Lib.Moutai import Moutai, Token
import jmespath
import arrow
from functools import reduce


class TrailbazerService:
    def __init__(self, host, user_name, password):
        self.host = host
        self.mou_tai = Moutai(host=self.host, token=Token("X-BA-TOKEN", "Token"))
        self.login(user_name, password)
        self.active_book = None
        self.course_plan_key = None
        self.user_id = None
        self.group_id = None
        self.get_student_info()
        self.book_contents = CourseBook(self.mou_tai, "TBV3", self.active_book, self.course_plan_key)

    def login(self, user_name, password):
        user_info = {
            "UserName": user_name,
            "Password": password,
            "DeviceId": "",
            "DeviceType": "",
            "Platform": 0
        }
        return self.mou_tai.set_request_context("post", user_info, "/api/v2/Authentication/TBV3/")

    def get_student_profile(self):
        return self.mou_tai.get("/api/v2/StudentProfile/TBV3")

    def get_student_info(self):
        profile = self.get_student_profile().json()
        self.active_book = jmespath.search('CourseGroups[0].Book.Key', profile)
        self.course_plan_key = jmespath.search('CourseGroups[0].Group.CoursePlanKey', profile)
        self.user_id = jmespath.search('UserId', profile)
        self.group_id = jmespath.search('CourseGroups[0].Group.OdinId', profile)


    def query_school_info(self):
        body = {
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

    def course_node_synchronize(self, book_key, course_play_key):
        body = {"BookKey": book_key,
                "CoursePlanKey": course_play_key,
                "ProductCode": "TBV3",
                "LastSynchronizedStamp": None,
                "LastSynchronizedKey": None,
                "UpsertsOnly": False,
                "Amount": 1000
                }

        response = self.mou_tai.post("/api/v2/CourseNode/Synchronize", json=body)
        return response

    def course_unlock(self, key):
        return self.mou_tai.get("/api/v2/CourseUnlock/TB/{0}".format(key))

    def get_homework_motivation_task_info(self, key):
        return self.mou_tai.get("/api/v2/HomeworkMotivationTaskInfo/{0}".format(key))

    def query_motivation_reward_summary(self, scope_key):
        body = {
            "ScopeKey": scope_key
        }
        return self.mou_tai.post("/api/v2/MotivationRewardSummary/", json=body
                                 )

    def query_motivation_point_audit(self, scope_key):
        body = {
            "ScopeKey": scope_key
        }
        return self.mou_tai.post("/api/v2/MotivationPointAudit", json=body
                                 )

    def progress_assessment__report_by_unit(self, unit_key):
        return self.mou_tai.get("/api/v2/ProgressAssessmentReport/ByUnit/{0}".format(unit_key))

    def acitivity_entity_web(self, activity_list):
        return self.mou_tai.post("/api/v2/ActivityEntity/Web", json=activity_list)

    def lesson_score_summary(self, lesson_key_list):
        return self.mou_tai.post("/api/v2/lessonScoreSummary", json=lesson_key_list)

    def digital_interaction_info(self, book_key):
        return self.mou_tai.get("/api/v2/DigitalInteractionInfo/ByBook/{0}".format(book_key))

    def get_child_node(self, parent_key):
        book = CourseBook(self.mou_tai, "TBV3",self.active_book,self.course_plan_key)
        book.content_nodes
        self.course_node_synchronize(self.active_book, self.course_plan_key)
        child_node = jmespath.search("@[?ParentNodeKey=='{0}']".format(parent_key), self.book_contents)
        return child_node

    def student_progress(self, course_key, completed_value, total_value):
        body = {"key": None,
                "CourseKey": course_key,
                "StudentId": self.user_id,
                "LastUpdatedStamp": arrow.utcnow().format('YYYY-MM-DDTHH:mm'),
                "CompletedValue": completed_value,
                "TotalValue": total_value,
                "Percentage": round(completed_value / total_value, 3)}
        return self.mou_tai.post("/api/v2/StudentProgress", json=body)

    def homework_lesson_answer(self, lesson_key, pass_lesson=True):
        body = self.book_contents.generate_submit_answer(lesson_key, self.group_id, pass_lesson)
        return self.mou_tai.put(url='/api/v2/HomeworkLessonAnswer', json=body)

    def homework_lesson_correction(self, lesson_key):
        activity_nodes= self.book_contents.get_child_nodes_by_parent_key(lesson_key.lower())
        activity_keys = self.book_contents.get_activity_keys(activity_nodes)
        detail_activities = self.book_contents.get_activity_json_by_activity_key(activity_keys)
        total_question_count = reduce(lambda x, y: x + y,
                                      map(lambda x: Activity().create_activity(x).total_question_count, detail_activities))
        body = {
            'CorrectedAmount': total_question_count,
            'CourseKey': lesson_key,
            'MistakeAmount': total_question_count
        }
        return self.mou_tai.put(url='/api/v2/HomeworkLessonCorrection', json=body)

    def sign_out(self):
        return self.mou_tai.delete(url="/api/v2/Token/")
