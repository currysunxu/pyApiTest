import os

from ptest.decorator import AfterMethod, BeforeSuite, AfterSuite, BeforeClass, AfterClass
from ...Business.TrailblazerV3 import TrailbazerService

from ...Settings import ENVIRONMENT, env_key
from ...Test_Data.TBData import TBUsers, TBSQLString
from ...Lib.db_mssql import MSSQLHelper
from ...Lib.Utils import *

class TraiblazerBaseClass():
    @BeforeClass()
    def create_tb(self):
        self.tb_test = TrailbazerService(ENVIRONMENT, TBUsers.tb_user[env_key]['username'],
                                         TBUsers.tb_user[env_key]['password'])
        self.picked_lesson = None

    @AfterClass()
    def sign_out(self):
        self.tb_test.sign_out()
        print("Logout")

    def clean_motivation_audit(self, user_id):

        ms_sql_server = MSSQLHelper('OnlineSchoolPlatform')
        max_audit_sql_path = os.path.join(os.path.dirname(__file__), 'sql', 'tb_get_max_balance.sql')
        max_audit = open_anything(max_audit_sql_path).read().replace('${user_id}', str(self.tb_test.user_id))
        query_audit = ms_sql_server.exec_query(max_audit)
        if len(query_audit) >0:
            latest_audit_sql = TBSQLString.latest_identifier_audit.format(user_id, query_audit[0][0])

            latest_audit = ms_sql_server.exec_query(latest_audit_sql)
            updated_balance = self.update_motivation_audit_summary(user_id, latest_audit[0][1] - latest_audit[0][0])

            delete_sql_string = TBSQLString.clean_motivation_point_audit.format(user_id, query_audit[0][0])
            ms_sql_server.exec_non_query(delete_sql_string)
            return query_audit[0][0], updated_balance
        else:
            return None, 0

    def update_motivation_audit_summary(self, user_id, balance):
        update_summary_sql = TBSQLString.update_motivation_audit_summary.format(user_id, balance)
        ms_sql_server = MSSQLHelper('OnlineSchoolPlatform')
        ms_sql_server.exec_non_query(update_summary_sql)
        return balance






