import datetime
import re
import time
from enum import Enum

import pytz
import requests

est = pytz.timezone('US/Eastern')
utc = pytz.utc


def local2utc_datetime(local_st):
    #本地时间转UTC时间（-8:00)
    local_time = datetime.datetime.strptime(local_st, "%Y-%m-%d %H:%M:%S")
    time_struct = time.mktime(local_time.timetuple())
    utc_st = datetime.datetime.utcfromtimestamp(time_struct)
    return utc_st


def local2est_datetime(local_st):
    return local2utc_datetime(local_st).replace(tzinfo=utc).astimezone(est)

def local2est(local_st):
    return local2est_datetime(local_st).strftime("%Y-%m-%d %H:%M:%S")

class HeaderContentType(Enum):
    FORM_HEAD = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.0; en-GB; rv:1.8.1.12) Gecko/20080201 Firefox/2.0.0.12',
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "Accept-Encoding": "gzip, deflate, sdch"}
    JSON_HEAD = {'Accept-Language': 'zh-CN,zh;q=0.8',
                 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
                 "Content-Type": "application/json:charset=utf-8", "X-Requested-With": "XMLHttpRequest",
                 "x-troopjs-request-id": "1460104704575"}

def local2utc(local_st):
    #本地时间转UTC时间（-8:00)
    return local2utc_datetime(local_st).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


class ServiceSubTypeCode(Enum):
    KONDemo = "KPLDemo"
    KONGPDemo = "KGPDemo"
    KONRegular = "KPL"
    KONGPRegular = "KGP"


class EvcServerCode(Enum):
    EVCUS1 = "evcus1"
    EVCCN1 = "evccn1"


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

    def set_admin(self, value):
        self.admin = value

    def set_serverSubTypeCode(self, value):
        self.serviceSubTypeCode = value

    def set_teacher(self, value):
        self.teacher = value

    def set_partner_code(self, value):
        self.partnerCode = value

    def set_classDuration(self, value):
        self.classDuration = value

    def set_levelCode(self, value):
        self.levelCode = value


class ScheduleClassTool:
    #url = 'https://lolita.englishtown.com/axis/_debug/testdatagenerator.aspx'
    #login_handler_url = "https://lolita.englishtown.com/login/handler.ashx"

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
            r = self.session.post(self.login_handler_url, data=parameters, headers=HeaderContentType.FORM_HEAD.value,
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

    def schedule_pl40(self, teacher_id, start_time, end_time):
        parameters = {
            '__VIEWSTATE': self.get_view_state(),
            '__VIEWSTATEGENERATOR': self.get_view_state_generator(),
            '__EVENTVALIDATION': self.get_event_validation(),
            'txtTeacherMemberId': teacher_id,
            'txtStartTime': start_time,
            'txtEndTime': end_time,
            'txtServiceTypeCode': 'PL',
            'txtServiceSubTypeCode': 'Global',
            'txtLevelCode': 'BEG',
            'txtLanguageCode': 'en',
            'txtMarketCode': 'Global',
            'txtPartnerCode': 'Global',
            'txtEvcServerCode': 'us1',
            'txtClassDuration': '60',
            'txtTemplateId': '1',
            'btnDoAll': 'Do All'

        }
        r = self.session.post(url=self.url, data=parameters, headers=HeaderContentType.FORM_HEAD.value, verify=False)

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


def get_UAT_schedule_tool():
    return ScheduleClassTool(admin="lliu17846", password="1",  host="http://lolita.englishtown.com")

def get_QA_schedule_tool():
    return ScheduleClassTool(admin="KONSA", password="1", host="http://qa.englishtown.com")

def get_STG_schedule_tool():
    return ScheduleClassTool(admin="BBroekmann1", password="mail", host="http://staging.englishtown.com")
