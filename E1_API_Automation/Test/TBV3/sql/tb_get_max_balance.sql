DECLARE @max_balance INT
DECLARE @user_id INT

SET @user_id = '${user_id}'
select @max_balance= Max(Balance) from [MotivationPointAudit] where UserId = @user_id
select Identifier from [MotivationPointAudit] where UserId = @user_id  and Balance = @max_balance