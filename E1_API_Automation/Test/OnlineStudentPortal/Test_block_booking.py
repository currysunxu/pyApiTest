import os
from datetime import *

from hamcrest import assert_that
from ptest.decorator import BeforeClass, Test, TestClass

from E1_API_Automation.Business.KidsEVC import KidsEVCService
from E1_API_Automation.Lib.HamcrestMatcher import match_to


@TestClass()
class TestBlockBooking():
    start_time = datetime.utcnow().date().strftime('%Y-%m-%d') + " 16:00:00"
    start_time_date = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S") + timedelta(days=1)
    end_time_date = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S") + timedelta(days=1)
    UTC_start_date = datetime.strftime(start_time_date, '%Y-%m-%dT%H:%M:%S.000Z')
    UTC_end_date = datetime.strftime(end_time_date, '%Y-%m-%dT%H:%M:%S.000Z')
    # os.environ["test_env"] = "QA"

    if os.environ["test_env"] == "QA":
        host = "https://e1svc-qa.ef.cn"
        user_info = {
            "UserName": "w01",  # unlock02
            "Password": "12345",
            "DeviceType": 0,
            "Platform": 0
        }

    if os.environ["test_env"] == "STG":
        host = "https://e1svc-staging.ef.cn"
        user_info = {
            "UserName": "osk01",
            "Password": "12345",
            "DeviceType": 0,
            "Platform": 0
        }

    @BeforeClass()
    def create_service(self):
        self.service = KidsEVCService(self.host)

    @Test()
    def block_booking_teacher_search_success(self):
        self.service.login(user_name=self.user_info["UserName"], password=self.user_info["Password"])
        response = self.service.block_booking_teacher_search(self.UTC_start_date, self.UTC_end_date)
        assert_that(response.status_code == 200)
        assert_that(response.json(), match_to("timeSlotTopics[].timeSlot[].startTime"))
        assert_that(response.json(), match_to("timeSlotTopics[].timeSlot[].endTime"))
        assert_that(response.json(), match_to("teachers"))

    @Test()
    def block_booking_success(self):
        self.service.login(user_name=self.user_info["UserName"], password=self.user_info["Password"])
        response, json = self.service.block_booking(self.UTC_start_date, self.UTC_end_date)
        assert_that(response.status_code == 200)
        assert_that(response.json(), match_to("[].classId"))
        assert_that(response.json(), match_to("[].startTime"))
        assert_that(response.json(), match_to("[].endTime"))

    @Test()
    def duplicate_block_booking_failed(self):
        self.service.login(user_name=self.user_info["UserName"], password=self.user_info["Password"])
        response, json = self.service.block_booking(self.UTC_start_date, self.UTC_end_date)
        assert_that(response.status_code == 200)
        assert_that(response.json(), match_to("[].classId"))
        assert_that(response.json(), match_to("[].startTime"))
        assert_that(response.json(), match_to("[].endTime"))
        response_sec = self.service.duplicate_block_booking(json)
        assert_that(response_sec.status_code == 409)
