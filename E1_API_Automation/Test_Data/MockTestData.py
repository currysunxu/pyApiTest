from enum import Enum


class MockTestStudentType(Enum):
    HasMockTest = 'HMT'
    HasNoMockTest = 'HNMT'


class MockTestUsers:
    MTUserPw = {
        'QA': {
            MockTestStudentType.HasMockTest.value: [{'username': 'hf2.cn.03', 'password': '12345', 'custom_id': '1003'},
                                                    {'username': 'mt.gz02', 'password': '12345','custom_id': '9000043'}],
            MockTestStudentType.HasNoMockTest.value: [
                {'username': 'tb3.cn.02', 'password': '12345', 'custom_id': '1023'}]
        },
        'Staging': {
            MockTestStudentType.HasMockTest.value: [
                {'username': 'hf.g2.84', 'password': '12345', 'custom_id': '101075163'},
                {'username': 'hf.g3.84', 'password': '12345', 'custom_id': '101075164'}],
            MockTestStudentType.HasNoMockTest.value: [
                {'username': 'tb3.cn.02', 'password': '12345', 'custom_id': '1023'}]
        }
    }


class TestIdList:
    TestId = {
        'QA': {'valid_test_id': '00000000-0000-0000-0000-000000000316'},
        'Staging': {'valid_test_id': '00000000-0000-0000-0000-000000121017'}
    }


class TestTableSQLString:
    get_paper_id_by_test_id_sql = {
        'QA': "SELECT * FROM mt_test_qa.test where Id = '{0}' limit 1",
        'Staging': "SELECT * FROM mt_test.test where Id = '{0}' limit 1"
    }
    get_data_from_result_table_by_test_id_sql = {
        'QA': "SELECT * FROM mt_result_qa.test_student_compact_result " \
              "where test_id = '{0}' limit 1",
        'Staging': "SELECT * FROM mt_result.test_student_compact_result " \
              "where test_id = '{0}' limit 1",
    }
