from E1_API_Automation.Business.BaseService import BaseService
from enum import Enum
import jmespath


class OMNIService(BaseService):
    def __init__(self):
        super().__init__("", {"X-ODIN-AppId": "grammarpro",
                                "X-ODIN-AppSecret": "U2FsdGVkX19SgIpGnlaC1bhAza7MSywQ4DDTcvlWmJ0="})

    def get_customer_id(self, user_name, password):
        user_info = {
            "UserName": user_name,
            "Password": password,
        }

        result = self.mou_tai.set_request_context("post", user_info, "/api/v1/customer")
        customer_id = jmespath.search("CustomerId", result.json())
        return customer_id

    def get_customer_inprogressgroups(self, customer_id):
        return self.mou_tai.get("/api/v1/customer/{0}/inprogressgroups".format(customer_id))

    def get_customer_groups(self, customer_id):
        return self.mou_tai.get("/api/v1/customer/{0}/groups".format(customer_id))

    def get_pl_session(self, customer_id):
        payload = {
            "url": "/services/apexrest/osd/v1/group/sessions",
            "http_method": "POST",
            "body": {
                "studentId": customer_id
            }
        }
        return self.mou_tai.post("/api/v1/sf/restapi", payload)


class CourseGroupInfo:
    def __init__(self, course_type_code, group_status, is_current_group, is_default=False):
        self.courseTypeCode = course_type_code
        self.groupStatus = group_status
        self.isCurrentGroup = is_current_group
        self.isDefaultCourse = is_default

    def set_is_default_course(self, is_default):
        self.isDefaultCourse = is_default


class CourseGroupStatus(Enum):
    Activated = 'Activated'
    Completed = 'Completed'
    Created = 'Created'
    Pending = 'Pending'
    Cancelled = 'Cancelled'
    Current = 'current'
    Past = 'past'
    Future = 'future'
