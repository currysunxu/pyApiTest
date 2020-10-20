
class StudyPlanEntity:
    def __init__(self, student_id, content_path, product_module):
        self.__studentID = student_id
        self.__product = None
        self.__productModule = product_module
        self.__refId = None
        self.__refContentPath = content_path
        self.__refProps = None
        self.__effectAt = None
        self.__expireAt = None
        self.__startAt = None
        self.__completeAt = None
        self.__state = None

    @property
    def student_id(self):
        return self.__studentID

    @student_id.setter
    def student_id(self, student_id):
        self.__studentID = student_id

    @property
    def product(self):
        return self.__product

    @product.setter
    def product(self, product):
        self.__product = product

    @property
    def product_module(self):
        return self.__productModule

    @product_module.setter
    def product_module(self, product_module):
        self.__productModule = product_module

    @property
    def ref_id(self):
        return self.__refId

    @ref_id.setter
    def ref_id(self, ref_id):
        self.__refId = ref_id

    @property
    def ref_content_path(self):
        return self.__refContentPath

    @ref_content_path.setter
    def ref_content_path(self, ref_content_path):
        self.__refContentPath = ref_content_path

    @property
    def ref_props(self):
        return self.__refProps

    @ref_props.setter
    def ref_props(self, ref_props):
        self.__refProps = ref_props

    @property
    def effect_at(self):
        return self.__effectAt

    @effect_at.setter
    def effect_at(self, effect_at):
        self.__effectAt = effect_at

    @property
    def expire_at(self):
        return self.__expireAt

    @expire_at.setter
    def expire_at(self, expire_at):
        self.__expireAt = expire_at

    @property
    def start_at(self):
        return self.__startAt

    @start_at.setter
    def start_at(self, start_at):
        self.__startAt = start_at

    @property
    def complete_at(self):
        return self.__completeAt

    @complete_at.setter
    def complete_at(self, complete_at):
        self.__completeAt = complete_at

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, state):
        self.__state = state