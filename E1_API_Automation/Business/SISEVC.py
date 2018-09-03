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
        url = self.host + '/api/v1/course-lessons?CourseType={0}&CourseLevelCode={1}'.format(course_type, course_level_code)
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
        url = self.host + '/api/v1/available-classes?StartDateTimeUtc={0}&EndDateTimeUtc={1}&StudentId={2}&Region={3}&CourseType={4}&ClassType={5}'
        utc = arrow.utcnow().shift(days=+1)
        start_time = utc.format('YYYY-MM-DD HH:mm')
        duration_days = duration_days + 1
        end_time = utc.shift(days=+ duration_days).format('YYYY-MM-DD HH:mm')
        url = url.format(start_time, end_time, student_id, region, course_type, class_type)
        print(url)
        return self.session.get(url=url, verify=False, headers=self.header)

    def post_bookings(self, class_id, teacher_id, student_id, course_type, level_code,unit_number, lesson_number, class_type):
        json = {
            "classId": class_id,
            "teacherId": teacher_id,
            "studentId": student_id,
            "region": "CN",
            "requiredCredits": 1,
            "courseType": course_type,
            "courseTypeLevelCode": level_code,
            "unitNumber": unit_number,
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
        url = self.host + '/api/v1/classes/{0}'.format(evc_booking_classid)
        return self.session.get(url=url, verify=False, headers=self.header)

    def get_student_book_history(self, student_id, start_date, course_type, class_type, end_date=None):
        if end_date==None:
            end_date = arrow.utcnow().format('YYYY-MM-DD HH:mm')
        url = self.host + '/api/v1/students/{0}/booking-history?StartDateTimeUtc={1}&EndDateTimeUtc={2}&CourseType={3}&ClassTypes={4}'
        url = url.format(student_id, start_date, end_date, course_type, class_type)
        return self.session.get(url=url, verify=False, headers=self.header)

    def get_student_credit_history(self, student_id):
        url = self.host + '/api/v1/students/{0}/credits-history'.format(student_id)
        return self.session.get(url=url, verify=False, headers=self.header)

    def get_class_video_record_url(self, class_id):
        url = self.host + '/api/v1/classes/{0}/video-record-url'.format(class_id)
        return self.session.get(url=url, verify=False, headers=self.header)

    def get_EF_classroom_app_info(self):
        url = self.host + '/api/v1/classroom-app'
        return self.session.get(url=url, verify=False, headers=self.header)

    def delete_class(self, class_id, student_id):
        url = self.host + '/api/v1/bookings?ClassId={0}&StudentId={1}'.format(class_id, student_id)

        return self.session.delete(url, verify=False, headers=self.header)

    def get_student_profile(self, student_id):
        url = self.host + 'api/v1/students/{0}/evc-profile'.format(student_id)
        return self.session.get(url=url, verify=False, headers=self.header)

    def edit_class_topic(self, student_id, class_id, course_type, course_level, unit_number, lesson_number):
        url = self.host + '/api/v1/bookings/topic'
        json = {
            "studentId": student_id,
            "bookingTopics": [
                {
                    "classId": class_id,
                    "region": "CN",
                    "courseType": course_type,
                    "courseTypeLevelCode": course_level,
                    "unitNumber": unit_number,
                    "lessonNumber": lesson_number
                }
            ]
        }
        return self.session.post(url=url, json=json, verify=False, headers=self.header)
