from enum import Enum


class MockTestStudentType(Enum):
    HasMockTest = 'HMT'
    HasNoMockTest = 'HNMT'


class MockTestUsers:
    MTUserPw = {
        'QA': {
            MockTestStudentType.HasMockTest.value: [{'username': 'hf2.cn.03', 'password': '12345','custom_id':'1003'},{'username': 'mt.gz02', 'password': '12345','custom_id':'9000043'}],
            MockTestStudentType.HasNoMockTest.value: [{'username': 'tb3.cn.02', 'password': '12345','custom_id':'1023'}]
        }
    }