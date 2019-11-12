class TBUsers:
    tb_user = {'QA': {'username': 'tb3.cn.auto1', 'password': '12345'},
               'Staging': {'username': 'tb3.cn.01', 'password': '12345'},
               'Staging_SG': {'username': 'tb3.id.auto1', 'password': '12345'},
               'Live':{'username': 'tb.cnlive.1', 'password': '12345'},
               'Live_SG': {'username': 'tb3.ru.01', 'password': '12345'}
               }


class TBSQLString:
    clean_motivation_point_audit = "delete FROM [OnlineSchoolPlatform].[dbo].[MotivationPointAudit] where UserId = {0} and Identifier ='{1}'"
    latest_identifier_audit = "select top(1) PointAmount, Balance FROM [OnlineSchoolPlatform].[dbo].[MotivationPointAudit] where UserId = {0} and Identifier ='{1}'"
    update_motivation_audit_summary = "update OnlineSchoolPlatform ..MotivationPointAuditSummary set Balance = {1} where UserId = {0}"

