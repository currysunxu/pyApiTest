from E1_API_Automation.Business.BaseService import BaseService


class RemediationService(BaseService):

    def get_remediation_activity(self, student_id, instance_key, pt_key):
        return self.mou_tai.get(
            "/api/v1/students/{0}/content-groups?testInstanceId={1}&testId={2}".format(student_id,
                                                                                       instance_key,
                                                                                       pt_key))

    def get_best_remediation_attempts(self, student_id, instance_key):
        return self.mou_tai.get(
            "/api/v1/students/{0}/attempts/best?testInstanceId={1}".format(student_id,
                                                                           instance_key,
                                                                           ))
