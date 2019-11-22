import random

from ..Lib.Moutai import Moutai, Token
from .AuthService import AuthService
from E1_API_Automation.Settings import AuthEnvironment,env_key
import jmespath
import requests




class KidsEVCService():

    def __init__(self, host):
        self.host = host
        print(self.host)
        self.mou_tai = Moutai(host=self.host, token=Token("X-BA-TOKEN", "Token"))

    def login(self, user_name, password):
        auth = AuthService(getattr(AuthEnvironment,env_key))
        id_token = auth.login(user_name, password).json()['idToken']
        ba_token = auth.get_v3_token(id_token)
        headers = {"X-BA-TOKEN": ba_token, "Content-Type": "application/json"}
        self.mou_tai.set_header(headers)
        return ba_token

    def get_offline_active_groups(self):
        return self.mou_tai.get("/ksdsvc/api/v2/groups")

    def get_offline_group_sessions(self, group_id):
        return self.mou_tai.get("/ksdsvc/api/v2/groups/"+group_id+"/offline-sessions")

    def get_user_profile(self):
        return self.mou_tai.get("/ksdsvc/api/v2/student/profile/")

    def get_credits(self):
        return self.mou_tai.get("/ksdsvc/api/v2/student/credits")

    def cancel_class(self, class_id):
        api_url = "/ksdsvc/api/v2/classes/" + class_id
        return self.mou_tai.delete(api_url)

    def get_course_lesson_structure(self,class_type, course_type):
        return self.mou_tai.get("/ksdsvc/api/v2/lessons?classType={0}&courseType={1}".format(class_type, course_type))

    def get_after_class_report(self, class_id):
        api_url = "/ksdsvc/api/v2/classes/{0}/acr".format(class_id)
        return self.mou_tai.get(api_url)

    def change_topic(self, class_id, course_type, class_type, courseTypeLevelCode, unit_number, lesson_number, region="CN"):
        body = {
            "bookingTopics": [
                {
                    "classId": class_id,
                    "courseType": course_type,
                    "classType": class_type,
                    "courseTypeLevelCode": courseTypeLevelCode,
                    "unitNumber": unit_number,
                    "lessonNumber": lesson_number,
                    "region": region,
                }
            ]
        }
        return self.mou_tai.put("/ksdsvc/api/v2/classes/lesson", json=body)

    def sign_out(self):
        return self.mou_tai.delete(url="/api/v1/Token/")

    def block_booking_teacher_search(self, start_date_time, end_date_time, course_type, unit_number, lesson_number):
        random_num = random.randint(0, 23)
        params = {
            'StartDateTimeUtc': start_date_time,
            'EndDateTimeUtc': end_date_time,
            'StartTime': str(random_num) + ":00",
            'EndTime': str(random_num) + ":30",
            'CourseLesson.ClassType': 'Regular',
            'CourseLesson.CourseType': course_type,
            'CourseLesson.CourseTypeLevelCode': 'C',
            'CourseLesson.UnitNumber': unit_number,
            'CourseLesson.LessonNumber': lesson_number,
            'CourseLesson.RegionCode': 'CN'
        }
        return self.mou_tai.get(url="/ksdsvc/api/v2/block-booking/teachers", params=params)

    def block_booking_search_by_weekday_timeslot(self, course_type, time_slots):
        json = {
            "timeSlots": time_slots
        }
        return self.mou_tai.post(url="/ksdsvc/api/v3/block-booking/teachers?courseType={0}&classType=Regular&regionCode=CN&PageIndex=0&PageSize=10".format(course_type),json=json)


    def block_booking_v3(self, course_type,course_type_level_code, teacher_id, book_slots):
        json = {
            "teacherId": teacher_id,
            "timeSlots": book_slots
        }
        return self.mou_tai.post(url="/ksdsvc/api/v3/block-booking?courseType={0}&courseTypeLevelCode={1}&classType=Regular&regionCode=CN".format(course_type, course_type_level_code), json=json)

    def block_booking_search_by_weekday_timeslot_teacher(self):
        return


    def block_booking(self, start_data_time, end_date_time, course_type):
        random_num = random.randint(0, 23)
        json = {
            "teacherMemberId": 10274591,
            "startDateTimeUtc": start_data_time,
            "endDateTimeUtc": end_date_time,
            "startTime": str(random_num) + ":00",
            "endTime": str(random_num) + ":30",
            "courseLesson": {
                "courseType": course_type,
                "courseTypeLevelCode": "C",
                "unitNumber": "1",
                "lessonNumber": "1",
                "classType": "Regular",
                "regionCode": "CN"
            }
        }
        return self.mou_tai.post(url="/ksdsvc/api/v2/block-booking", json=json), json

    def duplicate_block_booking(self, json):
        return self.mou_tai.post(url="/ksdsvc/api/v2/block-booking", json=json)

    def save_policy_agreement(self):
        json = {"product":"8","privacyDocumentId":3}
        return self.mou_tai.post(url = "/api/v2/PrivacyPolicy/StudentPrivacyPolicyAgreement", json = json)
    
    def student_evc_profile(self, host):
        student_id = jmespath.search('userInfo.userId',self.get_user_profile().json())
        print(student_id)
        response = requests.get(url=host +'/api/v1/students/Kids_{0}/evc-profile'.format(student_id), verify=False, headers={"Content-Type": "application/json"})

        return response

    def get_all_available_teachers(self, start_stamp, end_stamp, course_type, class_type, page_index, page_size):
        return self.mou_tai.get("/ksdsvc/api/v2/timeslots/" + start_stamp + "_" + end_stamp + "/teachers?courseType={0}&classType={1}&PageIndex={2}&PageSize={3}".format(course_type, class_type, page_index, page_size))

    def book_class(self, start_stamp, end_stamp, teacher_id, course_type, class_type, course_type_level_code, unit_number, lesson_number, is_reschedule, region="CN"):
        body = {
            "startDateTimeUtc": start_stamp,
            "endDateTimeUtc": end_stamp,
            "teacherId": teacher_id,
            "courseType": course_type,
            "classType": class_type,
            "courseTypeLevelCode": course_type_level_code,
            "unitNumber": unit_number,
            "lessonNumber": lesson_number,
            "regionCode": region,
            "isReschedule": is_reschedule
        }
        return self.mou_tai.post("/ksdsvc/api/v2/bookings", json=body)

    def query_booking_history(self, course_type, class_types):
        return self.mou_tai.get("/ksdsvc/api/v2/student/classes?courseType={0}&classTypes={1}".format(course_type, class_types))

    def get_app_download_url(self):
        return self.mou_tai.get("/ksdsvc/api/v2/classroom/app-info")
