from enum import Enum
from time import sleep

import arrow
import jmespath
from hamcrest import assert_that, equal_to
from ptest.decorator import TestClass, Test

from E1_API_Automation.Business.KidsEVC import KidsEVCService
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

    @Test(tags='qa,stg.live')
    def test_student_profile(self):
        self.test_login()
        response = self.evc_service.get_user_profile()
        assert_that(response.status_code == 200)
        assert_that(response.json(), match_to("studentOrientationInfo[0].courseTypeLevelCode"))
        assert_that(response.json(), exist("studentOrientationInfo[0].hasWatchedVideo"))
        assert_that(response.json(), exist("studentOrientationInfo[0].isInvisible"))
        assert_that(response.json(), match_to("studentOrientationInfo[0].lessonNumber"))
        assert_that(response.json(), match_to("studentOrientationInfo[0].packageType"))
        assert_that(response.json(), match_to("studentOrientationInfo[0].unitNumber"))
        assert_that(response.json(), match_to("userInfo"))

    @Test(tags='qa, stg,live')
    def test_get_calendar_demo_class(self):
        self.test_login()
        response = self.evc_service.get_calendar(self.HF_program_code, ClassType.DEMO.value, local2utc(self.start_time),
                                                 local2utc(self.end_time))
        assert_that(response.json(), exist("BookableSlots"))
        return response

    @Test(tags='qa, stg,live')
    def test_get_calendar_regular_class(self):
        self.test_login()
        start_date = arrow.utcnow().shift().format('YYYY-MM-DDTHH:mm;sssZ')
        end_date = arrow.utcnow().shift(days=+30).format('YYYY-MM-DDTHH:mm:sssZ')
        response = self.evc_service.get_calendar(self.HF_program_code, ClassType.REGULAR.value,
                                                 local2utc(self.regular_start_time),
                                                 local2utc(self.regular_end_time))
        assert_that(response.json(), exist("BookableSlots"))
        return response

    @Test(tags='qa, stg,live')
    def test_get_calendar_non_class(self):
        self.test_login()

        response = self.evc_service.get_calendar(self.HF_program_code, ClassType.REGULAR.value,
                                                 "2017-10-10T01:00:00.000000Z",
                                                 "2017-10-10T02:00:00.000000Z")
        assert_that(jmespath.search("BookableSlots", response.json()), equal_to(None))
        return response

    @Test(tags='qa, stg.live')
    def test_get_online_class_booking(self):
        student_id = jmespath.search("UserInfo.UserInfo.UserId", self.test_login().json())
        response = self.evc_service.query_online_class_booking(None, None, self.HF_program_code)
        assert_that(response.status_code == 200)

    
    # @Test(tags='qa')
    # def test_get_available_online_class_session_multiple_teacher(self):
    #     student_id = jmespath.search("UserInfo.UserInfo.UserId", self.test_login().json())
    # 
    #     response = self.evc_service.get_available_online_class_session(None, None, self.HF_program_code
    #                                                                    )
    #     assert_that(response.json(), match_to("[].TeacherProfile"))
    #     assert_that((str(self.teacher_id) in jmespath.search("[].TeacherProfile.UserInfo.UserId", response.json())))
    # 
    #     filter = "[?TeacherProfile.UserInfo.UserId=='" + self.teacher_profile["UserId"] + "']"
    #     assert_that(jmespath.search(filter + ".TeacherProfile.Description",
    #                                 response.json())[0] == self.teacher_profile["Description"])
    #     assert_that(
    #         jmespath.search(filter + ".TeacherProfile.UserInfo.UserId", response.json())[0] == self.teacher_profile[
    #             "UserId"])
    #     assert_that(
    #         jmespath.search(filter + ".TeacherProfile.UserInfo.Name", response.json())[0] == self.teacher_profile[
    #             "UserName"])
    #     assert_that(
    #         jmespath.search(filter + ".TeacherProfile.UserInfo.Gender", response.json())[0] == self.teacher_profile[
    #             "Gender"])
    #     assert_that(jmespath.search(filter + ".ProgramCode", response.json())[0] == self.HF_program_code)
    #     assert_that(jmespath.search(filter + ".ClassType", response.json())[0] == "Regular")
    #     assert_that(len(jmespath.search(filter + ".TeacherProfile.UserInfo.Cellphone", response.json())) == 0)
    #     assert_that(jmespath.search(filter + ".TeacherProfile.UserInfo.AvatarUrl",
    #                                 response.json())[0] == self.teacher_profile["AvatarUrl"])
    #     return response

    # @Test(tags='qa, stg')
    # def test_get_OCH_credit(self):
    #     student_id = jmespath.search("UserInfo.UserInfo.UserId", self.test_login().json())
    #     response = self.evc_service.get_OCH_credit(student_id, self.HF_program_code)
    #     assert_that(response.json(), match_to("[*].StudentId"))
    #     assert_that(jmespath.search("length([])", response.json()) == 2)
    #     assert_that(response.json(), match_to("[*].AvailableOCH"))
    #     return response

    # @Test(tags='retired')
    # def test_workflow(self):
    #     '''
    #     This workflow will run the following process:
    #     * Get mandatory parameter from API:
    #         1, login
    #         2, get calendar
    #         3, get online class session
    #     * Get lesson suggestion
    #     * Get OCH score
    #     * Book class and check class status code
    #     * Check lesson suggestion
    #     * Check OCH score
    #     * Book the same class to failed it
    #     * Change topic
    #     * Cancel class
    #     *
    #     :return:
    #     '''
    # 
    #     # Get necessary parameter which will be used at the following API call.
    #     student_id = jmespath.search("UserInfo.UserInfo.UserId", self.test_login().json())
    #     calendar_response = self.evc_service.get_calendar("HF", ClassType.REGULAR.value,
    #                                                       local2utc(self.regular_start_time),
    #                                                       local2utc(self.regular_end_time))
    #     session_start_time = jmespath.search("BookableSlots[0].StartStamp", calendar_response.json())
    #     session_end_time = jmespath.search("BookableSlots[0].EndStamp", calendar_response.json())
    #     class_session_response = self.evc_service.get_available_online_class_session(None, None, self.HF_program_code
    # 
    #                                                                                  )
    #     teacher_id = jmespath.search("[0].TeacherProfile.UserInfo.UserId", class_session_response.json())
    #     class_id = jmespath.search("[0].ClassId", class_session_response.json())
    #     program_code = jmespath.search("[0].ProgramCode", class_session_response.json())
    # 
    #     # Check the lesson suggestion before booking
    #     lesson_suggestion_response = self.evc_service.get_lesson_suggestion(program_code)
    #     assert_that(lesson_suggestion_response.json(), match_to("BookCode"))
    #     assert_that(lesson_suggestion_response.json(), match_to("LessonNumber"))
    #     # assert_that(jmespath.search("LessonNumber", lesson_suggestion.json()) == "3")
    # 
    #     # Check OCH before book
    #     och_response = self.evc_service.get_OCH_credit(student_id, program_code)
    #     assert_that(och_response.json(), match_to("[*].StudentId"))
    #     assert_that(jmespath.search("length([])", och_response.json()) == 2)
    #     # Verify that the student got 1000 OCH at Regular
    #     assert_that(och_response.json(), match_to("[?ClassType=='Regular'].AvailableOCH"))
    #     OCH_number_before_booking = jmespath.search("[?ClassType=='Regular'].AvailableOCH", och_response.json())
    #     sleep(2)
    #     print(class_id)
    #     book_response = self.evc_service.book_class("C", "2", "2", session_start_time, session_end_time, teacher_id,
    #                                                 program_code,
    #                                                 ClassType.REGULAR.value,
    #                                                 class_id,
    #                                                 True,
    #                                                 student_id,
    #                                                 "Begin")
    #     assert_that(book_response.json(), match_to("Succeed"))
    # 
    #     # Verify 1 available HF credit should be deducted after booking
    #     och_response = self.evc_service.get_OCH_credit(student_id, program_code)
    #     assert_that(jmespath.search("[?ClassType=='Regular'].AvailableOCH", och_response.json())[0] == (
    #                 OCH_number_before_booking[0] - 1))
    # 
    #     # Check book failed with the class which is already booked
    #     book_response = self.evc_service.book_class("C", "2", "2", session_start_time, session_end_time, teacher_id,
    #                                                 program_code,
    #                                                 ClassType.REGULAR.value,
    #                                                 class_id,
    #                                                 True,
    #                                                 student_id,
    #                                                 "Begin")
    #     assert_that("Reason: 207" in jmespath.search("Message", book_response.json()))
    # 
    #     query_lesson_history_response = self.evc_service.query_online_class_booking(local2utc(self.regular_start_time),
    #                                                                                 local2utc(self.regular_end_time),
    #                                                                                 program_code,
    #                                                                                 ClassType.REGULAR.value)
    # 
    #     '''
    #     Class status table:
    #     
    #     Name	Value (Dec)	Value (Hex)
    #     None	0	0x0
    #     Booked	1	0x1
    #     Attended	2	0x2
    #     StudentAbsent	3	0x3
    #     TeacherAbsent	4	0x4
    #     CanceledByCustomer	5	0x5
    #     CanceledByTeacher	6	0x6
    #     Completed	7	0x7
    #     '''
    #     assert_that(jmespath.search("[?ClassId=='" + class_id + "'].ClassStatus", query_lesson_history_response.json()),
    #                 "1")
    # 
    #     # Check lesson suggestion after booking class
    #     lesson_suggestion = self.evc_service.get_lesson_suggestion(program_code)
    #     assert_that(lesson_suggestion.json(), match_to("BookCode"))
    #     assert_that(lesson_suggestion.json(), match_to("LessonNumber"))
    #     ##TODO: there is a bug here for suggestion, after it's fix, will add code here.
    # 
    #     # Change topic
    #     change_topic_response = self.evc_service.change_topic(student_id, "C", "6", "1", session_start_time,
    #                                                           session_end_time, teacher_id, program_code,
    #                                                           ClassType.REGULAR.value, class_id, True)
    #     assert_that(change_topic_response.json(), match_to("Succeed"))
    # 
    #     # Cancel class
    #     cancel_response = self.evc_service.cancel_class(class_id)
    #     assert_that(cancel_response.json(), match_to("Succeed"))
    # 
    #     query_lesson_history_response = self.evc_service.query_online_class_booking(local2utc(self.regular_start_time),
    #                                                                                 local2utc(self.regular_end_time),
    #                                                                                 program_code,
    #                                                                                 ClassType.REGULAR.value)
    #     assert_that(jmespath.search("[?ClassId=='" + class_id + "'].ClassStatus", query_lesson_history_response.json()),
    #                 "6")
    # 

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
        self.evc_service.sign_out()
        response = self.evc_service.get_lesson_suggestion(self.HF_program_code)
        assert_that(response.status_code == 401)

    # @Test(tags='qa')
    # def get_after_class_report(self):
    #     self.test_login()  # This login is used to for after method. we will change it in the future.
    #     local_evc_service = KidsEVCService(host=self.host)
    #     local_evc_service.login(self.after_report_info["Student_User_Name"], self.after_report_info["Student_Password"])
    #     response = local_evc_service.get_after_class_report(self.after_report_info['ClassId'])
    #     local_evc_service.sign_out()
    #     assert_that(jmespath.search("ClassId", response.json()) == self.after_report_info['ClassId'])
    #     assert_that(response.json(), match_to("Comment"))
    #     assert_that(response.json(), match_to("Improvement"))
    #     assert_that(response.json(), match_to("Suggestion"))
    # 
    # @Test(tags='qa')
    # def book_class_error_code_with_not_enough_och(self):
    #     self.test_login()
    #     local_evc_service = KidsEVCService(host=self.host)
    #     response = local_evc_service.login(user_name=self.user_with_zero_och["UserName"],
    #                                        password=self.user_with_zero_och["Password"])
    #     student_id = jmespath.search("UserInfo.UserInfo.UserId", response)
    #     calendar_response = local_evc_service.get_calendar("HF", ClassType.REGULAR.value,
    #                                                        local2utc(self.regular_start_time),
    #                                                        local2utc(self.regular_end_time))
    #     session_start_time = jmespath.search("BookableSlots[0].StartStamp", calendar_response.json())
    #     session_end_time = jmespath.search("BookableSlots[0].EndStamp", calendar_response.json())
    #     class_session_response = local_evc_service.get_available_online_class_session(None, None,
    #                                                                                   self.HF_program_code
    # 
    #                                                                                   )
    #     teacher_id = jmespath.search("[0].TeacherProfile.UserInfo.UserId", class_session_response.json())
    #     class_id = jmespath.search("[0].ClassId", class_session_response.json())
    #     program_code = jmespath.search("[0].ProgramCode", class_session_response.json())
    # 
    #     response = local_evc_service.book_class("C", "2", "2", session_start_time, session_end_time, teacher_id,
    #                                             program_code,
    #                                             ClassType.REGULAR.value,
    #                                             class_id,
    #                                             True,
    #                                             student_id,
    #                                             "Begin")
    #     local_evc_service.sign_out()
    #     assert_that(jmespath.search("Code.Major", response.json()) == 403)
    #     assert_that(jmespath.search("Code.Minor", response.json()) == '600')
    # 
    # @Test(tags='qa')
    # def book_class_error_code_with_not_topic(self):
    #     student_id = jmespath.search("UserInfo.UserInfo.UserId", self.test_login().json())
    #     calendar_response = self.evc_service.get_calendar("HF", ClassType.REGULAR.value,
    #                                                       local2utc(self.regular_start_time),
    #                                                       local2utc(self.regular_end_time))
    #     session_start_time = jmespath.search("BookableSlots[0].StartStamp", calendar_response.json())
    #     session_end_time = jmespath.search("BookableSlots[0].EndStamp", calendar_response.json())
    #     class_session_response = self.evc_service.get_available_online_class_session(None, None,
    #                                                                                  self.HF_program_code
    #                                                                                  )
    #     teacher_id = jmespath.search("[0].TeacherProfile.UserInfo.UserId", class_session_response.json())
    #     class_id = jmespath.search("[0].ClassId", class_session_response.json())
    #     program_code = jmespath.search("[0].ProgramCode", class_session_response.json())
    # 
    #     response = self.evc_service.book_class("z", "2", "2", session_start_time, session_end_time, teacher_id,
    #                                            program_code,
    #                                            ClassType.REGULAR.value,
    #                                            class_id,
    #                                            True,
    #                                            student_id,
    #                                            "Begin")
    # 
    #     assert_that(jmespath.search("Code.Major", response.json()) == 403)
    #     assert_that(jmespath.search("Code.Minor", response.json()) == '601')
    # 
    # @Test(tags='qa')
    # def cancel_class_error_code_with_booking_not_found(self):
    #     student_id = jmespath.search("UserInfo.UserInfo.UserId", self.test_login().json())
    #     class_session_response = self.evc_service.get_available_online_class_session(None, None,
    #                                                                                  self.HF_program_code,
    #                                                                                  ClassType.REGULAR.value
    #                                                                                  )
    #     class_id = jmespath.search("[0].ClassId", class_session_response.json())
    #     response = self.evc_service.cancel_class(class_id)
    # 
    #     assert_that(jmespath.search("Code.Major", response.json()) == 403)
    #     assert_that(jmespath.search("Code.Minor", response.json()) == '610')
    # 
    # @Test(tags='qa')
    # def cancel_class_error_code_with_wrong_class_id(self):
    #     self.test_login()
    #     response = self.evc_service.cancel_class("30789")
    # 
    #     assert_that(jmespath.search("Code.Major", response.json()) == 500)

    @Test(tags='qa,stg,live')
    def save_policy_agreement(self):
        self.test_login()
        response = self.evc_service.save_policy_agreement()
        assert_that(response.status_code == 204)

    @Test(tags='qa,stg,live')
    def save_orientation_info(self):
        self.test_login()
        orientation_info = [
            {"courseType": "HF", "packageType": "24", "courseTypeLevelCode": "C","isActive":True, "unitNumber": "1", "lessonNumber": "1"}]
        response = self.evc_service.update_orientation_info(orientation_info)
        assert_that(response.status_code == 200)
