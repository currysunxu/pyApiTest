from ..Lib.Moutai import Moutai
from enum import Enum
import jmespath


class OMNIService:
    def __init__(self, host):
        self.host = host
        headers = {"Content-Type": "application/json", "X-ODIN-AppId": "grammarpro",
                   "X-ODIN-AppSecret": "U2FsdGVkX19SgIpGnlaC1bhAza7MSywQ4DDTcvlWmJ0="}
        self.mou_tai = Moutai(host=self.host, headers=headers)

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
