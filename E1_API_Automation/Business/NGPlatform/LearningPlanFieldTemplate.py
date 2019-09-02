from enum import Enum


class LearningPlanFieldTemplate:
    def __init__(self, field_name, field_type, is_required):
        self.__field_name = field_name
        self.__field_type = field_type
        self.__is_required = is_required
        self.__min_value = None
        self.__min_error_code = None
        self.__max_value = None
        self.__max_error_code = None
        self.__content_format = None

    @property
    def field_name(self):
        return self.__field_name

    @field_name.setter
    def field_name(self, field_name):
        self.__field_name = field_name

    @property
    def field_type(self):
        return self.__field_type

    @field_type.setter
    def field_type(self, field_type):
        self.__field_type = field_type

    @property
    def is_required(self):
        return self.__is_required

    @is_required.setter
    def bucket_id(self, is_required):
        self.__is_required = is_required

    @property
    def min_value(self):
        return self.__min_value

    @min_value.setter
    def min_value(self, min_value):
        self.__min_value = min_value

    @property
    def min_error_code(self):
        return self.__min_error_code

    @min_error_code.setter
    def min_error_code(self, min_error_code):
        self.__min_error_code = min_error_code

    @property
    def max_value(self):
        return self.__max_value

    @max_value.setter
    def max_value(self, max_value):
        self.__max_value = max_value

    @property
    def max_error_code(self):
        return self.__max_error_code

    @max_error_code.setter
    def max_error_code(self, max_error_code):
        self.__max_error_code = max_error_code

    @property
    def content_format(self):
        return self.__content_format

    @content_format.setter
    def content_format(self, content_format):
        self.__content_format = content_format


class FieldType(Enum):
    TypeInt = 'int'
    TypeString = 'string'
    TypeDate = 'date'


class FieldValueType(Enum):
    ExceedMax = 'exceedMax'
    BelowMin = 'belowMin'
    Max = 'max'
    Min = 'min'
