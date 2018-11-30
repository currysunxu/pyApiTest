import os

from hamcrest import assert_that, equal_to
from ptest.decorator import TestClass, BeforeClass, Test

from E1_API_Automation.Business.SISEVC import SISEVCService
from E1_API_Automation.Lib.ScheduleClassTool import ServiceSubTypeCode, local2est



@TestClass()
class QuickBook():

    '''
    os.environ['test_env'] = "QA"
    os.environ['teacher_id'] = "10274591"
    os.environ['student_id'] = "12226258"
    os.environ['start_time'] = "2018-11-29 10:00:00"
    os.environ['end_time'] = "2018-11-29 18:00:00"
    '''

    if os.environ["test_env"] == "QA":
        SIS_SERVICE = 'http://internal-e1-evc-booking-qa-cn.ef.com'
    elif os.environ["test_env"] == "STG":
        SIS_SERVICE = 'http://internal-e1-evc-booking-stg-cn.ef.com'

    est_start_time = local2est(os.environ['start_time'])
    est_end_time = local2est(os.environ['end_time'])

    @BeforeClass()
    def create_service(self):
        self.service = SISEVCService(self.SIS_SERVICE)

    def assign_class(self):
        from E1_API_Automation.Test.OnlineStudentPortal.EVCBaseClass import EVCBase
        evc_base = EVCBase()
        class_list = evc_base.create_and_assign_class(self.est_start_time, self.est_end_time,
                                                      teacher_id=os.environ['teacher_id'],
                                                      test_env=os.environ['test_env'],
                                                      subServiceType=ServiceSubTypeCode.KONRegular.value,
                                                      partner_code="Any", level_code="Any", market_code="Any",
                                                      evc_server_code="evccn1")
        return class_list

    @Test()
    def test_book_class(self):
        class_list = self.assign_class()

        if type(class_list) == list:
            for class_id in class_list:
                book_response = self.service.post_bookings(class_id=class_id, teacher_id=os.environ['teacher_id'],
                                                      student_id=os.environ['student_id'], course_type="HF", level_code="C",
                                                      unit_number="1", lesson_number="1", class_type="Regular")
                assert_that(book_response.status_code, equal_to(204))

        elif type(class_list) == int:
                book_response = self.service.post_bookings(class_id=str(class_list), teacher_id=os.environ['teacher_id'],
                                                               student_id=os.environ['student_id'], course_type="HF",
                                                               level_code="C",
                                                               unit_number="1", lesson_number="1", class_type="Regular")
                assert_that(book_response.status_code, equal_to(204))
