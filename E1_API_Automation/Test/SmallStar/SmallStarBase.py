import jmespath
from ptest.decorator import TestClass, BeforeClass, AfterMethod, BeforeMethod

from E1_API_Automation.Business.Athena import Student
from E1_API_Automation.Business.SmallStarV3 import SmallStarService
from E1_API_Automation.Business.TPIService import TPIService
from E1_API_Automation.Settings import ENVIRONMENT, Environment, TPI_ENVIRONMENT


@TestClass()
class SmallStarBase():
    current_book_key = None
    group_key = None
    product_code = None
    course_plan_key = None
    un_lock_lesson_keys = None
    if ENVIRONMENT == Environment.STAGING:
        user_name = "ss3.cn.01"
        password = '12345'
        culture_code = 'zh-CN'
    if ENVIRONMENT == Environment.STAGING_SG:
        user_name = "ss3.id.01"
        password = '12345'
        culture_code = 'id-ID'
    if ENVIRONMENT == Environment.QA:
        user_name = "ss3.cn.01"
        password = '12345'
        culture_code = 'zh-CN'
    if ENVIRONMENT == Environment.LIVE:
        user_name = "ss3.cn.01"
        password = '12345'
        culture_code = 'zh-CN'
    if ENVIRONMENT == Environment.LIVE_SG:
        user_name = "ss3.ru.01"
        password = '12345'
        culture_code = 'ru-RU'

    @BeforeClass()
    def set_up(self):
        self.small_star_service = SmallStarService(ENVIRONMENT)
        self.student = Student(ENVIRONMENT)
        self.tpi_service = TPIService(TPI_ENVIRONMENT)
        self.set_context()

    @AfterMethod()
    def sign_out(self):
        if self.un_lock_lesson_keys:
            self.reset_activity_answer(self.un_lock_lesson_keys[0])
            self.un_lock_lesson_keys = None

        self.small_star_service.sign_out()

    @BeforeMethod()
    def sign_in(self):
        self.small_star_service.login(self.user_name, self.password)

    def set_context(self):
        self.small_star_service.login(self.user_name, self.password)
        response = self.small_star_service.get_student_profile().json()
        self.user_id = jmespath.search('UserId', response)
        self.current_book_key = jmespath.search("CurrentBookKey", response)
        self.group_key = jmespath.search("CourseGroups[?Group.BookKey=='{}'].Group.Key".format(self.current_book_key), response)[0]
        self.group_id = jmespath.search("CourseGroups[?Group.BookKey=='{}'].Group.OdinId".format(self.current_book_key), response)[0]
        self.product_code = jmespath.search("CourseGroups[?Group.BookKey=='{}'].Group.ProductCode".format(self.current_book_key), response)[0]
        self.course_plan_key = jmespath.search("CourseGroups[?Group.BookKey=='{}'].Group.CoursePlanKey".format(self.current_book_key), response)[0]
        self.small_star_service.sign_out()

    def reset_activity_answer(self, lesson_key):
        response, submit_activity_key = self.small_star_service.submit_small_star_student_answers(self.product_code,
                                                                                                  self.group_id,
                                                                                                  self.current_book_key,
                                                                                                  lesson_key,
                                                                                                  self.course_plan_key,
                                                                                                  self.user_id, False)