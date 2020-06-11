#!/usr/bin/env python
# -*-coding:utf-8-*-

# author:Curry
# date:2019/10/30


class Hf35BffAttemptEntity:
    def __init__(self, learning_unit_content_id, activities):
        self.__start_time = None
        self.__end_time = None
        self.__course_content_id = None
        self.__course_content_revision = None
        self.__book_content_id = None
        self.__book_content_revision = None
        self.__unit_content_id = None
        self.__unit_content_revision = None
        self.__lesson_content_id = None
        self.__lesson_content_revision = None
        self.__learning_unit_content_id = learning_unit_content_id
        self.__learning_unit_content_revision = None
        self.__tree_revision = None
        self.__schema_version = None
        self.__parent_content_path = None
        self.__activities = activities

    @property
    def student_id(self):
        return self.__student_id

    @student_id.setter
    def student_id(self, student_id):
        self.__student_id = student_id

    @property
    def start_time(self):
        return self.__start_time

    @start_time.setter
    def start_time(self, start_time):
        self.__start_time = start_time

    @property
    def end_time(self):
        return self.__end_time

    @end_time.setter
    def end_time(self, end_time):
        self.__end_time = end_time

    @property
    def course_content_id(self):
        return self.__course_content_id

    @course_content_id.setter
    def course_content_id(self, course_content_id):
        self.__course_content_id = course_content_id

    @property
    def course_content_revision(self):
        return self.__course_content_revision

    @course_content_revision.setter
    def course_content_revision(self, course_content_revision):
        self.__course_content_revision = course_content_revision

    @property
    def book_content_id(self):
        return self.__book_content_id

    @book_content_id.setter
    def book_content_id(self, book_content_id):
        self.__book_content_id = book_content_id

    @property
    def book_content_revision(self):
        return self.__book_content_revision

    @book_content_revision.setter
    def book_content_revision(self, book_content_revision):
        self.__book_content_revision = book_content_revision

    @property
    def unit_content_id(self):
        return self.__unit_content_id

    @unit_content_id.setter
    def unit_content_id(self, unit_content_id):
        self.__unit_content_id = unit_content_id

    @property
    def unit_content_revision(self):
        return self.__unit_content_revision

    @unit_content_revision.setter
    def unit_content_revision(self, unit_content_revision):
        self.__unit_content_revision = unit_content_revision

    @property
    def lesson_content_id(self):
        return self.__lesson_content_id

    @lesson_content_id.setter
    def lesson_content_id(self, lesson_content_id):
        self.__lesson_content_id = lesson_content_id

    @property
    def lesson_content_revision(self):
        return self.__lesson_content_revision

    @lesson_content_revision.setter
    def lesson_content_revision(self, lesson_content_revision):
        self.__lesson_content_revision = lesson_content_revision

    @property
    def learning_unit_content_id(self):
        return self.__learning_unit_content_id

    @learning_unit_content_id.setter
    def learning_unit_content_id(self, learning_unit_content_id):
        self.__learning_unit_content_id = learning_unit_content_id

    @property
    def learning_unit_content_revision(self):
        return self.__learning_unit_content_revision

    @learning_unit_content_revision.setter
    def learning_unit_content_revision(self, learning_unit_content_revision):
        self.__learning_unit_content_revision = learning_unit_content_revision

    @property
    def tree_revision(self):
        return self.__tree_revision

    @tree_revision.setter
    def tree_revision(self, tree_revision):
        self.__tree_revision = tree_revision

    @property
    def schema_version(self):
        return self.__schema_version

    @schema_version.setter
    def schema_version(self, schema_version):
        self.__schema_version = schema_version

    @property
    def parent_content_path(self):
        return self.__parent_content_path

    @parent_content_path.setter
    def parent_content_path(self, parent_content_path):
        self.__parent_content_path = parent_content_path

    @property
    def activities(self):
        return self.__activities

    @activities.setter
    def activities(self, activities):
        self.__activities = activities
