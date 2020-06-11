from ..Lib.Moutai import Moutai, Token
from E1_API_Automation.Business.AuthService import AuthService
from E1_API_Automation.Business.Utils.EnvUtils import EnvUtils
from E1_API_Automation.Settings import AuthEnvironment, env_key
from E1_API_Automation.Test_Data.MockTestData import MockTestUsers, TestTableSQLString
from E1_API_Automation.Lib.HamcrestExister import exist
from E1_API_Automation.Settings import MYSQL_MOCKTEST_DATABASE
from E1_API_Automation.Lib.db_mysql import MYSQLHelper

from hamcrest import assert_that, equal_to, contains_string
import jmespath
import arrow


class MockTestBFFService:
    def __init__(self, host):
        self.host = host
        self.mou_tai = Moutai(host=self.host, token=Token("X-EF-ID", "Token"))

    def login(self, student_type):
        auth = AuthService(getattr(AuthEnvironment, env_key.upper()))
        user_name = MockTestUsers.MTUserPw[env_key][student_type][0]['username']
        password = MockTestUsers.MTUserPw[env_key][student_type][0]['password']
        id_token = auth.login(user_name, password).json()['idToken']
        headers = {"X-EF-ID": id_token, "Content-Type": "application/json"}
        self.mou_tai.set_header(headers)

    def post_mt_graphql(self, graphql_body):
        return self.mou_tai.post("/graphql", graphql_body)

    @staticmethod
    def get_valid_test_id_by_test_id_from_db():
        ms_sql_server = MYSQLHelper(MYSQL_MOCKTEST_DATABASE)
        return ms_sql_server.exec_query_return_dict_list(TestTableSQLString.get_valid_test_id_sql[env_key])[0]

    @staticmethod
    def get_test_details_by_test_id_from_db(test_id):
        ms_sql_server = MYSQLHelper(MYSQL_MOCKTEST_DATABASE)
        return ms_sql_server.exec_query_return_dict_list(
            TestTableSQLString.get_test_details_by_test_id_sql[env_key].format(test_id))

    @staticmethod
    def get_result_details_by_test_id_from_db(test_id, student_id):
        ms_sql_server = MYSQLHelper(MYSQL_MOCKTEST_DATABASE)
        return ms_sql_server.exec_query_return_dict_list(
            TestTableSQLString.get_result_details_by_test_id_sql[env_key].format(test_id, student_id))

    @staticmethod
    def get_paper_details_by_paper_id_from_db(paper_id):
        ms_sql_server = MYSQLHelper(MYSQL_MOCKTEST_DATABASE)
        return ms_sql_server.exec_query_return_dict_list(
            TestTableSQLString.get_paper_details_by_test_id_sql[env_key].format(paper_id))

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
            "operationName": "getTest",
            "variables": {
                "id": test_id
            },
            "query": "query getTest($id: ID!) {\n  test(id: $id) {\n    id\n    title\n    totalMinutes\n    totalScore\n    __typename\n  }\n}\n"
        }
        return self.post_mt_graphql(graphql_body)

    def post_insert_test_by_student(self, testid):
        graphql_body = {
            "operationName": "startTest",
            "variables": {
                "input": {
                    "testId": testid
                }
            },
            "query": "mutation startTest($input: StartTestInput!) {\n  startTest(input: $input) {\n    userErrors {\n      message\n      field\n      __typename\n    }\n    test {\n      id\n      startedDate\n      millisecondsLeftFromComplete\n      __typename\n    }\n    __typename\n  }\n}\n"
        }
        return self.post_mt_graphql(graphql_body)

    def get_test_processing_by_test_id(self, testId):
        graphql_body = {
            "operationName": "getTestProcessing",
            "variables": {"id": testId},
            "query": "query getTestProcessing($id: ID!) {\n  currentUser {\n    id\n    __typename\n  }\n  test(id: $id) {\n    id\n    title\n    testState\n    totalMinutes\n    totalScore\n    millisecondsLeftFromComplete\n    availableDate\n    expiryDate\n    startedDate\n    completedDate\n    totalSecondsSpent\n    paper {\n      course\n      id\n      title\n      parts {\n        title\n        type\n        sections {\n          id\n          resources\n          activities {\n            activityData\n            activityScore\n            id\n            extra {\n              sectionKey\n              sectionName\n              sectionSequence\n              part\n              partName\n              __typename\n            }\n            __typename\n          }\n          sectionScore\n          sectionType\n          title\n          __typename\n        }\n        resources {\n          duration\n          id\n          mimeType\n          sha1\n          size\n          url\n          __typename\n        }\n        __typename\n      }\n      questionCount\n      status\n      totalScore\n      version\n      __typename\n    }\n    __typename\n  }\n}\n"
        }
        return self.post_mt_graphql(graphql_body)

    def post_submit_test_result_by_test_id(self, test_id, total_seconds_spent):
        graphql_body = {
            "operationName": "submitTestResult",
            "variables": {"input": {"testId": test_id, "totalSecondsSpent": total_seconds_spent,
                                    "correctlyAnsweredQuestionCount": 0, "score": 0, "isForciblySubmitted": False,
                                    "activities": []}},
            "query": "mutation submitTestResult($input: SubmitTestResultInput!) {\n  submitTestResult(input: $input) {\n    userErrors {\n      message\n      field\n      __typename\n    }\n    test {\n      id\n      __typename\n    }\n    __typename\n  }\n}\n"
        }
        return self.post_mt_graphql(graphql_body)

    def get_test_result_by_testid(self, testid):
        graphql_body = {
            "operationName": "getTestResult",
            "variables": {"id": testid},
            "query": "query getTestResult($id: ID!) {\n  test(id: $id) {\n id\n    score\n    title\n    totalScore\n    totalMinutes\n    completedDate\n    totalSecondsSpent\n    paper {\n      id\n      title\n      parts {\n        title\n        type\n        resources {\n          duration\n          id\n          mimeType\n          sha1\n          size\n          url\n          __typename\n        }\n        sections {\n          id\n          title\n          sectionScore\n          activities {\n            id\n            activityScore\n            activityData\n            questionResults {\n              id\n              key\n              currentAnswer\n              score\n              totalScore\n              isAnsweredCorrectly\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      questionCount\n      status\n      totalScore\n      __typename\n    }\n    remediations {\n      id\n      part\n      learnerVectorKey\n      statistic {\n        totalQuestionCount\n        correctlyAnsweredQuestionCount\n        __typename\n      }\n      activities {\n        id\n        activityScore\n        activityData\n        extra {\n          sectionKey\n          sectionName\n          sectionSequence\n          part\n          partName\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
        }
        return self.post_mt_graphql(graphql_body)

    def get_remediation_by_testid(self, test_id, part):
        graphql_body = {
            "operationName": "getRemediation",
            "variables": {"testId": test_id, "part": part},
            "query": "query getRemediation($testId: ID!, $part: Int!) {\n  remediation(testId: $testId, part: $part) {\n    id\n    part\n    learnerVectorKey\n    statistic {\n      totalQuestionCount\n      correctlyAnsweredQuestionCount\n      __typename\n    }\n    activities {\n      id\n      activityScore\n      activityData\n      extra {\n        sectionKey\n        sectionName\n        sectionSequence\n        part\n        partName\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
        }
        return self.post_mt_graphql(graphql_body)

    def submit_remediation_by_test_id(self, test_id, learner_vector_key, correct_answer_count, total_question_count):
        graphql_body = {
            "operationName": "submitRemediationResult",
            "variables": {
                "input": {"testId": test_id, "part": 2,
                          "learnerVectorKey": learner_vector_key, "totalQuestionCount": total_question_count,
                          "correctlyAnsweredQuestionCount": correct_answer_count, "activities": []}},
            "query": "mutation submitRemediationResult($input: SubmitRemediationResultInput!) {\n  submitRemediationResult(input: $input) {\n    userErrors {\n      message\n      field\n      __typename\n    }\n    remediation {\n      testId\n      part\n      totalQuestionCount\n      correctlyAnsweredQuestionCount\n      __typename\n    }\n    __typename\n  }\n}\n"
        }
        return self.post_mt_graphql(graphql_body)

    def get_remediation_result_by_test_id(self, test_id):
        graphql_body = {
            "operationName": "getRemediationResult",
            "variables": {"testId": test_id, "part": 2},
            "query": "query getRemediationResult($testId: ID!, $part: Int!) {\n  remediation(testId: $testId, part: $part) {\n    id\n    statistic {\n      totalQuestionCount\n      correctlyAnsweredQuestionCount\n      __typename\n    }\n    __typename\n  }\n}\n"
        }
        return self.post_mt_graphql(graphql_body)

    def check_bff_get_current_user_structure(self, mt_response, student_type):
        assert_that(mt_response.status_code == 200)
        assert_that(mt_response.json(), exist("data.currentUser.avatar"))
        custom_id = MockTestUsers.MTUserPw[env_key][student_type][0]['custom_id']
        assert_that(jmespath.search("data.currentUser.id", mt_response.json()), equal_to(custom_id))
        # If not Live environment, then will do the DB verification
        if not EnvUtils.is_env_live():
            # Check student can only see tests configured for his city
            for i in range(len(jmespath.search("data.currentUser.tests", mt_response.json()))):
                test_id = jmespath.search("data.currentUser.tests[%d].id" % i, mt_response.json())
                assert_that(self.get_test_details_by_test_id_from_db(test_id)[0]['city'].upper(),
                            equal_to(MockTestUsers.MTUserPw[env_key][student_type][0]['city'].upper()))

    def check_bff_get_paper_resource_structure(self, mt_response, test_id):
        assert_that(mt_response.status_code == 200)
        assert_that(jmespath.search("data.test.id", mt_response.json()), equal_to(test_id))
        # If not Live environment, then will do the DB verification
        if not EnvUtils.is_env_live():
            assert_that(jmespath.search("data.test.paper.id", mt_response.json()),
                        equal_to(self.get_test_details_by_test_id_from_db(test_id)[0]["paper_id"]))
        assert_that(jmespath.search("data.test.paper.parts[*].type", mt_response.json()),
                    equal_to(['LISTENING', 'SYNTHESIS', 'READING']))

    def check_bff_get_test_intro_structure(self, mt_response, test_id):
        # If not Live environment, then will do the DB verification
        if not EnvUtils.is_env_live():
            expect_details = self.get_test_details_by_test_id_from_db(test_id)[0]
            self.check_test_basic_info(expect_details, mt_response)
        assert_that(mt_response.status_code == 200)
        assert_that(jmespath.search("data.test.id", mt_response.json()), equal_to(test_id))

    def set_negative_token(self, negative_token):
        if negative_token == "noToken":
            self.mou_tai.headers['X-EF-ID'] = ""
        elif negative_token == "invalid":
            self.mou_tai.headers['X-EF-ID'] = "invalidefaccesstoken"
        elif negative_token == "expired":
            self.mou_tai.headers[
                'X-EF-ID'] = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJqdGkiOiI2Y2QzMjEwMy05MDg4LTRiM2EtYmY1Ni1mZjE0ZjJhZjQ3MTUiLCJzdWIiOiIxMDAyIiwiaWF0IjoxNTgyNjE0NTYwLCJleHAiOjE1ODI2MjUzNjAsImNvcnJlbGF0aW9uX2lkIjoiY2Q5YWQ0ZjgtMjBmMy00YWUzLWE0YzEtMWZiOTBiMjEwOWY2IiwicmVmX2lkIjoiYWQ2MWRlMTQtMzUxMC00YjMxLTk1OTUtMzIyZWJmZjE1ZDMwIn0.sfl4sm7ON58rpUkxZ4g_PPMTb8bp1Vi4CIfYke8DxAfL0nNuQUR6fTfVCeHp71hf7GRPpnGIkgyhCX16aQMIMBZtVQWtYy_35EaCuKHCXoWUeAc6M7TJTp3qAW8UyvxX9Vh1aNvVPWWmWWI2OtvCKs1CLDRCOnVp9pDz2mm-3vUZ2IWeq1Di53tq1L2hp_DLQIK5LveLqHbGb9zesniHfVKVsPae-rOx2154Ffw6-YLxA_HJXlsgci5EQX4eYzlfcyH4jBj_u68IgZA8UflJ3ok_HkBXl2vWCOptEgq74O1o6N1qNBkHjLZZPIyI2CS79KENHYAoNln2lcEVkqjrtA"

    @staticmethod
    def check_bff_with_invalid_auth_structure(mt_response, invalid_jwt_token):
        assert_that(jmespath.search("data", mt_response.json()) is None)
        if invalid_jwt_token == "invalid":
            assert_that(jmespath.search("errors[0].extensions.code", mt_response.json()) == 400)
            assert_that(jmespath.search("errors[0].message", mt_response.json()),
                        contains_string("JWT strings must contain exactly 2 period characters"))
        elif invalid_jwt_token == "expired":
            assert_that(jmespath.search("errors[0].extensions.code", mt_response.json()) == 401)
            assert_that(jmespath.search("errors[0].message", mt_response.json()), contains_string("JWT expired"))
        elif invalid_jwt_token == "noToken":
            assert_that(jmespath.search("errors[0].extensions.code", mt_response.json()) == 401)
            assert_that(jmespath.search("errors[0].message", mt_response.json()), contains_string("Token not offered"))

    def check_insert_valid_test(self, mt_response, test_id, student_id):
        assert_that(jmespath.search("data.startTest.test.id", mt_response.json()), equal_to(test_id))
        # If not Live environment, then will do the DB verification
        if not EnvUtils.is_env_live():
            self.compare_response_date_and_db_date(
                jmespath.search("data.startTest.test.startedDate", mt_response.json()),
                self.get_result_details_by_test_id_from_db(test_id, student_id)[0][
                    "started_date"])

    @staticmethod
    def check_get_invalid_test_structure(mt_response, invalid_id):
        assert_that(mt_response.json(), exist("data.test"))
        assert_that(jmespath.search("data.test", mt_response.json()) is None)
        if invalid_id == "":
            assert_that(jmespath.search("errors[0].extensions.code", mt_response.json()) == 500)

    @staticmethod
    def check_insert_invalid_test_structure(mt_response, invalid_test):
        if invalid_test == "":
            assert_that(jmespath.search("data", mt_response.json()) is None)
            assert_that(jmespath.search("errors[0].extensions.code", mt_response.json()) == 500)
        else:
            assert_that(jmespath.search("data.startTest.test", mt_response.json()) is None)
            assert_that(jmespath.search("data.startTest.userErrors[0].__typename", mt_response.json()) == "UserError")

    @staticmethod
    def check_submit_invalid_test_result_structure(mt_response, invalid_id):
        assert_that(mt_response.json(), exist("data"))
        assert_that(jmespath.search("data", mt_response.json()) is None)
        assert_that(jmespath.search("errors[0].extensions.code", mt_response.json()) == 500)
        if invalid_id == "":
            assert_that(jmespath.search("errors[0].message", mt_response.json()),
                        equal_to("java.lang.NullPointerException"))
        else:
            assert_that(jmespath.search("errors[0].message", mt_response.json()), equal_to("Compact Result Not Found"))

    @staticmethod
    def check_get_invalid_remediation_structure(mt_response, invalid_part):
        if invalid_part == "":
            assert_that(jmespath.search("errors[0].extensions.code", mt_response.json()) == 500)
        else:
            assert_that(mt_response.json(), exist("data.remediation"))
            assert_that(jmespath.search("data.remediation", mt_response.json()) is None)

    @staticmethod
    def check_post_invalid_remediation_structure(mt_response, invalid_part):
        if invalid_part == "":
            assert_that(jmespath.search("errors[0].extensions.code", mt_response.json()) == 500)
        else:
            assert_that(mt_response.json(), exist("data.submitRemediationResult.remediation"))
            assert_that(jmespath.search("data.submitRemediationResult.remediation", mt_response.json()) is None)
            assert_that(jmespath.search("data.submitRemediationResult.userErrors[0].message", mt_response.json()),
                        equal_to('Test Not Found'))

    @staticmethod
    def check_bff_submit_test_result_structure(mt_response, test_id):
        assert_that(mt_response.status_code == 200)
        assert_that(jmespath.search("data.submitTestResult.__typename", mt_response.json()),
                    equal_to("SubmitTestResultPayload"))
        assert_that(jmespath.search("data.submitTestResult.test.__typename", mt_response.json()), equal_to('Test'))
        assert_that(jmespath.search("data.submitTestResult.test.id", mt_response.json()), equal_to(test_id))

    def check_bff_get_test_result_structure(self, mt_response, test_id):
        assert_that(mt_response.status_code == 200)
        assert_that(mt_response.json(), exist("data.test"))
        assert_that(len(jmespath.search("data.test.remediations", mt_response.json())) > 0)
        assert_that(jmespath.search("data.test.id", mt_response.json()), equal_to(test_id))
        # If not Live environment, then will do the DB verification
        if not EnvUtils.is_env_live():
            # Check test data
            expect_test_data = self.get_test_details_by_test_id_from_db(test_id)[0]
            self.check_test_basic_info(expect_test_data, mt_response)
            assert_that(jmespath.search("data.test.paper.id", mt_response.json()),
                        equal_to(expect_test_data["paper_id"]))
            # Check paper data
            self.check_paper_details(expect_test_data["paper_id"], mt_response)

    def check_bff_get_test_processing_structure(self, student_type, mt_response, test_id):
        assert_that(mt_response.status_code == 200)
        custom_id = MockTestUsers.MTUserPw[env_key][student_type][0]['custom_id']
        assert_that(jmespath.search("data.currentUser.id", mt_response.json()), equal_to(custom_id))
        assert_that(jmespath.search("data.test.id", mt_response.json()), equal_to(test_id))
        assert_that(jmespath.search("data.test.testState", mt_response.json()),
                    equal_to("COMPLETED_WITH_REMEDIATION_AVAILABLE"))
        # If not Live environment, then will do the DB verification
        if not EnvUtils.is_env_live():
            # Assert test data
            test_details = self.get_test_details_by_test_id_from_db(test_id)[0]
            self.check_test_basic_info(test_details, mt_response)
            self.compare_response_date_and_db_date(jmespath.search("data.test.availableDate", mt_response.json()),
                                                   test_details["start_date"])
            self.compare_response_date_and_db_date(jmespath.search("data.test.expiryDate", mt_response.json()),
                                                   test_details["end_date"])
            # Assert test result data
            result_details = self.get_result_details_by_test_id_from_db(test_id, custom_id)[0]
            self.compare_response_date_and_db_date(jmespath.search("data.test.completedDate", mt_response.json()),
                                                   result_details["completed_date"])
            self.compare_response_date_and_db_date(jmespath.search("data.test.startedDate", mt_response.json()),
                                                   result_details["started_date"])
            assert_that(jmespath.search("data.test.totalSecondsSpent", mt_response.json()),
                        equal_to(
                            self.date_diff_in_seconds(result_details["started_date"],
                                                      result_details["completed_date"])))
            # Assert paper data
            self.check_paper_details(result_details["paper_id"], mt_response)

    @staticmethod
    def check_test_basic_info(expect_details, mt_response):
        assert_that(mt_response.status_code == 200)
        assert_that(jmespath.search("data.test.title", mt_response.json()),
                    equal_to(expect_details["title"]))
        assert_that(jmespath.search("data.test.totalMinutes", mt_response.json()),
                    equal_to(expect_details["duration"]))
        assert_that(jmespath.search("data.test.totalScore", mt_response.json()),
                    equal_to(expect_details["paper_score"]))

    def check_paper_details(self, paper_id, mt_response):
        assert_that(mt_response.status_code == 200)
        assert_that(len(jmespath.search("data.test.paper.parts", mt_response.json())) > 0)
        # If not Live environment, then will do the DB verification
        if not EnvUtils.is_env_live():
            expect_paper_data = self.get_paper_details_by_paper_id_from_db(paper_id)[0]
            assert_that(jmespath.search("data.test.paper.title", mt_response.json()),
                        equal_to(expect_paper_data["title"]))
            assert_that(jmespath.search("data.test.paper.questionCount", mt_response.json()),
                        equal_to(expect_paper_data["question_count"]))
            assert_that(jmespath.search("data.test.paper.totalScore", mt_response.json()),
                        equal_to(expect_paper_data["total_score"]))

    @staticmethod
    def check_bff_get_remediation_structure(mt_response, part):
        assert_that(mt_response.status_code == 200)
        assert_that(jmespath.search("data.remediation.part", mt_response.json()), equal_to(part))
        for i in range(len(jmespath.search("data.remediation.activities", mt_response.json()))):
            assert_that(jmespath.search("data.remediation.activities[%d].__typename" % i, mt_response.json()),
                        equal_to("PaperActivity"))
            assert_that(mt_response.json(), exist("data.remediation.activities[%d].activityData" % i))
            assert_that(jmespath.search("data.remediation.activities[%d].activityScore" % i, mt_response.json()) > 0)

    @staticmethod
    def check_bff_submit_remediation_result_structure(mt_response, test_id, correct_answer_count, total_question_count):
        assert_that(mt_response.status_code == 200)
        assert_that(jmespath.search("data.submitRemediationResult.__typename", mt_response.json()),
                    equal_to("SubmitRemediationResultPayload"))
        assert_that(jmespath.search("data.submitRemediationResult.remediation.__typename", mt_response.json()),
                    equal_to('RemediationResult'))
        assert_that(jmespath.search("data.submitRemediationResult.remediation.testId", mt_response.json()),
                    equal_to(test_id))
        assert_that(jmespath.search("data.submitRemediationResult.remediation.correctlyAnsweredQuestionCount",
                                    mt_response.json()),
                    equal_to(correct_answer_count))
        assert_that(jmespath.search("data.submitRemediationResult.remediation.totalQuestionCount", mt_response.json()),
                    equal_to(total_question_count))
        assert_that(jmespath.search("data.submitRemediationResult.remediation.part", mt_response.json()),
                    equal_to(2))

    @staticmethod
    def check_bff_get_remediation_result_structure(mt_response, correct_answer_count, total_question_count):
        assert_that(mt_response.status_code == 200)
        assert_that(jmespath.search("data.remediation.__typename", mt_response.json()),
                    equal_to("Remediation"))
        assert_that(jmespath.search("data.remediation.statistic.__typename", mt_response.json()),
                    equal_to('RemediationStatistic'))
        assert_that(jmespath.search("data.remediation.statistic.correctlyAnsweredQuestionCount",
                                    mt_response.json()), equal_to(correct_answer_count))
        assert_that(jmespath.search("data.remediation.statistic.totalQuestionCount",
                                    mt_response.json()), equal_to(total_question_count))

    @staticmethod
    def compare_response_date_and_db_date(actual_date, expect_date):
        actual_date = arrow.get(actual_date).format('YYYY-MM-DDTHH:mm')
        expect_date = arrow.get(expect_date).format('YYYY-MM-DDTHH:mm')
        assert_that(actual_date, equal_to(expect_date))

    @staticmethod
    def date_diff_in_seconds(date1, date2):
        timedelta = date2 - date1
        return timedelta.days * 24 * 3600 + timedelta.seconds