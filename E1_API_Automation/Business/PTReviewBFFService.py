from ..Lib.Moutai import Moutai, Token
from E1_API_Automation.Business.AuthService import AuthService
from E1_API_Automation.Settings import AUTH_ENVIRONMENT, env_key
from E1_API_Automation.Test_Data.PTReviewData import BffUsers


class PTReviewBFFService:
    def __init__(self, host):
        self.host = host
        self.mou_tai = Moutai(host=self.host, token=Token("x-ef-token", "Token"))

    def login(self):
        auth = AuthService(AUTH_ENVIRONMENT)
        self.user_name = BffUsers.BffUserPw[env_key]['username']
        self.password = BffUsers.BffUserPw[env_key]['password']
        x_ef_token = auth.login(self.user_name, self.password).json()['idToken']
        headers = {"x-ef-token": x_ef_token, "Content-Type": "application/json"}
        self.mou_tai.set_header(headers)

    def post_ptr_graphql(self, graphql_body):
        return self.mou_tai.post("/ptr/graphql", graphql_body)

    def post_ptr_graphql_by_book_unit(self, course, test_primary_key):
        graphql_body = {
            "operationName": "getPtInstanceKey",
            "variables": {
                "testId": test_primary_key,
                "course": course
            },
            "query": "query getPtInstanceKey($course: String!, $testId: String!) {\n  test(course: $course, testId: $testId) {\n    id\n    ptInstanceKey\n    __typename\n  }\n}\n"
        }
        return self.post_ptr_graphql(graphql_body)

    def post_ptr_graphql_by_book(self, course, book_key):
        graphql_body = {
            "operationName": "getBookWithTests",
            "variables": {
                "course": course,
                "bookId": book_key
            },
            "query": "query getBookWithTests($bookId: String!, $course: String!) {\n  book(bookId: $bookId, course: $course) {\n    id\n    tests {\n      date\n      id\n      ptKey\n      name\n      type\n      score\n      status\n      ptInstanceKey\n      __typename\n    }\n    title\n    __typename\n  }\n}\n"
        }
        return self.post_ptr_graphql(graphql_body)

    def post_ptr_graphql_by_student(self, course):
        graphql_body = {
            "operationName": "getUserWithBooks",
            "variables": {
                "course": course
            },
            "query": "query getUserWithBooks($course: String!) {\n  viewer(course: $course) {\n    id\n    books {\n      id\n      title\n      code\n      isCurrent\n      isActive\n      __typename\n    }\n    __typename\n  }\n}\n"
        }
        return self.post_ptr_graphql(graphql_body)
