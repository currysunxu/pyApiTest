from ..Lib.Moutai import Moutai, Token
from E1_API_Automation.Business.AuthService import AuthService
from E1_API_Automation.Settings import AuthEnvironment, env_key
from E1_API_Automation.Test_Data.MockTestData import MockTestUsers
from E1_API_Automation.Lib.HamcrestExister import exist

from hamcrest import assert_that, equal_to
import jmespath


class MockTestBFFService:
    def __init__(self, host):
        self.host = host
        self.mou_tai = Moutai(host=self.host, token=Token("X-BA-TOKEN", "Token"))

    def login(self, student_type):
        auth = AuthService(getattr(AuthEnvironment, env_key))
        user_name = MockTestUsers.MTUserPw[env_key][student_type][0]['username']
        password = MockTestUsers.MTUserPw[env_key][student_type][0]['password']
        id_token = auth.login(user_name, password).json()['idToken']
        headers = {"X-EF-ID": id_token, "Content-Type": "application/json"}
        self.mou_tai.set_header(headers)

    def post_mt_graphql(self, graphql_body):
        return self.mou_tai.post("/graphql", graphql_body)

    def post_load_user_mt_list(self):
        graphql_body = {
            "operationName": "getCurrentUser",
            "variables": {},
            "query": "query getCurrentUser {\n  currentUser {\n    id\n    fullName\n    avatar {\n      url\n      alt\n      __typename\n    }\n    tests {\n      id\n      title\n      testState\n      availableDate\n      expiryDate\n      daysLeftFromAvailable\n      daysLeftFromExpiry\n      millisecondsLeftFromComplete\n      completedDate\n      score\n      totalScore\n      totalQuestionCount\n      __typename\n    }\n    __typename\n  }\n}\n"
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

    def post_insert_test_by_student(self, student_id, course):
        graphql_body = {
            "query": "query mutation startTest($input: StartTestInput!) {\n startTest(input: $input) {\n userErrors {\n message\n field\n __typename\n }\n test {\n id\n startedDate\n __typename\n }\n __typename\n }\n}\n",
            "variables": {
                "input": {
                    "testId": "00000000-0000-0000-0000-000000000005",
                    "startedDate": "2019-12-23T10:02:51Z"}
            },
            "operationName": "startTest"
        }
        return self.post_mt_graphql(graphql_body)

    def check_bff_get_current_user_structure(self, mt_response, student_type):
        assert_that(mt_response.status_code == 200)
        assert_that(mt_response.json(), exist("data.currentUser"))
        assert_that(mt_response.json(), exist("data.currentUser.avatar"))
        assert_that(mt_response.json(), exist("data.currentUser.tests"))
        assert_that(mt_response.json(), exist("extensions.tracing"))
        custom_id = MockTestUsers.MTUserPw[env_key][student_type][0]['custom_id']
        assert_that(jmespath.search("data.currentUser.id", mt_response.json()), equal_to(custom_id))

    def check_bff_get_test_intro_structure(self, mt_response, test_id):
        assert_that(mt_response.status_code == 200)
        assert_that(mt_response.json(), exist("data.test"))
        assert_that(mt_response.json(), exist("extensions.tracing"))
        assert_that(jmespath.search("data.test.id", mt_response.json()), equal_to(test_id))
        print(jmespath.search("data.test.id", mt_response.json()))