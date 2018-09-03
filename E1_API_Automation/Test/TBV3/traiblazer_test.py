import jmespath
from hamcrest import assert_that, equal_to

from ptest.decorator import TestClass, Test
from ...Lib.HamcrestMatcher import match_to
from ...Lib.HamcrestExister import exist

from ...Settings import env_key
from .traiblazer_base import TraiblazerBaseClass
from ...Test_Data.TBData import TBUsers


@TestClass()
class TBTestCases(TraiblazerBaseClass):
    @Test()
    def test_student_profile(self):
        self.tb_test.login(TBUsers.tb_user[env_key]['username'], TBUsers.tb_user[env_key]['password'])
        response = self.tb_test.get_student_profile().json()

        assert_that(response, match_to("UserId"))
        assert_that(response, exist("Email"))
        assert_that(response, match_to("Name"))
        assert_that(response, match_to("FunctionalRole"))
        assert_that(response, match_to("FirstName"))
        assert_that(response, match_to("LastName"))
        assert_that(response, match_to("EnglishFirstName"))
        assert_that(response, exist("EnglishMiddleName"))
        assert_that(response, match_to("EnglishLastName"))
        assert_that(response, exist("Gender"))
        assert_that(response, match_to("MarketRegion"))
        assert_that(response, match_to("CurrentBookKey"))
        assert_that(response, exist("AvatarBinaryStorage"))
        assert_that(response, exist("AvatarKey"))
        assert_that(response, exist("AvatarUrl"))
        assert_that(response, match_to("CourseGroups"))
        assert_that(response, exist("IsExpired"))
        assert_that(response, match_to("Key"))

    @Test()
    def test_course_node_synchronize_status(self):
        self.tb_test.login(TBUsers.tb_user[env_key]['username'], TBUsers.tb_user[env_key]['password'])
        self.tb_test.get_student_info()
        activity_contents = self.tb_test.course_node_synchronize(self.tb_test.active_book, self.tb_test.course_plan_key)
        assert_that(activity_contents.status_code == 200)

    @Test()
    def test_course_node_synchronize_schema(self):
        self.tb_test.login(TBUsers.tb_user[env_key]['username'], TBUsers.tb_user[env_key]['password'])
        self.tb_test.get_student_info()
        activity_contents = self.tb_test.course_node_synchronize(self.tb_test.active_book,
                                                                 self.tb_test.course_plan_key).json()
        assert_that(activity_contents, match_to("LastStamp"))
        assert_that(activity_contents, match_to("LastKey"))
        assert_that(activity_contents, match_to("Upserts"))
        assert_that(activity_contents, exist("Removals"))

    @Test()
    def test_course_node_synchronize_function(self):
        self.tb_test.login(TBUsers.tb_user[env_key]['username'], TBUsers.tb_user[env_key]['password'])
        self.tb_test.get_student_info()
        activity_contents = self.tb_test.course_node_synchronize(self.tb_test.active_book,
                                                                 self.tb_test.course_plan_key).json()
        book_content = jmespath.search("Upserts", activity_contents)
        assert_that(len(book_content) > 0)

    @Test()
    def test_activity_entity_status(self):
        self.tb_test.login(TBUsers.tb_user[env_key]['username'], TBUsers.tb_user[env_key]['password'])
        level_16_contents = self.tb_test.filter_activity_keys(level_no=16)
        response = self.tb_test.acitivity_entity_web(jmespath.search("@[*].ActivityKeys[0]", level_16_contents))
        assert_that(response.json(), match_to("Activities"))
        assert_that(response.json(), match_to("Resources"))
        assert_that(response.status_code == 200)

    @Test()
    def test_activity_entity_function(self):
        self.tb_test.login(TBUsers.tb_user[env_key]['username'], TBUsers.tb_user[env_key]['password'])
        level_16_contents = self.tb_test.filter_activity_keys(level_no=16)
        response = self.tb_test.acitivity_entity_web(jmespath.search("@[*].ActivityKeys[0]", level_16_contents))
        assert_that(len(jmespath.search('Activities', response.json())) == len(level_16_contents))
        assert_that(jmespath.search('Activities', response.json())[0], match_to("Stimulus"))
        assert_that(jmespath.search('Activities', response.json())[0], exist("Type"))
        assert_that(jmespath.search('Activities', response.json())[0], exist("Tags"))
        assert_that(jmespath.search('Activities', response.json())[0], match_to("Body"))
        assert_that(jmespath.search('Activities', response.json())[0], match_to("Key"))
        assert_that(jmespath.search('Activities', response.json())[0], exist("IsDynamicallyOrganized"))
        assert_that(jmespath.search('Activities', response.json())[0], match_to("Title"))
        assert_that(jmespath.search('Activities', response.json())[0], exist("ContentKey"))
        assert_that(jmespath.search('Activities', response.json())[0], match_to("Questions"))
