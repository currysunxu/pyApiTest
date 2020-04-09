from enum import Enum



class BffProduct(Enum):
    HFV35 = 'HFV35'
    TBV3 = 'TBV3'
    SSV3 = 'SSV3'
    FRV1 = 'FRV1'
    HFV2 = 'HFV2'
    HFV3 = 'HFV3'


class BffUsers:
    BffUserPw = {
        'QA': {
            BffProduct.HFV35.value: [{'username': 'hf3.cn.01', 'password': '12345'}],
            BffProduct.TBV3.value: [{'username': 'tb3.cn.01', 'password': '12345'}],
            BffProduct.SSV3.value: [{'username': 'ss3.cn.02', 'password': '12345'}],
            BffProduct.FRV1.value: [{'username': 'fr.cn.01', 'password': '12345'}],
            BffProduct.HFV2.value: [{'username': 'hf.cn.own.test01', 'password': '12345'},
                                     {'username': 'hf.cn.fra.test01', 'password': '12345'},
                                     {'username': 'hf.cn.emptybc.test01', 'password': '12345'},
                                     {'username': 'hf.id.fra.test01', 'password': '12345'}],
            BffProduct.HFV3.value: [{'username': 'hf3.cn.01', 'password': '12345'}]
        },
        'Staging': {
            # Todo need to do data refactor once Staging is ready
            BffProduct.HFV35.value: [{'username': 'hf3.cn.01', 'password': '12345'}],
        },
        'Live': {
            # Todo need to do data refactor once Staging is ready
            BffProduct.HFV35.value: [{'username': 'hf3.cn.01', 'password': '12345'}],
        }
    }


class HF35DependService:
    provisioning_service = {
        'QA': {
            'host': 'https://provisioning-qa.ef.cn',
            'ios-app-key': '6591032B-DF1F-405F-93B3-482371A99A13',
            'android-app-key': '43CF3DBD-FC07-4CE1-A319-F81D3BB17AAC'
        },
        'Staging': {
            'host': 'https://provisioning.ef.cn',
            'ios-app-key': 'a3362077-30d5-4941-af3c-730fc2d6fab7',
            'android-app-key': 'f6925fb9-0101-4fc9-8b6d-839f7045451b'
        },
        'Live': {
            'host': 'https://provisioning.ef.cn',
            'ios-app-key': 'd978ecfa-07c3-435f-9a88-ad5cdcc9c0f5',
            'android-app-key': 'b792a26f-e8a4-461d-9ae7-f82a2a5a6d51'
        }
    }

    ksd_internal_service = {
        'QA': {
            'host': 'https://internal-e1-evc-booking-qa-cn.ef.com'
        },
        'Staging': {
            'host': 'https://internal-e1-evc-booking-stg-cn.ef.com'
        },
        'Live': {
            'host': 'https://internal-e1-evc-booking-cn.ef.com'
        }
    }

    ups_service = {
        'QA': {
            'host': 'http://internal-e1-ups-privacy-stg-cn.ef.com'
        },
        'Staging': {
            'host': 'http://internal-e1-ups-privacy-stg-cn.ef.com'
        },
        'Live': {
            'host': 'http://internal-e1-ups-privacy-cn.ef.com'
        }
    }
