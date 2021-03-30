from E1_API_Automation.Lib.Moutai import Moutai


class RemediationService:
    def __init__(self, host):
        self.host = host
        self.mou_tai = Moutai(host=self.host)

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
