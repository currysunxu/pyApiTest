import jmespath
from ptest.assertion import assert_that

from ..Lib.Moutai import Moutai, Token
from ..Lib.ResetGPGradeTool import ResetGPGradeTool


class GPService():
    def __init__(self, host):
        self.host = host
        self.mou_tai = Moutai(host=self.host, token=Token("X-BA-TOKEN", "Token"))

    def login(self, user_name, password):
        user_info = {
            "UserName": user_name,  # "jenkin0528tb",
            "Password": password,  # "12345",
            "Platform": 0
        }
        return self.mou_tai.set_request_context("post", user_info, "/api/v2/Authentication/GP/")

    def get_student_profile(self):
        return self.mou_tai.get("/api/v2/StudentProfile/")

    def get_student_profile_gp(self):
        return self.mou_tai.get("/api/v2/StudentProfile/GP")

    def sign_out(self):
        return self.mou_tai.delete(url="/api/v2/Token/")

    def post_access_token(self):
        return self.mou_tai.post("/api/v2/xAPI/AccessToken/")

    def get_cn_privacy_policy(self):
        return self.mou_tai.get("/api/v2/PrivacyPolicy/StudentPrivacyPolicyAgreement/?product=7&cultureCode=zh-CN")

    def get_cn_student_report(self):
        return self.mou_tai.get("/api/v2/StudentReport/zh-CN")

    def get_en_student_report(self):
        return self.mou_tai.get("/api/v2/StudentReport/en-US")

    def get_custom_test(self):
        return self.mou_tai.get("/api/v2/CustomTest")

    def get_module_latest(self):
        return self.mou_tai.get("/api/v2/StudentDiagnosticTest/ModuleLatest")

    def get_student_progress(self):
        return self.mou_tai.get("/api/v2/StudentProgress")

    def post_students_lesson_progress(self, module_info):
        return self.mou_tai.post("/api/v2/StudentRemediationProgress", module_info)

    def post_students_lesson_activity(self, module_info):
        return self.mou_tai.post("/api/v2/ActivityEntity/Web/", module_info)

    def get_available_grade(self, region_key):
        return self.mou_tai.get("/api/v2/AvailableGradeList/?regionKey=%s&cultureCode=zh-CN" % region_key)

    def post_quiz_start(self, lesson_key):
        return self.mou_tai.post("/api/v2/RemediationLesson/Start/", lesson_key)

    def post_quiz_save(self, submit_answer):
        return self.mou_tai.post("/api/v2/RemediationLesson/Save/", submit_answer)

    def put_dt_start(self):
        return self.mou_tai.put("/api/v2/StudentDiagnosticTest/Start/")

    def put_dt_save(self, submit_answer):
        return self.mou_tai.put("/api/v2/StudentDiagnosticTest/Save/", submit_answer)

    def get_region_and_grade(self):
        return self.mou_tai.get("/api/v2/RegionAndGrade/?marketRegion=1&cultureCode=zh-CN")

    def put_profile_save(self, profile):
        return self.mou_tai.put("/api/v2/StudentProfile/Save/", profile)

    def put_custom_test_start(self, module_list):
        return self.mou_tai.put("/api/v2/CustomTest/Start/", module_list)

    def put_custom_test_save(self, test_answer):
        return self.mou_tai.put("/api/v2/CustomTest/Save/", test_answer)

    def get_custom_test_answer(self, module_list):

        question_list = self.put_custom_test_start(module_list[:4]).json()
        ct_key = jmespath.search('CustomTestKey', question_list)
        submit_data = {}
        module_activity_answers = []
        submit_data['CustomTestKey'] = ct_key
        for module in jmespath.search('Modules', question_list):
            module_key = jmespath.search('ModuleKey', module)
            for activity in jmespath.search('Activitys', module):
                activity_type = jmespath.search('Type', activity)
                activity_key = jmespath.search('Key', activity)
                for question in jmespath.search('Questions', activity):
                    question_key = jmespath.search('Key', question)
                    submit_question = self.set_submit_question(question_key)
                    submit_question['Score'] = 0
                    module_activity_answer = self.set_module_activity_answer(activity_key, activity_type, module_key,
                                                                             submit_question)
                    module_activity_answers.append(module_activity_answer)

        submit_data['StudentModuleActivityAnswer'] = module_activity_answers

        return submit_data

    def get_dt_submit_answer(self, failed_module_number, first_time=True):
        student_id = jmespath.search('UserId', self.get_student_profile_gp().json())
        if first_time == True:
            self.reset_grade(student_id)
        question_list = self.put_dt_start().json()
        # print(question_list)
        dt_key = jmespath.search('DiagnosticTestKey', question_list)
        failed_module_list, module_activity_answers = [], []
        submit_data = {}
        submit_data['DiagnosticTestKey'] = dt_key
        submit_data['Studentid'] = student_id

        for index, module in enumerate(jmespath.search('Modules', question_list)):
            module_key = jmespath.search('ModuleKey', module)
            for activity in jmespath.search('Activitys', module):
                activity_type = jmespath.search('Type', activity)
                activity_key = jmespath.search('Key', activity)
                for question in jmespath.search('Questions', activity):
                    question_key = jmespath.search('Key', question)
                    submit_question = self.set_submit_question(question_key)
                    if index + 1 > failed_module_number:
                        submit_question['Score'] = 1
                    else:
                        submit_question['Score'] = 0
                        failed_module_list.append(module_key)

                    module_activity_answer = self.set_module_activity_answer(activity_key, activity_type, module_key,
                                                                             submit_question)
                    module_activity_answers.append(module_activity_answer)

        submit_data['StudentModuleActivityAnswer'] = module_activity_answers
        # print(str(submit_data).encode('utf-8'))
        failed_module = list(set(failed_module_list))
        return submit_data, failed_module

    # def get_dt_not_first_time_submit_answer(self, failed_module_number):
    #     student_id = jmespath.search('UserId', self.get_student_profile_gp().json())
    #     question_list = self.put_dt_start().json()
    #     # print(question_list)
    #     dt_key = jmespath.search('DiagnosticTestKey', question_list)
    #     failed_module_list, module_activity_answers = [], []
    #     submit_data = {}
    #     submit_data['DiagnosticTestKey'] = dt_key
    #     submit_data['Studentid'] = student_id
    #     for index, module in enumerate(jmespath.search('Modules', question_list)):
    #         module_key = jmespath.search('ModuleKey', module)
    #         for activity in jmespath.search('Activitys', module):
    #             activity_type = jmespath.search('Type', activity)
    #             activity_key = jmespath.search('Key', activity)
    #             for question in jmespath.search('Questions', activity):
    #                 question_key = jmespath.search('Key', question)
    #                 submit_question = self.set_submit_question(question_key)
    #                 if index+1 > failed_module_number:
    #                     submit_question['Score'] = 1
    #                 else:
    #                     submit_question['Score'] = 0
    #                     failed_module_list.append(module_key)
    #
    #                 module_activity_answer = self.set_module_activity_answer(activity_key, activity_type, module_key,
    #                                                                          submit_question)
    #                 module_activity_answers.append(module_activity_answer)
    #
    #     submit_data['StudentModuleActivityAnswer'] = module_activity_answers
    #     failed_module=[]
    #     failed_module = [failed_module.append(i) for i in failed_module_list if not i in failed_module]
    #     print(str(submit_data).encode('utf-8'))
    #     return submit_data, failed_module

    def set_submit_question(self, question_key):
        submit_question = {}
        submit_question['Attempts'] = None
        submit_question['Detail'] = {"modelData": None}
        submit_question['Duration'] = None
        submit_question['key'] = None
        submit_question['LocalEndStamp'] = None
        submit_question['LocalStartStamp'] = None
        submit_question['QuestionKey'] = question_key
        submit_question['Star'] = None
        submit_question['TotalScore'] = 1
        submit_question['TotalStar'] = None
        return submit_question

    def set_module_activity_answer(self, activity_key, activity_type, module_key, submit_question):
        module_activity_answer = {}
        module_activity_answer['QuestionAnswer'] = submit_question
        module_activity_answer['ActivityKey'] = activity_key
        module_activity_answer['ModuleKey'] = module_key
        module_activity_answer['TemplateType'] = activity_type
        return module_activity_answer

    def reset_grade(self, student_id):
        reset_dt = ResetGPGradeTool()
        reset_dt.reset_grade(student_id)

    def get_all_module_quiz_answer(self):
        student_progress = self.get_student_progress().json()
        module_key = jmespath.search("DiagnosticTestProgress.NextDiagnosticTest.NeedToBeVerified", student_progress)
        for single_module_key in module_key:
            self.get_submit_quiz_answer(single_module_key)

    def get_quiz_start_info(self):
        student_progress = self.get_student_progress().json()
        print(student_progress)
        module_key = jmespath.search("RemediationProgress.Recommended[0].ModuleKey", student_progress)
        lesson_key = jmespath.search("RemediationProgress.Recommended[0].Lessons[2].LessonKey", student_progress)
        submit_data = {"ModuleKey": module_key, "LessonKey": lesson_key}

        return submit_data

    def get_lesson_activity_key(self):
        student_progress = self.get_student_progress().json()
        print(student_progress)
        activity_key = jmespath.search("RemediationProgress.Recommended[0].Lessons[0].ActivityKeys", student_progress)
        return activity_key

    def get_submit_quiz_answer(self, single_module_key):
        student_id = jmespath.search('UserId', self.get_student_profile_gp().json())
        submit_data = {}
        for lesson_number in range(1, 5):
            student_progress = self.get_student_progress().json()
            module_json = jmespath.search("RemediationProgress.Recommended[?ModuleKey=='" + single_module_key + "']",
                                          student_progress)

            single_activity_list, single_lesson_key = self.get_lesson_key_and_single_activity_list(lesson_number,
                                                                                                   module_json)
            question_key_list = self.post_students_lesson_activity(single_activity_list).json()
            submit_json = {"ModuleKey": single_module_key, "LessonKey": single_lesson_key}
            remediation_key = self.set_remediation_key(submit_json)
            submit_data['StudentRemediationKey'] = remediation_key
            submit_data['StudentId'] = student_id

            student_module_lesson_answers = []
            for activity in single_activity_list:
                activity_type = jmespath.search("Activities[?Key=='" + activity + "'].Type", question_key_list)[0]

                question_key, question_list = self.get_question_key_and_list(activity, question_key_list)
                questions = [x for x in question_list if x in question_key]

                for question in questions:
                    question_answer = self.set_question_answer(question)
                    student_module_lesson_answer = self.set_student_module_lesson_answer(activity,
                                                                                         activity_type,
                                                                                         single_module_key,
                                                                                         question_answer,
                                                                                         single_lesson_key)
                    student_module_lesson_answers.append(student_module_lesson_answer)
            submit_data['StudentModuleLessonAnswer'] = student_module_lesson_answers

            self.post_quiz_save(submit_data)

    def set_remediation_key(self, submit_json):
        remediation_key = self.post_quiz_start(submit_json).json()
        return remediation_key

    def get_lesson_key_and_single_activity_list(self, lesson_number, module_json):
        single_lesson_key = jmespath.search(
            "[].Lessons[?Sequence==`" + str(lesson_number) + "`].LessonKey[]",
            module_json)[0]
        single_activity_list = jmespath.search(
            "[].Lessons[?Sequence==`" + str(lesson_number) + "`].ActivityKeys[][]",
            module_json)
        return single_activity_list, single_lesson_key

    def get_question_key_and_list(self, activity, question_key_list):
        question_list = jmespath.search("Activities[?Key=='" + activity + "'].Questions[].Key",
                                        question_key_list)
        question_key = jmespath.search("Activities[?Body.tags.ActivitySubType=='Review'].Questions[].Key",
                                       question_key_list)
        return question_key, question_list

    def set_student_module_lesson_answer(self, activity, activity_type, single_module_key, question_answer,
                                         single_lesson_key):
        student_module_lesson_answer = {}
        student_module_lesson_answer['QuestionAnswer'] = question_answer
        student_module_lesson_answer['ActivityKey'] = activity
        student_module_lesson_answer['ModuleKey'] = single_module_key
        student_module_lesson_answer['LessonKey'] = single_lesson_key
        student_module_lesson_answer['TemplateType'] = activity_type
        return student_module_lesson_answer

    def set_question_answer(self, question):
        question_answer = {}
        question_answer['Attempts'] = None
        question_answer['Detail'] = {"modelData": None}
        question_answer['Duration'] = None
        question_answer['key'] = None
        question_answer['LocalEndStamp'] = None
        question_answer['LocalStartStamp'] = None
        question_answer['QuestionKey'] = question
        question_answer['Score'] = 1
        question_answer['Star'] = None
        question_answer['TotalScore'] = 1
        question_answer['TotalStar'] = None
        return question_answer

    def finish_first_dt(self, failed_module_number, first_time=True):
        submit_json = self.get_dt_submit_answer(failed_module_number, first_time)
        response = self.put_dt_save(submit_json[0])
        assert_that(response.status_code == 204)
        if failed_module_number != 0:
            self.finish_all_quiz_from_latest_dt()

    def finish_not_first_dt(self, failed_module_number, first_time=False, loop=1):
        for times in range(loop):
            submit_json = self.get_dt_submit_answer(failed_module_number, first_time)
            response = self.put_dt_save(submit_json[0])
            assert_that(response.status_code == 204)
            if failed_module_number != 0 and loop % 2 == 0:
                self.finish_all_quiz_from_latest_dt()

    def finish_all_quiz_from_latest_dt(self):
        submit_answer = self.get_all_module_quiz_answer()
        response = self.post_quiz_save(submit_answer)
        assert_that(response.status_code == 204)
