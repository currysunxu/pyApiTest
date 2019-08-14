class PTReviewSQLString:
    all_books_by_course_sql = "select CreatedBy, CreatedStamp, LastUpdatedBy, LastUpdatedStamp, [State], ActivityKeys, " \
                              "[Key], ContentKey, [Name], ParentNodeKey, TopNodeKey, Code, Theme, [Type], [Level], " \
                              "CoursePlanKey, [Sequence], Title, SubTitle, [Description], Body " \
                              "from [OnlineSchoolPlatform].[dbo].[view_CourseNodeV2] " \
                              "where parentNodeKey = (select courseKey from [OnlineSchoolPlatform].[dbo].CourseNodeSnapshot where [Code] = '{0}') " \
                              "and level =2 " \
                              "order by [sequence]"

    hf_pt_assessment_sql = "select a.StudentId, a.Code, a.TestInstanceKey,a.TestPrimaryKey, a.OriginalScore,a.OverwrittenScore, " \
                                "a.TotalScore,b.BookKey, b.BookCode, b. BookName, b.UnitKey, b.UnitCode, b.UnitName " \
                                "from OnlineSchoolPlatform.dbo.TestAssessmentMeta a " \
                                "inner join OnlineSchoolPlatform.dbo.ProgressTestUnitIndexBookIndex b " \
                                "on a.TestPrimaryKey = b.TestPrimaryKey " \
                                "where a.StudentId = {0} " \
                                "and b.BookKey = '{1}'"

    update_pt_score_sql = "update OnlineSchoolPlatform.dbo.TestAssessmentMeta set {0} " \
                          "where StudentId = {1} and TestPrimaryKey = '{2}'"


class PTReviewData:
    pt_hf_user_key_book_unit = {
        # key is student_id
        'QA': {
                '12214889': {
                    'TestPrimaryKey': 'C1C3AE7A-3368-4FCD-B0B2-0A75EEEA2E73',
                    'BookKey': '2F9B62E5-95EB-4291-9E79-8B2010279CA8',
                    'UnitKey': '30E54D73-C793-4F00-AD61-59CBF0423A0F'
                }
              },
        'Staging': {
                '100360697': {
                    'TestPrimaryKey': '30FF9C24-DEB4-49B2-9363-3C433D0B627F',
                    'BookKey': '2F9B62E5-95EB-4291-9E79-8B2010279CA8',
                    'UnitKey': '1EC56EC1-A123-4B47-9057-96BE3EE7534D'
                    }
                },
        'Staging_SG': {
            '10106831': {
                'TestPrimaryKey': '1B026C66-6ED0-440D-99BF-998507061E28',
                'BookKey': '0A5BF162-8FEA-4A22-80B5-9D18C704AD80',
                'UnitKey': '994AFEC8-F395-4FDC-83E4-5CFF2F22F28C'
            }
        },
        'Live': {
            '100201088': {
                'TestPrimaryKey': '', # no need to set TestPrimaryKey for live data
                'BookKey': '77F96708-2120-40CD-B6FD-4E063D6D7F33',
                'UnitKey': 'FE57BA80-ADEB-4933-A415-BB6C1B72F2C4'
            }
        },
        'Live_SG': {
            '100101406': {
                'TestPrimaryKey': '', # no need to set TestPrimaryKey for live data
                'BookKey': '77F96708-2120-40CD-B6FD-4E063D6D7F33',
                'UnitKey': 'FE57BA80-ADEB-4933-A415-BB6C1B72F2C4'
            }
        }
    }

    ptr_hf_user = {
        'QA':
            [{'username': 'ptReviewTest_PastCurrent', 'password': '12345'},
             {'username': 'ptReviewTest_Past', 'password': '12345'},
             {'username': 'ptReviewTest_FutureInvalid', 'password': '12345'},
             {'username': 'ptReviewTest_MixSSHF', 'password': '12345'},
             {'username': 'ptReviewTest_OneCurrent', 'password': '12345'},
             {'username': 'ptReviewTest01', 'password': '12345'},
            ]
    }

    ptr_resource_list = {
        'QA':
            [
                "2566bc78-da5e-4691-8015-986e1e3bda2d",
                "c20e7a40-04d9-47ec-b847-236e8d7bad01",
                "64ebd38b-1ed1-4871-b17c-2989267ef007",
                "b12f5cd0-b03f-4ba5-bec5-117f239c213d",
                "15880590-4a8d-4863-b648-5efff9cd6e56"
            ]
    }

    ptr_bff_data = {
        'QA': {
            'HF': {
                'StudentId': 12221442,
                'BookKey': '77F96708-2120-40CD-B6FD-4E063D6D7F33',
                'UnitKey': '50ED3E4D-BF78-4D9D-B6EE-05F6D4D9A260'
            }
        }
    }
