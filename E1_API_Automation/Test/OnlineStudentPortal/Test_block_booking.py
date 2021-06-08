from datetime import *

import arrow
import jmespath
from hamcrest import assert_that
from ptest.decorator import BeforeClass, Test, TestClass, AfterMethod

from E1_API_Automation.Business.KidsEVC import KidsEVCService
from E1_API_Automation.Business.Utils.EnvUtils import EnvUtils
from E1_API_Automation.Lib.HamcrestMatcher import match_to


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

    if EnvUtils.is_env_qa():
        user_info_HF = {
            "UserName": "hf2.cn.03",
            "Password": "12345",
            "course_type": 'HF'
        }
        teacher_id = "10274591"
        class_list = []

    if EnvUtils.is_env_stg_cn():
        user_info_HF = {
            "UserName": "hf3.cn.03",
            "Password": "12345",
            "course_type": 'HFV3Plus'
        }
        teacher_id = "10427158"
        class_list = []

    @BeforeClass()
    def create_service(self):
        self.service = KidsEVCService()

    def select_booking_time_slots_with_unit_lesson(self, unit_number, lesson_number, i):
        start_time = arrow.now().shift(weeks=i, days=1, hours=1).format('YYYY-MM-DD HH:00:00')
        end_time = arrow.now().shift(weeks=i, days=1, hours=1).format('YYYY-MM-DD HH:30:00')

        dict = {
            "unitNumber": unit_number,
            "lessonNumber": lesson_number,
            "startTime": start_time,
            "endTime": end_time
        }
        return dict

    def select_time_ranges_with_unit_lesson(self, unit_number, lesson_number, i):
        start_time = arrow.now().shift(weeks=i, days=1, hours=1).format('YYYY-MM-DD HH:00:00')
        end_time = arrow.now().shift(weeks=i, days=8, hours=1).format('YYYY-MM-DD HH:00:00')

        dict = {
            "unitNumber": unit_number,
            "lessonNumber": lesson_number,
            "startTime": start_time,
            "endTime": end_time
        }
        return dict

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
        unit_lesson = tuple(zip(unit, lesson))
        return unit_lesson

    def get_booking_time_slots(self, course_type, book):
        # get unit lesson
        unit_lesson = self.get_book_topics(course_type, book)

        # get booking time slots
        time_slots = []
        for index, data in enumerate(unit_lesson):
            time_slot = self.select_booking_time_slots_with_unit_lesson(str(data[0]), str(data[1]), index)
            time_slots.append(time_slot)
        return time_slots

    def get_booking_time_ranges(self, course_type, book):
        # get unit lesson
        unit_lesson = self.get_book_topics(course_type, book)

        # get booking time ranges
        time_ranges = []
        for index, data in enumerate(unit_lesson):
            time_range = self.select_time_ranges_with_unit_lesson(str(data[0]), str(data[1]), index)
            time_ranges.append(time_range)
        return time_ranges

    @Test(tags='qa,stg')
    def test_block_booking_search_by_weekday_and_timeslot(self):
        self.service.login(user_name=self.user_info_HF["UserName"], password=self.user_info_HF["Password"])

        # get current group
        course = self.get_active_offline_group()

        # search by weekday and time slot
        search_time_slots = self.get_booking_time_slots(course[0], course[1])
        search_result = self.service.block_booking_search_by_weekday_and_timeslot(self.user_info_HF["course_type"],
                                                                                  search_time_slots)

        # block booking
        block_booking_response = self.service.block_booking_v3(course[0], course[1], self.teacher_id, search_time_slots)
        assert_that(block_booking_response.status_code == 200)
        self.class_list = jmespath.search("[*].classId", block_booking_response.json())
        assert_that(block_booking_response.json(), match_to("[].classId"))
        assert_that(block_booking_response.json(), match_to("[].startTime"))
        assert_that(block_booking_response.json(), match_to("[].endTime"))
        assert_that(block_booking_response.json(), match_to("[].classStatusCode"))

    @Test(tags='qa,stg')
    def test_block_booking_search_by_weekday_slot_and_teacher(self):
        self.service.login(user_name=self.user_info_HF["UserName"], password=self.user_info_HF["Password"])

        # get current group
        course = self.get_active_offline_group()

        # search by weekday, time slot and teacher
        search_time_slots = self.get_booking_time_slots(course[0], course[1])
        self.service.block_booking_search_by_weekday_slot_and_teacher(self.user_info_HF["course_type"], self.teacher_id,
                                                                      search_time_slots)
        # block booking
        block_booking_response = self.service.block_booking_v3(course[0], course[1], self.teacher_id, search_time_slots)
        assert_that(block_booking_response.status_code == 200)
        self.class_list = jmespath.search("[*].classId", block_booking_response.json())
        assert_that(block_booking_response.json(), match_to("[].classId"))
        assert_that(block_booking_response.json(), match_to("[].startTime"))
        assert_that(block_booking_response.json(), match_to("[].endTime"))
        assert_that(block_booking_response.json(), match_to("[].classStatusCode"))

    @Test(tags='qa,stg')
    def test_block_booking_search_by_teacher(self):
        self.service.login(user_name=self.user_info_HF["UserName"], password=self.user_info_HF["Password"])

        # get current group
        course = self.get_active_offline_group()

        # search by teacher
        time_ranges = self.get_booking_time_ranges(course[0], course[1])
        self.service.block_booking_search_by_teacher(self.user_info_HF["course_type"], self.teacher_id, time_ranges)
        book_time_slots = self.get_booking_time_slots(course[0], course[1])

        # block booking
        block_booking_response = self.service.block_booking_v3(course[0], course[1], self.teacher_id, book_time_slots)
        assert_that(block_booking_response.status_code == 200)
        self.class_list = jmespath.search("[*].classId", block_booking_response.json())
        assert_that(block_booking_response.json(), match_to("[].classId"))
        assert_that(block_booking_response.json(), match_to("[].startTime"))
        assert_that(block_booking_response.json(), match_to("[].endTime"))
        assert_that(block_booking_response.json(), match_to("[].classStatusCode"))

    @Test(tags='qa,stg')
    def test_block_booking_search_by_weekday_and_teacher(self):
        self.service.login(user_name=self.user_info_HF["UserName"], password=self.user_info_HF["Password"])

        # get current group
        course = self.get_active_offline_group()

        # search by weekday and teacher
        time_ranges = self.get_booking_time_ranges(course[0], course[1])
        self.service.block_booking_search_by_weekday_and_teacher(self.user_info_HF["course_type"], self.teacher_id,
                                                                 time_ranges, "Monday")
        book_time_slots = self.get_booking_time_slots(course[0], course[1])

        # block booking
        block_booking_response = self.service.block_booking_v3(course[0], course[1], self.teacher_id, book_time_slots)
        assert_that(block_booking_response.status_code == 200)
        self.class_list = jmespath.search("[*].classId", block_booking_response.json())
        assert_that(block_booking_response.json(), match_to("[].classId"))
        assert_that(block_booking_response.json(), match_to("[].startTime"))
        assert_that(block_booking_response.json(), match_to("[].endTime"))
        assert_that(block_booking_response.json(), match_to("[].classStatusCode"))

    @Test(tags='qa,stg')
    def test_block_booking_search_by_slot_and_teacher(self):
        self.service.login(user_name=self.user_info_HF["UserName"], password=self.user_info_HF["Password"])

        # get current group
        course = self.get_active_offline_group()

        # search by time slot and teacher
        time_ranges = self.get_booking_time_ranges(course[0], course[1])
        self.service.block_booking_search_by_slot_and_teacher(self.user_info_HF["course_type"], self.teacher_id,
                                                              time_ranges, "16:30")
        book_time_slots = self.get_booking_time_slots(course[0], course[1])

        # block booking
        block_booking_response = self.service.block_booking_v3(course[0], course[1], self.teacher_id, book_time_slots)
        assert_that(block_booking_response.status_code == 200)
        self.class_list = jmespath.search("[*].classId", block_booking_response.json())
        assert_that(block_booking_response.json(), match_to("[].classId"))
        assert_that(block_booking_response.json(), match_to("[].startTime"))
        assert_that(block_booking_response.json(), match_to("[].endTime"))
        assert_that(block_booking_response.json(), match_to("[].classStatusCode"))

    @AfterMethod()
    def cancel_classes(self):
        for class_id in self.class_list:
            cancel_response = self.service.cancel_class(str(class_id))
            assert_that(cancel_response.status_code == 204)
