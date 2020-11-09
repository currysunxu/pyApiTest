from ..Lib.SvcService import SvcService


class StudentProgressService:
    def __init__(self):
        self.service = SvcService(service_wsdl="http://schoolservices-qa.ef.cn/StudentProgressService.svc?wsdl")
        self.service.create_service()

    def get_student_activity_detial_history_by_activity_ids(self, activity_ids, student_ids, course_type_code = None):
        param = self.service.client.factory.create('ns1:StudentsActivityDetailHistoryByActivityIdsRequest')
        param.ActivityIds.int = activity_ids
        param.StudentIds.int = student_ids
        if course_type_code:
            param.CourseTypeCode = course_type_code
        response = self.service.client.service.GetStudentsActivityDetailHistoryByActivityIds(param)
        return response




