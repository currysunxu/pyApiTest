from ..Lib.Moutai import Moutai


class TPIService:
    def __init__(self, host):
        self.host = host
        self.mou_tai = Moutai(host=self.host)

    def put_hf_student_omni_pt_assessment(self, pt_score_body):
        return self.mou_tai.put("/api/v2/OmniProgressTestAssessment/", pt_score_body)



