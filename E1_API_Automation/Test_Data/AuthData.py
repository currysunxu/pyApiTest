from enum import Enum


class AuthProduct(Enum):
    HFV2 = 'HFV2'
    SSV2 = 'SSV2'
    TBV3 = 'TBV3'
    SSV3 = 'SSV3'
    FRV1 = 'FRV1'
    HFV3 = 'HFV3'
    GP = 'GP'


class AuthUsers:
    AuthUsers = {
        'Staging': {
            AuthProduct.HFV2.value: {'username': 'hf2.cn.auto1', 'password': '12345'},
            AuthProduct.SSV2.value: {'username': 'ss2.cn.auto', 'password': '12345'},
            AuthProduct.TBV3.value: {'username': 'tb3.cn.auto1', 'password': '12345'},
            AuthProduct.SSV3.value: {'username': 'ss3.cn.auto1', 'password': '12345'},
            AuthProduct.FRV1.value: {'username': 'fr.cn.auto', 'password': '12345'},
            AuthProduct.HFV3.value: {'username': 'hf3.cn.auto1', 'password': '12345'},
            AuthProduct.GP.value: {'username': 'gp.cn.auto1', 'password': '12345'}
        },
        'Live': {
            AuthProduct.HFV2.value: {'username': 'hf2.cn.auto1', 'password': '12345'},
            AuthProduct.SSV2.value: {'username': 'ss2.cn.auto', 'password': '12345'},
            AuthProduct.TBV3.value: {'username': 'tb3.cn.auto1', 'password': '12345'},
            AuthProduct.SSV3.value: {'username': 'ss3.cn.auto1', 'password': '12345'},
            AuthProduct.FRV1.value: {'username': 'fr.cn.auto', 'password': '12345'},
            AuthProduct.HFV3.value: {'username': 'hf3.cn.auto1', 'password': '12345'},
            AuthProduct.GP.value: {'username': 'gp.cn.auto1', 'password': '12345'}
        }
    }


class AuthSQLString:
    get_student_profile_sql = "SELECT StudentProfile FROM [AuthenticationProfileService].[dbo].UserProfile " \
                              "with(nolock) where UserId = '{0}'"

