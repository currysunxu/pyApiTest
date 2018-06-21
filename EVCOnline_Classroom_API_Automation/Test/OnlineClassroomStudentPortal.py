from enum import Enum
from time import sleep

import jmespath
from hamcrest import assert_that, equal_to
from ptest.decorator import TestClass, Test

from ..HamcrestMatcher import match_to
from ..OnlineClassroom.BaseClass import Base
from ..OnlineClassroom.ScheduleClassTool import local2utc


class ClassType(Enum):
    DEMO = "Demo"
    REGULAR = "Regular"


@TestClass()
class APITestCases(Base):

    @Test()
    def login(self):
        response = self.evc_service.login(user_name=self.user_info["UserName"], password=self.user_info["Password"])
        assert_that(response.json(), match_to("Token"))
        assert_that(response.json(), match_to("UserInfo.UserInfo.UserId"))
        #assert_that(jmespath.search("UserInfo.UserInfo.UserId", response.json()), equal_to('12226218'))
        return response

    @Test()
    def get_calendar(self):
        self.login()
        response = self.evc_service.get_calendar("HF", ClassType.REGULAR.value, local2utc(self.start_time),
                                                 local2utc(self.end_time))
        assert_that(response.json(), match_to("BookableSlots"))
        return response

    @Test()
    def get_available_online_class_session(self):
        student_id = jmespath.search("UserInfo.UserInfo.UserId", self.login().json())
        response = self.evc_service.get_available_online_class_session(local2utc(self.start_time),
                                                                       local2utc(self.end_time), "HF",
                                                                       ClassType.REGULAR.value, student_id)
        assert_that(response.json(), match_to("[0].TeacherProfile"))
        return response

    @Test()
    def get_OCH_credit(self):
        student_id = jmespath.search("UserInfo.UserInfo.UserId", self.login().json())
        response = self.evc_service.get_OCH_credit(student_id, "HF")
        assert_that(response.json(), match_to("[*].StudentId"))
        return response

    @Test()
    def workflow(self):
        student_id = jmespath.search("UserInfo.UserInfo.UserId", self.login().json())

        calendar_response = self.evc_service.get_calendar("HF", ClassType.REGULAR.value, local2utc(self.start_time),
                                                          local2utc(self.end_time))
        session_start_time = jmespath.search("BookableSlots[0].StartStamp", calendar_response.json())
        session_end_time = jmespath.search("BookableSlots[0].EndStamp", calendar_response.json())

        class_session_response = self.evc_service.get_available_online_class_session(local2utc(self.start_time),
                                                                                     local2utc(self.end_time), "HF",
                                                                                     ClassType.REGULAR.value,
                                                                                     student_id)
        teacher_id = jmespath.search("[0].TeacherProfile.UserInfo.UserId", class_session_response.json())
        class_id = jmespath.search("[0].ClassId", class_session_response.json())
        program_code = jmespath.search("[0].ProgramCode", class_session_response.json())

        sleep(2)

        response = self.evc_service.book_class("C", "2", session_start_time, session_end_time, teacher_id, program_code,
                                               ClassType.REGULAR.value,
                                               class_id,
                                               True,
                                               student_id,
                                               "Begin")
        assert_that(response.json(), match_to("Succeed"))

        query_book_response = self.evc_service.query_online_class_booking(local2utc(self.start_time),
                                                                          local2utc(self.end_time), program_code,
                                                                          ClassType.REGULAR.value)
        assert_that(jmespath.search("[0].ClassStatus", query_book_response.json()), "1")



        lesson_suggestion = self.evc_service.get_lesson_suggestion(program_code)
        assert_that(lesson_suggestion.json(), match_to("BookCode"))
        assert_that(lesson_suggestion.json(), match_to("LessonNumber"))

        lesson_structure_response = self.evc_service.get_online_student_book_structure(program_code)
        assert_that(lesson_structure_response.json(), match_to("[0].Lessons"))

        cancel_response = self.evc_service.cancel_class(class_id)
        assert_that(cancel_response.json(), match_to("Succeed"))

        query_book_response = self.evc_service.query_online_class_booking(local2utc(self.start_time),
                                                                          local2utc(self.end_time), program_code,
                                                                          ClassType.REGULAR.value)
        assert_that(jmespath.search("[0].ClassStatus", query_book_response.json()), "5")

    #@Test()
    def cancel_class(self):
        self.login()
        self.evc_service.cancel_class("787157")
