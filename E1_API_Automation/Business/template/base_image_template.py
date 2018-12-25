import jmespath

from E1_API_Automation.Business.template.base_template import BaseTemplate


class BaseImageTemplate(BaseTemplate):
    def get_correct_answer(self, question_key):
        return super().get_correct_answer(question_key, type="image")

    def get_question_score(self, question_key):
        return len(self.get_correct_answer(question_key))
