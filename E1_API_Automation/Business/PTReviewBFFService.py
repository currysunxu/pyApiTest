from ..Lib.Moutai import Moutai


class PTReviewBFFService:
    def __init__(self, host):
        self.host = host
        self.mou_tai = Moutai(host=self.host)

    def post_ptr_graphql(self, graphql_body):
        return self.mou_tai.post("/ptr/graphql", graphql_body)

    def post_ptr_graphql_by_book_unit(self, student_id, book_key, unit_key):
        graphql_body = {
            "query": "query Viewer($id:ID!, $bookId:String!, $testId:String!){\n test(id:$id, bookId:$bookId, testId:$testId)\n{\n id \n name \n bookName \n ptKey \n type \n invalid \n score \n skills{\n type{\n id \n name \n} \n result{\n score \n totalScore \n} \n }\n}\n}",
            "variables": {
                            "id": student_id,
                            "bookId": book_key,
                            "testId": unit_key
                         },
            "operationName": None
        }
        return self.post_ptr_graphql(graphql_body)

    def post_ptr_graphql_by_book(self, student_id, course, book_key):
        graphql_body = {
            "query": "query Viewer($id:ID!,$course:String!, $bookId:String!){\n book(id:$id,course:$course, bookId:$bookId)\n{\n id \n code \n title \n tests{\n id \n name \n invalid \n type \n score \n } \n isCurrent\n isActive\n cover {\n url \n alt \n} \n } \n}",
            "variables": {
                "id": student_id,
                "course": course,
                "bookId": book_key
            },
            "operationName": None
        }
        return self.post_ptr_graphql(graphql_body)

    def post_ptr_graphql_by_student(self, student_id, course):
        graphql_body = {
            "query": "query Viewer($id:ID!, $course:String!){\n viewer(id:$id, course:$course)\n{\n id\n books {\n id \n code \n title \n tests{\n id \n name \n type \n invalid \n score \n } \n isCurrent\n isActive\n cover {\n url \n alt \n} \n }\n}\n}",
            "variables": {
                "id": student_id,
                "course": course
            },
            "operationName": None
        }
        return self.post_ptr_graphql(graphql_body)
