class PTReviewSQLString:
    highflyers_all_books_sql = "select CreatedBy, CreatedStamp, LastUpdatedBy, LastUpdatedStamp, [State], ActivityKeys, [Key], ContentKey, [Name], ParentNodeKey, TopNodeKey, Code, Theme, [Type], [Level], CoursePlanKey, [Sequence], Title, SubTitle, [Description], Body " \
                                "from [OnlineSchoolPlatform].[dbo].[view_CourseNodeV2] " \
                                "where parentNodeKey = (select courseKey from [OnlineSchoolPlatform].[dbo].CourseNodeSnapshot where [name] = 'High Flyers' ) order by [sequence]"

