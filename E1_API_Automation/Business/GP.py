from ..Lib.Moutai import Moutai,Token


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

    def get_available_grade(self):
        return self.mou_tai.get("/api/v2/AvailableGradeList/?regionKey=8ef7ccd2-8c58-4bc6-8a35-b3fcae4d0f0d&cultureCode=zh-CN")

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
