import datetime
import random

import jmespath
from hamcrest import assert_that

from E1_API_Automation.Business.KidsEVC import KidsEVCService
from E1_API_Automation.Settings import KSD_ENVIRONMENT


class EVCUtils:
    @staticmethod
    def schedule_evc_pl(id_token, start_date, course_type, class_type ='Regular'):
        evc_service = KidsEVCService(KSD_ENVIRONMENT)
        evc_service.mou_tai.headers['X-EF-TOKEN'] = id_token

        date_time_format = "%Y-%m-%dT%H:%M:%S.%fZ"


        # schedule a pl class for testing
        schedule_success = False
        while not schedule_success:
            evc_start_time_utc = start_date + datetime.timedelta(hours=1)
            # make the evc start time with zero minutes, seconds
            evc_start_time_utc = datetime.datetime(evc_start_time_utc.year, evc_start_time_utc.month,
                                                   evc_start_time_utc.day, evc_start_time_utc.hour, 0, 0, 0)
            evc_start_time_utc_str = evc_start_time_utc.strftime(date_time_format)
            evc_end_time_utc_str = (evc_start_time_utc + datetime.timedelta(minutes=30)).strftime(date_time_format)
            available_teachers_response = evc_service.get_all_available_teachers(
                evc_start_time_utc_str,
                evc_end_time_utc_str,
                course_type=course_type,
                class_type=class_type,
                page_index=0, page_size=10)
            # randomly choose a teacher so will not conflict when create another class
            available_teachers_list = available_teachers_response.json()
            random_teacher_index = random.randint(0, len(available_teachers_list) - 1)
            teacher_id = jmespath.search("[{0}].teacherId".format(random_teacher_index),
                                         available_teachers_response.json())
            try:
                book_response = evc_service.book_class(evc_start_time_utc_str,
                                                       evc_end_time_utc_str,
                                                       teacher_id, course_type= course_type,
                                                       class_type=class_type,
                                                       course_type_level_code='C', unit_number="1",
                                                       lesson_number="1", is_reschedule="true")

                assert_that(book_response.status_code == 201)
                schedule_success = True
            except:
                start_date = start_date + datetime.timedelta(hours=1)

        return book_response.json()