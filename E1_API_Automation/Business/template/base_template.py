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

    def get_correct_answer(self, question_key, type):
        question_json = jmespath.search("Questions[?Key=='{0}']".format(question_key), self.json)[0]
        answer_ids = jmespath.search("Body.answers[]", question_json)
        answers = list(map(lambda x: {"id": x, "{0}".format(type):
            jmespath.search("Body.options[?id=='{0}'].{1}".format(x, type), question_json)}, answer_ids))
        return answers
