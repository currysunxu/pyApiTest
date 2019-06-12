class PTReviewSQLString:
    highflyers_all_books_sql = "select CreatedBy, CreatedStamp, LastUpdatedBy, LastUpdatedStamp, [State], ActivityKeys, " \
                               "[Key], ContentKey, [Name], ParentNodeKey, TopNodeKey, Code, Theme, [Type], [Level], " \
                               "CoursePlanKey, [Sequence], Title, SubTitle, [Description], Body " \
                               "from [OnlineSchoolPlatform].[dbo].[view_CourseNodeV2] " \
                               "where parentNodeKey = (select courseKey from [OnlineSchoolPlatform].[dbo].CourseNodeSnapshot where [name] = 'High Flyers' ) order by [sequence]"


class PTReviewData:
    pt_hf_user_key_book_unit = {
        'QA': {
            'StudentId': 12214889,
            'TestPrimaryKey': 'C1C3AE7A-3368-4FCD-B0B2-0A75EEEA2E73',
            'BookKey': '2F9B62E5-95EB-4291-9E79-8B2010279CA8',
            'UnitKey': '30E54D73-C793-4F00-AD61-59CBF0423A0F'
        },
        'Staging': {
            'StudentId': 100362513,  # user ilab is: connie.test
            'TestPrimaryKey': 'D27608E2-0914-4BCE-9E76-9D4E6A0F05A7',
            'BookKey': '8605C95C-9CF8-418C-8C67-B7A3122C5445',
            'UnitKey': '22CFB67B-1CA2-4E71-A1EE-4FE8B0223FBA'
        }
    }