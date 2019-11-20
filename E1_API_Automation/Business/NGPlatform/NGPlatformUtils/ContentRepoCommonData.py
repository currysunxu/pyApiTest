#!/usr/bin/env python
# -*-coding:utf-8-*-

# author:Curry
# date:2019/11/6
import copy
import random
import string
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

		content_body = {"releaseRevision": ''.join(random.sample(string.ascii_letters + string.digits, 10)),
						"activities": activity_body}
		return content_body

	def create_content_group_body(self, activity_or_asset):
		"""
		create content group body by content group object
		:param activity_or_asset:
		:return: content group body
		"""
		content_obj_list = self.create_content_group_obj(activity_or_asset)
		content_group_body = {"releaseRevision": ''.join(random.sample(string.ascii_letters + string.digits, 10)),
							  "contentGroups": content_obj_list}
		return content_group_body

	def create_content_group_obj(self, activity_or_asset):
		"""
		create content group object by activity or asset or activity&asset
		:param activity_or_asset: use when test case include both activity and asset node
		:return: a common content object list
		"""
		content_obj_list = []
		if activity_or_asset == "activity_and_asset":
			for content_group_type in activity_or_asset.split("_and_"):
				content_obj = self.construct_content_obj(content_group_type)
				content_obj_list.append(content_obj)
				if content_obj_list.__len__() == 2:
					break
				self.ancestor_refs = self.create_ancestor_obj(activity_or_asset)
		else:
			content_obj = self.construct_content_obj(activity_or_asset)
			content_obj_list.append(content_obj)
		return content_obj_list


	def construct_content_obj(self, activity_or_asset):
		"""
		construct content object which include either activity or asset
		:param activity_or_asset:
		:return:
		"""
		content_obj = {
			"groupType": activity_or_asset.upper() + "_GROUP",
			"contentType": "HOMEWORK",
			"schemaVersion": 1,
			"parentRef": self.create_parent_obj(),
			"ancestorRefs": self.ancestor_refs,
			"childRefs": self.create_child_obj(activity_or_asset)
		}
		return content_obj

	def create_parent_obj(self):
		return self.ancestor_refs[0]

	def create_ancestor_obj(self,activity_and_asset = "activity"):
		"""
		create ancestor_refs by content_body
		:param: if data is activity_and_asset , then use deepcopy to create new list for ancestors
		:return: list of ancestor_refs
		"""
		ancestor_refs = []
		type_value = ["LESSON","BOOK","UNIT"]
		if activity_and_asset == "activity_and_asset":
			ancestors = copy.deepcopy(self.content_body["activities"])
		else:
			ancestors = self.content_body["activities"].copy()

		for act_num in ancestors:
			type_value.extend(type_value)
			if type_value.__len__() > ancestors.__len__():
				break

		index = 0
		for ancestor in ancestors:
			contentId = uuid.uuid4().__str__()
			ancestor.update({"type": type_value[index]})
			if "entity" in ancestor.keys():
				ancestor.pop("entity")
			if "url" in ancestor.keys():
				ancestor.pop("url")
			ancestor["contentId"] = contentId
			ancestor_refs.append(ancestor)
			index += 1
		return ancestor_refs

	def create_child_obj(self, activity_or_asset):
		"""
		create child_refs by content_body
		:param activity_or_asset: add "sha1" and "url" field if it is asset
		:return: list of child_refs
		"""
		child_refs = self.ancestor_refs[-1].copy()
		child_refs.update({"nodeType": activity_or_asset.upper(), "title": "Lesson 1: Activity&Asset - Listening"})
		if activity_or_asset == "asset":
			child_refs.update({"sha1":''.join(random.sample(string.ascii_letters + string.digits, 40))})
			child_refs.update({"url":''.join(random.sample(string.ascii_letters + string.digits, 30))})
		return [child_refs]

	def get_activity_content(self):
		return self.content_body

	def get_activity_or_asset_content_group(self):
		return self.content_group_body