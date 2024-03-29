import datetime
from enum import Enum

import re
from time import sleep
import time

import jmespath
import pytz
import requests
from hamcrest import assert_that, equal_to


est = pytz.timezone('US/Eastern')
utc = pytz.utc


class EvcServerCode(Enum):
    EVCUS1 = "evcus1"
    EVCCN1 = "evccn1"


class ServiceSubTypeCode(Enum):
    KONDemo = "KPLDemo"
    KONGPDemo = "KGPDemo"
    KONRegular = "KPL"
    KONGPRegular = "KGP"


class KidsClass():
    def __init__(self,
                 start_time,
                 end_time,
                 levelCode,
                 marketCode,
                 teacher={"id": "937668", "teacher_name": "KON1", "teacher_password": "1"},
                 serverSubTypeCode=ServiceSubTypeCode.KONDemo.value,
                 partnerCode="Kids",
                 evcServerCode=EvcServerCode.EVCCN1.value,
                 classDuration=30,
                 teachingItem="en"):
        self.teachingItem = teachingItem
        self.teacher = teacher
        self.serviceSubTypeCode = serverSubTypeCode
        self.partnerCode = partnerCode
        self.serverCode = evcServerCode
        self.classDuration = classDuration
        self.start_time = start_time
        self.end_time = end_time
        self.levelCode = levelCode
        self.marketCode = marketCode

class Moutai():
    def __init__(self, host, token=None, headers={"Content-Type": "application/json"}):
        self.token = token
        self.host = host
        self.headers = headers
        self.request_session = None

    def get_headers(self):
        return self.headers

    def set_header(self, headers):
        self.headers = headers

    def set_request_context(self, method, user_info, url, **kwargs):
        url_combined = self.host + url
        if self.token is None:
            self.request_session = requests.session()
            result = self.request_session.request(method, url_combined, json=user_info, verify=False, headers=self.headers, **kwargs)
            assert_that(result.status_code, equal_to(200))
            return result
        else:
            athentication_result = requests.request(method, url=url_combined, json=user_info,verify=False,
                                                 headers=self.headers, **kwargs)
            assert_that(athentication_result.status_code, equal_to(200), "Status code is not 200!")
            self.headers[self.token.get_name()] = self.__extract_token_value(self.token, athentication_result)
            return athentication_result

    def __extract_token_value(self, token, response):
        return jmespath.search(token.get_token_jemspath(), response.json())

    def post(self, url, json=None, **kwargs):
        url_combined = self.host + url
        if self.token is None:
            return self.request_session.post(url_combined, json=json,verify=False, headers=self.headers, **kwargs)
        else:
            return requests.post(url_combined, json=json,verify=False, headers=self.headers, **kwargs)

class Token():
    def __init__(self, name, jemspath):
        self.name = name
        self.token_jemspath = jemspath

    def get_name(self):
        return self.name

    def get_token_jemspath(self):
        return self.token_jemspath

class HeaderContentType(Enum):
    FORM_HEAD = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.0; en-GB; rv:1.8.1.12) Gecko/20080201 Firefox/2.0.0.12',
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "Accept-Encoding": "gzip, deflate, sdch"}
    JSON_HEAD = {'Accept-Language': 'zh-CN,zh;q=0.8',
                 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
                 "Content-Type": "application/json:charset=utf-8", "X-Requested-With": "XMLHttpRequest",
                 "x-troopjs-request-id": "1460104704575"}


