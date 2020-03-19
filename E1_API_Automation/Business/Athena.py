from ..Lib.Moutai import Moutai, Token
import jmespath
from ..Lib.ResetGPGradeTool import ResetGPGradeTool


class Athena():
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
        return self.mou_tai.set_request_context("post", user_info, "/api/v2/Authentication/Athena/")


class Staff():
    def __init__(self, host):
        self.host = host
        self.mou_tai = Moutai(host=self.host, token=Token("X-BA-TOKEN", "Token"))

    def login_staff(self, user_name, password):
        user_info = {
            "UserName": user_name,  # "jenkin0528tb",
            "Password": password,  # "12345",
            "DeviceId":"",
            "DeviceType":"",
            "Platform": 0
        }
        return self.mou_tai.set_request_context("post", user_info, "/api/v2/Authentication/Staff/")

    def login_Legacy(self, user_name, password):
        user_info = {
            "UserName": user_name,  # "jenkin0528tb",
            "Password": password,  # "12345",
            "DeviceId": "",
            "DeviceType": "",
            "Platform": 0
        }
        return self.mou_tai.set_request_context("post", user_info, "/api/v2/Authentication/Legacy/")


class Student():
    def __init__(self, host):
        self.host = host
        self.mou_tai = Moutai(host=self.host, token=Token("X-BA-TOKEN", "Token"))

    def login_student(self, lg_token, password):
        user_info = {
            "request": {
                "Username": lg_token,
                "Password": password,
                "DeviceId": "",
                "Domain": "",
                "DeviceType": 0,
                "Platform": 16
            },
            "realm": "evc-e1athena.ef.cn"
        }
        return self.mou_tai.set_request_context("post", user_info, "/api/v2/Authentication/AthenaStudent/")