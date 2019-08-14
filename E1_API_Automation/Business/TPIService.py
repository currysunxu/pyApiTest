from ..Lib.Moutai import Moutai


class TPIService:
    def __init__(self, host):
        self.host = host
        self.mou_tai = Moutai(host=self.host)

    def put_hf_student_omni_pt_assessment(self, pt_score_body):
        return self.mou_tai.put("/api/v2/OmniProgressTestAssessment/", pt_score_body)

    def post_enrolled_groups_with_state(self, customer_id, course):
        self.mou_tai.headers['X-BA-TOKEN'] = "54297119-42D7-4948-A075-CA79CF1B8250"
        body = {
            "StudentId": customer_id,
            "Course": course,
        }
        return self.mou_tai.post("/api/v2/CourseGroup/EnrolledGroupsWithState", body)

