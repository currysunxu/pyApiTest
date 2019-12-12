#!/usr/bin/env python
# -*-coding:utf-8-*-

# author:Curry
# date:2019/10/30

class Hf35BffAttemptEntity:
	def __init__(self, learning_unit_content_id, activities):
		self.__start_time_utc= None
		self.__end_time_utc = None
		self.__course_content_id = None
		self.__book_content_id = None
		self.__unit_content_id = None
		self.__lesson_content_id = None
		self.__learning_unit_content_id= learning_unit_content_id
		self.__tree_revision = None
		self.__activities = activities

	@property
	def student_id(self):
		return self.__student_id

	@student_id.setter
	def student_id(self, student_id):
		self.__student_id = student_id

	@property
	def start_time_utc(self):
		return self.__start_time_utc

	@start_time_utc.setter
	def start_time_utc(self, start_time_utc):
		self.__start_time_utc = start_time_utc

	@property
	def end_time_utc(self):
		return self.__end_time_utc

	@end_time_utc.setter
	def end_time_utc(self, end_time_utc):
		self.__end_time_utc = end_time_utc

	@property
	def course_content_id(self):
		return self.__course_content_id

	@course_content_id.setter
	def course_content_id(self, course_content_id):
		self.__course_content_id = course_content_id

	@property
	def book_content_id(self):
		return self.__book_content_id

	@book_content_id.setter
	def book_content_id(self, book_content_id):
		self.__book_content_id = book_content_id

	@property
	def unit_content_id(self):
		return self.__unit_content_id

	@unit_content_id.setter
	def unit_content_id(self, unit_content_id):
		self.__unit_content_id = unit_content_id

	@property
	def lesson_content_id(self):
		return self.__lesson_content_id

	@lesson_content_id.setter
	def lesson_content_id(self, lesson_content_id):
		self.__lesson_content_id = lesson_content_id

	@property
	def learning_unit_content_id(self):
		return self.__learning_unit_content_id

	@learning_unit_content_id.setter
	def learning_unit_content_id(self, learning_unit_content_id):
		self.__learning_unit_content_id = learning_unit_content_id

	@property
	def tree_revision(self):
		return self.__tree_revision

	@tree_revision.setter
	def tree_revision(self, tree_revision):
		self.__tree_revision = tree_revision

	@property
	def activities(self):
		return self.__activities

	@activities.setter
	def activities(self, activities):
		self.__activities = activities