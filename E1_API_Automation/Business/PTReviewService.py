from ..Lib.Moutai import Moutai
from ..Settings import DATABASE
from ..Test_Data.PTReviewData import PTReviewSQLString
from ..Lib.db_mssql import MSSQLHelper


class PTReviewService:
    def __init__(self, host):
        self.host = host
        self.mou_tai = Moutai(host=self.host)

    def get_all_books_by_course(self, course_code):
        # return self.mou_tai.get('/api/v2/HighflyersAllBooks')
        return self.mou_tai.get('/api/v2/AllBooksByCourse/{0}'.format(course_code))

    def post_hf_student_pt_assess_metas(self, student_id, book_key):
        pt_user = {
            "StudentId": student_id,
            "BookKey": book_key,
        }
        return self.mou_tai.post("/api/v2/StudentPaperDigitalProgressTestAssessmentMetas", pt_user)

    def post_hf_student_pt_assess_by_unit(self, student_id, book_key):
        pt_user = {
            "StudentId": student_id,
            "BookKey": book_key,
        }
        return self.mou_tai.post("/api/v2/StudentProgressTestAssessmentMetasGroupByUnit", pt_user)

    def post_hf_student_pt_assess_by_skill(self, student_id, book_key, unit_key):
        pt_user = {
            "StudentId": student_id,
            "BookKey": book_key,
            "UnitKey": unit_key
        }
        return self.mou_tai.post("/api/v2/StudentProgressTestAssessmentMetasGroupBySkill", pt_user)

    def get_all_books_by_course_from_db(self, course_code):
        ms_sql_server = MSSQLHelper(DATABASE, 'OnlineSchoolPlatform')
        return ms_sql_server.exec_query_return_dict_list(PTReviewSQLString.all_books_by_course_sql.format(course_code))

    def get_hf_pt_assessment_by_book_from_db(self, student_id, book_key):
        ms_sql_server = MSSQLHelper(DATABASE, 'OnlineSchoolPlatform')
        sql = PTReviewSQLString.hf_pt_assessment_sql.format(student_id, book_key)
        sql = sql + " order by b.UnitCode desc, a.Code"
        return ms_sql_server.exec_query_return_dict_list(sql)

    def get_hf_pt_assessment_from_db(self, student_id, book_key, unit_key):
        ms_sql_server = MSSQLHelper(DATABASE, 'OnlineSchoolPlatform')
        sql = PTReviewSQLString.hf_pt_assessment_sql + " and b.UnitKey = '{2}'"
        sql = sql.format(student_id, book_key, unit_key)
        return ms_sql_server.exec_query_return_dict_list(sql)

    def update_pt_assessment_original_overwritten_score(self, student_id, test_primary_key, skill_code,
                                                        original_score=None, overwritten_score=None):
        if original_score is None:
            original_score = 'null'

        if overwritten_score is None:
            overwritten_score = 'null'

        update_score = "OriginalScore = {0}, OverwrittenScore = {1}".format(original_score, overwritten_score)
        self.update_pt_assessment_data(student_id, test_primary_key, update_score, skill_code)

    def update_pt_assessment_total_score(self, student_id, test_primary_key, skill_code, total_score=None):
        if total_score is None:
            total_score = 'null'
        update_score = "TotalScore = {0}".format(total_score)
        self.update_pt_assessment_data(student_id, test_primary_key, update_score, skill_code)

    @staticmethod
    def update_pt_assessment_data(student_id, test_primary_key, update_score, skill_code=None):
        ms_sql_server = MSSQLHelper(DATABASE, 'OnlineSchoolPlatform')
        if skill_code is None:
            sql = PTReviewSQLString.update_pt_score_sql.format(update_score, student_id, test_primary_key)
        else:
            update_sql = PTReviewSQLString.update_pt_score_sql + " and code = '{3}'"
            sql = update_sql.format(update_score, student_id, test_primary_key, skill_code)
        ms_sql_server.exec_non_query(sql)

    '''
    update pt's original score as overwrittenscore, and overwrittenscore as null to test if API will get original score
    '''
    def update_pt_assessment_original_with_value(self, student_id, test_primary_key):
        update_score = "OriginalScore = OverwrittenScore, OverwrittenScore = null"
        self.update_pt_assessment_data(student_id, test_primary_key, update_score)

    '''
    update pt's overwrittenscore as original score, and original score as null to revert the change
    '''
    def update_pt_assessment_original_with_null(self, student_id, test_primary_key):
        update_score = "OverwrittenScore = OriginalScore, OriginalScore = null"
        self.update_pt_assessment_data(student_id, test_primary_key, update_score)