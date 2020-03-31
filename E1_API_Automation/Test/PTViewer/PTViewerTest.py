from hamcrest import assert_that
from ptest.decorator import TestClass, Test, BeforeClass

from E1_API_Automation.Business.E1TPIService import *
from E1_API_Automation.Business.PTViewer import PTViewerService
from E1_API_Automation.Business.ProgressTest import PTService
from E1_API_Automation.Lib.HamcrestMatcher import match_to
from E1_API_Automation.Settings import E1TPI_ENVIRONMENT, env_key, ENVIRONMENT
from E1_API_Automation.Test_Data.PTViewerData import *


@TestClass()
class PTViewerTestCases:

    @BeforeClass()
    def create_service(self):
        self.e1tpi_service = E1TPIService(E1TPI_ENVIRONMENT)
        self.pt_viewer_service = PTViewerService(ENVIRONMENT)
        self.pt_service = PTService(ENVIRONMENT)

    @Test(tags='stg, live')
    def test_get_pt_viewer_link(self):
        pt_viewer_data = PTViewerData.pt_viewer_data[env_key]
        pt_viewer_link = self.e1tpi_service.get_pt_viewer_link(pt_viewer_data)
        assert_that(pt_viewer_link.status_code == 200)

    @Test(tags='stg, live')
    def test_get_student_by_batch(self):
        self.pt_service.stuff_login(PTViewerData.pt_viewer_data[env_key]['username'],
                                    PTViewerData.pt_viewer_data[env_key]['password'])
        student_id = PTViewerData.pt_viewer_data[env_key]['studentsId']
        student_by_batch = self.pt_viewer_service.student_by_batch(student_id)
        assert_that(student_by_batch.status_code == 200)

    @Test(tags='stg, live')
    def test_progress_test_summary(self):
        self.pt_service.stuff_login(PTViewerData.pt_viewer_data[env_key]['username'],
                                    PTViewerData.pt_viewer_data[env_key]['password'])
        student_id = PTViewerData.pt_viewer_data[env_key]['studentsId']
        progress_test_key = PTViewerData.pt_viewer_data[env_key]['ptPrimaryKey']
        progress_test_summary = self.pt_viewer_service.progress_test_summary(progress_test_key, student_id)
        assert_that(progress_test_summary.status_code == 200)
        assert_that(progress_test_summary.json(), match_to("UnitName"))
        assert_that(progress_test_summary.json(), match_to("ProgressTestCourseNodes"))