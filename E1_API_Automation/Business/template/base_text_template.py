import jmespath

from E1_API_Automation.Business.template.base_template import BaseTemplate


class BaseTextTemplate(BaseTemplate):
    def get_correct_answer(self, question_key):
        question_json = jmespath.search("Questions[?Key=='{0}']".format(question_key), self.json)[0]
        answer_ids = jmespath.search("Body.answers[]", question_json)
        answers = []
        for answer_id in answer_ids:
            text = jmespath.search("Body.options[?id=='{0}'].text".format(answer_id), question_json)[0]
            answers.append({"id": answer_id, "image": text})
        return answers

    def get_question_score(self, question_key):
        return len(self.get_correct_answer(question_key))