from ..Lib.Moutai import Moutai, Token
import jmespath
import arrow
from ..Lib.ResetGPGradeTool import ResetGPGradeTool


class TrailbazerService():
    def __init__(self, host, user_name, password):
        self.host = host
        self.mou_tai = Moutai(host=self.host, token=Token("X-BA-TOKEN", "Token"))
        self.login(user_name, password)
        self.active_book = None
        self.course_plan_key = None
        self.user_id = None
        self.group_id = None
        self.book_contents = None
        self.get_student_info()

    def login(self, user_name, password):
        user_info = {
            "UserName": user_name,  # "jenkin0528tb",
            "Password": password,  # "12345",
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

    def filter_activity_keys(self, level_no):
        self.get_student_info()
        activity_contents = self.course_node_synchronize(self.active_book,
                                                         self.course_plan_key).json()
        level_content_keys = jmespath.search("Upserts[?Level ==`{0}`]".format(level_no), activity_contents)
        return level_content_keys

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
        self.book_contents = jmespath.search("Upserts", response.json())
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

    def homework_lesson_correction(self, course_key, correct_amount):
        body = {"CourseKey": course_key,
                "MistakeAmount": 27,
                "CorrectedAmount": correct_amount}

        return self.mou_tai.post("/api/v2/HomeworkLessonCorrection", json=body)

    def digital_interaction_info(self, book_key):
        return self.mou_tai.get("/api/v2/DigitalInteractionInfo/ByBook/{0}".format(book_key))

    def get_child_node(self, parent_key):
        self.course_node_synchronize(self.active_book, self.course_plan_key)
        child_node = jmespath.search("@[?ParentNodeKey=='{0}']".format(parent_key), self.book_contents)
        return child_node

    def student_progress(self, course_key, completed_value, total_value):
        body = {"key": None,
                "CourseKey": course_key,
                "StudentId": self.user_id,
                 "LastUpdatedStamp":  arrow.utcnow().format('YYYY-MM-DDTHH:mm'),
                "CompletedValue": completed_value,
                "TotalValue": total_value,
                "Percentage": round(completed_value/total_value, 3)}
        return self.mou_tai.post("/api/v2/StudentProgress", json=body)

    def generate_lesson_answer(self, lesson_key):
        lesson_activities = self.get_child_node(lesson_key.lower())
        activity_key = jmespath.search("[*].ActivityKeys[0]", lesson_activities)
        detail_activity = self.acitivity_entity_web(activity_key).json()
        submit_data = {}
        submit_data["GroupId"] = self.group_id
        submit_data["LessonKey"] = lesson_key
        activity_answers = []
        for activity in jmespath.search("Activities", detail_activity):
            # answers = []
            # for question in jmespath.search("Questions", activity):
            #     question_answer = self.set_question_anwser(question)
            #     answers.append(question_answer)
            answers = [self.set_question_anwser(question) for question in jmespath.search("Questions", activity)]
            activity_answer = self.set_activity_answer(activity, answers, lesson_activities)
            activity_answers.append(activity_answer)

        submit_data["ActivityAnswers"] = activity_answers
        return submit_data

    def set_activity_answer(self, activity, answers, lesson_activities):
        activity_answer = {}
        activity_answer["Answers"] = answers
        activity_answer["CompletedQuestionCount"] = None
        activity_answer["correctQuestionCount"] = 1
        activity_answer["TotalQuestionCount"] = None
        activity_answer["ActivityKey"] = jmespath.search("Key", activity)
        activity_answer["ActivityCourseKey"] = \
        jmespath.search("@[?ActivityKeys[0]=='{0}'].Key".format(activity_answer["ActivityKey"]), lesson_activities)[0]
        return activity_answer

    def set_question_anwser(self, question):
        question_answer = {}
        question_answer["Attempts"] = None
        question_answer["Detail"] = {"modelData": None}
        question_answer["Duration"] = None
        question_answer["LocalEndStamp"] = None
        question_answer["Key"] = None
        question_answer["Score"] = 8
        question_answer["TotalScore"] = 8
        question_answer["Star"] = None
        question_answer["TotalStar"] = None
        question_answer["LocalStartStamp"] = None
        question_answer["LocalEndStamp"] = arrow.utcnow().format('YYYY-MM-DDTHH:mm:ssZZ')
        question_answer["QuestionKey"] = jmespath.search("Key", question)
        return question_answer

    def homework_lesson_answer(self, lesson_key):
        body = self.generate_lesson_answer(lesson_key)
        return self.mou_tai.put(url='/api/v2/HomeworkLessonAnswer', json=body)

    def sign_out(self):
        return self.mou_tai.delete(url="/api/v2/Token/")

