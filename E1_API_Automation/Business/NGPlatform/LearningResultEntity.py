
class LearningResultEntity:
    def __init__(self, product, student_key, product_module):
        self.__product = product
        self.__student_key = student_key
        self.__product_module = product_module
        self.__business_key = None
        # self.__plan_system_key = None
        # self.__trace_key = None
        self.__route = None
        # self.__atomic_key = None
        self.__expected_score = None
        self.__actual_score = None
        self.__created_by = None
        self.__extension = None
        self.__details = None
        self.__duration = None
        self.__start_time = None
        self.__end_time = None

    @property
    def product(self):
        return self.__product

    @product.setter
    def product(self, product):
        self.__product = product

    @property
    def business_key(self):
        return self.__business_key

    @business_key.setter
    def business_key(self, business_key):
        self.__business_key = business_key

    @property
    def student_key(self):
        return self.__student_key

    @student_key.setter
    def student_key(self, student_key):
        self.__student_key = student_key

    # @property
    # def plan_system_key(self):
    #     return self.__plan_system_key
    #
    # @plan_system_key.setter
    # def plan_system_key(self, plan_system_key):
    #     self.__plan_system_key = plan_system_key

    @property
    def product_module(self):
        return self.__product_module

    @product_module.setter
    def product_module(self, product_module):
        self.__product_module = product_module

    # @property
    # def trace_key(self):
    #     return self.__trace_key
    #
    # @trace_key.setter
    # def trace_key(self, trace_key):
    #     self.__trace_key = trace_key

    @property
    def route(self):
        return self.__route

    @route.setter
    def route(self, route):
        self.__route = route

    # @property
    # def atomic_key(self):
    #     return self.__atomic_key
    #
    # @atomic_key.setter
    # def atomic_key(self, atomic_key):
    #     self.__atomic_key = atomic_key

    @property
    def expected_score(self):
        return self.__expected_score

    @expected_score.setter
    def expected_score(self, expected_score):
        self.__expected_score = expected_score

    @property
    def actual_score(self):
        return self.__actual_score

    @actual_score.setter
    def actual_score(self, actual_score):
        self.__actual_score = actual_score

    @property
    def created_by(self):
        return self.__created_by

    @created_by.setter
    def created_by(self, created_by):
        self.__created_by = created_by

    @property
    def extension(self):
        return self.__extension

    @extension.setter
    def extension(self, extension):
        self.__extension = extension

    @property
    def details(self):
        return self.__details

    @details.setter
    def details(self, details):
        self.__details = details

    @property
    def duration(self):
        return self.__duration

    @duration.setter
    def duration(self, duration):
        self.__duration = duration

    @property
    def start_time(self):
        return self.__start_time

    @start_time.setter
    def start_time(self, start_time):
        self.__start_time = start_time

    @property
    def end_time(self):
        return self.__end_time

    @end_time.setter
    def end_time(self, end_time):
        self.__end_time = end_time

