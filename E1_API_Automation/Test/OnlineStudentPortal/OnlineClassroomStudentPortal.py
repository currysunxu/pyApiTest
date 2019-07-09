from enum import Enum
from time import sleep
import jmespath
from hamcrest import assert_that
from ptest.decorator import TestClass, Test

from ...Lib.HamcrestMatcher import match_to
from ...Lib.HamcrestExister import exist
from ...Lib.ScheduleClassTool import local2utc
from ...Test.OnlineStudentPortal.EVCBaseClass import EVCBase


class ClassType(Enum):
    DEMO = "Demo"
    REGULAR = "Regular"


@TestClass()
class APITestCases(EVCBase):

    @Test(tags='qa, stg,live')
    def test_login(self):
        # Login failed was also verified at the lower layer.
        response = self.evc_service.login(user_name=self.user_info["UserName"], password=self.user_info["Password"])
        assert_that(response.json(), match_to("Token"))
        assert_that(response.json(), match_to("UserInfo.UserInfo.UserId"))
        return response

    @Test(tags='qa,stg,live')
    def test_student_profile(self):
        self.test_login()
        response = self.evc_service.get_user_profile()
        assert_that(response.status_code == 200)
        assert_that(response.json(), match_to("studentOrientationInfo[0].courseTypeLevelCode"))
        assert_that(response.json(), match_to("studentOrientationInfo[0].courseType"))
        assert_that(response.json(), exist("studentOrientationInfo[0].hasWatchedVideo"))
        assert_that(response.json(), exist("studentOrientationInfo[0].isInvisible"))
        assert_that(response.json(), match_to("studentOrientationInfo[0].lessonNumber"))
        assert_that(response.json(), match_to("studentOrientationInfo[0].packageType"))
        assert_that(response.json(), match_to("studentOrientationInfo[0].unitNumber"))
        assert_that(response.json(), match_to("userInfo"))

    @Test(tags='qa,stg,live')
    def test_get_credits(self):
        self.test_login()

        response = self.evc_service.get_credits()
        assert_that(response.status_code == 200)
        assert_that(jmespath.search("length([])", response.json()) >= 1)
        assert_that(response.json()[0]["classType"] == "Demo")
        assert_that(response.json()[0]["courseType"] == "HF" or "HFV3Plus")

    @Test(tags='qa, stg,live')
    def test_get_recommended_lesson(self):
        self.test_login()

        student_profile_response = self.evc_service.get_user_profile()
        hf_program_code = jmespath.search('studentOrientationInfo[0].courseType', student_profile_response.json())
        package_type = jmespath.search('studentOrientationInfo[0].packageType', student_profile_response.json())

        response = self.evc_service.get_recommended_class(hf_program_code, package_type)
        assert_that(response.status_code == 200)
        assert_that(response.json()["classType"] == "Regular")
        assert_that(response.json()["courseType"] == hf_program_code)
        assert_that(response.json()["packageType"] == package_type)
        assert_that(response.json(), exist("courseTypeLevelCode"))
        assert_that(response.json(), exist("unitNumber"))
        assert_that(response.json(), exist("lessonNumber"))
        assert_that(response.json(), exist("topicId"))
        assert_that(response.json(), exist("topicStatement"))

    @Test(tags='qa, stg,live')
    def test_get_all_available_teachers_demo_class(self):
        self.test_login()

        student_profile_response = self.evc_service.get_user_profile()
        hf_program_code = jmespath.search('studentOrientationInfo[0].courseType', student_profile_response.json())

        available_teachers_response = self.evc_service.get_all_available_teachers(local2utc(self.regular_start_time),
                                                                                   local2utc(self.regular_end_time),
                                                                                   course_type=hf_program_code,
                                                                                   class_type=ClassType.DEMO.value,
                                                                                   page_index=0, page_size=10)
        assert_that(available_teachers_response.json(), match_to("[0].teacherId"))

    @Test(tags='qa, stg,live')
    def test_get_all_available_teachers_regular_class(self):
        self.test_login()

        student_profile_response = self.evc_service.get_user_profile()
        hf_program_code = jmespath.search('studentOrientationInfo[0].courseType', student_profile_response.json())

        available_teachers_response = self.evc_service.get_all_available_teachers(local2utc(self.regular_start_time),
                                                                                   local2utc(self.regular_end_time),
                                                                                   course_type=hf_program_code,
                                                                                   class_type=ClassType.REGULAR.value,
                                                                                   page_index=0, page_size=10)
        assert_that(available_teachers_response.json(), match_to("[0].teacherId"))

    @Test(tags='qa, stg, live')
    def test_get_online_class_booking(self):
        self.test_login()

        student_profile_response = self.evc_service.get_user_profile()
        hf_program_code = jmespath.search('studentOrientationInfo[0].courseType', student_profile_response.json())

        query_booking_history_response = self.evc_service.query_booking_history(hf_program_code,
                                                                                ClassType.REGULAR.value)
        assert_that(query_booking_history_response.status_code == 200)

    @Test(tags='retired')
    def test_workflow(self):
        '''
        This workflow will run the following process:
        * Get mandatory parameter from API:
            1, login
            2, get student profile
        * Get lesson suggestion
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
        # Login
        self.test_login()

        # Get student profile
        student_profile_response = self.evc_service.get_user_profile()
        hf_program_code = jmespath.search('studentOrientationInfo[0].courseType', student_profile_response.json())
        package_type = jmespath.search('studentOrientationInfo[0].packageType', student_profile_response.json())

        # Check the recommended lesson before booking
        recommend_class_response = self.evc_service.get_recommended_class(hf_program_code, package_type)
        assert_that(recommend_class_response.json(), match_to("courseTypeLevelCode"))
        assert_that(recommend_class_response.json(), match_to("unitNumber"))
        recommend_book = jmespath.search("courseTypeLevelCode", recommend_class_response.json())
        recommend_unit = jmespath.search("unitNumber", recommend_class_response.json())
        recommend_lesson = jmespath.search("lessonNumber", recommend_class_response.json())

        # Check OCH before book
        och_response = self.evc_service.get_credits()
        assert_that(jmespath.search("length([])", och_response.json()) >= 2)
        assert_that(och_response.json(), match_to("[?classType=='Regular'].available"))
        OCH_number_before_booking = int(jmespath.search("[?classType=='Regular'].available", och_response.json())[0])
        sleep(2)

        # Get all available teachers
        available_teachers_response = self.evc_service.get_all_available_teachers(local2utc(self.regular_start_time),
                                                                                  local2utc(self.regular_end_time),
                                                                                  course_type=hf_program_code,
                                                                                  class_type=ClassType.REGULAR.value,
                                                                                  page_index=0, page_size=10)
        teacher_id = jmespath.search("[0].teacherId", available_teachers_response.json())

        # Book a class
        book_response = self.evc_service.book_class(local2utc(self.regular_start_time),
                                                    local2utc(self.regular_end_time),
                                                    teacher_id, course_type=hf_program_code,
                                                    class_type=ClassType.REGULAR.value, package=package_type,
                                                    course_type_level_code=recommend_book, unit_number=recommend_unit,
                                                    lesson_number=recommend_lesson)
        assert_that(book_response.status_code == 201)
        class_id = jmespath.search("axisClassId", book_response.json())

        # Verify 1 available HF credit should be deducted after booking
        och_response = self.evc_service.get_credits()
        assert_that(int(jmespath.search("[?classType=='Regular'].available", och_response.json())[0]) == (
                OCH_number_before_booking - 1))

        # Check book failed with the class which is already booked
        book_response = self.evc_service.book_class(local2utc(self.regular_start_time),
                                                    local2utc(self.regular_end_time),
                                                    teacher_id, course_type=hf_program_code,
                                                    class_type=ClassType.REGULAR.value, package=package_type,
                                                    course_type_level_code=recommend_book, unit_number=recommend_unit,
                                                    lesson_number=recommend_lesson)
        assert_that(book_response.status_code == 409)
        assert_that(jmespath.search("status", book_response.json()) == 409)
        assert_that(jmespath.search("subStatus", book_response.json()) == 1004)

        # Query booking history
        query_booking_history_response = self.evc_service.query_booking_history(hf_program_code,
                                                                                ClassType.REGULAR.value)
        assert_that(query_booking_history_response.json(), match_to("[*].classId"))
        assert_that(query_booking_history_response.json(), match_to("[*].classStatus"))

        # Change topic
        change_topic_response = self.evc_service.change_topic(str(class_id), hf_program_code, package_type,
                                                              ClassType.REGULAR.value, "H", recommend_unit,
                                                              recommend_lesson)
        assert_that(change_topic_response.status_code == 204)

        # Cancel class
        cancel_response = self.evc_service.cancel_class(str(class_id))
        assert_that(cancel_response.status_code == 204)

        # Query booking history again
        query_booking_history_response = self.evc_service.query_booking_history(hf_program_code,
                                                                                ClassType.REGULAR.value)
        assert_that(query_booking_history_response.json(), match_to("[*].classId"))
        assert_that(query_booking_history_response.json(), match_to("[*].classStatus"))

    @Test(tags='qa, stg,live')
    def test_get_online_student_book_structure(self):
        self.test_login()
        response = self.evc_service.get_user_profile()
        hf_program_code = jmespath.search('studentOrientationInfo[0].courseType', response.json())
        package_type = jmespath.search('studentOrientationInfo[0].packageType', response.json())

        lesson_structure_response = self.evc_service.get_course_lesson_structure('Regular', hf_program_code,
                                                                                 package_type)

        assert_that(lesson_structure_response.json(), match_to("[0].classType"))
        # Check that there are 192 lessons
        assert_that(jmespath.search("length([])", lesson_structure_response.json()) == 192)
        # Check the book name
        assert_that(set(jmespath.search("[].courseTypeLevelCode", lesson_structure_response.json())) == set(
            ["C", "D", "E", "F", "G", "H", "I", "J"]))

    @Test(tags='qa, stg,live')
    def test_get_online_student_book_structure_hfv3plus(self):
        self.test_login()
        lesson_structure_response = self.evc_service.get_course_lesson_structure('Regular', 'hfv3plus',
                                                                                 '20')
        assert_that(lesson_structure_response.json(), match_to("[0].classType"))
        # Check that there are 160 lessons

        assert_that(jmespath.search("length([])", lesson_structure_response.json()) == 160)
        # Check the book name
        assert_that(set(jmespath.search("[].courseTypeLevelCode", lesson_structure_response.json())) == set(
            ["C", "D", "E", "F", "G", "H", "I", "J"]))

    @Test(tags='qa, stg,live')
    def test_get_online_student_book_structure_demo(self):
        self.test_login()
        lesson_structure_response = self.evc_service.get_course_lesson_structure('demo', 'hfv3plus',
                                                                                 '20')
        assert_that(lesson_structure_response.json(), match_to("[0].classType"))
        # Check that there are 160 lessons

        assert_that(jmespath.search("length([])", lesson_structure_response.json()) == 1)
        # Check the book name
        assert_that(set(jmespath.search("[].courseTypeLevelCode", lesson_structure_response.json())) == set(
            ["X"]))
        lesson_structure_response_hf = self.evc_service.get_course_lesson_structure('demo', 'hf',
                                                                                    '24')
        assert_that(lesson_structure_response_hf.json(), match_to("[0].classType"))
        # Check that there are 160 lessons

        assert_that(jmespath.search("length([])", lesson_structure_response_hf.json()) == 1)
        # Check the book name
        assert_that(set(jmespath.search("[].courseTypeLevelCode", lesson_structure_response_hf.json())) == set(
            ["X"]))

    @Test(tags='qa,stg,live')
    def test_verify_token_expired(self):
        self.test_login()

        student_profile_response = self.evc_service.get_user_profile()
        hf_program_code = jmespath.search('studentOrientationInfo[0].courseType', student_profile_response.json())
        package_type = jmespath.search('studentOrientationInfo[0].packageType', student_profile_response.json())

        self.evc_service.sign_out()
        response = self.evc_service.get_recommended_class(hf_program_code, package_type)
        assert_that(response.status_code == 401)

    @Test(tags='qa')
    def get_after_class_report(self):
        self.test_login()  # This login is used to for after method. we will change it in the future.
        self.evc_service.login(self.after_report_info["Student_User_Name"], self.after_report_info["Student_Password"])
        response = self.evc_service.get_after_class_report(self.after_report_info['ClassId'])
        self.evc_service.sign_out()
        assert_that(jmespath.search("classId", response.json()) == int(self.after_report_info['ClassId']))
        assert_that(response.json(), match_to("improvement"))
        assert_that(response.json(), match_to("strengths"))

    @Test(tags='qa,stg,live')
    def test_get_after_class_report(self):
        self.test_login()
        class_id = self.after_report_info['ClassId']
        response = self.evc_service.get_after_class_report(class_id)
        assert_that(response.status_code == 200)
        assert_that(response.json(), match_to("improvement"))
        assert_that(response.json(), match_to("strengths"))
        assert_that(response.json(), match_to("suggestion"))

    @Test(tags='qa')
    def book_class_error_code_with_not_enough_och(self):
        self.test_login()
        self.evc_service.login(user_name=self.user_with_zero_och["UserName"],
                                password=self.user_with_zero_och["Password"])

        student_profile_response = self.evc_service.get_user_profile()
        hf_program_code = jmespath.search('studentOrientationInfo[0].courseType', student_profile_response.json())
        package_type = jmespath.search('studentOrientationInfo[0].packageType', student_profile_response.json())

        available_teachers_response = self.evc_service.get_all_available_teachers(local2utc(self.regular_start_time),
                                                                                   local2utc(self.regular_end_time),
                                                                                   course_type=hf_program_code,
                                                                                   class_type=ClassType.REGULAR.value,
                                                                                   page_index=0, page_size=10)
        teacher_id = jmespath.search("[0].teacherId", available_teachers_response.json())

        book_response = self.evc_service.book_class(local2utc(self.regular_start_time),
                                                     local2utc(self.regular_end_time),
                                                     teacher_id, course_type=hf_program_code,
                                                     class_type=ClassType.REGULAR.value, package=package_type,
                                                     course_type_level_code="C", unit_number="2", lesson_number="2")
        self.evc_service.sign_out()
        assert_that(book_response.status_code == 409)
        assert_that(jmespath.search("status", book_response.json()) == 409)
        assert_that(jmespath.search("subStatus", book_response.json()) == 600)

    @Test(tags='qa')
    def book_class_error_code_with_not_topic(self):
        self.test_login()

        student_profile_response = self.evc_service.get_user_profile()
        hf_program_code = jmespath.search('studentOrientationInfo[0].courseType', student_profile_response.json())
        package_type = jmespath.search('studentOrientationInfo[0].packageType', student_profile_response.json())

        available_teachers_response = self.evc_service.get_all_available_teachers(local2utc(self.regular_start_time),
                                                                                   local2utc(self.regular_end_time),
                                                                                   course_type=hf_program_code,
                                                                                   class_type=ClassType.REGULAR.value,
                                                                                   page_index=0, page_size=10)
        teacher_id = jmespath.search("[0].teacherId", available_teachers_response.json())

        book_response = self.evc_service.book_class(local2utc(self.regular_start_time),
                                                     local2utc(self.regular_end_time),
                                                     teacher_id, course_type=hf_program_code,
                                                     class_type=ClassType.REGULAR.value, package=package_type,
                                                     course_type_level_code="Z", unit_number="2", lesson_number="2")
        assert_that(book_response.status_code == 404)
        assert_that(jmespath.search("status", book_response.json()) == 404)
        assert_that(jmespath.search("subStatus", book_response.json()) == 601)

    @Test(tags='qa,stg,live')
    def cancel_class_error_code_with_wrong_class_id(self):
        self.test_login()

        response = self.evc_service.cancel_class("30789")
        assert_that(jmespath.search("status", response.json()) == 404)

    @Test(tags='qa,stg,live')
    def save_policy_agreement(self):
        self.test_login()

        response = self.evc_service.save_policy_agreement()
        assert_that(response.status_code == 204)

    @Test(tags='qa,stg,live')
    def save_orientation_info(self):
        self.test_login()
        orientation_info = [
            {"courseType": "HF", "packageType": "24", "courseTypeLevelCode": "C", "isActive": True, "unitNumber": "1",
             "lessonNumber": "1"}]
        response = self.evc_service.update_orientation_info(orientation_info)
        assert_that(response.status_code == 200)

    @Test(tags='qa,stg,live')
    def test_evc_student_profile(self):
        self.test_login()
        response = self.evc_service.student_evc_profile(host=self.evc_profile_host)
        assert_that((response.status_code == 200))
        assert_that(response.json(), match_to('studentId'))
