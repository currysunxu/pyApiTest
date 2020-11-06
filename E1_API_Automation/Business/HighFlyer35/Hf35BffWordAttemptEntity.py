
class Hf35BffWordAttemptEntity:
    def __init__(self):
        self.__context_tree_revision = None
        self.__context_content_path = None
        self.__context_lesson_content_id = None
        self.__start_time = None
        self.__end_time = None
        self.__activities = None

    @property
    def context_tree_revision(self):
        return self.__context_tree_revision

    @context_tree_revision.setter
    def context_tree_revision(self, context_tree_revision):
        self.__context_tree_revision = context_tree_revision

    @property
    def context_content_path(self):
        return self.__context_content_path

    @context_content_path.setter
    def context_content_path(self, context_content_path):
        self.__context_content_path = context_content_path

    @property
    def context_lesson_content_id(self):
        return self.__context_lesson_content_id

    @context_lesson_content_id.setter
    def context_lesson_content_id(self, context_lesson_content_id):
        self.__context_lesson_content_id = context_lesson_content_id

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
    def activities(self):
        return self.__activities

    @activities.setter
    def activities(self, activities):
        self.__activities = activities


class Hf35BffWordActivitiesEntity:
    def __init__(self):
        self.__parent_content_path = None
        self.__book_content_id = None
        self.__book_content_revision = None
        self.__unit_content_id = None
        self.__unit_content_revision = None
        self.__word_content_id = None
        self.__word_content_revision = None
        self.__detail = None

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
    def word_content_id(self):
        return self.__word_content_id

    @word_content_id.setter
    def word_content_id(self, word_content_id):
        self.__word_content_id = word_content_id

    @property
    def word_content_revision(self):
        return self.__word_content_revision

    @word_content_revision.setter
    def word_content_revision(self, word_content_revision):
        self.__word_content_revision = word_content_revision

    @property
    def parent_content_path(self):
        return self.__parent_content_path

    @parent_content_path.setter
    def parent_content_path(self, parent_content_path):
        self.__parent_content_path = parent_content_path

    @property
    def detail(self):
        return self.__detail

    @detail.setter
    def detail(self, detail):
        self.__detail = detail


class Hf35BffWordAttemptDetailEntity:
    def __init__(self):
        self.__current_level = None
        self.__score = None
        self.__last_study_at = None

    @property
    def current_level(self):
        return self.__current_level

    @current_level.setter
    def current_level(self, current_level):
        self.__current_level = current_level

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, score):
        self.__score = score

    @property
    def last_study_at(self):
        return self.__last_study_at

    @last_study_at.setter
    def last_study_at(self, last_study_at):
        self.__last_study_at = last_study_at
