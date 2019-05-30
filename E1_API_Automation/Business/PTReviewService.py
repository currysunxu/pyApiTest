from ..Lib.Moutai import Moutai
from ..Settings import DATABASE
from ..Test_Data.PTReviewData import PTReviewSQLString
from ..Lib.db_mssql import MSSQLHelper
import datetime


class PTReviewService:
    def __init__(self, host):
        self.host = host
        self.mou_tai = Moutai(host=self.host)

    def get_hf_all_books_url(self):
        return self.mou_tai.get('/api/v2/HighflyersAllBooks')

    def get_hf_all_books_from_db(self):
        ms_sql_server = MSSQLHelper(DATABASE, 'OnlineSchoolPlatform')
        return ms_sql_server.exec_query_return_dict_list(PTReviewSQLString.highflyers_all_books_sql)

    def verify_api_db_result(self, api_response_json, db_query_result):
        # check if all the data return from API is consistent with DB
        error_message = ''
        time_format = '%Y-%m-%d %H:%M:%S.%f'
        for i in range(len(api_response_json)):
            response_json = api_response_json[i]
            db_result = db_query_result[i]
            for key in response_json.keys():
                actual_result = response_json[key]
                expected_result = db_result[key]
                if actual_result is None:
                    actual_result = ''
                if expected_result is None:
                    expected_result = ''
                if key in ('CreatedBy', 'LastUpdatedBy', 'Key', 'ParentNodeKey', 'TopNodeKey'):
                    # the value get from the DB is UUID type
                    expected_result = str(expected_result)
                elif key in ('CreatedStamp', 'LastUpdatedStamp'):
                    actual_result = datetime.datetime.strptime(actual_result, '%Y-%m-%dT%H:%M:%S.%fZ')
                    actual_result = actual_result.strftime(time_format)
                    expected_result = expected_result.strftime(time_format)

                if str(actual_result) != str(expected_result):
                    error_message = error_message + "List[" + i + "].key:" + key + "'s api result not equal to db value, the result return in API is:" + str(
                        actual_result) + ", but the value in DB is:" + str(expected_result) + ";"

        return error_message
