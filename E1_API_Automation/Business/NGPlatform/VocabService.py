#!/usr/bin/env python
# -*-coding:utf-8-*-

# author:Curry
# date:2021/05/06
from E1_API_Automation.Business.BaseService import BaseService


class VocabService(BaseService):

    def get_vocab_progress(self, student_id, book_content_id):
        api_url = '/api/v1/students/{0}/progress?bookContentId={1}'.format(student_id, book_content_id)
        return self.mou_tai.get(api_url)
