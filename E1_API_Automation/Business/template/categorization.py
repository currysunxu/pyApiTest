import jmespath
from functools import reduce

from E1_API_Automation.Business.template.base_template import BaseTemplate


class Categorization(BaseTemplate):
    def __init__(self, activity_json):
        self.json = activity_json

    def get_correct_answer(self, question_key):
        question_json = jmespath.search("Questions[?Key=='{0}']".format(question_key), self.json)[0]
        answer_ids = jmespath.search("Body.answers", question_json)
        anwser_match = [list(
            map(lambda x: {"id": x,
                           "text": jmespath.search("Body.options[?id=='{0}'].text".format(x), question_json)[0]},
                answer_option)) for answer_option in answer_ids]

        return anwser_match

    def get_question_score(self, question_key):
        question_json = jmespath.search("Questions[?Key=='{0}']".format(question_key), self.json)[0]
        answer_ids = jmespath.search("Body.answers", question_json)
        total_score = reduce(lambda x,y:x+y,(map(lambda x: len(x), answer_ids)))
        return total_score

