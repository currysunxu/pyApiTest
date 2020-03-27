from enum import Enum
from time import sleep
import jmespath
from hamcrest import assert_that
from ptest.decorator import TestClass, Test

from ...Lib.HamcrestMatcher import match_to
from ...Lib.ScheduleClassTool import local2utc
from ...Test.OnlineStudentPortal.EVCBaseClass import EVCBase
import os
import arrow

class ClassType(Enum):
    DEMO = "Demo"
    REGULAR = "Regular"


@TestClass()
class APITestCases(EVCBase):

    @Test(tags='qa, stg,live, stg_sg, live_sg')
    def test_login(self):
        # Login failed was also verified at the lower layer.
        response = self.evc_service.login(user_name=self.user_info["UserName"], password=self.user_info["Password"])
        return response

    @Test(tags='qa,stg,live')
    def test_get_offline_active_group_info(self):
        self.test_login()

        group_response = self.evc_service.get_offline_active_groups()
        assert_that(group_response.json(), match_to("[*].courseType"))
        assert_that(group_response.json(), match_to("[*].courseTypeLevelCode"))

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

    @Test(tags='stg_sg, live_sg')
    def test_get_offline_active_groups(self):
        self.test_login()
        group_response = self.evc_service.get_offline_active_groups()
        assert_that(group_response.status_code == 200)

    @Test(tags='qa,stg,live, stg_sg, live_sg')
    def test_offline_classes(self):
        self.test_login()

        offline_classes_response = self.evc_service.get_offline_classes()
        assert_that(offline_classes_response.status_code == 200)

    @Test(tags='qa,stg,live')
    def test_get_offline_group_sessions(self):
        self.test_login()

        group_response = self.evc_service.get_offline_active_groups()
        group_id = str(jmespath.search("[0].groupSFId", group_response.json()))
        session_response = self.evc_service.get_offline_group_sessions(group_id)
        assert_that(session_response.json(), match_to("[*].reservationId"))
        assert_that(session_response.json(), match_to("[*].sequenceNumber"))
        assert_that(session_response.json(), match_to("[*].startTime"))
        assert_that(session_response.json(), match_to("[*].endTime"))
        assert_that(session_response.json(), match_to("[*].sessionType"))
        assert_that(session_response.json(), match_to("[*].program"))
        assert_that(session_response.json(), match_to("[*].programLevel"))
        assert_that(session_response.json(), match_to("[*].lessons[0].unitNumber"))
        assert_that(session_response.json(), match_to("[*].lessons[0].lessonNumber"))

    @Test(tags='qa,stg,live, stg_sg, live_sg')
    def test_student_profile(self):
        self.test_login()
        response = self.evc_service.get_user_profile()
        assert_that(response.status_code == 200)
        assert_that(response.json(), match_to("userInfo"))

    @Test(tags='qa,stg,live')
    def test_get_credits(self):
        self.test_login()

        response = self.evc_service.get_credits()
        assert_that(response.status_code == 200)
        assert_that(jmespath.search("length([])", response.json()) >= 1)
        assert_that(response.json()[0]["courseType"] == "HF" or "HFV3Plus" or "TB")

    @Test(tags='qa, stg,live')
    def test_get_all_available_teachers_demo_class(self):
        course = self.test_get_offline_active_groups()
        course_type = course[0]

        available_teachers_response = self.evc_service.get_all_available_teachers(local2utc(self.regular_start_time),
                                                                                  local2utc(self.regular_end_time),
                                                                                  course_type=course_type,
                                                                                  class_type=ClassType.DEMO.value,
                                                                                  page_index=0, page_size=10)
        assert_that(available_teachers_response.json(), match_to("[0].teacherId"))

    @Test(tags='qa, stg,live')
    def test_get_all_available_teachers_regular_class(self):
        course = self.test_get_offline_active_groups()
        course_type = course[0]

        available_teachers_response = self.evc_service.get_all_available_teachers(local2utc(self.regular_start_time),
                                                                                  local2utc(self.regular_end_time),
                                                                                  course_type=course_type,
                                                                                  class_type=ClassType.REGULAR.value,
                                                                                  page_index=0, page_size=10)
        assert_that(available_teachers_response.json(), match_to("[0].teacherId"))

    @Test(tags='qa, stg, live')
    def test_get_online_class_booking_history(self):
        course = self.test_get_offline_active_groups()
        course_type = course[0]

        query_booking_history_response = self.evc_service.query_booking_history(course_type,
                                                                                ClassType.REGULAR.value)
        assert_that(query_booking_history_response.status_code == 200)

    @Test(enabled=os.environ['environment'].lower() in 'qa,stg', tags='qa, stg')
    def test_workflow(self):
        '''
        This workflow will run the following process:
        * Get mandatory parameter from API:
            1, login
            2, get student profile
        * Get OCH score
        * Get all available teachers
        * Book class and check class status code
        * Check lesson suggestion
        * Check OCH score
        * Book the same class to failed it
        * Change topic
        * Cancel class
        *
        :return:
        '''
        # Login and get active offline groups
        course = self.test_get_offline_active_groups()
        course_type = course[0]
        book_code = course[1]
        # Check OCH before book
        och_response = self.evc_service.get_credits()
        assert_that(och_response.json(), match_to("[?classType=='Regular'].available"))
        OCH_number_before_booking = int(jmespath.search("[?classType=='Regular'].available", och_response.json())[0])
        sleep(2)

        # Get all available teachers
        available_teachers_response = self.evc_service.get_all_available_teachers(local2utc(self.regular_start_time),
                                                                                  local2utc(self.regular_end_time),
                                                                                  course_type=course_type,
                                                                                  class_type=ClassType.REGULAR.value,
                                                                                  page_index=0, page_size=10)
        teacher_id = jmespath.search("[0].teacherId", available_teachers_response.json())

        # Book a class
        book_response = self.evc_service.book_class(local2utc(self.regular_start_time),
                                                    local2utc(self.regular_end_time),
                                                    teacher_id, course_type=course_type,
                                                    class_type=ClassType.REGULAR.value,
                                                    course_type_level_code=book_code, unit_number="1",
                                                    lesson_number="1", is_reschedule="true")
        assert_that(book_response.status_code == 201)
        class_id = jmespath.search("axisClassId", book_response.json())

        # Verify 1 available course_type credit should be deducted after booking
        och_response = self.evc_service.get_credits()
        assert_that(int(jmespath.search("[?classType=='Regular'].available", och_response.json())[0]) == (
                OCH_number_before_booking - 1))

        # Check book failed with the class which is already booked
        book_response = self.evc_service.book_class(local2utc(self.regular_start_time),
                                                    local2utc(self.regular_end_time),
                                                    teacher_id, course_type=course_type,
                                                    class_type=ClassType.REGULAR.value,
                                                    course_type_level_code=book_code, unit_number="1",
                                                    lesson_number="1", is_reschedule="true")
        assert_that(book_response.status_code == 409)
        assert_that(jmespath.search("status", book_response.json()) == 409)
        assert_that(jmespath.search("subStatus", book_response.json()) == 1004)

        # Query booking history
        query_booking_history_response = self.evc_service.query_booking_history(course_type,
                                                                                ClassType.REGULAR.value)
        assert_that(query_booking_history_response.json(), match_to("[*].classId"))
        assert_that(query_booking_history_response.json(), match_to("[*].classStatus"))

        # Change topic
        change_topic_response = self.evc_service.change_topic(str(class_id), course_type,
                                                              ClassType.REGULAR.value, "H", "1",
                                                              "1")
        assert_that(change_topic_response.status_code == 204)

        # Cancel class
        cancel_response = self.evc_service.cancel_class(str(class_id))
        assert_that(cancel_response.status_code == 204)

        # Query booking history again
        query_booking_history_response = self.evc_service.query_booking_history(course_type,
                                                                                ClassType.REGULAR.value)
        assert_that(query_booking_history_response.json(), match_to("[*].classId"))
        assert_that(query_booking_history_response.json(), match_to("[*].classStatus"))

    @Test(tags='qa, stg,live')
    def test_get_online_book_structure_hf(self):
        self.test_login()
        lesson_structure_response = self.evc_service.get_course_lesson_structure('Regular', 'HF')
        assert_that(lesson_structure_response.json(), match_to("[0].classType"))
        # Check regular lessons
        assert_that(jmespath.search("length([])", lesson_structure_response.json()) == 192)
        assert_that(set(jmespath.search("[].courseTypeLevelCode", lesson_structure_response.json())) == set(
            ["C", "D", "E", "F", "G", "H", "I", "J"]))

        # Check demo lesson
        lesson_structure_response_hf = self.evc_service.get_course_lesson_structure('DEMO', 'HF')
        assert_that(lesson_structure_response_hf.json(), match_to("[0].classType"))
        assert_that(jmespath.search("length([])", lesson_structure_response_hf.json()) == 1)
        assert_that(set(jmespath.search("[].courseTypeLevelCode", lesson_structure_response_hf.json())) == set(
            ["X"]))

    @Test(tags='qa, stg,live')
    def test_get_online_book_structure_hfv3plus(self):
        self.test_login()
        lesson_structure_response = self.evc_service.get_course_lesson_structure('Regular', 'HFV3Plus')
        assert_that(lesson_structure_response.json(), match_to("[0].classType"))
        # Check regular lessons
        assert_that(jmespath.search("length([])", lesson_structure_response.json()) == 160)
        assert_that(set(jmespath.search("[].courseTypeLevelCode", lesson_structure_response.json())) == set(
            ["C", "D", "E", "F", "G", "H", "I", "J"]))

        # Check demo lesson
        lesson_structure_response = self.evc_service.get_course_lesson_structure('DEMO', 'HFV3Plus')
        assert_that(lesson_structure_response.json(), match_to("[0].classType"))
        assert_that(jmespath.search("length([])", lesson_structure_response.json()) == 1)
        assert_that(set(jmespath.search("[].courseTypeLevelCode", lesson_structure_response.json())) == set(
            ["X"]))

    @Test(tags='qa, stg,live')
    def test_get_online_book_structure_tb(self):
        self.test_login()
        lesson_structure_response = self.evc_service.get_course_lesson_structure('Regular', 'TB')
        assert_that(lesson_structure_response.json(), match_to("[0].classType"))
        # Check regular lessons
        assert_that(jmespath.search("length([])", lesson_structure_response.json()) == 160)
        assert_that(set(jmespath.search("[].courseTypeLevelCode", lesson_structure_response.json())) == set(
            ["1", "2", "3", "4", "5", "6", "7", "8"]))

        # Check demo lesson
        lesson_structure_response = self.evc_service.get_course_lesson_structure('DEMO', 'TB')
        assert_that(lesson_structure_response.json(), match_to("[0].classType"))
        assert_that(jmespath.search("length([])", lesson_structure_response.json()) == 1)
        assert_that(set(jmespath.search("[].courseTypeLevelCode", lesson_structure_response.json())) == set(
            ["X"]))

    # @Test(tags='qa,stg,live')
    def test_verify_token_expired(self):
        self.test_login()
        self.evc_service.sign_out()

        student_profile_response = self.evc_service.get_user_profile()
        assert_that(student_profile_response.status_code == 401)

    @Test(tags='qa,stg,live')
    def test_get_after_class_report(self):
        self.test_login()  # This login is used to for after method. we will change it in the future.
        self.evc_service.login(self.after_report_info["Student_User_Name"], self.after_report_info["Student_Password"])
        response = self.evc_service.get_after_class_report(self.after_report_info['ClassId'])
        self.evc_service.sign_out()
        assert_that(jmespath.search("classId", response.json()) == int(self.after_report_info['ClassId']))
        assert_that(response.json(), match_to("improvement"))
        assert_that(response.json(), match_to("strengths"))
        assert_that(response.json(), match_to("suggestion"))

    @Test(tags='qa,stg,live')
    def test_book_class_error_code_with_not_enough_och(self):
        self.test_login()
        self.evc_service.login(user_name=self.user_with_zero_och["UserName"],
                               password=self.user_with_zero_och["Password"])

        group_response = self.evc_service.get_offline_active_groups()
        course_type_list = jmespath.search("[?isCurrentGroup==`true`].courseType", group_response.json())
        book_code_list = jmespath.search("[?isCurrentGroup==`true`].courseTypeLevelCode", group_response.json())
        if course_type_list == []:
            course_type = str(jmespath.search("[0].courseType", group_response.json()))
            book_code = str(jmespath.search("[0].courseTypeLevelCode", group_response.json()))
        else:
            course_type = str(course_type_list[0])
            book_code = str(book_code_list[0])

        available_teachers_response = self.evc_service.get_all_available_teachers(local2utc(self.regular_start_time),
                                                                                  local2utc(self.regular_end_time),
                                                                                  course_type=course_type,
                                                                                  class_type=ClassType.REGULAR.value,
                                                                                  page_index=0, page_size=10)
        teacher_id = jmespath.search("[0].teacherId", available_teachers_response.json())

        book_response = self.evc_service.book_class(local2utc(self.regular_start_time),
                                                    local2utc(self.regular_end_time),
                                                    teacher_id, course_type=course_type,
                                                    class_type=ClassType.REGULAR.value,
                                                    course_type_level_code=book_code, unit_number="2",
                                                    lesson_number="2", is_reschedule="false")
        # self.evc_service.sign_out()
        assert_that(book_response.status_code == 409)
        assert_that(jmespath.search("status", book_response.json()) == 409)
        assert_that(jmespath.search("subStatus", book_response.json()) == 600)

    @Test(tags='qa,stg,live')
    def test_book_class_error_code_with_topic_not_found(self):
        course = self.test_get_offline_active_groups()
        course_type = course[0]

        available_teachers_response = self.evc_service.get_all_available_teachers(local2utc(self.regular_start_time),
                                                                                  local2utc(self.regular_end_time),
                                                                                  course_type=course_type,
                                                                                  class_type=ClassType.REGULAR.value,
                                                                                  page_index=0, page_size=10)
        teacher_id = jmespath.search("[0].teacherId", available_teachers_response.json())

        book_response = self.evc_service.book_class(local2utc(self.regular_start_time),
                                                    local2utc(self.regular_end_time),
                                                    teacher_id, course_type=course_type,
                                                    class_type=ClassType.REGULAR.value,
                                                    course_type_level_code="Z", unit_number="2", lesson_number="2", is_reschedule="false")
        assert_that(book_response.status_code == 404)
        assert_that(jmespath.search("status", book_response.json()) == 404)
        assert_that(jmespath.search("subStatus", book_response.json()) == 601)

    @Test(tags='qa,stg,live')
    def test_cancel_class_error_code_with_class_id_not_found(self):
        self.test_login()

        response = self.evc_service.cancel_class("30789")
        assert_that(jmespath.search("status", response.json()) == 404)

    @Test(tags='qa,stg,live')
    def test_evc_student_profile(self):
        self.test_login()
        response = self.evc_service.student_evc_profile(host=self.evc_profile_host)
        assert_that((response.status_code == 200))
        assert_that(response.json(), match_to('studentId'))

    @Test(tags='qa,stg,live')
    def test_app_download_url(self):
        response = self.evc_service.get_app_download_url()
        assert_that(response.status_code == 200)
        assert_that(response.json(), match_to("appLinkForiOS"))
        assert_that(response.json(), match_to("downloadLinkForAndroid"))

    @Test(enabled=os.environ['environment'].lower() in 'qa,stg', tags='qa, stg')
    def test_reschedule(self):
        # Login and get active offline groups
        course = self.test_get_offline_active_groups()
        course_type = course[0]
        book_code = course[1]

        # Get all available teachers
        available_teachers_response = self.evc_service.get_all_available_teachers(local2utc(self.regular_start_time),
                                                                                  local2utc(self.regular_end_time),
                                                                                  course_type=course_type,
                                                                                  class_type=ClassType.REGULAR.value,
                                                                                  page_index=0, page_size=10)
        teacher_id = jmespath.search("[0].teacherId", available_teachers_response.json())

        # Book a class
        book_response = self.evc_service.book_class(local2utc(self.regular_start_time),
                                                    local2utc(self.regular_end_time),
                                                    teacher_id, course_type=course_type,
                                                    class_type=ClassType.REGULAR.value,
                                                    course_type_level_code=book_code, unit_number="1",
                                                    lesson_number="1", is_reschedule="true")
        assert_that(book_response.status_code == 201)
        class_id = jmespath.search("axisClassId", book_response.json())

        # Get all available teachers again
        reschedule_start_time = arrow.now().shift(weeks=1, days=1, hours=1).format('YYYY-MM-DD HH:00:00')
        reschedule_end_time = arrow.now().shift(weeks=1, days=1, hours=1).format('YYYY-MM-DD HH:30:00')

        current_available_teachers_response = self.evc_service.get_all_available_teachers(reschedule_start_time,
                                                                                  reschedule_end_time,
                                                                                  course_type=course_type,
                                                                                  class_type=ClassType.REGULAR.value,
                                                                                  page_index=0, page_size=10)
        teacher_id = jmespath.search("[0].teacherId", current_available_teachers_response.json())

        # Reschedule
        reschedule_response = self.evc_service.reschedule(class_id, teacher_id, reschedule_start_time, reschedule_end_time)
        assert_that(reschedule_response.status_code == 200)
        assert_that(int(jmespath.search("classId", reschedule_response.json())) == int(class_id))

        # Cancel class
        cancel_response = self.evc_service.cancel_class(str(class_id))
        assert_that(cancel_response.status_code == 204)