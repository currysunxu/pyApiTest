from datetime import *

import arrow
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
        host = "https://study-qa.ef.cn"
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
        host = "https://study-staging.ef.cn"
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

    def select_booking_timeslots(self, booking_number):
        timeslot_list = []

        for i in range(0, booking_number):
            start_time = arrow.now().shift(weeks=i, days=1, hours=1).format('YYYY-MM-DD HH:00:00')
            end_time = arrow.now().shift(weeks=i, days=1, hours=1).format('YYYY-MM-DD HH:30:00')

            dict = {
                "startTime": start_time,
                "endTime": end_time
            }
            i = i + 1
            timeslot_list.append(dict)
        return timeslot_list

    def get_active_offline_group(self):
        group_response = self.service.get_offline_active_groups()
        course_type_list = jmespath.search("[?isCurrentGroup==`true`].courseType", group_response.json())
        book_code_list = jmespath.search("[?isCurrentGroup==`true`].courseTypeLevelCode", group_response.json())
        if course_type_list == []:
            course_type = str(jmespath.search("[0].courseType", group_response.json()))
            book_code = str(jmespath.search("[0].courseTypeLevelCode", group_response.json()))
        else:
            course_type = str(course_type_list[0])
            book_code = str(book_code_list[0])
        course = []
        course.append(course_type)
        course.append(book_code)
        return course

    def get_book_topics(self, course_type, book):
        lesson_structure_response = self.service.get_course_lesson_structure('Regular', course_type)

        unit = jmespath.search("[?courseTypeLevelCode=='" + book + "'].unitNumber",
                               lesson_structure_response.json())
        lesson = jmespath.search("[?courseTypeLevelCode=='" + book + "'].lessonNumber",
                                 lesson_structure_response.json())
        return unit, lesson

    @Test()
    def test_block_booking_search_by_weekday_and_timeslot(self):
        self.service.login(user_name=self.user_info_HFV3["UserName"], password=self.user_info_HFV3["Password"])

        # get current group
        course = self.get_active_offline_group()

        # get topics
        topics = self.get_book_topics(course[0], course[1])

        # search by weekday and time slot
        time_slots = self.select_booking_timeslots(2)
        search_result = self.service.block_booking_search_by_weekday_timeslot(self.user_info_HFV3["course_type"], time_slots)
        teacher_id = jmespath.search("[0].teacherId", search_result.json())

        for index, slot in enumerate(time_slots):
            slot['unitNumber'] = topics[0][index]
            slot['lessonNumber'] = topics[1][index]

        # block booking
        block_booking_response = self.service.block_booking_v3(course[0], course[1], teacher_id, time_slots)
        assert_that(block_booking_response.status_code == 200)
        class_list = jmespath.search("[*].classId", block_booking_response.json())

        assert_that(block_booking_response.json(), match_to("[].classId"))
        assert_that(block_booking_response.json(), match_to("[].startTime"))
        assert_that(block_booking_response.json(), match_to("[].endTime"))
        assert_that(block_booking_response.json(), match_to("[].classStatusCode"))

        # cancel classes
        for class_id in class_list:
            cancel_response = self.service.cancel_class(str(class_id))
            assert_that(cancel_response.status_code == 204)

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
