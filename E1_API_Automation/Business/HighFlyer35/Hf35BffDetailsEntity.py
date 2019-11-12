#!/usr/bin/env python
# -*-coding:utf-8-*-

# author:Curry
# date:2019/10/30

class Hf35BffDetailsEntity:
	def __init__(self, question_id):
		self.__question_id = question_id
		self.__total_score= None
		self.__score= None
		self.__answer = None

	@property
	def question_id(self):
		return self.__question_id

	@question_id.setter
	def question_id(self, question_id):
		self.__question_id = question_id

	@property
	def total_score(self):
		return self.__total_score

	@total_score.setter
	def total_score(self, total_score):
		self.__total_score = total_score

	@property
	def score(self):
		return self.__score

	@score.setter
	def score(self, score):
		self.__score = score

	@property
	def answer(self):
		return self.__answer

	@answer.setter
	def answer(self, answer):
		self.__answer = answer
