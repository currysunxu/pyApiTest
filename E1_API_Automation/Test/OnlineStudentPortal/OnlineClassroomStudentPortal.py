from enum import Enum
from time import sleep

import jmespath
from hamcrest import assert_that, equal_to
from ptest.decorator import TestClass, Test

from ...Lib.HamcrestMatcher import match_to
from ...Lib.ScheduleClassTool import local2utc
from ...Test.OnlineStudentPortal.EVCBaseClass import EVCBase


class ClassType(Enum):
    DEMO = "Demo"
    REGULAR = "Regular"


@TestClass()
class APITestCases(EVCBase):

    @Test()
    def test_login(self):
        #Login failed was also verified at the lower layer.
        response = self.evc_service.login(user_name=self.user_info["UserName"], password=self.user_info["Password"])
        assert_that(response.json(), match_to("Token"))
        assert_that(response.json(), match_to("UserInfo.UserInfo.UserId"))
        return response

    @Test()
    def test_get_calendar_demo_class(self):
        self.test_login()
        response = self.evc_service.get_calendar(self.HF_program_code, ClassType.DEMO.value, local2utc(self.start_time),
                                                 local2utc(self.end_time))
        assert_that(response.json(), match_to("BookableSlots"))
        return response

    @Test()
    def test_get_calendar_regular_class(self):
        self.test_login()
        response = self.evc_service.get_calendar(self.HF_program_code, ClassType.REGULAR.value, local2utc(self.regular_start_time),
                                                 local2utc(self.regular_end_time))
        assert_that(response.json(), match_to("BookableSlots"))
        return response

    @Test()
    def test_get_calendar_non_class(self):
        self.test_login()
        response = self.evc_service.get_calendar(self.HF_program_code, ClassType.REGULAR.value, "2017-10-10T01:00:00.000000Z",
                                                 "2017-10-10T02:00:00.000000Z")
        assert_that(jmespath.search("BookableSlots", response.json()), equal_to(None))
        return response

    @Test()
    def test_get_available_online_class_session(self):
        student_id = jmespath.search("UserInfo.UserInfo.UserId", self.test_login().json())
        response = self.evc_service.get_available_online_class_session(local2utc(self.start_time),
                                                                       local2utc(self.end_time), self.HF_program_code,
                                                                       ClassType.DEMO.value, student_id)
        assert_that(response.json(), match_to("[0].TeacherProfile"))
        return response

    @Test()
    def test_get_available_online_class_session_multiple_teacher(self):
        student_id = jmespath.search("UserInfo.UserInfo.UserId", self.test_login().json())

        response = self.evc_service.get_available_online_class_session(local2utc(self.regular_start_time),
                                                                       local2utc(self.regular_end_time), self.HF_program_code,
                                                                       ClassType.REGULAR.value, student_id)
        assert_that(response.json(), match_to("[0].TeacherProfile"))
        assert_that((str(self.teacher_id) in jmespath.search("[].TeacherProfile.UserInfo.UserId", response.json())))
        assert_that(jmespath.search("[1].TeacherProfile.Description",
                                    response.json()) == self.teacher_profile["Description"])
        assert_that(jmespath.search("[1].TeacherProfile.UserInfo.UserId", response.json()) == self.teacher_profile["UserId"])
        assert_that(jmespath.search("[1].TeacherProfile.UserInfo.Name", response.json()) == self.teacher_profile["UserName"])
        assert_that(jmespath.search("[1].TeacherProfile.UserInfo.Gender", response.json()) == 2)
        assert_that(jmespath.search("[1].ProgramCode", response.json()) == self.HF_program_code)
        assert_that(jmespath.search("[1].ClassType", response.json()) == "Regular")
        assert_that(jmespath.search("[1].TeacherProfile.UserInfo.Cellphone", response.json()) == self.teacher_profile["Cellphone"])
        assert_that(jmespath.search("[1].TeacherProfile.UserInfo.AvatarUrl",
                                    response.json()) == self.teacher_profile["AvatarUrl"])
        return response

    @Test()
    def test_get_OCH_credit(self):
        student_id = jmespath.search("UserInfo.UserInfo.UserId", self.test_login().json())
        response = self.evc_service.get_OCH_credit(student_id, self.HF_program_code)
        assert_that(response.json(), match_to("[*].StudentId"))
        assert_that(jmespath.search("length([])", response.json()) == 2)
        return response

    @Test()
    def test_workflow(self):
        '''
        This workflow will run the following process:
        * Get mandatory parameter from API:
            1, login
            2, get calendar
            3, get online class session
        * Get lesson suggestion
        * Get OCH score
        * Book class and check class status code
        * Check lesson suggestion
        * Check OCH score
        * Book the same class to failed it.
        *
        :return:
        '''

        #Get neccessary parameter which will be used at the following API call.
        student_id = jmespath.search("UserInfo.UserInfo.UserId", self.test_login().json())
        calendar_response = self.evc_service.get_calendar("HF", ClassType.REGULAR.value, local2utc(self.regular_start_time),
                                                          local2utc(self.regular_end_time))
        session_start_time = jmespath.search("BookableSlots[0].StartStamp", calendar_response.json())
        session_end_time = jmespath.search("BookableSlots[0].EndStamp", calendar_response.json())
        class_session_response = self.evc_service.get_available_online_class_session(local2utc(self.regular_start_time),
                                                                                     local2utc(self.regular_end_time), self.HF_program_code,
                                                                                     ClassType.REGULAR.value,
                                                                                     student_id)
        teacher_id = jmespath.search("[0].TeacherProfile.UserInfo.UserId", class_session_response.json())
        class_id = jmespath.search("[0].ClassId", class_session_response.json())
        program_code = jmespath.search("[0].ProgramCode", class_session_response.json())


        #Check the lesson suggestion before booking
        lesson_suggestion = self.evc_service.get_lesson_suggestion(program_code)
        assert_that(lesson_suggestion.json(), match_to("BookCode"))
        assert_that(lesson_suggestion.json(), match_to("LessonNumber"))
        #assert_that(jmespath.search("LessonNumber", lesson_suggestion.json()) == "3")


        # Check the OCH scores before book
        response = self.evc_service.get_OCH_credit(student_id, program_code)
        assert_that(response.json(), match_to("[*].StudentId"))
        assert_that(jmespath.search("length([])", response.json()) == 2)
        #Verify that the student got 1000 OCH at Regular
        assert_that(response.json(), match_to("[?ClassType=='Regular'].AvailableOCH"))
        OCH_number_before_booking = jmespath.search("[?ClassType=='Regular'].AvailableOCH" ,response.json())
        sleep(2)
        print(class_id)
        response = self.evc_service.book_class("C", "2", session_start_time, session_end_time, teacher_id, program_code,
                                               ClassType.REGULAR.value,
                                               class_id,
                                               True,
                                               student_id,
                                               "Begin")
        assert_that(response.json(), match_to("Succeed"))

        #Check that the student OCH is subtracted with 1.
        response = self.evc_service.get_OCH_credit(student_id, program_code)
        assert_that(jmespath.search("[?ClassType=='Regular'].AvailableOCH", response.json())[0] == (OCH_number_before_booking[0] - 1))

        #Check book failed with the class which is already booked.
        response = self.evc_service.book_class("C", "2", session_start_time, session_end_time, teacher_id, program_code,
                                               ClassType.REGULAR.value,
                                               class_id,
                                               True,
                                               student_id,
                                               "Begin")
        assert_that(jmespath.search("Succeed", response.json()) == False)

        query_book_response = self.evc_service.query_online_class_booking(local2utc(self.regular_start_time),
                                                                          local2utc(self.regular_end_time), program_code,
                                                                          ClassType.REGULAR.value)

        '''
        Class status table:
        
        Name	Value (Dec)	Value (Hex)
        None	0	0x0
        Booked	1	0x1
        Attended	2	0x2
        StudentAbsent	3	0x3
        TeacherAbsent	4	0x4
        CanceledByCustomer	5	0x5
        CanceledByTeacher	6	0x6
        Completed	7	0x7
        '''

        assert_that(jmespath.search("[0].ClassStatus", query_book_response.json()), "1")

        #Check lesson suggestion after booking class.
        lesson_suggestion = self.evc_service.get_lesson_suggestion(program_code)
        assert_that(lesson_suggestion.json(), match_to("BookCode"))
        assert_that(lesson_suggestion.json(), match_to("LessonNumber"))
        ##TODO: there is a bug here for suggestion, after it's fix, will add code here.

        cancel_response = self.evc_service.cancel_class(class_id)
        assert_that(cancel_response.json(), match_to("Succeed"))

        query_book_response = self.evc_service.query_online_class_booking(local2utc(self.regular_start_time),
                                                                          local2utc(self.regular_end_time), program_code,
                                                                          ClassType.REGULAR.value)
        assert_that(jmespath.search("[0].ClassStatus", query_book_response.json()), "6")

    @Test()
    def test_get_online_student_book_structure(self):
        self.test_login()
        lesson_structure_response = self.evc_service.get_online_student_book_structure(self.HF_program_code)
        assert_that(lesson_structure_response.json(), match_to("[0].Lessons"))
        #Check that there are 8 books
        assert_that(jmespath.search("length([])", lesson_structure_response.json()) == 8)
        #Check the book name
        assert_that(set(jmespath.search("[].BookCode", lesson_structure_response.json())) == set(["C", "D", "E", "F", "G", "H", "I", "J"]))
        #Check the lesson number, each should be 24
        lessons_content = jmespath.search("[].Lessons", lesson_structure_response.json())
        for lesson in lessons_content:
            assert_that(len(lesson) == 24)
        #Check every book got 24 lessons, so the total will be 24 x 8 = 192
        assert_that(jmespath.search("length([].Lessons[])", lesson_structure_response.json()) == 192)


    @Test()
    def test_verify_token_expired(self):
        self.test_login()
        self.evc_service.sign_out()
        response = self.evc_service.get_lesson_suggestion(self.HF_program_code)
        assert_that(response.status_code == 401)


    #@Test()
    def get_after_class_report(self):
        # TODO: Blocked, we need to have a already finished class with teacher response, and to retrieve the class report
        self.test_login()
        response = self.evc_service.get_after_class_report("796213")
        print("Test")
