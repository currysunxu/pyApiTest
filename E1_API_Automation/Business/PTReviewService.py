from E1_API_Automation.Business.BaseService import BaseService
from ..Settings import DATABASE
from ..Test_Data.PTReviewData import PTReviewSQLString
from ..Lib.db_mssql import MSSQLHelper


class PTReviewService(BaseService):

    def post_resource_batch(self, resource_list):
        return self.mou_tai.post("/Resource/Batch", resource_list)

    def options_resource_batch(self):
        return self.mou_tai.options("/Resource/Batch")

    @staticmethod
    def get_all_books_by_course_from_db(course_code):
        ms_sql_server = MSSQLHelper(DATABASE, 'OnlineSchoolPlatform')
        return ms_sql_server.exec_query_return_dict_list(PTReviewSQLString.all_books_by_course_sql.format(course_code))

    @staticmethod
    def get_hf_pt_assessment_by_book_from_db(student_id, book_key):
        ms_sql_server = MSSQLHelper(DATABASE, 'OnlineSchoolPlatform')
        sql = PTReviewSQLString.hf_pt_assessment_sql.format(student_id, book_key)
        sql = sql + " order by b.UnitCode desc, a.Code"
        return ms_sql_server.exec_query_return_dict_list(sql)

    @staticmethod
    def get_hf_pt_assessment_from_db(student_id, book_key, unit_key):
        ms_sql_server = MSSQLHelper(DATABASE, 'OnlineSchoolPlatform')
        sql = PTReviewSQLString.hf_pt_assessment_sql + " and b.UnitKey = '{2}'"
        sql = sql.format(student_id, book_key, unit_key)
        return ms_sql_server.exec_query_return_dict_list(sql)

    @staticmethod
    def update_pt_assessment_original_overwritten_score(student_id, test_primary_key, skill_code,
                                                        original_score=None, overwritten_score=None):
        if original_score is None:
            original_score = 'null'

        if overwritten_score is None:
            overwritten_score = 'null'

        update_score = "OriginalScore = {0}, OverwrittenScore = {1}".format(original_score, overwritten_score)
        PTReviewService.update_pt_assessment_data(student_id, test_primary_key, update_score, skill_code)

    @staticmethod
    def update_pt_assessment_total_score(student_id, test_primary_key, skill_code, total_score=None):
        if total_score is None:
            total_score = 'null'
        update_score = "TotalScore = {0}".format(total_score)
        PTReviewService.update_pt_assessment_data(student_id, test_primary_key, update_score, skill_code)

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
    @staticmethod
    def update_pt_assessment_original_with_value(student_id, test_primary_key):
        update_score = "OriginalScore = OverwrittenScore, OverwrittenScore = null"
        PTReviewService.update_pt_assessment_data(student_id, test_primary_key, update_score)

    '''
    update pt's overwrittenscore as original score, and original score as null to revert the change
    '''
    @staticmethod
    def update_pt_assessment_original_with_null(student_id, test_primary_key):
        update_score = "OverwrittenScore = OriginalScore, OriginalScore = null"
        PTReviewService.update_pt_assessment_data(student_id, test_primary_key, update_score)