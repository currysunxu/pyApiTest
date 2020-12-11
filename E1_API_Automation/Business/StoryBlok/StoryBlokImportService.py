import requests

from E1_API_Automation.Lib.Moutai import Moutai
from E1_API_Automation.Lib.db_mysql import MYSQLHelper
from E1_API_Automation.Settings import MYSQL_MOCKTEST_DATABASE
from E1_API_Automation.Test_Data.StoryblokData import MTTableSQLString, MockTestData


class StoryBlokImportService:
    def __init__(self, host):
        self.host = host
        self.mou_tai = Moutai(host=self.host)

    @staticmethod
    def get_valid_activities_from_mt_db(table_name, version):
        ms_sql_server = MYSQLHelper(MYSQL_MOCKTEST_DATABASE)
        return \
            ms_sql_server.exec_query_return_dict_list(
                MTTableSQLString.get_valid_activity_sql.format(table_name, version, MockTestData.MockTest['ActivityInitVersion']))

    @staticmethod
    def get_activity_by_uuid_from_mt_db(table_name, uuid):
        ms_sql_server = MYSQLHelper(MYSQL_MOCKTEST_DATABASE)
        return ms_sql_server.exec_query_return_dict_list(
            MTTableSQLString.get_activity_by_uuid_sql.format(table_name, uuid))

    @staticmethod
    def get_mt_resource(mt_resource_url):
        api_url = MockTestData.MockTest['ResourceHost'] + mt_resource_url
        return requests.get(api_url)

    @staticmethod
    def get_storyblok_resource(storyblok_resource_url):
        return requests.get(storyblok_resource_url)

    def get_storyblok_import_status(self):
        api_url = "/management/api/v1/importStatus/type/ACTIVITY"
        return self.mou_tai.get(api_url)
