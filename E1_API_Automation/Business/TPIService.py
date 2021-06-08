from E1_API_Automation.Business.BaseService import BaseService


class TPIService(BaseService):
    def __init__(self, host):
        super().__init__(host, {"X-BA-TOKEN": "97096cec-091a-486a-9cef-4c1097a33a46"})

    def put_hf_student_omni_pt_assessment(self, pt_score_body):
        return self.mou_tai.put("/api/v2/OmniProgressTestAssessment", pt_score_body)

    def post_enrolled_groups_with_state(self, customer_id, course):
        body = {
            "StudentId": customer_id,
            "Course": course,
        }
        return self.mou_tai.post("/api/v2/CourseGroup/EnrolledGroupsWithState", body)

    def v3_product_unlock(self, student_id, lesson_key, product_code):
        body = {
            "StudentIdCollection": [student_id],
            "CourseKeys": [lesson_key]
        }
        if product_code == 'SS':
            return self.mou_tai.put("/api/v2/SmallStarUnlock", body)
        elif product_code == 'TBV3':
            return self.mou_tai.put("/api/v2/TrailblazerUnlock", body)

    def pt_web_unlock(self,expected_entity_dict):
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
        return self.mou_tai.put("/api/v2/ProgressTestUnlock", body_json)

    def lite_product_unlock(self, student_id, content_path, product_code):
        body = {
            "StudentIdCollection": [student_id],
            "ContentPaths": [content_path]
        }
        if product_code == 'SS':
            return self.mou_tai.put("/api/v2/SmallStarUnlockByContentPath", body)
        elif product_code == 'TBV3':
            return self.mou_tai.put("/api/v2/TrailblazerUnlockByContentPath'", body)