class ScheduleClassTool:
    def __init__(self, admin, password, host):
        self.admin = admin
        self.password = password
        self.host = host
        self.login_handler_url = host + "/login/handler.ashx"
        self.url = host + "/axis/_debug/testdatagenerator.aspx"
        self.__login()

    def __login(self, try_number=2):
        parameters = {
            'username': self.admin,
            'password': self.password,
            'onsuccess': '/axis/_debug/testdatagenerator.aspx'
        }
        self.session = requests.session()
        try_time = 0
        while True:
            r = self.session.post(self.login_handler_url, data=parameters,
                                  headers=HeaderContentType.FORM_HEAD.value,
                                  verify=False)
            try_time += 1
            if r.status_code == 200 or try_time > try_number:
                break

        if r.status_code == 200:
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            self.cookie = cookies
            self.login_response_content = str(r.content)
            if not self.is_login_successful(r.text):
                raise Exception("Login Failed")
        else:
            raise Exception("Login Failed")

    def __match(self, regular_expression, to_be_matched):
        pattern = re.compile(regular_expression)
        match_result = pattern.findall(to_be_matched)
        if len(match_result) == 0:
            return False
        if len(match_result) >= 1:
            return True
        return False

    def is_login_successful(self, response):
        if not self.__match('id="__VIEWSTATE"', response):
            return False
        if not self.__match('id="__VIEWSTATEGENERATOR"', response):
            return False
        if not self.__match('id="__EVENTVALIDATION', response):
            return False
        return True

    def schedule_kids_class(self, kids_class: KidsClass):
        return self.schedule_cp20(teacher_id=kids_class.teacher["id"],
                                  start_time=kids_class.start_time,
                                  end_time=kids_class.end_time,
                                  serviceSubTypeCode=kids_class.serviceSubTypeCode,
                                  partnercode=kids_class.partnerCode,
                                  evcServerCode=kids_class.serverCode,
                                  classDuration=str(kids_class.classDuration),
                                  levelCode=kids_class.levelCode,
                                  marketCode=kids_class.marketCode,
                                  teachingItem=kids_class.teachingItem)

    def schedule_cp20(self, teacher_id,
                      start_time,
                      end_time,
                      serviceSubTypeCode=ServiceSubTypeCode.KONDemo.value,
                      partnercode='KON',
                      serviceTpyeCode="PL",
                      levelCode="BEG",
                      languageCode="en",
                      marketCode="Global",
                      evcServerCode="evcus1",
                      classDuration="20",
                      teachingItem="en"
                      ):
        parameters = {
            '__VIEWSTATE': self.get_view_state(),
            '__VIEWSTATEGENERATOR': self.get_view_state_generator(),
            '__EVENTVALIDATION': self.get_event_validation(),
            'txtTeacherMemberId': teacher_id,
            'txtStartTime': start_time,
            'txtEndTime': end_time,
            'txtServiceType': serviceTpyeCode,
            'txtServiceSubType': serviceSubTypeCode,
            'txtLevel': levelCode,
            'txtLanguage': languageCode,
            'txtMarket': marketCode,
            'txtPartner': partnercode,
            'txtEvcServer': evcServerCode,
            'txtClassDuration': classDuration,
            'txtTeachingItem': teachingItem,
            'txtTemplateId': '1',
            'btnDoAll': 'Do All'

        }
        r = self.session.post(url=self.url, data=parameters, headers=HeaderContentType.FORM_HEAD.value, verify=False)
        return self.__get_classIds(r.text)

    def get_view_state(self):
        temp = self.login_response_content[self.login_response_content.index('id="__VIEWSTATE"'):]
        view_state_value = temp[temp.index('value="') + 7:temp.index('/>') - 2]
        return view_state_value

    def get_view_state_generator(self):
        temp = self.login_response_content[self.login_response_content.index('id="__VIEWSTATEGENERATOR"'):]
        view_stategenerator_value = temp[temp.index('value="') + 7:temp.index('/>') - 2]
        return view_stategenerator_value

    def get_event_validation(self):
        temp = self.login_response_content[self.login_response_content.index('id="__EVENTVALIDATION"'):]
        event_validation_value = temp[temp.index('value="') + 7:temp.index('/>') - 2]
        return event_validation_value

    def __get_classIds(self, response):
        pattern = re.compile(r'ClassIds: (\d.*\d)</span>')
        match_result = pattern.findall(response)
        print("match classes: ", match_result)
        if len(match_result) == 0:
            print("Failed to assign class. It's might be already booked.")
        if len(match_result) == 1:
            return match_result[0].split(", ")
        if len(match_result) > 1:
            raise Exception("Need to update regular expression. Too many result. It basically should be one.")
        return -1


def get_UAT_schedule_tool():
    return ScheduleClassTool(admin="lliu17846", password="1", host="http://lolita.englishtown.com")


def get_QA_schedule_tool():
    return ScheduleClassTool(admin="KONSA", password="1", host="http://qa.englishtown.com")


def get_STG_schedule_tool():
    return ScheduleClassTool(admin="BBroekmann1", password="mail", host="http://staging.englishtown.com")


def create_and_assign_class(start_time, end_time, teacher_id, test_env="QA",
                            subServiceType=ServiceSubTypeCode.KONDemo.value, partner_code="any", level_code="Any",
                            market_code="any", evc_server_code="evccn1", teaching_item="en"):
    kids_class = KidsClass(start_time, end_time,
                           teacher={"id": teacher_id, "teacher_name": "KON1", "teacher_password": "1"},
                           serverSubTypeCode=subServiceType, evcServerCode=evc_server_code, partnerCode=partner_code,
                           levelCode=level_code, marketCode=market_code, teachingItem=teaching_item)
    school_service = None
    if "QA" == test_env:
        school_service = get_QA_schedule_tool()
    if "UAT" == test_env:
        school_service = get_UAT_schedule_tool()
    if "STG" == test_env:
        school_service = get_STG_schedule_tool()
    sleep(2)
    return school_service.schedule_kids_class(kids_class)


def local2utc_datetime(local_st):
    # 本地时间转UTC时间（-8:00)
    local_time = datetime.datetime.strptime(local_st, "%Y-%m-%d %H:%M:%S")
    time_struct = time.mktime(local_time.timetuple())
    utc_st = datetime.datetime.utcfromtimestamp(time_struct)
    return utc_st


def local2est_datetime(local_st):
    return local2utc_datetime(local_st).replace(tzinfo=utc).astimezone(est)


def local2est(local_st):
    return local2est_datetime(local_st).strftime("%Y-%m-%d %H:%M:%S")


