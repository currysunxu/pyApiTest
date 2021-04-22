class Hf35BffReaderAttemptEntity:
    def __init__(self, relevant_content_id):
        self.__relevant_content_id = relevant_content_id
        self.__start_time = None
        self.__end_time = None
        self.__reader_content_id = None
        self.__reader_content_revision = None
        self.__reader_type = None
        self.__parent_content_path = None
        self.__need_check_upgrade = None
        self.__progress = None
        self.__practice = None
        self.__details = None

    @property
    def relevant_content_id(self):
        return self.__relevant_content_id

    @relevant_content_id.setter
    def relevant_content_id(self, relavant_content_id):
        self.__relevant_content_id = relavant_content_id

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
    def reader_content_id(self):
        return self.__reader_content_id

    @reader_content_id.setter
    def reader_content_id(self, reader_content_id):
        self.__reader_content_id = reader_content_id

    @property
    def reader_content_revision(self):
        return self.__reader_content_revision

    @reader_content_revision.setter
    def reader_content_revision(self, reader_content_revision):
        self.__reader_content_revision = reader_content_revision

    @property
    def reader_type(self):
        return self.__reader_type

    @reader_type.setter
    def reader_type(self, reader_type):
        self.__reader_type = reader_type

    @property
    def reader_progress(self):
        return self.__progress

    @reader_type.setter
    def reader_progress(self, progress):
        self.__progress = progress

    @property
    def reader_practice(self):
        return self.__practice

    @reader_type.setter
    def reader_practice(self, practice):
        self.__practice = practice

    @property
    def parent_content_path(self):
        return self.__parent_content_path

    @parent_content_path.setter
    def parent_content_path(self, parent_content_path):
        self.__parent_content_path = parent_content_path

    @property
    def need_check_upgrade(self):
        return self.__need_check_upgrade

    @need_check_upgrade.setter
    def need_check_upgrade(self, need_check_upgrade):
        self.__need_check_upgrade = need_check_upgrade

    @property
    def details(self):
        return self.__details

    @details.setter
    def details(self, details):
        self.__details = details
