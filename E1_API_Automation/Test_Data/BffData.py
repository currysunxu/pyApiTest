import json
import random
import string
import uuid
from enum import Enum
import time
from json import dumps

import jsonpath


class BffProduct(Enum):
    HFV35 = 'HFV35'
    TBV3 = 'TBV3'
    SSV3 = 'SSV3'
    FRV1 = 'FRV1'
    HFV2 = 'HFV2'
    HFV3 = 'HFV3'


class BffUsers:
    BffUserPw = {
        'QA': {
            BffProduct.HFV35.value: [{'username': 'ptReviewTest06', 'password': '12345'}],
            BffProduct.TBV3.value: [{'username': 'tb3.cn.01', 'password': '12345'}],
            BffProduct.SSV3.value: [{'username': 'ss3.cn.02', 'password': '12345'}],
            BffProduct.FRV1.value: [{'username': 'fr.cn.01', 'password': '12345'}],
            BffProduct.HFV2.value: [{'username': 'hf.cn.own.test01', 'password': '12345'},
                                     {'username': 'hf.cn.fra.test01', 'password': '12345'},
                                     {'username': 'hf.cn.emptybc.test01', 'password': '12345'},
                                     {'username': 'hf.id.fra.test01', 'password': '12345'}],
            BffProduct.HFV3.value: [{'username': 'hf3.cn.01', 'password': '12345'}]
        },
        'Staging': {
            # Todo need to do data refactor once Staging is ready
            BffProduct.HFV35.value: [{'username': 'hf3.cn.auto1', 'password': '12345'}],
        },
        'Live': {
            # Todo need to do data refactor once Staging is ready
            BffProduct.HFV35.value: [{'username': 'hf3.cn.auto1', 'password': '12345'}],
        }
    }


class BffCommonData:
    attempt_json = {}
    plan_business = []
    previous_attempt = {}
    score = 0

    def __init__(self):
        self.attempt_json = self.create_json_body()
        self.plan_business = self.create_plan_business()
        self.previous_attempt = self.attempt_json

    def create_json_body(self):
        random_student_id = ''.join(random.sample(string.digits, 8))
        random_date_time = time.strftime("%Y-%m-%dT%H:%M:%S.%jZ", time.localtime())

        act2_details_array = {
                                 "questionId":uuid.uuid4().__str__(),
                                 "totalScore":1,
                                 "score":1,
                                 "answer": [{"answer_key":"homeworkSVC_Test_01",
                                             "options":[
                                                 {
                                                  "id":"homeworkSVC_TestID_01",
                                                 "image":{
                                                     "id":"/content/adam/courses/highflyers/book-2/unit-1/activities/homework/ss-multiple-select-lesson0-activity1-vocabulary/a1q1/jcr:content/parsys_question/highflyersresponse/image",
                                                     "url":"https://study-qa.ef.cn/portal/#/login",
                                                     "size": 1000,
                                                     "sha1": "697f80b6027a1fa223b044b844d2fabd71f9497a",
                                                     "mimeType": "image/png",
                                                     "width": 500,
                                                     "height": 500
                                                 }
                                             }
                                            ]}]
                             }, {
                                 "questionId": uuid.uuid4().__str__(),
                                 "totalScore": 5,
                                 "score": 3,
                                 "answer": [{"answer_key":"homeworkSVC_Test_Answer_01",
                                             "options":[
                                                 {
                                                  "id":"homeworkSVC_TestID_02_01",
                                                 "image":{
                                                     "id":"homeworkSVC_image_id_02",
                                                     "url":"https://study-qa.ef.cn/portal/#/login",
                                                     "size": 3000,
                                                     "sha1": "697f80b6027a1fa223b044b844d2fabd71f9497d",
                                                     "mimeType": "image/png",
                                                     "width": 600,
                                                     "height": 600
                                                 }
                                             }
                                            ]}]
                             }

        act1_details_array = {
                                 "questionId": uuid.uuid4().__str__(),
                                 "totalScore": 3,
                                 "score": 2,
                                 "answer": "<footer><pstyle=\"text-align:center;\"><ahref=\"/support/license.html\">License</a>|<ahref=\"/support/privacy.html\">connietestRoute29</a>|<ahref=\"/support/terms.html\">answer02_01</a></p></footer>"
                             }, {
                                 "questionId": uuid.uuid4().__str__(),
                                 "totalScore": 6,
                                 "score": 4,
                                 "answer": [
                                     "A",
                                     "B",
                                     "0",
                                     "1"
                                 ]
                             }

        act_obj1 = {
            "activityContentId": uuid.uuid4().__str__(),
            "activityContentRevision": "activityContentRevisionTest01",
            "details": act2_details_array
        }

        act_obj2 = {
            "activityContentId":uuid.uuid4().__str__(),
            "activityContentRevision": "activityContentRevisionTest02",
            "details": act1_details_array
        }

        obj = [act_obj1, act_obj2]

        json_body = {
            "studentId": random_student_id,
            "startTimeUtc": random_date_time,
            "endTimeUtc": random_date_time,
            "courseContentId": uuid.uuid4().__str__(),
            "bookContentId": uuid.uuid4().__str__(),
            "unitContentId": uuid.uuid4().__str__(),
            "lessonContentId": uuid.uuid4().__str__(),
            "learningUnitContentId": uuid.uuid4().__str__(),
            "treeRevision": "test",
            "activities": obj
        }
        print(dumps(json_body))

        return json_body

    def create_plan_business(self):
        courseContentId = self.get_attempt_body()["courseContentId"]
        bookContentId = self.get_attempt_body()["bookContentId"]
        unitContentId = self.get_attempt_body()["unitContentId"]
        lessonContentId = self.get_attempt_body()["lessonContentId"]
        learningUnitContentId = self.get_attempt_body()["learningUnitContentId"]
        plan_business_list = []
        plan_business_list.append(courseContentId)
        plan_business_list.append(bookContentId)
        plan_business_list.append(unitContentId)
        plan_business_list.append(lessonContentId)
        plan_business_list.append(learningUnitContentId)
        return plan_business_list

    def get_attempt_body(self):
        return self.attempt_json

    def set_best_attempt(self):
        for act_index in range(len(jsonpath.jsonpath(json.loads(json.dumps(self.previous_attempt)), '$..activities[*]'))):
            for details_index in range(len(jsonpath.jsonpath(json.loads(json.dumps(self.previous_attempt)), '$..details'))):
                self.previous_attempt["activities"][act_index]["details"][details_index]["totalScore"] *= 2
                self.previous_attempt["activities"][act_index]["details"][details_index]["score"] *= 2
        print("Double increase totalScore and score : ")

class BffUtil:

    @staticmethod
    def get_value_by_json_path(json_body,expression):
        return jsonpath.jsonpath(json.loads(json.dumps((json_body))),expression)