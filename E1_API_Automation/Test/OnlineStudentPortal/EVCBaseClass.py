import datetime
import os
from time import sleep

import arrow
from ptest.decorator import AfterMethod, BeforeSuite

from ...Business.KidsEVC import KidsEVCService
from ...Lib.ScheduleClassTool import KidsClass, get_QA_schedule_tool, local2est, \
    ServiceSubTypeCode, get_UAT_schedule_tool, get_STG_schedule_tool
from ...Lib.Moutai import Token
from E1_API_Automation.Settings import ENVIRONMENT, Environment,env_key

class EVCBase():
    token_pattern = Token("X-BA-TOKEN", "Token")
    class_id = None
    user_info = None
    teacher_profile = None
    sis_test_student = None
    sis_test_teacher_list = None

    host = None
    start_time = None
    end_time = None
    HF_program_code = "HF"

    teacher_list = {}

    try:
        print(os.environ["Start_Time"])
        print(os.environ["End_Time"])
    except:
        os.environ["Start_Time"] = "Default"
        os.environ["End_Time"] = "Default"

    if os.environ["Start_Time"] == "Default":
        a = arrow.now()
        start_time = arrow.now().shift(days=1, hours=1).format('YYYY-MM-DD hh:00:00')

    else:
        start_time = os.environ["Start_Time"]

    if os.environ["End_Time"] == "Default":
        end_time = arrow.now().shift(days=1, hours=1).format('YYYY-MM-DD hh:30:00')

    else:
        end_time = os.environ["End_Time"]
    est_start_time = local2est(start_time)
    est_end_time = local2est(end_time)

    regular_start_time_date = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=1)
    regular_start_time = regular_start_time_date.strftime("%Y-%m-%d %H:%M:%S")

    regular_end_time_date = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=1)
    regular_end_time = regular_end_time_date.strftime("%Y-%m-%d %H:%M:%S")



    est_regular_start_time = local2est(regular_start_time)
    est_regular_end_time = local2est(regular_end_time)

    if ENVIRONMENT == Environment.QA:
        try:
            teacher_id = os.environ['Teacher_Id']
        except:
            teacher_id = "10703777"
        host = "https://e1svc-qa.ef.cn"
        SIS_SERVICE = 'https://internal-e1-evc-booking-qa-cn.ef.com'
        user_info = {
            "UserName": "jimmy",#unlock02
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
            "Gender": 1,
            "Cellphone": None,
            "AvatarUrl": "https://qa.englishtown.cn/opt-media/?id=e9e4d04d-e15a-460d-af0a-5fd91c10b226"
        }
        after_report_info = {
            "Student_User_Name": "fr062201",
            "Student_Password": "12345",
            "ClassId": "801720"
        }
        sis_test_student = 12226094
        sis_test_teacher_list = [10703777, 10366576]
    if ENVIRONMENT == Environment.STAGING:
        '''
        STG data will be flesh out when SF team to migrate the Live data every 28 days.
        Caroline is working on this data.
        The code will be changed for STG in the coming day.
        '''
        try:
            teacher_id = os.environ['Teacher_Id']
        except:

            teacher_id = "10369666"
        host = "https://e1svc-staging.ef.cn"
        SIS_SERVICE = 'http://internal-e1-evc-booking-stg-cn.ef.com'
        user_info = {
            "UserName": "hf2.cn.auto1",
            "Password": "12345",
            "DeviceType": 0,
            "Platform": 0
        }

        user_info_v3 = {
            "UserName": "hf3.cn.auto1",
            "Password": "12345",
            "DeviceType": 0,
            "Platform": 0
        }
        user_with_zero_och = {
            "UserName" : "hf3.cn.auto2",
            "Password" : "12345"
        }
        teacher_list = ["10584669", "10427158", "5888455"]
        teacher_profile = {
            "UserId": "5888455",
            "Description": "\"Hello, I’m Margaret from Shanghai. Before I worked for EF, I was a high school English teacher and I have experience in English education.\"-\"The aim of education is to inspire students.\"",
            "UserName": "Margaret Wang",
            "Gender": 2,
            "Cellphone": None,
            "AvatarUrl": "https://staging.englishtown.cn/opt-media/?id=79f51ea2-cf76-42ca-9565-a8d41206c027"
        }
        after_report_info = {
            "Student_User_Name": "hf2.cn.auto2",
            "Student_Password": "12345",
            "ClassId": "248427"
        }
        sis_test_student = 43195098
        sis_test_teacher_list = [10584669, 10427158]
    if ENVIRONMENT == Environment.LIVE:
        '''
        STG data will be flesh out when SF team to migrate the Live data every 28 days.
        Caroline is working on this data.
        The code will be changed for STG in the coming day.
        '''
        try:
            teacher_id = os.environ['Teacher_Id']
        except:

            teacher_id = "10369666"
        host = "https://e1svc.ef.cn"
        SIS_SERVICE = 'http://internal-e1-evc-booking-cn.ef.com'
        user_info = {
            "UserName": "hftest.1113",
            "Password": "12345",
            "DeviceType": 0,
            "Platform": 0
        }

        user_info_v3 = {
            "UserName": "hf3.cn.auto1",
            "Password": "12345",
            "DeviceType": 0,
            "Platform": 0
        }
        user_with_zero_och = {
            "UserName" : "hf3.cn.auto2",
            "Password" : "12345"
        }
        teacher_list = ["10584669", "10427158", "5888455"]
        teacher_profile = {
            "UserId": "5888455",
            "Description": "\"Hello, I’m Margaret from Shanghai. Before I worked for EF, I was a high school English teacher and I have experience in English education.\"-\"The aim of education is to inspire students.\"",
            "UserName": "Margaret Wang",
            "Gender": 2,
            "Cellphone": None,
            "AvatarUrl": "https://staging.englishtown.cn/opt-media/?id=79f51ea2-cf76-42ca-9565-a8d41206c027"
        }
        after_report_info = {
            "Student_User_Name": "hf2.cn.auto2",
            "Student_Password": "12345",
            "ClassId": "248427"
        }
        sis_test_student = 43195098
        sis_test_teacher_list = [10584669, 10427158]

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
        schedule_class, schedule_class_regular = (-1, -1)
        try_time = 0
        while schedule_class == -1 and try_time < 3:
            schedule_class = self.create_and_assign_class(self.est_start_time, self.est_end_time,
                                                          teacher_id=self.teacher_id,
                                                          test_env=env_key,
                                                          subServiceType=ServiceSubTypeCode.KONDemo.value,
                                                          partner_code="Any", level_code="Any", market_code="Any", evc_server_code="EvcCN2")
            try_time = try_time + 1
        try_time = 0
        while schedule_class_regular == -1 and try_time < 3:
            schedule_class_regular = self.create_and_assign_class(self.est_regular_start_time, self.est_regular_end_time, teacher_id=self.teacher_id,
                                         test_env=env_key, level_code="Any", market_code="Any", partner_code="Any",
                                         evc_server_code="EvcCN2",
                                         subServiceType=ServiceSubTypeCode.KONRegular.value)
            try_time = try_time + 1

            #Same time slot with different teacher
            self.create_and_assign_class(self.est_regular_start_time, self.est_regular_end_time,
                                         teacher_id=self.another_teacher,
                                         test_env=env_key, partner_code="Any", level_code="Any", market_code="Any",evc_server_code="EvcCN2",
                                         subServiceType=ServiceSubTypeCode.KONRegular.value)

    def get_different_teacher(self, teacher_id, teacher_list):
        for teacher in teacher_list:
            if teacher != teacher_id:
                return teacher
        return None

    def create_and_assign_class(self, start_time, end_time, teacher_id, test_env="QA",
                                subServiceType=ServiceSubTypeCode.KONDemo.value, partner_code="any", level_code="Any",
                                market_code="any", evc_server_code = "EvcCN2",  teaching_item="en"):

        school_service = None
        kids_class = KidsClass(start_time, end_time,
                               teacher={"id": teacher_id, "teacher_name": "KON1", "teacher_password": "1"},
                               serverSubTypeCode=subServiceType, evcServerCode=evc_server_code,
                               partnerCode=partner_code,
                               levelCode=level_code, marketCode=market_code, teachingItem=teaching_item)
        if "QA" == test_env:
            school_service = get_QA_schedule_tool()
        if "UAT" == test_env:
            school_service = get_UAT_schedule_tool()
        if "Staging" == test_env:
            school_service = get_STG_schedule_tool()
        if "Live" == test_env:
            school_service = None
        sleep(2)
        if school_service is not None:
            schedule_class = school_service.schedule_kids_class(kids_class)
            return schedule_class
        return None

    @AfterMethod()
    def sign_out(self):
        self.evc_service.sign_out()
        print("Logout")
