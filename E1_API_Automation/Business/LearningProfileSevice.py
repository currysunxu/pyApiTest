from E1_API_Automation.Business.BaseService import BaseService
from ..Lib.Moutai import Token


class LearningProfileService(BaseService):
    def __init__(self):
        super().__init__("", {}, Token("X-EF-ID", "Token"))

    def get_learning_profile(self, access_token, student_id, class_id):
        self.mou_tai.headers["X-EF-Access"] = access_token
        return self.mou_tai.get("/api/v1/students/{}/learningprofile/{}".format(student_id, class_id))