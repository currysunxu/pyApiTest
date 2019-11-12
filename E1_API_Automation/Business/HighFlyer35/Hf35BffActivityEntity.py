#!/usr/bin/env python
# -*-coding:utf-8-*-

# author:Curry
# date:2019/10/30

class Hf35BffActivityEntity:
	def __init__(self, activity_content_id,details):
		self.__activity_content_id = activity_content_id
		self.__activity_content_revision= None
		self.__details = details

	@property
	def activity_content_id(self):
		return self.__activity_content_id

	@activity_content_id.setter
	def activity_content_id(self, activity_content_id):
		self.__activity_content_id = activity_content_id

	@property
	def activity_content_revision(self):
		return self.__activity_content_revision

	@activity_content_revision.setter
	def activity_content_revision(self, activity_content_revision):
		self.__activity_content_revision = activity_content_revision

	@property
	def details(self):
		return self.__details

	@details.setter
	def details(self, details):
		self.__details = details
