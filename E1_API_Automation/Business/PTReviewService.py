from ..Lib.Moutai import Moutai
from ..Settings import DATABASE
from ..Test_Data.PTReviewData import PTReviewSQLString
from ..Lib.db_mssql import MSSQLHelper


class PTReviewService:
    def __init__(self, host):
        self.host = host
        self.mou_tai = Moutai(host=self.host)

    def get_hf_all_books_url(self):
        return self.mou_tai.get('/api/v2/HighflyersAllBooks')

    def post_hf_student_pt_assess_metas(self, student_id, book_key):
        pt_user = {
            "StudentId": student_id,
            "BookKey": book_key,
        }
        return self.mou_tai.post("/api/v2/StudentPaperDigitalProgressTestAssessmentMetas", pt_user)

    def get_hf_all_books_from_db(self):
        ms_sql_server = MSSQLHelper(DATABASE, 'OnlineSchoolPlatform')
        return ms_sql_server.exec_query_return_dict_list(PTReviewSQLString.highflyers_all_books_sql)

