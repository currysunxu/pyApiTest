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
            BffProduct.HFV35.value: [{'username': 'ptReviewTest06', 'password': '12345'}],
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
            BffProduct.HFV35.value: [{'username': 'hf3.cn.auto1', 'password': '12345'}],
        },
        'Live': {
			# Todo need to do data refactor once Staging is ready
			BffProduct.HFV35.value: [{'username': 'hf3.cn.auto1', 'password': '12345'}],
        }
    }


