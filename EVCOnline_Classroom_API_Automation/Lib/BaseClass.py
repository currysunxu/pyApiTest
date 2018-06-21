import datetime
import os
from time import sleep

from ptest.decorator import BeforeClass, AfterMethod

from ..Lib.Moutai import Token
from .KidsEVC import KidsEVCService
from .ScheduleClassTool import KidsClass, get_QA_schedule_tool, local2utc, local2est, \
    ServiceSubTypeCode, get_UAT_schedule_tool, get_STG_schedule_tool


class Base():
    token_pattern = Token("X-BA-TOKEN", "Token")
    class_id = None
    user_info = None

    teacher_id =  os.environ['Teacher_Id']
    host = None
    start_time = None
    end_time = None

    if os.environ["Start_Time"] == "Default":
        start_time = datetime.datetime.now().date().strftime('%Y-%m-%d') + " 20:00:00"
        start_time_date = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=1)
        start_time = start_time_date.strftime("%Y-%m-%d %H:%M:%S")
    else:
        start_time = os.environ["Start_Time"]

    if os.environ["End_Time"] == "Default":
        end_time =  datetime.datetime.now().date().strftime('%Y-%m-%d') + " 21:30:00"
        end_time_date = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=1)
        end_time = end_time_date.strftime("%Y-%m-%d %H:%M:%S")
    else:
        end_time = os.environ["End_Time"]

    if os.environ["test_env"] == "QA":
        host = "https://e1svc-qa.ef.com"
        user_info = {
            "UserName": "jenkin0528tb",
            "Password": "12345",
            "DeviceType": 0,
            "Platform": 0
        }
    if os.environ["test_env"] == "STG":
        host = "https://e1svc-staging.ef.cn"
        user_info = {
            "UserName": "null183",
            "Password": "12345",
            "DeviceType": 0,
            "Platform": 0
        }

    # "2018-6-24 7:00:00"
    est_start_time = local2est(start_time)
    est_end_time = local2est(end_time)

    evc_service = None

    @BeforeClass()
    def create_class(self):
        self.evc_service = KidsEVCService(host=self.host)
        self.create_and_assign_class(self.est_start_time, self.est_end_time, teacher_id=self.teacher_id, test_env=os.environ['test_env'])#os.environ['test_env'])
        print(local2utc(self.est_start_time))
        print(local2utc(self.est_end_time))

    def create_and_assign_class(self, start_time, end_time, teacher_id, test_env="QA"):
        kids_class = KidsClass(start_time, end_time, teacher={"id": teacher_id, "teacher_name": "KON1", "teacher_password": "1"}, serverSubTypeCode=ServiceSubTypeCode.KONRegular.value)
        school_service = None
        if "QA" == test_env:
            school_service = get_QA_schedule_tool()
        if "UAT" == test_env:
            school_service = get_UAT_schedule_tool()
        if "STG" == test_env:
            school_service = get_STG_schedule_tool()
        print(school_service.schedule_kids_class(kids_class))
        sleep(3)

    @AfterMethod()
    def signout(self):
        self.evc_service.sign_out()
        print("Logout")
