from E1_API_Automation.Business.SISEVC import SISEVCService
from ptest.decorator import TestClass, Test, BeforeClass
from E1_API_Automation.Lib.HamcrestMatcher import match_to
from E1_API_Automation.Lib.HamcrestExister import exist

from hamcrest import assert_that, equal_to, instance_of
import jmespath
from ...Test.OnlineStudentPortal.EVCBaseClass import EVCBase


@TestClass()
class TestSisEVCService(EVCBase):
    @BeforeClass()
    def create_service(self):
        self.service = SISEVCService(self.SIS_SERVICE)

    @Test()
    def test_enroll_course(self):
        response = self.service.enroll_course_credits(self.sis_test_student, ["HF"])
        assert_that(response.status_code, equal_to(204))
        r = self.service.get_student_credits(self.sis_test_student)
        student_rolled_credts = jmespath.search("[?courseType=='HF']", r.json())
        enroll_course = jmespath.search("[?classType == 'Demo']", student_rolled_credts)
        assert_that(response.content, equal_to(b''))
        assert_that(len(enroll_course) == 1)
        assert_that(jmespath.search('available', enroll_course[0]) > 0)

    @Test()
    def test_get_teacher_profile_response_status(self):
        response = self.service.get_teacher_profiles(self.sis_test_teacher_list)
        assert_that(response.status_code, equal_to(200))

    @Test()
    def test_get_teacher_profile(self):
        response = self.service.get_teacher_profiles(self.sis_test_teacher_list)
        assert_that(len(response.json()), 2)

    @Test()
    def test_get_teacher_profile_schema(self):
        response = self.service.get_teacher_profiles(self.sis_test_teacher_list).json()
        assert_that(response[0], match_to("teacherId"))
        assert_that(response[0], match_to("displayName"))
        assert_that(response[0], exist("gender"))
        assert_that(response[0], match_to("avatarUrl"))
        assert_that(response[0], match_to("selfIntroduction"))
        response_ids = sorted(map(lambda x: x['teacherId'], response))
        assert_that(response_ids, equal_to(sorted(self.sis_test_teacher_list)))

    @Test()
    def test_student_credit_status(self):
        response = self.service.get_student_credits(self.sis_test_student)
        assert_that(response.status_code, equal_to(200))

    @Test()
    def test_student_credit_logic(self):
        response = self.service.get_student_credits(self.sis_test_student)
        assert_that(response.json(), instance_of(list))

    @Test()
    def test_get_course_lesson_status(self):
        response = self.service.get_course_lesson_topic('HF', 'C')
        assert_that(response.status_code, equal_to(200))

    @Test()
    def test_get_course_Lesson_logic(self):
        response = self.service.get_course_lesson_topic('HF', 'D')
        assert_that(len(response.json()), equal_to(24))

    @Test()
    def test_get_course_Lesson_schema(self):
        response = self.service.get_course_lesson_topic('HF', 'F').json()[0]
        assert_that(response, match_to("courseType"))
        assert_that(response, match_to("courseLevelCode"))
        assert_that(response, match_to("unitNumber"))
        assert_that(response, match_to("topicId"))
        assert_that(response, match_to("lessonNumber"))
        assert_that(response, match_to("topicStatement"))

    @Test()
    def test_get_available_time_slots_status(self):
        response = self.service.get_available_time_slot(30, self.sis_test_student, 'HF', 'Regular')
        assert_that(response.status_code, equal_to(200))

    @Test()
    def test_get_available_time_slots_status(self):
        response = self.service.get_available_time_slot(30, self.sis_test_student, 'HF', 'Regular')
        assert_that(response.status_code, equal_to(200))

    @Test()
    def test_get_available_time_slots_schema(self):
        response = self.service.get_available_time_slot(30, self.sis_test_student, 'HF', 'Regular').json()[0]
        assert_that(response, match_to("classType"))
        assert_that(response, match_to("courseType"))
        assert_that(response, match_to("startDateTimeUtc"))
        assert_that(response, match_to("endDateTimeUtc"))

    @Test()
    def test_get_available_time_slots_logic(self):
        response = self.service.get_available_time_slot(30, self.sis_test_student, 'HF', 'Regular').json()
        for evc_class in response:
            assert_that(jmespath.search('classType', evc_class), equal_to('Regular'))
            assert_that(jmespath.search('courseType', evc_class), equal_to('HF'))

    @Test()
    def test_get_bookable_class_status(self):
        response = self.service.get_available_class(30, self.sis_test_student, 'HF', 'Regular')
        assert_that(response.status_code, equal_to(200))

    @Test()
    def test_get_bookable_class_schema(self):
        response = self.service.get_available_class(30, self.sis_test_student, 'HF', 'Regular').json()[0]
        assert_that(response, match_to("classId"))
        assert_that(response, match_to("courseType"))
        assert_that(response, match_to("startDateTimeUtc"))
        assert_that(response, match_to("endDateTimeUtc"))
        assert_that(response, match_to("classType"))
        assert_that(response, exist("roomId"))
        assert_that(response, exist("teacherProfile.avatarUrl"))
        assert_that(response, exist("teacherProfile.selfIntroduction"))
        assert_that(response, exist("teacherProfile.displayName"))
        assert_that(response, exist("teacherProfile.gender"))
        assert_that(response, match_to("teacherProfile.teacherId"))
        assert_that(response, match_to("teacherProfile"))

    @Test()
    def test_get_class_info(self):
        available_class = self.service.get_available_class(30, self.sis_test_student, 'HF', 'Regular').json()[0]
        class_id = jmespath.search('classId', available_class)
        class_detail = self.service.get_class_info(class_id)
        print(class_detail.json())
        assert_that(class_detail.status_code, equal_to(200))
        assert_that(class_detail.json(), match_to('classId'))
        assert_that(class_detail.json(), match_to('startDateTimeUTC'))
        assert_that(class_detail.json(), match_to('endDateTimeUTC'))
        assert_that(class_detail.json(), match_to('teacherId'))
        assert_that(class_detail.json(), exist('studentId'))

    @Test()
    def test_get_student_booking_history_status(self):
        history = self.service.get_student_book_history(self.sis_test_student, '2018-02-01', 'Hf', "Regular")
        assert_that(history.status_code, equal_to(200))

    @Test()
    def test_get_student_booking_history_schema(self):
        history = self.service.get_student_book_history(self.sis_test_student, '2018-02-01', 'Hf', "Regular").json()
        assert_that(history[0], match_to('classId'))
        assert_that(history[0], match_to('classStatus'))
        assert_that(history[0], match_to('classType'))
        assert_that(history[0], match_to('classStatusReason'))
        assert_that(history[0], match_to('courseLevelCode'))
        assert_that(history[0], match_to("courseType"))
        assert_that(history[0], match_to('endDateTimeUtc'))
        assert_that(history[0], match_to('startDateTimeUtc'))
        assert_that(history[0], match_to('studentId'))
        assert_that(history[0], match_to('teacherId'))
        assert_that(history[0], match_to('unitNumber'))
        assert_that(history[0], match_to('topicId'))
        assert_that(history[0], match_to('lessonNumber'))

    @Test()
    def test_get_student_credits_history_status(self):
        response = self.service.get_student_credit_history(self.sis_test_student)
        assert_that(response.status_code, equal_to(200))

    @Test()
    def test_get_student_credits_history_schema(self):
        response = self.service.get_student_credit_history(self.sis_test_student).json()[0]
        assert_that(response, match_to("studentId"))
        assert_that(response, match_to("courseType"))
        assert_that(response, match_to("operationType"))
        assert_that(response, match_to("classType"))
        assert_that(response, exist("classId"))
        assert_that(response, exist("operatedDateTimeUtc"))
        assert_that(response, exist("operateAmount"))
        assert_that(response, exist("classStartDateTimeUTC"))
        assert_that(response, exist("classEndDateTimeUTC"))

    @Test()
    def test_get_ef_classroom_app_status(self):
        response = self.service.get_EF_classroom_app_info()
        assert_that(response.status_code, equal_to(200))
        assert_that(response.json(), match_to("android.minSupportedOSVersion"))
        assert_that(response.json(), match_to("android.downloadLink"))
        assert_that(response.json(), match_to("android.appLink"))
        assert_that(response.json(), match_to("iOS.minSupportedOSVersion"))
        assert_that(response.json(), exist("iOS.downloadLink"))
        assert_that(response.json(), match_to("iOS.appLink"))
        assert_that(response.json(), exist("errorCode"))
