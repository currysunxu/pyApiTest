
class LearningResultDetailEntity:
    def __init__(self, activity_key):
        self.__activity_key = activity_key
        self.__activity_version = None
        self.__question_key = None
        self.__question_version = None
        self.__answer = None
        self.__extension = None
        self.__expected_score = None
        self.__actual_score = None
        self.__duration = None
        self.__start_time = None
        self.__end_time = None

    @property
    def activity_key(self):
        return self.__activity_key

    @activity_key.setter
    def activity_key(self, activity_key):
        self.__activity_key = activity_key

    @property
    def activity_version(self):
        return self.__activity_version

    @activity_version.setter
    def activity_version(self, activity_version):
        self.__activity_version = activity_version

    @property
    def question_key(self):
        return self.__question_key

    @question_key.setter
    def question_key(self, question_key):
        self.__question_key = question_key

    @property
    def question_version(self):
        return self.__question_version

    @question_version.setter
    def question_version(self, question_version):
        self.__question_version = question_version

    @property
    def answer(self):
        return self.__answer

    @answer.setter
    def answer(self, answer):
        self.__answer = answer

    @property
    def extension(self):
        return self.__extension

    @extension.setter
    def extension(self, extension):
        self.__extension = extension

    @property
    def expected_score(self):
        return self.__expected_score

    @expected_score.setter
    def expected_score(self, expected_score):
        self.__expected_score = expected_score

    @property
    def actual_score(self):
        return self.__actual_score

    @actual_score.setter
    def actual_score(self, actual_score):
        self.__actual_score = actual_score

    @property
    def duration(self):
        return self.__duration

    @duration.setter
    def duration(self, duration):
        self.__duration = duration

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

