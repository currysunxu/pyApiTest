import jmespath
from hamcrest import assert_that
from ptest.decorator import TestClass, Test, BeforeClass

from E1_API_Automation.Business.E1TPIService import *
from E1_API_Automation.Business.PTViewer import HomeworkViewerService
from E1_API_Automation.Business.TrailblazerV3 import TrailbazerService
from E1_API_Automation.Lib.HamcrestMatcher import match_to
from E1_API_Automation.Settings import E1TPI_ENVIRONMENT, env_key, ENVIRONMENT
from E1_API_Automation.Test_Data.PTViewerData import *
from E1_API_Automation.Test_Data.TBData import TBUsers


@TestClass()
class HomeworkViewerTestCases:

    @BeforeClass()
    def create_service(self):
        self.e1tpi_service = E1TPIService(E1TPI_ENVIRONMENT)
        self.homework_viewer_service = HomeworkViewerService(ENVIRONMENT)
        self.tb_service = TrailbazerService(ENVIRONMENT, TBUsers.tb_user[env_key]['username'],
                                         TBUsers.tb_user[env_key]['password'])
        profile = self.tb_service.get_student_profile().json()
        self.book_key = jmespath.search('CourseGroups[0].Book.Key', profile)
        self.course_plan_key = jmespath.search('CourseGroups[0].Group.CoursePlanKey', profile)

    @Test(tags='stg, live')
    def test_get_homework_viewer_link(self):
        homework_viewer_data = HomeworkViewerData.homework_viewer_data[env_key]
        homework_viewer_link = self.e1tpi_service.get_homework_viewer_link(homework_viewer_data)
        assert_that(homework_viewer_link.status_code == 200)

    @Test(tags='stg, live')
    def test_homework_viewer_book_structure(self):
        book_structure = self.homework_viewer_service.homework_viewer_book_structure(self.book_key,
                                                                                     HomeworkViewerData.homework_viewer_data[env_key]['Region'],
                                                                                     self.course_plan_key)
        assert_that(book_structure.status_code == 200)
        assert_that(book_structure.json()), match_to('ActivityKeys')

    @Test(tags='stg, live')
    def test_homework_viewer_answers(self):
        student_answers = self.homework_viewer_service.homework_viewer_answers(
            HomeworkViewerData.homework_viewer_data[env_key]['studentsId'],
            HomeworkViewerData.homework_viewer_data[env_key]['CourseActivityKeys'])
        assert_that(student_answers.status_code == 200)
        assert_that(student_answers.json()), match_to('StudentsAnswers')

    @Test(tags='stg, live')
    def test_homework_viewer_progress_info(self):
        progress_info = self.homework_viewer_service.homework_viewer_progress_info(
            HomeworkViewerData.homework_viewer_data[env_key]['studentsId'],
            HomeworkViewerData.homework_viewer_data[env_key]['CourseActivityKeys'])
        assert_that(progress_info.status_code == 200)
        assert_that(progress_info.json()), match_to('StudentsProgressInfo')
