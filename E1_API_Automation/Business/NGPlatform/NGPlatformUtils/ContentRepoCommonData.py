#!/usr/bin/env python
# -*-coding:utf-8-*-

# author:Curry
# date:2019/11/6
import random
import string
import time
import uuid


class ContentRepoCommonData:
	def __init__(self,number = 3,activity_or_asset = "activity"):
		self.content_body = self.create_activity_content_body(number)
		self.ancestor_refs = self.create_ancestor_obj()
		self.content_group_body = self.create_content_group_body(activity_or_asset)

	def create_activity_content_body(self,number):
		"""
		generate activity content body
		:return: content json body
		"""
		activity_body = []
		for index in range(number):
			activity_obj = {
				"schemaVersion": 1,
				"contentId": uuid.uuid4().__str__(),
				"contentRevision": ''.join(random.sample(string.ascii_letters + string.digits, 10)),
				"url": ''.join(random.sample(string.ascii_letters + string.digits, 10)),
				"entity": random.sample([1, 2, 33, 8, 77, "score", "english"], 4)
			}
			activity_body.append(activity_obj)

		content_body = {"releaseRevision": "releaseRevisionTest",
						"activities": activity_body}
		return content_body

	def create_content_group_body(self, activity_or_asset):
		content_obj = [{
			"groupType": activity_or_asset.upper()+"_GROUP",
			"contentType": "HOMEWORK",
			"schemaVersion": 1,
			"parentRef": self.create_parent_obj(),
			"ancestorRefs": self.ancestor_refs,
			"childRefs": self.create_child_obj(activity_or_asset)
		}]
		content_group_body = {"releaseRevision": "releaseRevision_contentGroup_Test02",
							  "contentGroups": content_obj}
		return content_group_body

	def create_parent_obj(self):
		return self.ancestor_refs[0]

	def create_ancestor_obj(self):
		"""
		create ancestor_refs by content_body
		:return: list of ancestor_refs
		"""
		ancestor_refs = []
		type_value = ["LESSON","BOOK","UNIT"]
		activities = self.content_body["activities"].copy()

		for act_num in activities:
			type_value.extend(type_value)
			if type_value.__len__() > activities.__len__():
				break

		index = 0
		for ancestor in activities:
			ancestor.update({"type": type_value[index]})
			ancestor.pop("entity")
			ancestor.pop("url")
			ancestor_refs.append(ancestor)
			index += 1
		return ancestor_refs

	def create_child_obj(self, activity_or_asset):
		"""
		create child_refs by content_body
		:param activity_or_asset: add "sha1" field if it is asset
		:return: list of child_refs
		"""
		child_refs = self.ancestor_refs[-1].copy()
		child_refs.update({"nodeType": activity_or_asset.upper(), "title": "Lesson 1: Activity&Asset - Listening"})
		if activity_or_asset == "asset":
			child_refs.update({"sha1":''.join(random.sample(string.ascii_letters + string.digits, 40))})
		return [child_refs]

	def get_activity_content(self):
		return self.content_body

	def get_activity_or_asset_content_group(self):
		return self.content_group_body