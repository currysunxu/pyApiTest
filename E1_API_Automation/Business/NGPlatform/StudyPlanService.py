from E1_API_Automation.Business.BaseService import BaseService
from E1_API_Automation.Lib.Moutai import Moutai


class StudyPlanService(BaseService):

    def put_study_plan_test_entity(self, study_plan_entity):
        body_json = {
            "studentId": study_plan_entity.student_id,
            "product": study_plan_entity.product,
            "productModule": study_plan_entity.product_module,
            "refId": study_plan_entity.ref_id,
            "refContentPath": study_plan_entity.ref_content_path,
            "refProps": study_plan_entity.ref_props,
            "effectAt": study_plan_entity.effect_at,
            "expireAt": study_plan_entity.expire_at,
            "startAt": study_plan_entity.start_at,
            "completeAt": study_plan_entity.complete_at,
            "state": study_plan_entity.state
        }
        return self.mou_tai.put("/api/v1/plans", body_json)
