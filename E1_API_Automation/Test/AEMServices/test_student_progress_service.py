from ...Business.AEM import StudentProgressService
from ptest.decorator import TestClass, Test, BeforeClass

from hamcrest import assert_that, equal_to


@TestClass()
class TestStudentProgressService:
    @BeforeClass()
    def create_service(self):
        self.service = StudentProgressService()

    @Test()
    def get_student_activity_detail_history_by_activity_ids_2_students(self):
        response = self.service.get_student_activity_detial_history_by_activity_ids([17847, 17451],
                                                                                    [12226207, 12224023], 'FR')
        history_list = response.ActivityDetailHistoryList.ActivityDetailHistoryList
        result_student_ids = list(set(map(lambda x: x.Student_Id, history_list)))

        # Verify the Student List output is correct
        assert_that(len(history_list), equal_to(2))
        assert_that(result_student_ids, equal_to([ 12224023, 12226207]))

    @Test()
    def get_student_activity_detail_history_by_activity_ids_1_student(self):
        response = self.service.get_student_activity_detial_history_by_activity_ids([17847, 17451], [12224023])
        history_list = response.ActivityDetailHistoryList.ActivityDetailHistoryList
        assert_that(len(history_list), equal_to(1))
        assert_that(len(history_list[0].ActivityScore.ActivityScore), equal_to(2))

        # Verify the activity list is correct.
        activity_ids = list(set(map(lambda  x:x.ActivityId, history_list[0].ActivityScore.ActivityScore)))
        assert_that(activity_ids, equal_to([17451, 17847]))
