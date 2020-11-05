from ..Lib.Moutai import Moutai, Token


class LearningProfileService:
    def __init__(self, host):
        self.host = host
        print(host)
        self.mou_tai = Moutai(host=self.host, token=Token("X-EF-ID", "Token"))

    def get_learning_profile(self, access_token, student_id, class_id):
        self.mou_tai.headers["X-EF-Access"] = access_token
        return self.mou_tai.get("/api/v1/students/{}/learningprofile/{}".format(student_id, class_id))