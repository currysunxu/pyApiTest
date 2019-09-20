
class LearningResultEntity:
    def __init__(self, product_id, plan_business_key, student_key):
        self.__product_id = product_id
        self.__plan_business_key = plan_business_key
        self.__student_key = student_key
        self.__plan_system_key = None
        self.__plan_type = None
        self.__trace_key = None
        self.__route = None
        self.__atomic_key = None
        self.__expected_score = None
        self.__actual_score = None
        self.__created_by = None
        self.__extension = None
        self.__details = None

    @property
    def product_id(self):
        return self.__product_id

    @product_id.setter
    def product_id(self, product_id):
        self.__product_id = product_id

    @property
    def plan_business_key(self):
        return self.__plan_business_key

    @plan_business_key.setter
    def plan_business_key(self, plan_business_key):
        self.__plan_business_key = plan_business_key

    @property
    def student_key(self):
        return self.__student_key

    @student_key.setter
    def student_key(self, student_key):
        self.__student_key = student_key

    @property
    def plan_system_key(self):
        return self.__plan_system_key

    @plan_system_key.setter
    def plan_system_key(self, plan_system_key):
        self.__plan_system_key = plan_system_key

    @property
    def plan_type(self):
        return self.__plan_type

    @plan_type.setter
    def plan_type(self, plan_type):
        self.__plan_type = plan_type

    @property
    def trace_key(self):
        return self.__trace_key

    @trace_key.setter
    def trace_key(self, trace_key):
        self.__trace_key = trace_key

    @property
    def route(self):
        return self.__route

    @route.setter
    def route(self, route):
        self.__route = route

    @property
    def atomic_key(self):
        return self.__atomic_key

    @atomic_key.setter
    def atomic_key(self, atomic_key):
        self.__atomic_key = atomic_key

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

