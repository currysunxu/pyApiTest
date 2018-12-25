class TBUsers:
    tb_user = {'QA': {'username': 'Unlock_Test01', 'password': '12345'},
               'Staging': {'username': 'web001', 'password': '12345'},
               'Staging_SG': {'username': 'tb0605ru.wu', 'password': '12345'}
               }


class TBSQLString:
    clean_motivation_point_audit = "delete FROM [OnlineSchoolPlatform].[dbo].[MotivationPointAudit] where UserId = {0} and Identifier ='{1}'"
    latest_identifier_audit = "select top(1) PointAmount, Balance FROM [OnlineSchoolPlatform].[dbo].[MotivationPointAudit] where UserId = {0} and Identifier ='{1}'"
    update_motivation_audit_summary = "update OnlineSchoolPlatform ..MotivationPointAuditSummary set Balance = {1} where UserId = {0}"

