class LearningPlanSQLString:
    get_specific_plan_sql = "SELECT * FROM studentplan where productid = {0} and planbusinesskey = '{1}' " \
                            "and bucketid = {2} and studentkey = '{3}' and systemkey = {4}"

    get_user_plan_sql = "SELECT * FROM studentplan where productid = {0} and planbusinesskey = '{1}' " \
                        "and bucketid = {2} and studentkey = '{3}'"

    get_partition_plan_sql = "SELECT * FROM studentplan where productid = {0} and planbusinesskey = '{1}' " \
                             "and bucketid = {2}"

    get_specific_result_sql = "SELECT * FROM studentresult where productid = {0} and studentkey = '{1}' " \
                              "and planbusinesskey = '{2}' and plansystemkey = {3}"

    get_user_result_sql = "SELECT * FROM studentresult where productid = {0} and studentkey = '{1}' " \
                          "and planbusinesskey = '{2}'"

    get_partition_result_sql = "SELECT * FROM studentresult where productid = {0} and studentkey = '{1}'"