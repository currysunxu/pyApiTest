#!/usr/bin/env python
# -*-coding:utf-8-*-

# author:Curry
# date:2021/05/06
from E1_API_Automation.Business.BaseService import BaseService
from E1_API_Automation.Business.Utils.CommonUtils import CommonUtils


class GeneralTestService(BaseService):

    def put_unlock_unit_quiz(self, student_id, content_path_last_lesson, unlock_at=CommonUtils.datetime_format(),
                             product=1):
        api_url = '/api/v1/stateful-test/quiz'
        unlock_body = {
            "studentId": student_id,
            "product": product,
            "contentPath": content_path_last_lesson,
            "unlockedAt": unlock_at
        }
        return self.mou_tai.put(api_url, unlock_body)

    def get_content_group_for_unit_quiz(self, test_id):
        api_url = '/api/v1/stateful-test/quiz/{0}/content'.format(test_id)
        return self.mou_tai.get(api_url)

    def get_asset_group_for_unit_quiz(self, test_id):
        api_url = '/api/v1/stateful-test/quiz/{0}/content-assets'.format(test_id)
        return self.mou_tai.get(api_url)

    def get_unit_quiz(self, test_id):
        api_url = '/api/v1/stateful-test/quiz/{0}?_withResult=false'.format(test_id)
        return self.mou_tai.get(api_url)

    def get_test_by_student_and_content_path(self, student_id, content_path, product=1):
        api_url = '/api/v1/stateful-test/quiz?product={0}&studentId={1}&contentPath={2}&_withResult=false'.format(
            product,
            student_id,
            content_path)
        return self.mou_tai.get(api_url)
