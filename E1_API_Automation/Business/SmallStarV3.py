from ..Lib.Moutai import Moutai, Token
import jmespath
from ..Lib.ResetGPGradeTool import ResetGPGradeTool


class SmallStarService():
    def __init__(self, host):
        self.host = host
        self.mou_tai = Moutai(host=self.host, token=Token("X-BA-TOKEN", "Token"))

    def login(self, user_name, password):
        user_info = {
            "UserName": user_name,  # "jenkin0528tb",
            "Password": password,  # "12345",
            "DeviceId":"",
            "DeviceType":"",
            "Platform": 0
        }
        return self.mou_tai.set_request_context("post", user_info, "/api/v2/Authentication/SS/")

    def get_student_profile(self):
        return self.mou_tai.get("/api/v2/StudentProfile/SS/")

    def sign_out(self):
        return self.mou_tai.delete(url="/api/v2/Token/")