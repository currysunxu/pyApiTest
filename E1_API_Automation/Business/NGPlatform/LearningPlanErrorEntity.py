
class LearningPlanErrorEntity:
    def __init__(self, field_name, error_code, rejected_value):
        self.__field_name = field_name
        self.__error_code = error_code
        self.__rejected_value = rejected_value


    @property
    def field_name(self):
        return self.__field_name

    @field_name.setter
    def field_name(self, field_name):
        self.__field_name = field_name

    @property
    def error_code(self):
        return self.__error_code

    @error_code.setter
    def plan_business_key(self, error_code):
        self.__error_code = error_code

    @property
    def rejected_value(self):
        return self.__rejected_value

    @rejected_value.setter
    def bucket_id(self, rejected_value):
        self.__rejected_value = rejected_value
