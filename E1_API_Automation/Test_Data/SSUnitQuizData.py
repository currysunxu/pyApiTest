#!/usr/bin/env python
# -*-coding:utf-8-*-

# author:Curry
# date:2021/04/23
import random
import uuid

from E1_API_Automation.Business.Utils.CommonUtils import CommonUtils
from E1_API_Automation.Lib.db_mysql import MYSQLHelper
from E1_API_Automation.Settings import MYSQL_MOCKTEST_DATABASE, env_key


class SSUnitQuizData:

    @staticmethod
    def build_ss_unit_quiz_attempts(test_id):
        body = {
            "testId": test_id,
            "startTime": CommonUtils.datetime_format(),
            "endTime": CommonUtils.datetime_format(),
            "treeRevision": None,
            "bookContentId": None,
            "bookContentRevision": None,
            "unitContentId": None,
            "unitContentRevision": None,
            "lessonContentId": None,
            "lessonContentRevision": None,
            "learningUnitContentId": str(uuid.uuid1()),
            "learningUnitContentRevision": str(uuid.uuid1()),
            "parentContentPath": None,
            "activityQuestionMd5": None,
            "activities": [
                {
                    "part": "listening",
                    "activityContentId": str(uuid.uuid1()),
                    "activityContentRevision": str(uuid.uuid1()),
                    "details": [
                        {
                            "questionId": CommonUtils.random_gen_str(),
                            "totalScore": random.randint(2, 10),
                            "score": random.randint(1, 2),
                            "duration": random.uniform(0, 2),
                            "answer": {}
                        },
                        {
                            "questionId": CommonUtils.random_gen_str(),
                            "totalScore": random.randint(2, 10),
                            "score": random.randint(1, 2),
                            "duration": random.uniform(0, 2),
                            "answer": {}
                        }
                    ]
                },
                {
                    "part": "reading",
                    "activityContentId": str(uuid.uuid1()),
                    "activityContentRevision": str(uuid.uuid1()),
                    "details": [
                        {
                            "questionId": CommonUtils.random_gen_str(),
                            "totalScore": random.randint(2, 10),
                            "score": random.randint(1, 2),
                            "duration": random.uniform(0, 2),
                            "answer": {}
                        },
                        {
                            "questionId": CommonUtils.random_gen_str(),
                            "totalScore": random.randint(2, 10),
                            "score": random.randint(1, 2),
                            "duration": random.uniform(0, 2),
                            "answer": {}
                        }
                    ]
                }
            ]
        }
        return body

    clean_unit_quiz_by_test_id_sql = {
        'QA': "DELETE FROM kt_test_qa.stateful_test where student_key ='{0}'",
        'Staging': "DELETE FROM kt_test.stateful_test where student_key ='{0}'",
        'Live': ""
    }

    @staticmethod
    def clean_unit_quiz_by_test_id_from_db(student_id):
        ms_sql_server = MYSQLHelper(MYSQL_MOCKTEST_DATABASE)
        return ms_sql_server.exec_query_return_dict_list(
            SSUnitQuizData.clean_unit_quiz_by_test_id_sql[env_key].format(student_id))