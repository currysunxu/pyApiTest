from datetime import *

import jmespath
from hamcrest import assert_that
from ptest.decorator import BeforeClass, Test, TestClass

from E1_API_Automation.Business.KidsEVC import KidsEVCService
from E1_API_Automation.Lib.HamcrestExister import exist
from E1_API_Automation.Lib.HamcrestMatcher import match_to
from E1_API_Automation.Settings import ENVIRONMENT, Environment


@TestClass()
class TestBlockBooking():
    start_time = datetime.utcnow().date().strftime('%Y-%m-%d') + " 16:00:00"
    start_time_date = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S") + timedelta(days=1)
    end_time_date = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S") + timedelta(days=1)
    end_time_date_multiple = end_time_date + timedelta(days=14)
    end_time_date_over_24_weeks = end_time_date + timedelta(days=169)
    UTC_start_date = datetime.strftime(start_time_date, '%Y-%m-%dT%H:%M:%S.000Z')
    UTC_end_date = datetime.strftime(end_time_date, '%Y-%m-%dT%H:%M:%S.000Z')
    UTC_end_date_multiple = datetime.strftime(end_time_date_multiple, '%Y-%m-%dT%H:%M:%S.000Z')
    # os.environ["test_env"] = "QA"

    if ENVIRONMENT == Environment.QA:
        host = "https://e1svc-qa.ef.cn"
        user_info_HF = {
            "UserName": "hf2.cn.03",
            "Password": "12345",
            "course_type": 'HF'
        }

        user_info_HFV3 = {
            "UserName": "hf2.cn.03",
            "Password": "12345",
            "course_type": 'HFV3Plus'
        }

        user_info_credits = {
            "UserName": "hf2.cn.02",
            "Password": "12345",
            "course_type": 'HF'
        }


    if ENVIRONMENT == Environment.STAGING:
        host = "https://e1svc-staging.ef.cn"
        user_info_HF = {
            "UserName": "hf2.cn.01",
            "Password": "12345",
            "course_type": 'HF'
        }

        user_info_HFV3 = {
            "UserName": "hf3.cn.01",
            "Password": "12345",
            "course_type": 'HFV3Plus'
        }

        user_info_credits = {
            "UserName": "hf2.cn.02",
            "Password": "12345",
            "course_type": 'HF'
        }

    @BeforeClass()
    def create_service(self):
        self.service = KidsEVCService(self.host)

    @Test()
    def block_booking_teacher_search_success_for_HF_student(self):
        self.service.login(user_name=self.user_info_HF["UserName"], password=self.user_info_HF["Password"])
        response = self.service.block_booking_teacher_search(self.UTC_start_date, self.UTC_end_date_multiple,
                                                             self.user_info_HF["course_type"], 1, 1)
        assert_that(response.status_code == 200)
        assert_that(response.json(), match_to("timeSlotTopics[].timeSlot[].startTime"))
        assert_that(response.json(), match_to("timeSlotTopics[].timeSlot[].endTime"))
        assert_that(response.json(), exist("teachers"))
        assert_that((jmespath.search("length(timeSlotTopics)", response.json())) == 3)

    @Test()
    def block_booking_teacher_search_success_for_HF_student_over_24_classes(self):
        self.service.login(user_name=self.user_info_HF["UserName"], password=self.user_info_HF["Password"])
        response = self.service.block_booking_teacher_search(self.UTC_start_date, self.end_time_date_over_24_weeks,
                                                             self.user_info_HF["course_type"], 1, 1)
        assert_that(response.status_code == 200)
        assert_that((jmespath.search("length(timeSlotTopics)", response.json())) == 24)

    @Test()
    def block_booking_teacher_search_success_for_HFV3Plus_student_over_20_classes(self):
        self.service.login(user_name=self.user_info_HFV3["UserName"], password=self.user_info_HFV3["Password"])
        response = self.service.block_booking_teacher_search(self.UTC_start_date, self.end_time_date_over_24_weeks,
                                                             self.user_info_HFV3["course_type"], 1, 1)
        assert_that(response.status_code == 200)
        assert_that((jmespath.search("length(timeSlotTopics)", response.json())) == 20)

    @Test()
    def block_booking_teacher_search_success_for_HFV3Plus_student(self):
        self.service.login(user_name=self.user_info_HFV3["UserName"], password=self.user_info_HFV3["Password"])
        response = self.service.block_booking_teacher_search(self.UTC_start_date, self.UTC_end_date,
                                                             self.user_info_HFV3["course_type"], 1, 1)
        assert_that(response.status_code == 200)
        assert_that(response.json(), match_to("timeSlotTopics[].timeSlot[].startTime"))
        assert_that(response.json(), match_to("timeSlotTopics[].timeSlot[].endTime"))
        assert_that(response.json(), match_to("teachers"))
        assert_that((jmespath.search("length(timeSlotTopics)", response.json())) == 1)

    @Test()
    def block_booking_teacher_search_success_for_HF_student_start_from_last_unit(self):
        self.service.login(user_name=self.user_info_HF["UserName"], password=self.user_info_HF["Password"])
        response = self.service.block_booking_teacher_search(self.UTC_start_date, self.UTC_end_date_multiple,
                                                             self.user_info_HF["course_type"],6, 3)
        assert_that(response.status_code == 200)
        assert_that((jmespath.search("length(timeSlotTopics)", response.json())) == 2)


    @Test()
    def block_booking_teacher_credits_limitation(self):
        self.service.login(user_name=self.user_info_credits["UserName"], password=self.user_info_credits["Password"])
        response = self.service.block_booking_teacher_search(self.UTC_start_date, self.end_time_date_over_24_weeks,
                                                             self.user_info_HF["course_type"], 1, 1)
        assert_that(response.status_code == 200)
        assert_that((jmespath.search("length(timeSlotTopics)", response.json())) == 2)

    @Test()
    def block_booking_success_HFV3Plus_student(self):
        self.service.login(user_name=self.user_info_HFV3["UserName"], password=self.user_info_HFV3["Password"])
        response, json = self.service.block_booking(self.UTC_start_date, self.UTC_end_date,
                                                    self.user_info_HFV3["course_type"])
        assert_that(response.status_code == 200)
        assert_that(response.json(), match_to("[].classId"))
        assert_that(response.json(), match_to("[].startTime"))
        assert_that(response.json(), match_to("[].endTime"))

    @Test()
    def block_booking_success_HF_student(self):
        self.service.login(user_name=self.user_info_HF["UserName"], password=self.user_info_HF["Password"])
        response, json = self.service.block_booking(self.UTC_start_date, self.UTC_end_date,
                                                    self.user_info_HF["course_type"])
        assert_that(response.status_code == 200)
        assert_that(response.json(), match_to("[].classId"))
        assert_that(response.json(), match_to("[].startTime"))
        assert_that(response.json(), match_to("[].endTime"))

    @Test()
    def duplicate_block_booking_failed(self):
        self.service.login(user_name=self.user_info_HF["UserName"], password=self.user_info_HF["Password"])
        response, json = self.service.block_booking(self.UTC_start_date, self.UTC_end_date,
                                                    self.user_info_HF["course_type"])
        assert_that(response.status_code == 200)
        assert_that(response.json(), match_to("[].classId"))
        assert_that(response.json(), match_to("[].startTime"))
        assert_that(response.json(), match_to("[].endTime"))
        response_sec = self.service.duplicate_block_booking(json)
        assert_that(response_sec.status_code == 409)
