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

	def get_ecas(self,content_json_body):
		api_url = "/api/v1/eca"
		return self.mou_tai.post(api_url,content_json_body)

	def get_activities_group(self,content_group_json_body):
		api_url = "/api/v1/content-groups"
		return self.mou_tai.post(api_url,content_group_json_body)

	def get_content_groups_by_param(self, content_type, group_type, parent_content_id, parent_content_revision, parent_schema_version):
		content_group_body = {
			"contentType": content_type,
			"groupType": group_type,
			"parentContentId": parent_content_id,
			"parentContentRevision": parent_content_revision,
			"parentSchemaVersion": parent_schema_version
		}
		api_url = "/api/v1/content-groups"
		return self.mou_tai.post(api_url, content_group_body)

	def get_latest_ecas(self, content_id_list):
		api_url = "/api/v1/eca/latest"
		return self.mou_tai.post(api_url, content_id_list)

	def get_latest_activities(self, content_id_list):
		api_url = "/api/v1/activities/latest"
		return self.mou_tai.post(api_url, content_id_list)

	def get_asset_group(self, remediation_response):
		api_url = "/api/v1/asset-groups"
		return self.mou_tai.post(api_url, remediation_response)