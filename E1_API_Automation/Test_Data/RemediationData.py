#!/usr/bin/env python
# -*-coding:utf-8-*-

# author:Curry
# date:2021/03/23
import random
import uuid

from arrow import now
from E1_API_Automation.Business.Utils.CommonUtils import CommonUtils


class RemediationData:

    @staticmethod
    def build_remediation_activities(test_instance_id, test_id, score):
        body = {
            "startTime": CommonUtils.datetime_format(),
            "endTime": CommonUtils.datetime_format(),
            "activityContentId": str(uuid.uuid1()),
            "testInstanceId": test_instance_id,
            "testId": test_id,
            "contentPath": "highflyers/cn-3/book-1/unit-3",
            "activityResults": {
                "Mid-HF-Book1": [
                    {
                        "activity1": str(uuid.uuid1())
                    },
                    {
                        "activity2": str(uuid.uuid1())
                    }
                ]
            },
            "score": score,
            "totalScore": "20.0",
            "activityQuestionMd5":CommonUtils.random_gen_str(32)
        }
        return body
