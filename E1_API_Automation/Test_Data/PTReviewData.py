class PTReviewSQLString:
    all_books_by_course_sql = "select CreatedBy, CreatedStamp, LastUpdatedBy, LastUpdatedStamp, [State], ActivityKeys, " \
                              "[Key], ContentKey, [Name], ParentNodeKey, TopNodeKey, Code, Theme, [Type], [Level], " \
                              "CoursePlanKey, [Sequence], Title, SubTitle, [Description], Body " \
                              "from [OnlineSchoolPlatform].[dbo].[view_CourseNodeV2] " \
                              "where parentNodeKey = (select courseKey from [OnlineSchoolPlatform].[dbo].CourseNodeSnapshot where [Code] = '{0}') " \
                              "and level =2 " \
                              "order by [sequence]"

    hf_pt_assessment_sql = "select a.StudentId, a.Code, a.TestInstanceKey,a.TestPrimaryKey, a.OriginalScore,a.OverwrittenScore, " \
                           "a.TotalScore,a.TestInstanceKey,b.BookKey, b.BookCode, b. BookName, b.UnitKey, b.UnitCode, b.UnitName " \
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
            },
            # this record is to test the omni API for multiple user,
            # it need to have same pt key with the first student
            '12214890': {
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
                'TestPrimaryKey': '',  # no need to set TestPrimaryKey for live data
                'BookKey': '77F96708-2120-40CD-B6FD-4E063D6D7F33',
                'UnitKey': 'FE57BA80-ADEB-4933-A415-BB6C1B72F2C4'
            }
        },
        'Live_SG': {
            '100101406': {
                'TestPrimaryKey': '',  # no need to set TestPrimaryKey for live data
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
             ],
        'Staging':
            [{'username': 'hf3.cn.02', 'password': '12345'},
             {'username': 'tb3.cn.02', 'password': '12345'}
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
            ],
        'Staging':
            [
                "b3251797-f6d8-e811-814a-02bc62143fc0",
                "b4251797-f6d8-e811-814a-02bc62143fc0",
                "b5251797-f6d8-e811-814a-02bc62143fc0",
                "b6251797-f6d8-e811-814a-02bc62143fc0"
            ],
        'Staging_SG':
            [
                "63d3075a-f4d8-e811-814a-02bc62143fc0",
                "65d3075a-f4d8-e811-814a-02bc62143fc0",
                "66d3075a-f4d8-e811-814a-02bc62143fc0",
                "64d3075a-f4d8-e811-814a-02bc62143fc0"
            ],
        'Live':
            [
                "a543df45-9408-401c-8232-649c894de105",
                "46642319-f5d8-e811-814a-02bc62143fc0",
                "47642319-f5d8-e811-814a-02bc62143fc0",
                "5f91d558-9b9b-e811-814a-02bc62143fc0",
                "48642319-f5d8-e811-814a-02bc62143fc0"
            ],
        'Live_SG':
            [
                "a543df45-9408-401c-8232-649c894de105",
                "a7e0eb06-f5d8-e811-814a-02bc62143fc0",
                "a8e0eb06-f5d8-e811-814a-02bc62143fc0",
                "a9e0eb06-f5d8-e811-814a-02bc62143fc0",
                "fd7ca371-983f-4af1-ab32-755b872909a8"
            ]
    }

    ptr_bff_data = {
        'QA': {
            'HF': {
                'StudentId': 1070,
                'BookKey': '77F96708-2120-40CD-B6FD-4E063D6D7F33',
                'TestPrimaryKey': 'C1C3AE7A-3368-4FCD-B0B2-0A75EEEA2E73',
                'UnitKey': '50ED3E4D-BF78-4D9D-B6EE-05F6D4D9A260'
            }
        },
        'Staging': {
            'HF': {
                'StudentId': 101077451,
                'BookKey': '77f96708-2120-40cd-b6fd-4e063d6d7f33',
                'UnitKey': 'b9803492-67b6-47c1-a5e8-fc6ea48228d0',
            }
        },
        'Live': {
            'HF': {
                'StudentId': 101521757,
                'BookKey': '77f96708-2120-40cd-b6fd-4e063d6d7f33',
                'UnitKey': '9e2a3e47-3889-41e5-b4cb-6ff17bb4bb49'
            }
        }
    }


class BffUsers:
    BffUserPw = {
        'QA': {'username': 'hf3.cn.01', 'password': '12345'
               },
        'Staging': {
            'username': 'hf.pt.w1', 'password': '12345',
        },
        'Live': {
            'username': 'gz1.g5.02', 'password': '12345',
        }
    }


