from ..Lib.Moutai import Moutai,Token
import jmespath
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
        return self.mou_tai.set_request_context("post", user_info, "/api/v2/Authentication/OnlineStudentPortal/")

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

    def get_sumbit_anwser(self,testresult):
        student_id = jmespath.search('UserId',self.get_student_profile_gp().json())

        reset_dt = ResetGPGradeTool()
        reset_dt.reset_grade(student_id)
        question_list = self.put_dt_start().json()
        print(question_list)
        dt_key = jmespath.search('DiagnosticTestKey',question_list)
        submit_data = {}
        module_list = []
        submit_data['DiagnosticTestKey'] = dt_key
        submit_data['Studentid'] = student_id
        module_activity_answers = []
        for module in jmespath.search('Modules', question_list):
            module_key = jmespath.search('ModuleKey', module)
            module_list.append(module_key)
            for activity in jmespath.search('Activitys', module):
                activity_type = jmespath.search('Type', activity)
                activity_Title = jmespath.search('Title', activity)
                activity_key = jmespath.search('Key', activity)
                for question in jmespath.search('Questions', activity):
                    submit_question = {}
                    module_activity_answer = {}
                    question_key = jmespath.search('Key', question)
                    submit_question['Attempts'] = None
                    submit_question['Detail'] = {"modelData":None}
                    submit_question['Duration'] = None
                    submit_question['key'] = None
                    submit_question['LocalEndStamp'] = None
                    submit_question['LocalStartStamp'] = None
                    submit_question['QuestionKey'] = question_key
                    if testresult == 'Pass':
                        submit_question['Score'] = 1

                    elif testresult== 'Failed':
                        submit_question['Score'] = 0

                    submit_question['Star'] = None
                    submit_question['TotalScore'] = 1
                    submit_question['TotalStar'] = None
                    module_activity_answer['QuestionAnswer'] = submit_question
                    module_activity_answer['ActivityKey'] = activity_key
                    module_activity_answer['ModuleKey'] = module_key
                    module_activity_answer['TemplateType'] = activity_type
                    module_activity_answers.append(module_activity_answer)

        submit_data['StudentModuleActivityAnswer'] = module_activity_answers
        print(submit_data)
        return submit_data

    def get_lesson_progress_module_key(self):
        student_progress= self.get_student_progress().json()
        print(student_progress)
        module_key = jmespath.search("DiagnosticTestProgress.NextDiagnosticTest.NeedToBeVerified",student_progress)
        return module_key

    def get_quiz_start_info(self):
        student_progress = self.get_student_progress().json()
        print(student_progress)
        module_key = jmespath.search("RemediationProgress.Recommended[0].ModuleKey", student_progress)
        lesson_key= jmespath.search("RemediationProgress.Recommended[0].Lessons[2].LessonKey", student_progress)
        submit_data = {"ModuleKey": module_key, "LessonKey": lesson_key}
        return submit_data



    def get_lesson_activity_key(self):
        student_progress = self.get_student_progress().json()
        print(student_progress)
        module_key = jmespath.search("RemediationProgress.Recommended[0].Lessons[2].ActivityKeys", student_progress)
        return module_key



    def get_submit_quiz_anwser(self):
        student_id = jmespath.search('UserId', self.get_student_profile_gp().json())
        activity_list =self.get_lesson_activity_key()
        queston_key_list=self.post_students_lesson_activity(activity_list).json()
        print(queston_key_list)
        module_key = self.get_quiz_start_info()
        remediation_key= self.post_quiz_start(module_key).json()
        print(module_key['LessonKey'])
        print(module_key['ModuleKey'])
        print(activity_list)
        submit_data = {}
        submit_data['StudentRemediationKey']=remediation_key
        submit_data['StudentId'] = student_id
        student_module_lesson_answers =[]


        for activity in activity_list:
            activity_type= jmespath.search("Activities[?Key=='" + activity + "'].Type", queston_key_list)[0]
            activity_key = activity
            question_list= jmespath.search("Activities[?Key=='" + activity + "'].Questions[].Key", queston_key_list)

            question_key = jmespath.search("Activities[?Body.tags.ActivitySubType=='Review'].Questions[].Key", queston_key_list)
            questions = [x for x in question_list if x in question_key]

            for question in questions:
                        question_answer = {}
                        student_module_lesson_answer = {}
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
                        student_module_lesson_answer['QuestionAnswer'] = question_answer
                        student_module_lesson_answer['ActivityKey'] = activity_key
                        student_module_lesson_answer['ModuleKey'] = module_key['ModuleKey']
                        student_module_lesson_answer['LessonKey'] = module_key['LessonKey']
                        student_module_lesson_answer['TemplateType'] = activity_type
                        student_module_lesson_answers.append(student_module_lesson_answer)


        submit_data['StudentModuleLessonAnswer'] = student_module_lesson_answers
        print(submit_data)
        return submit_data







    # def get_sumbit_quiz_anwser(self,lessonkey):
    #     student_id = jmespath.search('UserId',self.get_student_profile_gp().json())
    #     question_list = self.post_quiz_start(lessonkey)
    #     print(question_list)
    #     remediation_key = jmespath.search('StudentRemediationKey',question_list)
    #     submit_data = {}
    #     module_list = []
    #     submit_data['StudentRemediationKey'] = remediation_key
    #     submit_data['Studentid'] = student_id
    #     Student_Module_lesson_answers = []
    #     for module in jmespath.search('Modules', question_list):
    #         module_key = jmespath.search('ModuleKey', module)
    #         module_list.append(module_key)
    #
    #         for lesson in jmespath.search('Modules', question_list):
    #         for activity in jmespath.search('Activitys', module):
    #             activity_type = jmespath.search('Type', activity)
    #             activity_Title = jmespath.search('Title', activity)
    #             activity_key = jmespath.search('Key', activity)
    #             for question in jmespath.search('Questions', activity):
    #                 submit_question = {}
    #                 module_activity_answer = {}
    #                 question_key = jmespath.search('Key', question)
    #                 submit_question['Attempts'] = None
    #                 submit_question['Detail'] = {"modelData":None}
    #                 submit_question['Duration'] = None
    #                 submit_question['key'] = None
    #                 submit_question['LocalEndStamp'] = None
    #                 submit_question['LocalStartStamp'] = None
    #                 submit_question['QuestionKey'] = question_key
    #                 submit_question['Score'] = 1
    #                 submit_question['Star'] = None
    #                 submit_question['TotalScore'] = 1
    #                 submit_question['TotalStar'] = None
    #                 module_activity_answer['QuestionAnswer'] = submit_question
    #                 module_activity_answer['ActivityKey'] = activity_key
    #                 module_activity_answer['ModuleKey'] = module_key
    #                 module_activity_answer['TemplateType'] = activity_type
    #                 module_activity_answers.append(module_activity_answer)
    #
    #     submit_data['StudentModuleActivityAnswer'] = module_activity_answers
    #     print(submit_data)
    #     return submit_data

