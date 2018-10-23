from hamcrest import assert_that
from ptest.decorator import TestClass, Test

from E1_API_Automation.Lib.HamcrestExister import exist
from E1_API_Automation.Test.PT.ProgressTestBase import ProgressTestClass
from E1_API_Automation.Test_Data.PTData import PTUsers
from ...Lib.HamcrestMatcher import match_to
from ...Settings import env_key
import jmespath



@TestClass()
class PTAPITestCases(ProgressTestClass):

    @Test()
    def test_stuff_login(self):
        response=self.pttest.stuff_login(PTUsers.pt_user[env_key]['username'], PTUsers.pt_user[env_key]['password'])
        assert_that(response.status_code==200)
        assert_that(response.json(),match_to("UserInfo.UserId"))
        assert_that(response.json(), match_to("UserInfo.FunctionalRole"))

    @Test()
    def test_course_schedule(self):
        user_info=self.pttest.stuff_login(PTUsers.pt_user[env_key]['username'], PTUsers.pt_user[env_key]['password'])
        teacher_id=jmespath.search('UserInfo.UserId',user_info.json())
        course_schedule=self.pttest.get_course_schedule(teacher_id)
        assert_that(course_schedule.json(),match_to("[].ProgressTestCollection[].Key"))
        assert_that(course_schedule.json(), match_to("[].ProgressTestCollection[].CourseKey"))


    @Test()
    def test_root_course_info(self):
        self.pttest.stuff_login(PTUsers.pt_user[env_key]['username'], PTUsers.pt_user[env_key]['password'])
        root_course_id=PTUsers.RootCourseKey
        for key in root_course_id:
            root_course_info=self.pttest.get_root_course_info(root_course_id[key])
            assert_that(root_course_info.status_code==200)


    @Test()
    def test_region_info(self):
        self.pttest.stuff_login(PTUsers.pt_user[env_key]['username'], PTUsers.pt_user[env_key]['password'])
        region_key=PTUsers.region_key
        for key in region_key:
            school_info=self.pttest.query_school_info(region_key[key])
            assert_that(school_info.status_code==200)
            assert_that(school_info.json(), match_to("[].Name"))
            assert_that(school_info.json(), match_to("[].Code"))

    @Test()
    def test_get_web_socket(self):
        web_socket=self.pttest.get_web_socket_url()
        assert_that(web_socket.json(),match_to("WebSocketFullUrl"))

    @Test()
    def test_books_info(self):
        books_info=self.pttest.get_books_info()
        assert_that(books_info.json(),match_to("[].Key"))
        assert_that(books_info.json(), match_to("[].Name"))

    @Test()
    def test_content_info(self):
        content_info=self.pttest.post_content_info(self.pttest.get_book_key_list())
        assert_that(content_info.status_code==200)

    @Test()
    def test_synchronize(self):
        book_list=self.pttest.get_book_key_list()
        for book_key in book_list:
            course_node=self.pttest.post_courseNode_sync(book_key)
            assert_that(course_node.json(),exist("LastStamp"))
            assert_that(course_node.json(), exist("LastKey"))
            activity=self.pttest.post_activity_sync(book_key)
            assert_that(activity.json(),exist("LastStamp"))
            assert_that(activity.json(), exist("LastKey"))
            Binary_data=self.pttest.post_binary_data_sync(book_key)
            assert_that(Binary_data.json(),exist("LastStamp"))
            assert_that(Binary_data.json(), exist("LastKey"))





