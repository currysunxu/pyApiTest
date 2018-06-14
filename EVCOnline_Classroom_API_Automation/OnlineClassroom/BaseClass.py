import datetime
from time import sleep

from ptest.decorator import BeforeClass, AfterMethod

from ..Moutai import Token
from ..OnlineClassroom.KidsEVC import KidsEVCService
from ..OnlineClassroom.ScheduleClassTool import KidsClass, get_QA_schedule_tool, local2utc, local2est, \
    ServiceSubTypeCode


class Base():
    token_pattern = Token("X-BA-TOKEN", "Token")
    class_id = None
    host = "https://e1svc-qa.ef.com"
    user_info = {
        "UserName": "jenkin0528tb",
        "Password": "12345",
        "DeviceType": 0,
        "Platform": 0
    }

    start_time = datetime.datetime.now().date().strftime('%Y-%m-%d') + " 20:00:00"
    start_time_date = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=14)
    start_time = start_time_date.strftime("%Y-%m-%d %H:%M:%S")

    end_time =  datetime.datetime.now().date().strftime('%Y-%m-%d') + " 21:30:00"
    end_time_date = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=14)
    end_time = end_time_date.strftime("%Y-%m-%d %H:%M:%S")
#"2018-6-24 7:00:00"
    est_start_time =  local2est(start_time)
    est_end_time = local2est(end_time)

    evc_service = None

    @BeforeClass()
    def create_class(self):
        self.evc_service = KidsEVCService(host=self.host)
        #self.create_and_assign_class_at_QA(self.est_start_time, self.est_end_time, teacher_id="10366584")
        print(local2utc(self.est_start_time))
        print(local2utc(self.est_end_time))

    def create_and_assign_class_at_QA(self, start_time, end_time, teacher_id):
        kids_class = KidsClass(start_time, end_time, teacher={"id": teacher_id, "teacher_name": "KON1", "teacher_password": "1"}, serverSubTypeCode=ServiceSubTypeCode.KONRegular.value)
        school_service = get_QA_schedule_tool()
        print(school_service.schedule_kids_class(kids_class))
        sleep(3)

    @AfterMethod()
    def signout(self):
        self.evc_service.sign_out()
        print("Logout")