from ..Lib.Moutai import Moutai
from enum import Enum
from E1_API_Automation.Settings import DATABASE
from ..Lib.db_mssql import MSSQLHelper
from E1_API_Automation.Test_Data.AuthData import AuthSQLString
import jmespath


class AuthService:
    def __init__(self, host):
        self.host = host
        self.mou_tai = Moutai(host=self.host, headers={"Content-Type": "application/json;charset=UTF-8"})

    def login(self, user_name, password, platform='UNDEFINED', device_type='NONE'):
        user_info = {
            "userName": user_name,
            "password": password,
            "platform": platform,
            "deviceType": device_type
        }

        athentication_result = self.mou_tai.set_request_context("post", user_info, "/api/v1/auth/login")
        idToken = jmespath.search('idToken', athentication_result.json())
        self.mou_tai.headers['X-EF-TOKEN'] = idToken
        return athentication_result

    def sign_out(self):
        return self.mou_tai.delete(url="/api/v1/auth/logout")

    def legacy_sign_out(self, customer_id):
        token_value = self.mou_tai.headers.pop('X-EF-TOKEN')
        self.mou_tai.headers['X-BA-TOKEN'] = token_value
        return self.mou_tai.delete(url="/api/v1/auth/legacyLogout/{0}".format(customer_id))

    def get_user_products(self):
        return self.mou_tai.get(url="/api/v1/acl/products")

    def get_student_profile_from_db(self, customer_id):
        ms_sql_server = MSSQLHelper(DATABASE, 'AuthenticationProfileService')
        return ms_sql_server.exec_query(AuthSQLString.get_student_profile_sql.format(customer_id))


class AuthPlatform(Enum):
    Undefined = 'UNDEFINED'
    IOS = 'IOS'
    Android = 'ANDROID'
    UniversalWindowsPlatform = 'UNIVERSAL_WINDOWS_PLATFORM'
    BlackBerry = 'BLACK_BERRY'
    Web = 'WEB'


class AuthDeviceType(Enum):
    NoneValue = 'NONE'
    Phone = 'PHONE'
    Pad = 'PAD'
    PC = 'PC'
    Wearable = 'WEARABLE'