class PTDATA:
    pt_web_data = {
        'QA': {
            'HFJ': {
                # Book J Unit 2
                'StudentId': 1070,
                'BookKey': 'ECCCB7B0-4EF6-4B1F-853C-3585F72C941C',
                'TestPrimaryKey': 'C6F0F367-9ACD-475A-8D55-61CA6C4AD9BF',
                'UnitKey': '27B6915B-63D6-48DB-8BA5-1A468054DCE8',
            },
            'HFD': {
                # Book D unit 5
                'StudentId': 1070,
                'BookKey': '8ADF3ABF-276E-41EE-8502-87E2C8AA4F84',
                'TestPrimaryKey': '89068F85-5B12-4138-B0C2-6156856D9E2F',
                'UnitKey': '756D2516-6655-4066-9048-7489D6FEC303',
            },
            'HFJ3': {
                # Book J unit 3
                'StudentId': 1070,
                'BookKey': 'ECCCB7B0-4EF6-4B1F-853C-3585F72C941C',
                'TestPrimaryKey': 'E53200F3-6B45-4F66-A9BF-A51EE667769D',
                'UnitKey': '8DA57DB0-9A6C-4FEF-9641-80D5B7A9F0E3',
            }
        },
        'Staging': {
            'HFJ': {
                # Book J Unit 2
                'StudentId': 101077451,
                'BookKey': 'ECCCB7B0-4EF6-4B1F-853C-3585F72C941C',
                'TestPrimaryKey': '8D36EC86-0789-4C0A-B30F-E4A5F4A3F593',
                'UnitKey': '27B6915B-63D6-48DB-8BA5-1A468054DCE8',
            },
            'HFD': {
                # Book D unit 5
                'StudentId': 1070,
                'BookKey': '8ADF3ABF-276E-41EE-8502-87E2C8AA4F84',
                'TestPrimaryKey': '0CE75CF8-9D92-4DBF-A100-7921B4D8ABA2',
                'UnitKey': '756D2516-6655-4066-9048-7489D6FEC303',
            },
            'HFJ3': {
                # Book J unit 3
                'StudentId': 101077451,
                'BookKey': 'ECCCB7B0-4EF6-4B1F-853C-3585F72C941C',
                'TestPrimaryKey': '0D70761A-DA33-429C-BD38-6A8709DD1DE7',
                'UnitKey': '8DA57DB0-9A6C-4FEF-9641-80D5B7A9F0E3',
            }
        },
        'Live': {
            'HFJ': {
                # Book J Unit 2
                'StudentId': 101521757,
                'BookKey': 'ECCCB7B0-4EF6-4B1F-853C-3585F72C941C',
                'TestPrimaryKey': 'B201AE4F-558E-42FD-9F87-644381CE5743',
                'UnitKey': '27B6915B-63D6-48DB-8BA5-1A468054DCE8',
            }
        }
    }


class PtWebSQLString:
    get_pt_instance_key_sql = "SELECT top 1 [Key] FROM OnlineSchoolPlatform.dbo.ProgressTestEntity " \
                              "with(nolock) where ProgressTestKey = '{0}' order by CreatedStamp desc"

    get_pt_metadata_key_sql = "SELECT top 1 [Key] FROM OnlineSchoolPlatform.dbo.TestAssessmentMeta " \
                              "with(nolock) where TestPrimaryKey = '{0}' and StudentId = '{1}'"

    delete_pt_paper_version_sql = "DELETE FROM OnlineSchoolPlatform.dbo.TestAssessmentMeta " \
                                  "where TestPrimaryKey = '{0}' and StudentId = '{1}'"

    insert_pt_paper_version_sql = "INSERT INTO OnlineSchoolPlatform.dbo.TestAssessmentMeta ([Key], StudentId, TestType, TestPrimaryKey, TestInstanceKey, Code, CourseKey, CourseSnapshotKey, OriginalScore, TotalScore, OverwrittenScore, OverwrittenByStaffId, OverwrittenByUserKey, OverwrittenStamp, CreatedStamp, LastUpdatedStamp, CreatedBy, LastUpdatedBy, State)" \
                                  "VALUES(newid(), '{0}', 1, '{1}', Null, '{2}', Null, Null, Null, 10, 9, Null, Null, Null, getutcdate(), getutcdate(), Null, Null, 0)"
