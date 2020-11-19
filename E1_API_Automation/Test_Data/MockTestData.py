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
                {'username': 'auto.test', 'password': '12345', 'custom_id': '101521473', 'city': ''}],
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
        'QA': {'finished_test_id': '249ec74a-28c4-45eb-b523-72257db37d43'},
        'Staging': {'finished_test_id': '414d3c87-0c77-11eb-9786-405bd819f9ec'},
        'Live': {'finished_test_id': '00000101-0000-0000-0000-000000000002'}
    }

    RemediationActivities = {
        'QA':'[{"activityId":"00000000-0000-0000-0000-000014157425","questions":[{"currentAnswer":[["B"]],"isAnsweredCorrectly":false,"questionId":"mt/14183615/question","key":"mt/14183615/question"}]}]'
    }


class TestTableSQLString:
    get_paper_details_by_test_id_sql = {
        'QA': "SELECT * FROM mt_paper_qa.paper WHERE id = '{0}'",
        'Staging': "SELECT * FROM mt_paper.paper WHERE id = '{0}'",
        'Live': ""
    }

    get_test_details_by_test_id_sql = {
        'QA': "SELECT {0} FROM kt_test_qa.stateful_test " \
              "WHERE id = '{1}' and student_key ='{2}' limit 1",
        'Staging': "SELECT '{0}' FROM kt_test_qa.stateful_test " \
              "WHERE id = '{1}' and student_key ='{2}' limit 1",
        'Live': ""
    }

    get_valid_test_id_sql = {
        'QA': "SELECT id FROM kt_test_qa.stateful_test where student_key ='{0}' and product=32 and product_module=32 ORDER BY created_timestamp DESC limit 1",
        'Staging': "SELECT id FROM kt_test_qa.stateful_test where student_key ='{0}' and product=32 and product_module=32 ORDER BY created_timestamp DESC limit 1",
        'Live': ""
    }