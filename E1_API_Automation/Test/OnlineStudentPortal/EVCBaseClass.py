import datetime
import os
from time import sleep

from ptest.decorator import AfterMethod, BeforeSuite

from ...Business.KidsEVC import KidsEVCService
from ...Lib.ScheduleClassTool import KidsClass, get_QA_schedule_tool, local2est, \
    ServiceSubTypeCode, get_UAT_schedule_tool, get_STG_schedule_tool
from ...Lib.Moutai import Token


class EVCBase():
    token_pattern = Token("X-BA-TOKEN", "Token")
    class_id = None
    user_info = None
    teacher_profile = None

    '''
    Uncomment the following to run or debugger the automation.
    os.environ['Teacher_Id'] = "5888455"
    os.environ["Start_Time"] = "2018-8-18 1:00:00"
    os.environ["End_Time"] = "2018-8-18 1:30:00"
    os.environ["test_env"] = "STG"
    '''

    teacher_id = os.environ['Teacher_Id']
    host = None
    start_time = None
    end_time = None
    HF_program_code = "HF"

    teacher_list = {}

    if os.environ["Start_Time"] == "Default":
        start_time = datetime.datetime.now().date().strftime('%Y-%m-%d') + " 21:00:00"
        start_time_date = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=1)
        start_time = start_time_date.strftime("%Y-%m-%d %H:%M:%S")
    else:
        start_time = os.environ["Start_Time"]

    if os.environ["End_Time"] == "Default":
        end_time = datetime.datetime.now().date().strftime('%Y-%m-%d') + " 21:30:00"
        end_time_date = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=1)
        end_time = end_time_date.strftime("%Y-%m-%d %H:%M:%S")
    else:
        end_time = os.environ["End_Time"]
    est_start_time = local2est(start_time)
    est_end_time = local2est(end_time)

    regular_start_time_date = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=2)
    regular_start_time = regular_start_time_date.strftime("%Y-%m-%d %H:%M:%S")

    regular_end_time_date = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=2)
    regular_end_time = regular_end_time_date.strftime("%Y-%m-%d %H:%M:%S")

    # "2018-6-24 7:00:00"

    est_regular_start_time = local2est(regular_start_time)
    est_regular_end_time = local2est(regular_end_time)

    if os.environ["test_env"] == "QA":
        host = "https://e1svc-qa.ef.cn"
        user_info = {
            "UserName": "unlock02",#"jenkin0528tb",
            "Password": "12345",
            "DeviceType": 0,
            "Platform": 0
        }
        user_with_zero_och = {
            "UserName" : "c",
            "Password" : "12345"
        }
        teacher_list = ["10703777", "10366584", "10366576"]
        teacher_profile = {
            "UserId" : "10703777",
            "Description": "\"\"Hey everyone, I'm chris b.teacher.\"\"-chris b.",
            "UserName": "chris b.",
            "Gender": 2,
            "Cellphone": None,
            "AvatarUrl": "http://qa.englishtown.cn/opt-media/?id=b54fe1b3-aa1f-4676-965b-d0b5107ed69c"
        }
        after_report_info = {
            "Student_User_Name": "fr062201",
            "Student_Password": "12345",
            "ClassId": "801720"
        }
    if os.environ["test_env"] == "STG":
        '''
        STG data will be flesh out when SF team to migrate the Live data every 28 days.
        Caroline is working on this data.
        The code will be changed for STG in the coming day.
        '''
        host = "https://e1svc-staging.ef.cn"
        user_info = {
            "UserName": "null183",
            "Password": "12345",
            "DeviceType": 0,
            "Platform": 0
        }
        user_with_zero_och = {
            "UserName" : "CN_osk",
            "Password" : "12345"
        }
        teacher_list = ["10584669", "10427158", "5888455"]
        teacher_profile = {
            "UserId": "5888455",
            "Description": "\"Hello, I’m Margaret from Shanghai. Before I worked for EF, I was a high school English teacher and I have experience in English education.\"-\"The aim of education is to inspire students.\"",
            "UserName": "Margaret Wang",
            "Gender": 2,
            "Cellphone": None,
            "AvatarUrl": "http://staging.englishtown.cn/opt-media/?id=79f51ea2-cf76-42ca-9565-a8d41206c027"
        }
        after_report_info = {
            "Student_User_Name": "addison",
            "Student_Password": "12345",
            "ClassId": "247002"
        }

    def get_different_teacher(teacher_id, teacher_list):
        for teacher in teacher_list:
            if teacher != teacher_id:
                return teacher
        return None

    evc_service = None
    another_teacher = get_different_teacher(teacher_id, teacher_list)
    @BeforeSuite()
    def create_class(self):
        self.evc_service = KidsEVCService(host=self.host)

        # prepare the class which is assigned to teacher, which will follow the different environment.
        self.create_and_assign_class(self.est_start_time, self.est_end_time, teacher_id=self.teacher_id,
                                     test_env=os.environ['test_env'], subServiceType=ServiceSubTypeCode.KONDemo.value,
                                     partner_code="Any", level_code="ELE", market_code="Any",
                                     evc_server_code="evccn1")
        self.create_and_assign_class(self.est_regular_start_time, self.est_regular_end_time, teacher_id=self.teacher_id,
                                     test_env=os.environ['test_env'], level_code="ELE", market_code="Any", partner_code="Any",
                                     evc_server_code="evccn1",
                                     subServiceType=ServiceSubTypeCode.KONRegular.value)

        #Same time slot with different teacher
        self.create_and_assign_class(self.est_regular_start_time, self.est_regular_end_time,
                                     teacher_id=self.another_teacher,
                                     test_env=os.environ['test_env'], partner_code="Any", level_code="ELE", market_code="Any",evc_server_code="evccn1",
                                     subServiceType=ServiceSubTypeCode.KONRegular.value)


    def get_different_teacher(self, teacher_id, teacher_list):
        for teacher in teacher_list:
            if teacher != teacher_id:
                return teacher
        return None

    def create_and_assign_class(self, start_time, end_time, teacher_id, test_env="QA",
                                subServiceType=ServiceSubTypeCode.KONDemo.value, partner_code="any", level_code="ELE",
                                market_code="any", evc_server_code = "evccn1",  teaching_item="en"):
        kids_class = KidsClass(start_time, end_time,
                               teacher={"id": teacher_id, "teacher_name": "KON1", "teacher_password": "1"},
                               serverSubTypeCode=subServiceType, evcServerCode=evc_server_code, partnerCode=partner_code,
                               levelCode=level_code, marketCode=market_code, teachingItem=teaching_item)
        school_service = None
        if "QA" == test_env:
            school_service = get_QA_schedule_tool()
        if "UAT" == test_env:
            school_service = get_UAT_schedule_tool()
        if "STG" == test_env:
            school_service = get_STG_schedule_tool()
        print(school_service.schedule_kids_class(kids_class))
        sleep(2)

    @AfterMethod()
    def sign_out(self):
        self.evc_service.sign_out()
        print("Logout")
