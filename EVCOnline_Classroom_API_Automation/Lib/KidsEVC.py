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

    def book_class(self, book_code, lesson_number, start_stamp, end_stamp, teacher_id, program_code, class_type,
                   class_id, need_recoder, student_id, state):
        body = {
            "BookCode": book_code,
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

    def sign_out(self):
        return self.mou_tai.delete(url="/api/v2/Token/")
