from enum import Enum


class MockTestStudentType(Enum):
    HasMockTest = 'HMT'
    HasNoMockTest = 'HNMT'


class MockTestUsers:
    MTUserPw = {
        'QA': {
            MockTestStudentType.HasMockTest.value: [
                {'username': 'mt.gz02', 'password': '12345', 'custom_id': '9000043', 'city': 'Guangzhou'}],
            MockTestStudentType.HasNoMockTest.value: [
                {'username': 'hf.id.fra.test01', 'password': '12345', 'custom_id': '9000008'}]
        },
        'Staging': {
            MockTestStudentType.HasMockTest.value: [
                {'username': 'hf.g2.84', 'password': '12345', 'custom_id': '101075163', 'city': 'Hangzhou'}],
            MockTestStudentType.HasNoMockTest.value: [
                {'username': 'tb3.cn.02', 'password': '12345', 'custom_id': '1023'}]
        },
        'Live': {
            MockTestStudentType.HasMockTest.value: [
                {'username': 'hf3.cn.auto1', 'password': '12345', 'custom_id': '1075', 'city': 'Jiuquan'}],
            MockTestStudentType.HasNoMockTest.value: [
                {'username': 'tb3.cn.auto1', 'password': '12345', 'custom_id': '1025'}]
        }
    }


class TestDataList:
    TestId = {
        'QA': {'finished_test_id': '00000030-0000-0000-0000-000000000001'},
        'Staging': {'finished_test_id': '00000000-0000-0000-0000-000000121023'},
        'Live': {'finished_test_id': '00000101-0000-0000-0000-000000000002'}
    }

    Remediation = {
        'QA': {'learner_vector_key': '1298812346793226242'},
        'Staging': {'learner_vector_key': '1262317729063399425'},
        'Live': {'learner_vector_key': '1265892248264929281'}
    }


class TestTableSQLString:
    get_test_details_by_test_id_sql = {
        'QA': "SELECT * FROM mt_test_qa.test WHERE Id = '{0}' limit 1",
        'Staging': "SELECT * FROM mt_test.test WHERE Id = '{0}' limit 1",
        'Live':""
    }

    get_paper_details_by_test_id_sql = {
        'QA': "SELECT * FROM mt_paper_qa.paper WHERE id = '{0}'",
        'Staging': "SELECT * FROM mt_paper.paper WHERE id = '{0}'",
        'Live': ""
    }

    get_result_details_by_test_id_sql = {
        'QA': "SELECT * FROM mt_result_qa.test_student_compact_result " \
              "WHERE test_id = '{0}' and student_id ='{1}' limit 1",
        'Staging': "SELECT * FROM mt_result.test_student_compact_result " \
                   "WHERE test_id = '{0}' and student_id ='{1}' limit 1",
        'Live': ""
    }

    get_valid_test_id_sql = {
        'QA': "SELECT id FROM mt_test_qa.test ORDER BY id DESC limit 1",
        'Staging': "SELECT id FROM mt_test.test ORDER BY id DESC limit 1",
        'Live': ""
    }