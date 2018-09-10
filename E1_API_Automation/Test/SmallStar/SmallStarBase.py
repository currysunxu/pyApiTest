import jmespath
from ptest.decorator import TestClass, BeforeClass, AfterMethod, BeforeMethod

from E1_API_Automation.Business.SmallStarV3 import SmallStarService
from E1_API_Automation.Settings import ENVIRONMENT


@TestClass()
class SmallStarBase():
    current_book_key = None
    group_key = None
    product_code = None
    course_plan_key = None

    @BeforeClass()
    def set_up(self):
        self.small_star_service = SmallStarService(ENVIRONMENT)
        self.set_context()


    @AfterMethod()
    def sign_out(self):
        self.small_star_service.sign_out()

    @BeforeMethod()
    def sigin(self):
        self.small_star_service.login("ssv303", '12345')

    def set_context(self):
        self.small_star_service.login('ssv303', '12345')
        response = self.small_star_service.get_student_profile().json()
        self.current_book_key = jmespath.search("CurrentBookKey", response)
        self.group_key = jmespath.search("CourseGroups[?Group.BookKey=='{}'].Group.Key".format(self.current_book_key), response)[0]
        self.product_code = jmespath.search("CourseGroups[?Group.BookKey=='{}'].Group.ProductCode".format(self.current_book_key), response)[0]
        self.course_plan_key =jmespath.search("CourseGroups[?Group.BookKey=='{}'].Group.CoursePlanKey".format(self.current_book_key), response)[0]
        self.small_star_service.sign_out()