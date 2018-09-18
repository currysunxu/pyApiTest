import jmespath

class BaseTemplate:
    def __init__(self, activity_json):
        self.json = activity_json

    @property
    def key(self):
        return jmespath.search("Key", self.json)

    @property
    def total_question_count(self):
        return len(jmespath.search("Questions", self.json))

    @property
    def question_key_list(self):
        return jmespath.search("Questions[*].Key", self.json)

    @property
    def activity_type(self):
        return jmespath.search("Type", self.json)




