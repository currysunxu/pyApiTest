import requests

from ..Lib.Moutai import Moutai


class TPIService:
    def __init__(self, host):
        self.host = host
        self.session = requests.session()
        self.header = {"Content-Type": "application/json", "X-BA-TOKEN":"97096cec-091a-486a-9cef-4c1097a33a46"}


    def put_hf_student_omni_pt_assessment(self, pt_score_body):
        return self.session.put(self.host + "/api/v2/OmniProgressTestAssessment/", json=pt_score_body,verify=False, headers =self.header)

    def post_enrolled_groups_with_state(self, customer_id, course):
        self.header['X-BA-TOKEN'] = "54297119-42D7-4948-A075-CA79CF1B8250"
        body = {
            "StudentId": customer_id,
            "Course": course,
        }
        return self.session.post(self.host + "/api/v2/CourseGroup/EnrolledGroupsWithState", json=body,verify=False, headers =self.header)

    def v3_product_unlock(self, student_id, lesson_key, product_code):
        self.header['X-BA-TOKEN'] = "97096cec-091a-486a-9cef-4c1097a33a46"
        body = {
            "StudentIdCollection": [student_id],
            "CourseKeys": [lesson_key]
        }
        if product_code == 'SS':
            return self.session.put(self.host + '/api/v2/SmallStarUnlock', json=body,verify=False, headers =self.header)
        elif product_code == 'TBV3':
            return self.session.put(self.host + '/api/v2/TrailblazerUnlock', json=body,verify=False, headers =self.header)

    def pt_web_unlock(self,expected_entity_dict):
        self.mou_tai.headers['X-BA-TOKEN'] = "6C35BA68-AD5C-49C0-943D-5125271EFF46"
        student_id_collection = expected_entity_dict["StudentIdCollection"]
        if not isinstance(student_id_collection, list):
            student_id_collection = [expected_entity_dict["StudentIdCollection"]]
        body_json = {
            "TeacherId": expected_entity_dict["TeacherId"],
            "ProgressTestKey": expected_entity_dict["ProgressTestKey"],
            "GroupId": expected_entity_dict["GroupId"],
            "StudentIdCollection": student_id_collection,
            "SchoolCode": expected_entity_dict["SchoolCode"]
        }
        return self.mou_tai.put(url = self.host + "/api/v2/ProgressTestUnlock", verify=False, json=body_json,headers =self.header)

