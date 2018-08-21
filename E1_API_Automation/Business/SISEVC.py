import requests
import arrow


class SISEVCService:
    def __init__(self, host):
        self.host = host
        self.session = requests.session()
        self.header = {"Content-Type": "application/json"}

    def enroll_course_credits(self, student_id, course_type):
        json = {
            "studentId": student_id,
            "courseTypes": course_type
        }
        url = self.host + '/api/v1/credits'
        response = self.session.post(url=url, json=json, verify=False, headers=self.header)
        return response

    def get_teacher_profiles(self, teacher_ids):
        url = self.host + '/api/v1/teacher-profiles?'
        for teacher in teacher_ids:
            url = url + 'ids=' + str(teacher) + '&'

        url = url[:len(url) - 1]

        return self.session.get(url=url, verify=False, headers=self.header)

    def get_student_credits(self, student_id):
        url = self.host + '/api/v1/students/%s/credits' % str(student_id)
        return self.session.get(url=url, verify=False, headers=self.header)

    def get_course_lesson_topic(self, course_type, course_level_code):
        url = self.host + '/api/v1/course-lessons?CourseType=%s&CourseLevelCode=%s' % (course_type, course_level_code)
        return self.session.get(url=url, verify=False, headers=self.header)

    def get_available_time_slot(self, duration_days, student_id, course_type, class_type, region='CN'):
        url = self.host + '/api/v1/available-time-slots?StartDateTimeUtc=%s&EndDateTimeUtc=%s&StudentId=%s&Region=%s&CourseType=%s&ClassType=%s'
        utc = arrow.utcnow().shift(days=+1)
        start_time = utc.format('YYYY-MM-DD HH:mm')
        duration_days = duration_days + 1
        end_time = utc.shift(days=+ duration_days).format('YYYY-MM-DD HH:mm')
        url = url % (start_time, end_time, student_id, region, course_type, class_type)
        print(url)
        return self.session.get(url=url, verify=False, headers=self.header)

    def get_available_class(self, duration_days, student_id, course_type, class_type, region='CN'):
        url = self.host + '/api/v1/available-classes?StartDateTimeUtc=%s&EndDateTimeUtc=%s&StudentId=%s&Region=%s&CourseType=%s&ClassType=%s'
        utc = arrow.utcnow().shift(days=+1)
        start_time = utc.format('YYYY-MM-DD HH:mm')
        duration_days = duration_days + 1
        end_time = utc.shift(days=+ duration_days).format('YYYY-MM-DD HH:mm')
        url = url % (start_time, end_time, student_id, region, course_type, class_type)
        print(url)
        return self.session.get(url=url, verify=False, headers=self.header)

    def post_bookings(self, class_id, teacher_id, student_id, course_type, level_code, lesson_number, class_type):
        json = {
            "classId": class_id,
            "teacherId": teacher_id,
            "studentId": student_id,
            "region": "CN",
            "requiredCredits": 1,
            "courseType": course_type,
            "courseTypeLevelCode": level_code,
            "unitNumber": 2,
            "lessonNumber": lesson_number,
            "classType": class_type,
            "classLimit": 9999,
            "studentNeedRecord": True
        }
        url = self.host + '/api/v1/bookings'
        header = {"Content-Type": "application/json",
                  "Accept": "text/plain"
                  }
        return self.session.post(url=url, json=json, verify=False, headers=header)

    def get_evc_class_url(self, class_id, student_id):
        url = self.host + '/api/v1/evc/classrooms'
        json = {
            "classId": class_id,
            "studentId": student_id
        }
        return self.session.post(url=url, json=json, verify=False, headers=self.header)

    def get_class_info(self, evc_booking_classid):
        url = self.host + '/api/v1/classes/%s' % evc_booking_classid
        return self.session.get(url=url, verify=False, headers=self.header)

    def get_student_book_history(self, student_id, start_date, course_type, class_type):
        end_time = arrow.utcnow().format('YYYY-MM-DD HH:mm')
        url = self.host + '/api/v1/students/%s/booking-history?StartDateTimeUtc=%s&EndDateTimeUtc=%s&CourseType=%s&ClassTypes=%s'
        url = url % (student_id, start_date, end_time, course_type, class_type)
        return self.session.get(url=url, verify=False, headers=self.header)

    def get_student_credit_history(self, student_id):
        url = self.host + '/api/v1/students/%s/credits-history' % student_id
        return self.session.get(url=url, verify=False, headers=self.header)

    def get_class_video_record_url(self, class_id):
        url = self.host + '/api/v1/classes/%s/video-record-url' % class_id
        return self.session.get(url=url, verify=False, headers=self.header)

    def get_EF_classroom_app_info(self):
        url = self.host + '/api/v1/classroom-app'
        return self.session.get(url=url, verify=False, headers=self.header)

    def delete_class(self, class_id, student_id):
        url = '/api/v1/bookings?ClassId=%s&StudentId=%s' % class_id, student_id
        return self.session.delete(url, verify=False, headers=self.header)

    def get_student_profile(self, student_id):
        url = 'api/v1/students/%s/evc-profile' % student_id
        return self.session.get(url=url, verify=False, headers=self.header)
