import random

from ..Lib.Moutai import Moutai, Token


class KidsEVCService():

    def __init__(self, host):
        self.host = host
        self.mou_tai = Moutai(host=self.host, token=Token("X-BA-TOKEN", "Token"))
    def login(self, user_name, password):
        user_info = {
            "UserName": user_name,  # "jenkin0528tb",
            "Password": password,  # "12345",
            "DeviceType": 0,
            "Platform": 0
        }
        return self.mou_tai.set_request_context("post", user_info, "/api/v2/Authentication/OnlineStudentPortal/")

    def get_calendar(self, program_code, class_type, start_stamp, end_stamp):
        body = {
            "ProgramCode": program_code,
            "ClassType": class_type,
            "StartStamp": start_stamp,
            "EndStamp": end_stamp
        }
        return self.mou_tai.post("/api/v2/OnlineClassroomCalendar/", json=body)

    def get_available_online_class_session(self, start_stamp, end_stamp, program_code, class_type, student_id):
        body = {
            "StartStamp": start_stamp,
            "EndStamp": end_stamp,
            "ProgramCode": program_code,
            "ClassType": class_type,
            "StudentId": student_id
        }

        return self.mou_tai.post("/api/v2/OnlineClassSession/", json=body)

    def get_OCH_credit(self, student_id, program_code):
        body = {
            "StudentId": student_id,
            "ProgramCode": program_code
        }
        return self.mou_tai.post("/api/v2/OCHCreditSummary/", json=body)

    def book_class(self, book_code, unit_number, lesson_number, start_stamp, end_stamp, teacher_id, program_code,
                   class_type,
                   class_id, need_recoder, student_id, state):
        body = {
            "BookCode": book_code,
            "UnitNumber": unit_number,
            "LessonNumber": lesson_number,
            "StartStamp": start_stamp,
            "EndStamp": end_stamp,
            "TeacherId": teacher_id,
            "ProgramCode": program_code,
            "ClassType": class_type,
            "ClassId": class_id,
            "NeedRecord": need_recoder,
            "UserId": student_id,
            "State": state
        }

        return self.mou_tai.put("/api/v2/OnlineClassBooking/", json=body)

    def cancel_class(self, class_id):
        api_url = "/api/v2/OnlineClassBooking/" + class_id
        return self.mou_tai.delete(api_url)

    def get_lesson_suggestion(self, program_code):
        api_url = "/api/v2/SuggestionLesson/" + program_code
        return self.mou_tai.get(api_url)

    def get_online_student_book_structure(self, program_code):
        api_url = "/api/v2/OnlineBookStructure/" + program_code
        return self.mou_tai.get(api_url)

    def query_online_class_booking(self, start_stamp, end_stamp, program_code, class_type):
        body = {
            "StartStamp": start_stamp,
            "EndStamp": end_stamp,
            "ProgramCode": program_code,
            "ClassType": class_type
        }

        return self.mou_tai.post(url="/api/v2/OnlineClassBooking/", json=body)

    def get_after_class_report(self, class_id):
        api_url = "/api/v2/AfterClassReport/" + class_id
        return self.mou_tai.get(api_url)

    def change_topic(self, student_id, book_code, unit_number, lesson_number, start_stamp, end_stamp, teacher_id,
                     program_code, class_type,
                     class_id, need_recoder):
        body = {
            "StudentId": student_id,
            "BookCode": book_code,
            "UnitNumber": unit_number,
            "LessonNumber": lesson_number,
            "StartStamp": start_stamp,
            "EndStamp": end_stamp,
            "TeacherId": teacher_id,
            "ProgramCode": program_code,
            "ClassType": class_type,
            "ClassId": class_id,
            "NeedRecord": need_recoder
        }
        return self.mou_tai.post(url="/api/v2/OnlineClassroom/Topic/", json=body)

    def sign_out(self):
        return self.mou_tai.delete(url="/api/v2/Token/")

    def block_booking_teacher_search(self, start_date_time, end_date_time, course_type, package_type, unit_number, lesson_number):
        random_num = random.randint(0, 23)
        params = {
            'StartDateTimeUtc': start_date_time,
            'EndDateTimeUtc': end_date_time,
            'StartTime': str(random_num) + ":00",
            'EndTime': str(random_num) + ":30",
            'CourseLesson.BookCode': 'C',
            'CourseLesson.ClassType': 'Regular',
            'CourseLesson.CourseType': course_type,
            'CourseLesson.LessonNumber': lesson_number,
            'CourseLesson.PackageType': package_type,
            'CourseLesson.RegionCode': 'CN',
            'CourseLesson.UnitNumber': unit_number,
        }
        return self.mou_tai.get(url="/ksdsvc/api/v2/block-booking/teachers", params=params)

    def block_booking(self, start_data_time, end_date_time, course_type, package_type):
        random_num = random.randint(0, 23)
        json = {
            "teacherMemberId": 10274591,
            "startDateTimeUtc": start_data_time,
            "endDateTimeUtc": end_date_time,
            "startTime": str(random_num) + ":00",
            "endTime": str(random_num) + ":30",
            "courseLesson": {
                "courseType": course_type,
                "packageType": package_type,
                "bookCode": "C",
                "unitNumber": "1",
                "lessonNumber": "1",
                "classType": "Regular",
                "regionCode": "CN"
            }
        }
        return self.mou_tai.post(url="/ksdsvc/api/v2/block-booking", json=json), json

    def duplicate_block_booking(self, json):
        return self.mou_tai.post(url="/ksdsvc/api/v2/block-booking", json=json)