class BookClassService():
    def __init__(self, host):
        self.host = host
        self.session = requests.session()
        self.mou_tai = Moutai(host=self.host, token=Token("X-BA-TOKEN", "Token"))

    def login(self, user_name, password):
        user_info = {
            "UserName": user_name,  # "jenkin0528tb",
            "Password": password,  # "12345",
            "DeviceType": 0,
            "Platform": 0
        }
        response = self.mou_tai.set_request_context("post", user_info, "/api/v2/Authentication/OnlineStudentPortal/")
        return jmespath.search('UserInfo.UserInfo.UserId',response.json())


    def book_class(self, class_id, class_start_time, class_end_time, teacher_id, course_type, package_type,
                      level_code, unit_number, lesson_number,
                      class_type):
        json = {
            "classId": class_id,
            "bookCode": level_code,
            "endStamp": class_end_time,
            "startStamp": class_start_time,
            "teacherId": teacher_id,
            "packageType": package_type,
            "programCode" : course_type,
            "unitNumber": unit_number,
            "lessonNumber": lesson_number,
            "classType": class_type,
            "needRecord": True
        }
        url = '/ksdsvc/api/v2/onlineclassbooking/'
        header = {"Content-Type": "application/json",
                  "Accept": "text/plain"
                  }
        return self.mou_tai.post(url=url, json=json)


    def post_bookings(self, class_id, teacher_id, student_id, course_type, level_code, unit_number, lesson_number,
                      class_type):
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


if __name__ == '__main__':
    test_env = "STG"
    teacher_id = "10584669"  # staging"10584669"  # QA "10274591" uat "23659223"
    student_name = 'hf2.cn.01'
    start_time = "2019-03-06 13:00:00"
    end_time = "2019-03-06 13:30:00"
    course_type = "HF"
    level_code = "C"
    unit_number = "1"
    lesson_number = "1"
    package_type = '24'
    class_type = "Regular"

    Book_by = ''
    # UAT didn't support book_by = SIS, can book class any time you need
    # QA support both, can book class any time you need
    # STG book_by= 'KSD'  only can book class  time > 24H,  use book_by= 'SIS' can book the class time < 24H
    # book_by = 'KSD' can support course_type = 'HF' or 'HFV3Plus', book_by  'SIS' only can support course_type = 'HF'
    if Book_by == 'KSD':

        if test_env == "QA":
            host = 'https://e1svc-qa.ef.cn'
        elif test_env == "STG":
            host = 'https://e1svc-staging.ef.cn'
        elif test_env == "UAT":
            host = 'http://e1svc-uat.englishtown.com'

    else:
        if test_env == "QA":
            host =  'https://e1svc-qa.ef.cn'
            book_host = 'http://internal-e1-evc-booking-qa-cn.ef.com'
        elif test_env == "STG":
            host =  'https://e1svc-staging.ef.cn'
            book_host = 'http://internal-e1-evc-booking-stg-cn.ef.com'
        elif test_env == "UAT":
            host = 'http://e1svc-uat.englishtown.com'
            book_host = 'N/A' # uat didn't support

    service = BookClassService(host)
    class_list = ['264246']
    # class_list = create_and_assign_class(local2est(start_time), local2est(end_time),
    #                                      teacher_id=teacher_id,
    #                                      test_env=test_env,
    #                                      subServiceType=ServiceSubTypeCode.KONRegular.value,
    #                                      partner_code="Any",
    #                                      level_code="Any",
    #                                      market_code="Any",
    #                                      evc_server_code="evccn1",
    #                                      teaching_item="en")

    student_id = service.login(student_name, '12345')
    if type(class_list) == list:
        for class_id in class_list:
            if Book_by != 'KSD':
                service.host = book_host
                book_response = service.post_bookings(class_id=class_id, teacher_id=teacher_id,
                                                      student_id=student_id, course_type=course_type,
                                                      level_code=level_code,
                                                      unit_number=unit_number, lesson_number=lesson_number,
                                                      class_type=class_type)
                assert_that(book_response.status_code, equal_to(204))
            else:
                service = BookClassService(host)
                book_response = service.book_class(class_id=class_id, teacher_id=teacher_id,
                                                      course_type=course_type, class_start_time = local2est(start_time),class_end_time=local2est(end_time),
                                                      level_code=level_code, package_type=package_type,
                                                      unit_number=unit_number, lesson_number=lesson_number,
                                                      class_type=class_type)

                assert_that(book_response.status_code, equal_to(204))

    elif type(class_list) == int:

        if Book_by != 'KSD':
            service.host = book_host
            book_response = service.post_bookings(class_id=str(class_list), teacher_id=teacher_id,
                                                  student_id=student_id, course_type=course_type,
                                                  level_code=level_code,
                                                  unit_number=unit_number, lesson_number=lesson_number,
                                                  class_type=class_type)
            assert_that(book_response.status_code, equal_to(204))
        else:
            service = BookClassService(host)
            book_response = service.book_class(class_id=str(class_list), teacher_id=teacher_id,
                                               course_type=course_type, class_start_time=local2est(start_time),
                                               class_end_time=local2est(end_time),
                                               level_code=level_code, package_type=package_type,
                                               unit_number=unit_number, lesson_number=lesson_number,
                                               class_type=class_type)

            assert_that(book_response.status_code, equal_to(204))
