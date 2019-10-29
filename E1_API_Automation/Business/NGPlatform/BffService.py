import requests
import random

from E1_API_Automation.Lib.Moutai import Moutai
import jmespath


class BffService:
    def __init__(self, host):
        self.host = host
        self.mou_tai = Moutai(host=self.host,headers={"Content-Type":"application/json;charset=UTF-8"})

    def login(self, user_name, password):
        user_info = {
            "userName": user_name,
            "password": password,
        }

        athentication_result = self.mou_tai.post("/api/v1/auth/login",user_info)
        idToken = jmespath.search('idToken', athentication_result.json())
        self.mou_tai.headers['X-EF-TOKEN'] = idToken
        return athentication_result

    def get_auth_token(self):
        token_value = self.mou_tai.headers.pop('X-EF-TOKEN')
        return token_value

    def submit_new_attempt_with_negative_auth_token(self, is_invalid="valid"):
        if is_invalid.__eq__("invalid"):
            self.mou_tai.headers['X-EF-TOKEN'] = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI5MDAwMDIyIiwiZ2"
        attempt_result = self.mou_tai.post("/api/v1/homework/attempts")
        return attempt_result

    def get_course_structure(self):
        self.mou_tai.get("/api/v1/course/structure")

    def submit_new_attempt(self, user_name, password,attempt_json):
        self.login(user_name, password)
        attempt_result = self.mou_tai.post("/api/v1/homework/attempts",attempt_json)
        return attempt_result

    def get_partition_plan_without_limit_page(self, product_id,bucket_id,plan_business_key):
        api_url = '/api/v1/plans/{0}/{1}/{2}'.format(product_id, bucket_id,
                                                     plan_business_key)
        return self.mou_tai.get(api_url)

    def get_learning_result(self, product_id,student_id):
        api_url = '/api/v1/results/{0}/{1}/'.format(product_id, student_id)
        return self.mou_tai.get(api_url)

    def get_the_best_attempt(self,student_id,book_content_id):
        api_url = '/api/v1/homework/attempts/best?studentId={0}&bookContentId={1}'.format(student_id, book_content_id)
        return self.mou_tai.get(api_url)


