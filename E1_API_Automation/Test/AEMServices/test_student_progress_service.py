from ...Business.WCFServices import StudentProgressService
from ...Test_Data.StudentProgresSeviceData import StudentProgressData
from E1_API_Automation.Settings import *
from ptest.decorator import TestClass, Test, BeforeClass


from hamcrest import assert_that, equal_to


@TestClass()
class TestStudentProgressService:
    @BeforeClass()
    def create_service(self):
        self.service = StudentProgressService()


    @Test()
    def get_student_activity_detail_history_by_activity_ids_2_students(self):
        activitiy_list = StudentProgressData.activity_data[env_key]['FR']['activity_id']
        student_id_List = StudentProgressData.activity_data[env_key]['FR']['student_id']
        response = self.service.get_student_activity_detial_history_by_activity_ids(activitiy_list,
                                                                                    student_id_List, 'FR')
        history_list = response.ActivityDetailHistoryList.ActivityDetailHistoryList
        result_student_ids = list(set(map(lambda x: x.Student_Id, history_list)))

        # Verify the Student List output is correct
        assert_that(len(history_list), equal_to(len(student_id_List)))
        assert_that(sorted(result_student_ids), equal_to(sorted(student_id_List)))

    @Test()
    def get_student_activity_detail_history_by_activity_ids_1_student(self):
        activitiy_list = StudentProgressData.activity_data[env_key]['FR']['activity_id']
        student_id = [StudentProgressData.activity_data[env_key]['FR']['student_id'][0]]
        response = self.service.get_student_activity_detial_history_by_activity_ids(activitiy_list, student_id)
        history_list = response.ActivityDetailHistoryList.ActivityDetailHistoryList
        assert_that(len(history_list), equal_to(len(student_id)))
        assert_that(len(history_list[0].ActivityScore.ActivityScore), equal_to(len(activitiy_list)))

        # Verify the activity list is correct.
        activity_ids = list(set(map(lambda  x:x.ActivityId, history_list[0].ActivityScore.ActivityScore)))
        assert_that(sorted(activity_ids), equal_to(sorted(activitiy_list)))
