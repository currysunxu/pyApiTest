
class LearningPlan:
    def __init__(self, product_id, plan_business_key, bucket_id, student_key):
        self.__product_id = product_id
        self.__plan_business_key = plan_business_key
        self.__bucket_id = bucket_id
        self.__student_key = student_key
        self.__plan_type = None
        self.__state = None
        self.__route = None
        self.__learning_unit = None
        self.__created_time = None
        self.__created_by = None
        self.__last_updated_time = None
        self.__last_updated_by = None
        self.__start_time = None
        self.__end_time = None
        self.__system_key = None

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
    def bucket_id(self):
        return self.__bucket_id

    @bucket_id.setter
    def bucket_id(self, bucket_id):
        self.__bucket_id = bucket_id

    @property
    def student_key(self):
        return self.__student_key

    @student_key.setter
    def student_key(self, student_key):
        self.__student_key = student_key

    @property
    def plan_type(self):
        return self.__plan_type

    @plan_type.setter
    def plan_type(self, plan_type):
        self.__plan_type = plan_type

    @property
    def route(self):
        return self.__route

    @route.setter
    def route(self, route):
        self.__route = route

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, state):
        self.__state = state

    @property
    def learning_unit(self):
        return self.__learning_unit

    @learning_unit.setter
    def learning_unit(self, learning_unit):
        self.__learning_unit = learning_unit

    @property
    def created_time(self):
        return self.__created_time

    @created_time.setter
    def created_time(self, created_time):
        self.__created_time = created_time

    @property
    def created_by(self):
        return self.__created_by

    @created_by.setter
    def created_by(self, created_by):
        self.__created_by = created_by

    @property
    def last_updated_time(self):
        return self.__last_updated_time

    @last_updated_time.setter
    def last_updated_time(self, last_updated_time):
        self.__last_updated_time = last_updated_time

    @property
    def last_updated_by(self):
        return self.__last_updated_by

    @last_updated_by.setter
    def last_updated_by(self, last_updated_by):
        self.__last_updated_by = last_updated_by

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

    @property
    def system_key(self):
        return self.__system_key

    @system_key.setter
    def system_key(self, system_key):
        self.__system_key = system_key
