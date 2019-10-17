import requests
import random

from E1_API_Automation.Lib.Moutai import Moutai
import jmespath


class BffService:
    def __init__(self, host):
        self.host = host
        self.mou_tai = Moutai(host=self.host,headers={"Content-Type":"application/json;charset=UTF-8"})

    def login(self, user_name, password, platform='UNDEFINED', device_type='NONE'):
        user_info = {
            "userName": user_name,
            "password": password,
            "platform": platform,
            "deviceType": device_type
        }

        self.request_session = requests.session()
        athentication_result = self.mou_tai.post("/api/v1/auth/login",user_info)
        idToken = jmespath.search('idToken', athentication_result.json())
        self.mou_tai.headers['X-EF-TOKEN'] = idToken
        return athentication_result

    def get_auth_token(self):
        token_value = self.mou_tai.headers.pop('X-EF-TOKEN')
        return token_value

    def submit_new_attempt(self):
        print()

    def submit_new_attempt_with_negative_auth_token(self,is_invalid="valid"):
        if is_invalid.__eq__("invalid"):
            self.mou_tai.headers['X-EF-TOKEN'] = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI5MDAwMDIyIiwiZ2"
        self.request_session = requests.session()
        attempt_result = self.mou_tai.post("/api/v1/homework/attempts")
        return attempt_result


    def get_course_structure(self):
        self.mou_tai.get("/api/v1/course/structure")


