import jmespath

from E1_API_Automation.Business.template.base_template import BaseTemplate


class Categorization(BaseTemplate):
    def __init__(self, activity_json):
        self.json = activity_json

    def get_correct_answer(self, question_key):
        question_json = jmespath.search("Questions[?Key=='{0}']".format(question_key), self.json)[0]
        answer_ids = jmespath.search("Body.answers", question_json)
        anwser_match = []
        for answer_match in answer_ids:
            answers = []
            for answer_id in answer_match:
                text = jmespath.search("Body.options[?id=='{0}'].text".format(answer_id), question_json)[0]
                answers.append({"id": answer_id, "text": text})
            anwser_match.append(answers)
        return anwser_match

    def get_question_score(self, question_key):
        question_json = jmespath.search("Questions[?Key=='{0}']".format(question_key), self.json)[0]
        answer_ids = jmespath.search("Body.answers", question_json)
        total_score = 0
        for answer_match in answer_ids:
            for answer_id in answer_match:
              total_score = total_score + 1
        return total_score
