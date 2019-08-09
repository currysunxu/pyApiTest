from ..Lib.Moutai import Moutai


class OSPService:
    def __init__(self, host):
        self.host = host
        self.mou_tai = Moutai(host=self.host)

    def get_all_books_by_course(self, course_code):
        return self.mou_tai.get('/api/v2/AllBooksByCourse/{0}'.format(course_code))

    def post_hf_student_pt_assess_metas(self, student_id, book_key):
        pt_user = {
            "StudentId": student_id,
            "BookKey": book_key,
        }
        return self.mou_tai.post("/api/v2/StudentPaperDigitalProgressTestAssessmentMetas", pt_user)

    def post_hf_student_pt_assess_by_unit(self, student_id, book_key):
        pt_user = {
            "StudentId": student_id,
            "BookKey": book_key,
        }
        return self.mou_tai.post("/api/v2/StudentProgressTestAssessmentMetasGroupByUnit", pt_user)

    def post_hf_student_pt_assess_by_skill(self, student_id, book_key, unit_key):
        pt_user = {
            "StudentId": student_id,
            "BookKey": book_key,
            "UnitKey": unit_key
        }
        return self.mou_tai.post("/api/v2/StudentProgressTestAssessmentMetasGroupBySkill", pt_user)