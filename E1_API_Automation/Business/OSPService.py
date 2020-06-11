import random
import uuid

from ..Lib.Moutai import Moutai


class OSPService:
    def __init__(self, host):
        self.host = host
        self.mou_tai = Moutai(host=self.host)
        headers = {"x-ba-token": "3C40AB54-798C-4517-A82A-26017EE98285", "Content-Type": "application/json"}
        self.mou_tai.set_header(headers)

    def get_all_books_by_course(self, course_code):
        return self.mou_tai.get('/api/v2/AllBooksByCourse/{0}'.format(course_code))

    def post_hf_student_pt_assess_metas(self, student_id, book_key):
        pt_user = {
            "StudentId": student_id,
            "BookKey": book_key,
        }
        return self.mou_tai.post("/api/v2/StudentPaperDigitalProgressTestAssessmentMetas", pt_user)

    def post_hf_student_pt_assess_by_unit(self, student_id, book_key):
        pt_user = {
            "StudentId": student_id,
            "BookKey": book_key,
        }
        return self.mou_tai.post("/api/v2/StudentProgressTestAssessmentMetasGroupByUnit", pt_user)

    def post_hf_student_pt_assess_by_skill(self, student_id, book_key, unit_key):
        pt_user = {
            "StudentId": student_id,
            "BookKey": book_key,
            "UnitKey": unit_key
        }
        return self.mou_tai.post("/api/v2/StudentProgressTestAssessmentMetasGroupBySkill", pt_user)

    def put_create_progress_test_entity(self, expected_entity_dict):
        body_json = {
            "TeacherId": expected_entity_dict["TeacherId"],
            "ProgressTestKey": expected_entity_dict["ProgressTestKey"],
            "GroupId": expected_entity_dict["GroupId"],
            "StudentIdCollection": [expected_entity_dict["StudentIdCollection"]],
            "SchoolCode": expected_entity_dict["SchoolCode"]
        }
        return self.mou_tai.put("/api/v2/ProgressTestEntry", body_json)

    def post_query_pt_by_student_book_state(self, student_id, book_key):
        body_json = {
            "StudentId": student_id,
            "BookKey": book_key,
            "State": 1
        }
        return self.mou_tai.post("/api/v2/StudentProgressTests", body_json)

    def post_query_pt_test_result_by_student_book(self, student_id, book_key):
        body_json = {
            "StudentId": student_id,
            "BookKey": book_key
        }
        return self.mou_tai.post("/api/v2/StudentProgressTestAssessmentMetasGroupByUnit", body_json)

    def put_commit_progress_test_hc(self,student_id,pt_instance_key):
        body_json = {
          "StudentId": student_id,
          "ProgressTestInstanceKey": pt_instance_key,
          "Results": [
            {
              "ProgressTestInstanceKey": pt_instance_key,
              "ActivityKey": uuid.uuid4().__str__(),
              "StudentId": student_id,
              "GroupId": random.randint(0,20),
              "Answers": []
            }
          ]
        }

        return self.mou_tai.put("/api/v2/WebProgressTestResult/Commit", body_json)

