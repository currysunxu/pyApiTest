from E1_API_Automation.Lib.db_cassandra import CassandraHelper
from E1_API_Automation.Settings import CASSANDRA_DATABASE
from E1_API_Automation.Test_Data.LearningPlanData import LearningPlanSQLString


class LearningDBUtils:
    @staticmethod
    def get_specific_plan(learning_plan):
        cassandra_sql_server = CassandraHelper(CASSANDRA_DATABASE)
        sql = LearningPlanSQLString.get_specific_plan_sql.format(learning_plan.product_id,
                                                                 learning_plan.plan_business_key,
                                                                 learning_plan.bucket_id,
                                                                 learning_plan.student_key,
                                                                 learning_plan.system_key)
        result_dict_list = cassandra_sql_server.exec_query_return_dict_list(sql)
        return result_dict_list

    @staticmethod
    def get_partition_plan(learning_plan):
        cassandra_sql_server = CassandraHelper(CASSANDRA_DATABASE)
        sql = LearningPlanSQLString.get_partition_plan_sql.format(learning_plan.product_id,
                                                                  learning_plan.plan_business_key,
                                                                  learning_plan.bucket_id)
        result_dict_list = cassandra_sql_server.exec_query_return_dict_list(sql)
        return result_dict_list

    @staticmethod
    def get_user_plan(learning_plan):
        cassandra_sql_server = CassandraHelper(CASSANDRA_DATABASE)
        sql = LearningPlanSQLString.get_user_plan_sql.format(learning_plan.product_id,
                                                             learning_plan.plan_business_key,
                                                             learning_plan.bucket_id,
                                                             learning_plan.student_key)
        result_dict_list = cassandra_sql_server.exec_query_return_dict_list(sql)
        return result_dict_list

    @staticmethod
    def get_specific_result(learning_result):
        cassandra_sql_server = CassandraHelper(CASSANDRA_DATABASE)
        sql = LearningPlanSQLString.get_specific_result_sql.format(learning_result.product,
                                                                   learning_result.student_key,
                                                                   learning_result.product_module,
                                                                   learning_result.business_key)
        result_dict_list = cassandra_sql_server.exec_query_return_dict_list(sql)
        return result_dict_list

    @staticmethod
    def get_partition_result(learning_result):
        cassandra_sql_server = CassandraHelper(CASSANDRA_DATABASE)
        sql = LearningPlanSQLString.get_partition_result_sql.format(learning_result.product,
                                                                    learning_result.student_key)
        result_dict_list = cassandra_sql_server.exec_query_return_dict_list(sql)
        return result_dict_list

    @staticmethod
    def get_user_result(learning_result):
        cassandra_sql_server = CassandraHelper(CASSANDRA_DATABASE)
        sql = LearningPlanSQLString.get_user_result_sql.format(learning_result.product,
                                                               learning_result.student_key,
                                                               learning_result.product_module)
        result_dict_list = cassandra_sql_server.exec_query_return_dict_list(sql)
        return result_dict_list
