import jmespath
from hamcrest import assert_that
from ptest.decorator import TestClass, Test

from E1_API_Automation.Lib.HamcrestExister import exist
from E1_API_Automation.Test.PT.ProgressTestBase import ProgressTestClass
from E1_API_Automation.Test_Data.PTData import PTUsers
from ...Lib.HamcrestMatcher import match_to
from ...Settings import env_key


@TestClass()
class PTAPITestCases(ProgressTestClass):

    @Test()
    def test_stuff_login(self):
        response = self.PTService.stuff_login(PTUsers.pt_user[env_key]['username'],
                                              PTUsers.pt_user[env_key]['password'])
        assert_that(response.status_code == 200)
        assert_that(response.json(), match_to("UserInfo.UserId"))
        assert_that(response.json(), match_to("UserInfo.FunctionalRole"))

    @Test()
    def test_course_schedule(self):
        user_info = self.PTService.stuff_login(PTUsers.pt_user[env_key]['username'],
                                               PTUsers.pt_user[env_key]['password'])
        teacher_id = jmespath.search('UserInfo.UserId', user_info.json())
        course_schedule = self.PTService.get_course_schedule(teacher_id, PTUsers.pt_user[env_key]['school'],
                                                             PTUsers.pt_user[env_key]['hf_scheduledDate'])
        assert_that(course_schedule.json(), match_to("[].ProgressTestCollection[].Key"))
        assert_that(course_schedule.json(), match_to("[].ProgressTestCollection[].CourseKey"))

    @Test()
    def test_sspt_course_schedule(self):
        user_info = self.PTService.stuff_login(PTUsers.pt_user[env_key]['username'],
                                               PTUsers.pt_user[env_key]['password'])
        teacher_id = jmespath.search('UserInfo.UserId', user_info.json())
        course_schedule = self.PTService.get_sspt_course_schedule(teacher_id, PTUsers.pt_user[env_key]['school'],
                                                                  PTUsers.pt_user[env_key]['ss_scheduledDate'])
        assert_that(course_schedule.json(), match_to("[].ProgressTestCollection[].Key"))
        assert_that(course_schedule.json(), match_to("[].ProgressTestCollection[].CourseKey"))

    @Test()
    def test_root_course_info(self):
        self.PTService.stuff_login(PTUsers.pt_user[env_key]['username'], PTUsers.pt_user[env_key]['password'])
        root_course_id = PTUsers.RootCourseKey
        for key in root_course_id:
            root_course_info = self.PTService.get_root_course_info(root_course_id[key])
            assert_that(root_course_info.status_code == 200)

    @Test()
    def test_region_info(self):
        self.PTService.stuff_login(PTUsers.pt_user[env_key]['username'], PTUsers.pt_user[env_key]['password'])
        region_key = PTUsers.region_key
        for key in region_key:
            school_info = self.PTService.query_school_info(region_key[key])
            assert_that(school_info.status_code == 200)
            assert_that(school_info.json(), match_to("[].Name"))
            assert_that(school_info.json(), match_to("[].Code"))

    @Test()
    def test_get_web_socket(self):
        web_socket = self.PTService.get_web_socket_url()
        assert_that(web_socket.json(), match_to("WebSocketFullUrl"))

    @Test()
    def test_tb_books_info(self):
        books_info = self.PTService.get_books_info("tb")
        assert_that(books_info.json(), match_to("[].Key"))
        assert_that(books_info.json(), match_to("[].Name"))

    @Test()
    def test_ss_books_info(self):
        books_info = self.PTService.get_books_info("ss")
        assert_that(books_info.json(), match_to("[].Key"))
        assert_that(books_info.json(), match_to("[].Name"))

    @Test()
    def test_tb_content_info(self):
        book_key_list = self.PTService.get_book_key_list("tb")
        content_info = self.PTService.post_content_info(book_key_list, "PT")
        assert_that(content_info.status_code == 200)

    @Test()
    def test_ss_content_info(self):
        book_key_list = self.PTService.get_book_key_list("ss")
        content_info = self.PTService.post_content_info(book_key_list, "SSPT")
        assert_that(content_info.status_code == 200)

    @Test()
    def test_tb_synchronize(self):
        book_list = self.PTService.get_book_key_list("tb")
        for book_key in book_list:
            course_node = self.PTService.post_courseNode_sync(book_key)
            assert_that(course_node.json(), exist("LastStamp"))
            assert_that(course_node.json(), exist("LastKey"))
            activity = self.PTService.post_activity_sync(book_key)
            assert_that(activity.json(), exist("LastStamp"))
            assert_that(activity.json(), exist("LastKey"))
            Binary_data = self.PTService.post_binary_data_sync(book_key)
            assert_that(Binary_data.json(), exist("LastStamp"))
            assert_that(Binary_data.json(), exist("LastKey"))

    @Test()
    def test_ss_synchronize(self):
        book_list = self.PTService.get_book_key_list("ss")
        for book_key in book_list:
            course_node = self.PTService.post_courseNode_sync(book_key)
            assert_that(course_node.json(), exist("LastStamp"))
            assert_that(course_node.json(), exist("LastKey"))
            activity = self.PTService.post_activity_sync(book_key)
            assert_that(activity.json(), exist("LastStamp"))
            assert_that(activity.json(), exist("LastKey"))
            Binary_data = self.PTService.post_binary_data_sync(book_key)
            assert_that(Binary_data.json(), exist("LastStamp"))
            assert_that(Binary_data.json(), exist("LastKey"))
