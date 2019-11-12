#!/usr/bin/env python
# -*-coding:utf-8-*-

# author:Curry
# date:2019/11/6
import random
import time
import uuid

from E1_API_Automation.Lib.Moutai import Moutai


class ContentRepoService:
	def __init__(self, host):
		self.host = host
		self.mou_tai = Moutai(host=self.host)

	def post_content(self,content_json_body):
		api_url ="/admin/api/v1/contents"
		return self.mou_tai.post(api_url,content_json_body)

	def post_content_group(self,content_group_json_body):
		api_url ="/admin/api/v1/content-groups"
		return self.mou_tai.post(api_url,content_group_json_body)

	def get_activities(self,content_json_body):
		api_url = "/api/v1/activities"
		return self.mou_tai.post(api_url,content_json_body)

	def get_activities_group(self,content_group_json_body):
		api_url = "/api/v1/content-groups"
		return self.mou_tai.post(api_url,content_group_json_body)

