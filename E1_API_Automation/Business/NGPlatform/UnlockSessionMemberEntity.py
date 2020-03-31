class UnlockSessionMemberEntity:
    def __init__(self, session_id, student_id, is_removed, replay_id):
        self.__session_id = session_id
        self.__student_id = student_id
        self.__is_removed = is_removed
        self.__replay_id = replay_id

    @property
    def session_id(self):
        return self.__session_id

    @session_id.setter
    def session_id(self, session_id):
        self.__session_id = session_id

    @property
    def student_id(self):
        return self.__student_id

    @student_id.setter
    def student_id(self, student_id):
        self.__student_id = student_id

    @property
    def is_removed(self):
        return self.__is_removed

    @is_removed.setter
    def is_removed(self, is_removed):
        self.__is_removed = is_removed

    @property
    def replay_id(self):
        return self.__replay_id

    @replay_id.setter
    def replay_id(self, replay_id):
        self.__replay_id = replay_id
