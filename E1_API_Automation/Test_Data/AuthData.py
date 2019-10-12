from enum import Enum


class AuthProduct(Enum):
    HFV2 = 'HF'
    SSV2 = 'SSLEGACY'
    TBV3 = 'TB'
    SSV3 = 'SS'
    FRV1 = 'FR'
    HFV3 = 'HF'
    GP = 'GL'


class AuthUsers:
    AuthUsers = {
        'QA': {
            # For CN,if a highflyer user is Franchise, need to set the BusinessLineCode, otherwise, don't need to set,
            # code will treat it as OWN by default
            AuthProduct.HFV2.value: [{'username': 'hf.cn.own.test01', 'password': '12345'},
                                     {'username': 'hf.cn.fra.test01', 'password': '12345', 'BusinessLineCode': 'FRA'},
                                     {'username': 'hf.cn.emptybc.test01', 'password': '12345', 'BusinessLineCode': ''},
                                     {'username': 'hf.id.fra.test01', 'password': '12345', 'countrycode': 'ID'}],
            AuthProduct.TBV3.value: [{'username': 'tb3.cn.01', 'password': '12345'}],
            AuthProduct.SSV3.value: [{'username': 'ss3.cn.01', 'password': '12345'}],
            AuthProduct.FRV1.value: [{'username': 'fr.cn.01', 'password': '12345'}],
            AuthProduct.HFV3.value: [{'username': 'hf3.cn.01', 'password': '12345'}]
        },
        'Staging': {
            # For CN,if a highflyer user is Franchise, need to set the BusinessLineCode, otherwise, don't need to set,
            # code will treat it as OWN by default
            AuthProduct.HFV2.value: [{'username': 'hf2.cn.auto1', 'password': '12345'},
                                     {'username': 'hf2.cn.06', 'password': '12345', 'BusinessLineCode': 'FRA'}],
            AuthProduct.SSV2.value: [{'username': 'ss2.cn.auto', 'password': '12345'}],
            AuthProduct.TBV3.value: [{'username': 'tb3.cn.auto1', 'password': '12345'}],
            AuthProduct.SSV3.value: [{'username': 'ss3.cn.auto1', 'password': '12345'}],
            AuthProduct.FRV1.value: [{'username': 'fr.cn.auto', 'password': '12345'}],
            AuthProduct.HFV3.value: [{'username': 'hf3.cn.auto1', 'password': '12345'}],
            AuthProduct.GP.value: [{'username': 'gp.cn.auto1', 'password': '12345'}]
        },
        'Staging_SG': {
            AuthProduct.HFV2.value: [{'username': 'hf2.id.auto', 'password': '12345'},
                                     {'username': 'hf2.ru.01', 'password': '12345'}],
            AuthProduct.SSV2.value: [{'username': 'ss2.id.auto', 'password': '12345'}],
            AuthProduct.TBV3.value: [{'username': 'tb3.id.auto1', 'password': '12345'}],
            AuthProduct.SSV3.value: [{'username': 'ss3.ru.auto1', 'password': '12345'}],
            AuthProduct.FRV1.value: [{'username': 'fr.ru.auto', 'password': '12345'}],
            AuthProduct.HFV3.value: [{'username': 'hf3.id.auto', 'password': '12345'}],
            AuthProduct.GP.value: [{'username': 'gp.ru.auto1', 'password': '12345'}]
        },
        'Live': {
            AuthProduct.HFV2.value: [{'username': 'hf2.cn.auto1', 'password': '12345'}],
            AuthProduct.SSV2.value: [{'username': 'ss2.cn.auto', 'password': '12345'}],
            AuthProduct.TBV3.value: [{'username': 'tb3.cn.auto1', 'password': '12345'}],
            AuthProduct.SSV3.value: [{'username': 'ss3.cn.auto1', 'password': '12345'}],
            AuthProduct.FRV1.value: [{'username': 'fr.cn.auto', 'password': '12345'}],
            AuthProduct.HFV3.value: [{'username': 'hf3.cn.auto1', 'password': '12345'}],
            AuthProduct.GP.value: [{'username': 'gp.cn.auto1', 'password': '12345'}]
        }
    }


class AuthSQLString:
    get_student_profile_sql = "SELECT StudentProfile FROM [AuthenticationProfileService].[dbo].UserProfile " \
                              "with(nolock) where UserId = '{0}'"

