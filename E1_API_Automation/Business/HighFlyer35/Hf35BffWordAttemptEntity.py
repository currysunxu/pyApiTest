
class Hf35BffWordAttemptEntity:
    def __init__(self, course_content_id, book_content_id):
        self.__course_content_id = course_content_id
        self.__course_content_revision = None
        self.__book_content_id = book_content_id
        self.__book_content_revision = None
        self.__unit_content_id = None
        self.__unit_content_revision = None
        self.__word_content_id = None
        self.__word_content_revision = None
        self.__tree_revision = None
        self.__schema_version = None
        self.__detail = None

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
    def detail(self):
        return self.__detail

    @detail.setter
    def detail(self, detail):
        self.__detail = detail


class Hf35BffWordAttemptDetailEntity:
    def __init__(self):
        self.__current_level = None
        self.__score = None
        self.__last_study_time = None

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
    def last_study_time(self):
        return self.__last_study_time

    @last_study_time.setter
    def last_study_time(self, last_study_time):
        self.__last_study_time = last_study_time
