#!/usr/bin/env python
# -*-coding:utf-8-*-

# author:Curry
# date:2019/10/29
from E1_API_Automation.Lib.Moutai import Moutai


class VocabService:
    def __init__(self, host):
        self.host = host
        self.mou_tai = Moutai(host=self.host, headers={"Content-Type": "application/json;charset=UTF-8"})

    def get_vocab_progress(self, student_id, book_content_id):
        api_url = '/api/v1/students/{0}/progress?bookContentId={1}'.format(student_id, book_content_id)
        return self.mou_tai.get(api_url)
