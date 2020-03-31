from ..Lib.Moutai import Moutai, Token
from E1_API_Automation.Business.AuthService import AuthService
from E1_API_Automation.Settings import AuthEnvironment, env_key
from E1_API_Automation.Test_Data.MockTestData import MockTestUsers, TestTableSQLString
from E1_API_Automation.Lib.HamcrestExister import exist
from E1_API_Automation.Settings import MYSQL_MOCKTEST_DATABASE
from E1_API_Automation.Lib.db_mysql import MYSQLHelper

from hamcrest import assert_that, equal_to
import jmespath
import arrow


class MockTestBFFService:
    def __init__(self, host):
        self.host = host
        self.mou_tai = Moutai(host=self.host, token=Token("X-EF-ID", "Token"))

    def login(self, student_type):
        auth = AuthService(getattr(AuthEnvironment, env_key))
        user_name = MockTestUsers.MTUserPw[env_key][student_type][0]['username']
        password = MockTestUsers.MTUserPw[env_key][student_type][0]['password']
        id_token = auth.login(user_name, password).json()['idToken']
        headers = {"X-EF-ID": id_token, "Content-Type": "application/json"}
        self.mou_tai.set_header(headers)

    def post_mt_graphql(self, graphql_body):
        return self.mou_tai.post("/graphql", graphql_body)

    @staticmethod
    def get_test_details_by_test_id_from_db(test_id):
        ms_sql_server = MYSQLHelper(MYSQL_MOCKTEST_DATABASE)
        return ms_sql_server.exec_query_return_dict_list(TestTableSQLString.get_paper_id_by_test_id_sql.format(test_id))

    def post_load_user_mt_list(self):
        graphql_body = {
            "operationName": "getCurrentUser",
            "variables": {},
            "query": "query getCurrentUser {\n  currentUser {\n    id\n    fullName\n    avatar {\n      url\n      alt\n      __typename\n    }\n    tests {\n      id\n      title\n      testState\n      availableDate\n      expiryDate\n      daysLeftFromAvailable\n      daysLeftFromExpiry\n      millisecondsLeftFromComplete\n      completedDate\n      score\n      totalScore\n      totalQuestionCount\n      __typename\n    }\n    __typename\n  }\n}\n"
        }
        return self.post_mt_graphql(graphql_body)

    def get_paper_resource(self, test_id):
        graphql_body = {
            "operationName": "getResources",
            "variables": {"id": test_id},
            "query": "query getResources($id: ID!) {\n  test(id: $id) {\n    id\n    paper {\n      id\n      parts {\n        type\n        sections {\n          id\n          activities {\n            id\n            activityData\n            __typename\n          }\n          __typename\n        }\n        resources {\n          duration\n          id\n          mimeType\n          sha1\n          size\n          url\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
        }
        return self.post_mt_graphql(graphql_body)

    def post_load_test_intro(self, test_id):
        graphql_body = {
            "query": "query getTest($id: ID!) {\n  test(id: $id) {\n    id\n    title\n    totalMinutes\n    totalScore\n    __typename\n  }\n}\n",
            "variables": {
                "id": test_id
            },
            "operationName": "getTest"
        }
        return self.post_mt_graphql(graphql_body)

    def post_insert_test_by_student(self, testid):
        graphql_body = {
            "query": "mutation startTest($input: StartTestInput!) {\n  startTest(input: $input) {\n    userErrors {\n      message\n      field\n      __typename\n    }\n    test {\n      id\n      startedDate\n      millisecondsLeftFromComplete\n      __typename\n    }\n    __typename\n  }\n}\n",
            "variables": {
                "input": {
                    "testId": testid
                }
            },
            "operationName": "startTest"
        }
        return self.post_mt_graphql(graphql_body)

    @staticmethod
    def check_bff_get_current_user_structure(mt_response, student_type):
        assert_that(mt_response.status_code == 200)
        assert_that(mt_response.json(), exist("data.currentUser"))
        assert_that(mt_response.json(), exist("data.currentUser.avatar"))
        assert_that(mt_response.json(), exist("data.currentUser.tests"))
        assert_that(mt_response.json(), exist("extensions.tracing"))
        custom_id = MockTestUsers.MTUserPw[env_key][student_type][0]['custom_id']
        assert_that(jmespath.search("data.currentUser.id", mt_response.json()), equal_to(custom_id))

    def check_bff_get_paper_resource_structure(self, mt_response, test_id):
        assert_that(mt_response.status_code == 200)
        assert_that(mt_response.json(), exist("data.test"))
        assert_that(mt_response.json(), exist("extensions.tracing"))
        assert_that(jmespath.search("data.test.id", mt_response.json()), equal_to(test_id))
        assert_that(jmespath.search("data.test.paper.id", mt_response.json()),
                    equal_to(self.get_test_details_by_test_id_from_db(test_id)[0]["paper_id"]))
        assert_that(jmespath.search("data.test.paper.parts[*].type", mt_response.json()), equal_to(['LISTENING', 'SYNTHESIS', 'READING']))

    def check_bff_get_test_intro_structure(self, mt_response, test_id):
        assert_that(mt_response.status_code == 200)
        assert_that(mt_response.json(), exist("data.test"))
        assert_that(mt_response.json(), exist("extensions.tracing"))
        assert_that(jmespath.search("data.test.id", mt_response.json()), equal_to(test_id))
        assert_that(jmespath.search("data.test.title", mt_response.json()),
                    equal_to(self.get_test_details_by_test_id_from_db(test_id)[0]["title"]))
        assert_that(jmespath.search("data.test.totalMinutes", mt_response.json()),
                    equal_to(self.get_test_details_by_test_id_from_db(test_id)[0]["duration"]))
        assert_that(jmespath.search("data.test.totalScore", mt_response.json()),
                    equal_to(self.get_test_details_by_test_id_from_db(test_id)[0]["paper_score"]))

    def set_negative_token(self, negative_token):
        if negative_token == "noToken":
            self.mou_tai.headers['X-EF-ID'] = ""
        elif negative_token == "invalid":
            self.mou_tai.headers['X-EF-ID'] = "invalidefaccesstoken"
        elif negative_token == "expired":
            self.mou_tai.headers[
                'X-EF-ID'] = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJqdGkiOiI2Y2QzMjEwMy05MDg4LTRiM2EtYmY1Ni1mZjE0ZjJhZjQ3MTUiLCJzdWIiOiIxMDAyIiwiaWF0IjoxNTgyNjE0NTYwLCJleHAiOjE1ODI2MjUzNjAsImNvcnJlbGF0aW9uX2lkIjoiY2Q5YWQ0ZjgtMjBmMy00YWUzLWE0YzEtMWZiOTBiMjEwOWY2IiwicmVmX2lkIjoiYWQ2MWRlMTQtMzUxMC00YjMxLTk1OTUtMzIyZWJmZjE1ZDMwIn0.sfl4sm7ON58rpUkxZ4g_PPMTb8bp1Vi4CIfYke8DxAfL0nNuQUR6fTfVCeHp71hf7GRPpnGIkgyhCX16aQMIMBZtVQWtYy_35EaCuKHCXoWUeAc6M7TJTp3qAW8UyvxX9Vh1aNvVPWWmWWI2OtvCKs1CLDRCOnVp9pDz2mm-3vUZ2IWeq1Di53tq1L2hp_DLQIK5LveLqHbGb9zesniHfVKVsPae-rOx2154Ffw6-YLxA_HJXlsgci5EQX4eYzlfcyH4jBj_u68IgZA8UflJ3ok_HkBXl2vWCOptEgq74O1o6N1qNBkHjLZZPIyI2CS79KENHYAoNln2lcEVkqjrtA"

    @staticmethod
    def check_bff_get_test_with_invalid_auth_structure(mt_response, invalid_jwt_token):
        assert_that(jmespath.search("data", mt_response.json()) is None)
        if invalid_jwt_token == "invalid":
            assert_that(jmespath.search("errors[0].extensions.code", mt_response.json()) == 400)
        elif invalid_jwt_token == "expired" or invalid_jwt_token == "noToken":
            assert_that(jmespath.search("errors[0].extensions.code", mt_response.json()) == 401)

    @staticmethod
    def check_insert_valid_test(mt_response, test_id):
        assert_that(jmespath.search("data.startTest.test.id", mt_response.json()), equal_to(test_id))
        utc_time = arrow.utcnow().format('YYYY-MM-DDTHH:mm')
        started_time = jmespath.search("data.startTest.test.startedDate", mt_response.json())
        started_time = arrow.get(started_time).format('YYYY-MM-DDTHH:mm')
        assert_that(started_time, equal_to(utc_time))

    @staticmethod
    def check_get_invalid_test_structure(mt_response, invalid_test):
        assert_that(jmespath.search("data.test", mt_response.json()) is None)
        if invalid_test == "":
            assert_that(jmespath.search("errors[0].extensions.code", mt_response.json()) == 500)

    @staticmethod
    def check_insert_invalid_test_structure(mt_response, invalid_test):
        if invalid_test == "":
            assert_that(jmespath.search("data", mt_response.json()) is None)
            assert_that(jmespath.search("errors[0].extensions.code", mt_response.json()) == 500)
        elif invalid_test == "00000000-0000-0000-0000-000000000":
            assert_that(jmespath.search("data.startTest.test", mt_response.json()) is None)
            assert_that(jmespath.search("data.startTest.userErrors[0].__typename", mt_response.json()) == "UserError")