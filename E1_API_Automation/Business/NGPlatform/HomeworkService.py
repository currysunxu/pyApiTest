#!/usr/bin/env python
#-*-coding:utf-8-*-

#author:Curry
#date:2019/10/29
from E1_API_Automation.Lib.Moutai import Moutai


class HomeworkService:
	def __init__(self, host):
		self.host = host
		self.mou_tai = Moutai(host=self.host, headers={"Content-Type": "application/json;charset=UTF-8"})

	def get_the_best_attempt(self, student_id, book_content_id):
		api_url = '/api/v1/attempts/best?studentId={0}&bookContentId={1}'.format(student_id, book_content_id)
		return self.mou_tai.get(api_url)

	def submit_new_attempt(self, attempt_json):
		attempt_result = self.mou_tai.post("/api/v1/attempts", attempt_json)
		return attempt_result

	def get_vocab_progress(self, student_id, book_content_id):
		api_url = '/api/v1/vocab/progress?studentId={0}&bookContentId={1}'.format(student_id, book_content_id)
		return self.mou_tai.get(api_url)
