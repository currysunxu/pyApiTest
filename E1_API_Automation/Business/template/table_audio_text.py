import jmespath

from E1_API_Automation.Business.template.base_template import BaseTemplate


class TableAudioText(BaseTemplate):
    def __init__(self, activity_json):
        self.json = activity_json


    def get_correct_answer(self, question_key):
        question_json = jmespath.search("Questions[?Key=='{0}']".format(question_key), self.json)[0]
        answer = jmespath.search("Body.options[?type=='gap']", question_json)

        return answer

    def get_question_score(self, question_key):
        return len(self.get_correct_answer(question_key))
