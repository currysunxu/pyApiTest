from hamcrest import assert_that
from ptest.decorator import TestClass, Test, BeforeClass

from E1_API_Automation.Lib.HamcrestExister import exist
from E1_API_Automation.Business.LearningProfileSevice import LearningProfileService
from E1_API_Automation.Settings import env_key
from E1_API_Automation.Test_Data.LearningProfileData import LearningProfileData


@TestClass()
class LearningProfileTestCases():
    @BeforeClass()
    def set_up(self):
        self.learning_profile_service = LearningProfileService()

    @Test(tags='stg, live')
    def test_learning_profile(self):
        student_id = LearningProfileData.learing_profile_data[env_key]['student_id']
        class_id = LearningProfileData.learing_profile_data[env_key]['class_id']
        access_token = LearningProfileData.learing_profile_data[env_key]['access_token']
        learning_profile = self.learning_profile_service.get_learning_profile(access_token, student_id, class_id)
        assert_that(learning_profile.status_code == 200)
        assert_that(learning_profile.json(), exist("tjBookingId"))
        assert_that(learning_profile.json(), exist("studentId"))
        assert_that(learning_profile.json(), exist("offlineAttendanceStatus"))
        assert_that(learning_profile.json(), exist("skillType"))