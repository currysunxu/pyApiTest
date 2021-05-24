from E1_API_Automation.Business.BaseService import BaseService
import os
from enum import Enum
from E1_API_Automation.Settings import DATABASE
from ..Lib.db_mssql import MSSQLHelper
from E1_API_Automation.Test_Data.AuthData import AuthSQLString
from ..Lib.jwt_helper import JWTHelper
import jmespath


class AuthService(BaseService):

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

    def get_v3_token(self, id_token):
        project_dir = os.path.dirname(os.path.abspath(__file__))
        user_info = JWTHelper.decode_token(id_token, project_dir + "/rsa/public_key.pem")
        ba_token = jmespath.search('tokens[?version==`3`].value', user_info)[0]
        return ba_token

    def get_auth_token(self):
        token_value = self.mou_tai.headers.pop('X-EF-TOKEN')
        return token_value

    def sign_out(self):
        return self.mou_tai.delete(url="/api/v1/auth/logout")

    def legacy_sign_out(self, customer_id):
        token_value = self.mou_tai.headers.pop('X-EF-TOKEN')
        self.mou_tai.headers['X-BA-TOKEN'] = token_value
        return self.mou_tai.delete(url="/api/v1/auth/legacyLogout/{0}".format(customer_id))

    def get_user_products(self):
        return self.mou_tai.get(url="/api/v1/acl/products")

    def get_custom_id(self):
        profile_result = self.mou_tai.get(url="/api/v1/profile/basic")
        custom_id = jmespath.search('userId', profile_result.json())
        return custom_id

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


class Auth2Service(BaseService):

    def __init__(self, host, access_token):
        super().__init__(host, {"EF-Access-Token": access_token})

    def get_acl_response(self):
        api_url = '/auth2/internal/api/v2/auth/acl'
        return self.mou_tai.get(api_url)
