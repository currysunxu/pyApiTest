from ...Business.SISEVC import SISEVCService
from ptest.decorator import TestClass, Test, BeforeClass
from ...Lib.HamcrestMatcher import match_to
from ...Lib.HamcrestExister import exist

from hamcrest import assert_that, equal_to, instance_of
import jmespath
from ...Settings import SIS_SERVICE

test_student_id = 12226094
test_teacher_ids = [10703777, 10366576]


@TestClass()
class TestSisEVCService:
    @BeforeClass()
    def create_service(self):
        self.service = SISEVCService(SIS_SERVICE)

    @Test()
    def test_enroll_course(self):
        response = self.service.enroll_course_credits(test_student_id, ["HF"])
        assert_that(response.status_code, equal_to(204))
        assert_that(response.content, equal_to(b''))

    @Test()
    def test_get_teacher_profile_response_status(self):
        response = self.service.get_teacher_profiles(test_teacher_ids)
        assert_that(response.status_code, equal_to(200))

    @Test()
    def test_get_teacher_profile(self):
        response = self.service.get_teacher_profiles(test_teacher_ids)
        assert_that(len(response.json()), 2)

    @Test()
    def test_get_teacher_profile_schema(self):
        response = self.service.get_teacher_profiles(test_teacher_ids).json()[0]
        assert_that(response, match_to("teacherId"))
        assert_that(response, match_to("displayName"))
        assert_that(response, match_to("gender"))
        assert_that(response, match_to("avatarUrl"))
        assert_that(response, match_to("selfIntroduction"))
        assert_that(jmespath.search('teacherId', response), equal_to(test_teacher_ids[0]))

    @Test()
    def test_student_credit_status(self):
        response = self.service.get_student_credits(test_student_id)
        assert_that(response.status_code, equal_to(200))

    @Test()
    def test_student_credit_logic(self):
        response = self.service.get_student_credits(test_student_id)
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
        response = self.service.get_available_time_slot(30, test_student_id, 'HF', 'Regular')
        assert_that(response.status_code, equal_to(200))

    @Test()
    def test_get_available_time_slots_status(self):
        response = self.service.get_available_time_slot(30, test_student_id, 'HF', 'Regular')
        assert_that(response.status_code, equal_to(200))

    @Test()
    def test_get_available_time_slots_schema(self):
        response = self.service.get_available_time_slot(30, test_student_id, 'HF', 'Regular').json()[0]
        assert_that(response, match_to("classType"))
        assert_that(response, match_to("courseType"))
        assert_that(response, match_to("startDateTimeUtc"))
        assert_that(response, match_to("endDateTimeUtc"))

    @Test()
    def test_get_available_time_slots_logic(self):
        response = self.service.get_available_time_slot(30, test_student_id, 'HF', 'Regular').json()
        for evc_class in response:
            assert_that(jmespath.search('classType', evc_class), equal_to('Regular'))
            assert_that(jmespath.search('courseType', evc_class), equal_to('HF'))

    @Test()
    def test_get_bookable_class_status(self):
        response = self.service.get_available_class(30, test_student_id, 'HF', 'Regular')
        assert_that(response.status_code, equal_to(200))

    @Test()
    def test_get_bookable_class_schema(self):
        response = self.service.get_available_class(30, test_student_id, 'HF', 'Regular').json()[0]
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
        available_class = self.service.get_available_class(30, test_student_id, 'HF', 'Regular').json()[0]
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
        history = self.service.get_student_book_history(test_student_id, '2018-02-01', 'Hf', "Regular")
        assert_that(history.status_code, equal_to(200))

    @Test()
    def test_get_student_booking_history_schema(self):
        history = self.service.get_student_book_history(test_student_id, '2018-02-01', 'Hf', "Regular").json()
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
        response = self.service.get_student_credit_history(test_student_id)
        assert_that(response.status_code, equal_to(200))

    @Test()
    def test_get_student_credits_history_schema(self):
        response = self.service.get_student_credit_history(test_student_id).json()[0]
        assert_that(response, match_to("studentId"))
        assert_that(response, match_to("courseType"))
        assert_that(response, match_to("operationType"))
        assert_that(response, match_to("classType"))
        assert_that(response, exist("classId"))
        assert_that(response, exist("operatedDateTimeUtc"))
        assert_that(response, exist("operateAmount"))
        assert_that(response, exist("classStartDateTimeUTC"))
        assert_that(response, match_to("classEndDateTimeUTC"))

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
