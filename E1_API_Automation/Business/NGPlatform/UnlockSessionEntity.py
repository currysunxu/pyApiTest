class UnlockSessionEntity:
    def __init__(self, reservation_id, sequence, type, group_id, course, course_level):
        self.__reservation_id = reservation_id
        self.__sequence = sequence
        self.__type = type
        self.__group_id = group_id
        self.__course = course
        self.__course_level = course_level
        self.__is_deleted = None
        self.__start_time = None
        self.__end_time = None
        self.__lessons = None
        self.__replay_id = None

    @property
    def reservation_id(self):
        return self.__reservation_id

    @reservation_id.setter
    def reservation_id(self, reservation_id):
        self.__reservation_id = reservation_id

    @property
    def sequence(self):
        return self.__sequence

    @sequence.setter
    def sequence(self, sequence):
        self.__sequence = sequence

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, type):
        self.__type = type

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
    def is_deleted(self):
        return self.__is_deleted

    @is_deleted.setter
    def is_deleted(self, is_deleted):
        self.__is_deleted = is_deleted

    @property
    def group_id(self):
        return self.__group_id

    @group_id.setter
    def group_id(self, group_id):
        self.__group_id = group_id

    @property
    def course(self):
        return self.__course

    @course.setter
    def course(self, course):
        self.__course = course

    @property
    def course_level(self):
        return self.__course_level

    @course_level.setter
    def course_level(self, course_level):
        self.__course_level = course_level

    @property
    def lessons(self):
        return self.__lessons

    @lessons.setter
    def lessons(self, lessons):
        self.__lessons = lessons

    @property
    def replay_id(self):
        return self.__replay_id

    @replay_id.setter
    def replay_id(self, replay_id):
        self.__replay_id = replay_id


class UnlockSessionLessonEntity:
    def __init__(self, unit_number, lesson_number):
        self.__unit_number = unit_number
        self.__lesson_number = lesson_number

    @property
    def unit_number(self):
        return self.__unit_number

    @unit_number.setter
    def unit_number(self, unit_number):
        self.__unit_number = unit_number

    @property
    def lesson_number(self):
        return self.__lesson_number

    @lesson_number.setter
    def lesson_number(self, lesson_number):
        self.__lesson_number = lesson_number
