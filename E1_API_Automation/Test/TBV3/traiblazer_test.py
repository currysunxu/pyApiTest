import jmespath
from hamcrest import assert_that, equal_to, contains_string

from ptest.decorator import TestClass, Test
from ...Lib.HamcrestMatcher import match_to
from ...Lib.HamcrestExister import exist

from .traiblazer_base import TraiblazerBaseClass


@TestClass()
class TBTestCases(TraiblazerBaseClass):
    @Test(tags="qa, stg, live")
    def test_student_profile(self):
        response = self.tb_test.get_student_profile().json()
        assert_that(response, match_to("UserId"))
        assert_that(response, exist("Email"))
        assert_that(response, match_to("Name"))
        assert_that(response, match_to("FunctionalRole"))
        assert_that(response, exist("FirstName"))
        assert_that(response, exist("LastName"))
        assert_that(response, exist("EnglishFirstName"))
        assert_that(response, exist("EnglishMiddleName"))
        assert_that(response, exist("EnglishLastName"))
        assert_that(response, exist("Gender"))
        assert_that(response, match_to("MarketRegion"))
        assert_that(response, match_to("CurrentBookKey"))
        assert_that(response, exist("AvatarBinaryStorage"))
        assert_that(response, exist("AvatarKey"))
        assert_that(response, exist("AvatarUrl"))
        assert_that(response, match_to("CourseGroups"))
        assert_that(response, exist("IsExpired"))
        assert_that(response, match_to("Key"))

    @Test(tags="qa, stg, live")
    def test_course_node_synchronize_status(self):
        activity_contents = self.tb_test.course_node_synchronize(self.tb_test.active_book, self.tb_test.course_plan_key)
        assert_that(activity_contents.status_code == 200)

    @Test(tags="qa, stg, live" )
    def test_get_privacy_policy(self):
        privacy_content = self.tb_test.get_privacy_content()
        assert_that(privacy_content.status_code == 200)
        assert_that(privacy_content.json(), exist("LatestPrivacyPolicyDocumentResult"))

    @Test(tags="qa, stg, live" )
    def test_save_privacy(self):
        save_result = self.tb_test.save_privacy(2, 3)
        assert_that(save_result.status_code == 204)

    @Test(tags="qa, stg, live")
    def test_course_node_synchronize_schema(self):
        activity_contents = self.tb_test.course_node_synchronize(self.tb_test.active_book,
                                                                 self.tb_test.course_plan_key).json()
        assert_that(activity_contents, match_to("LastStamp"))
        assert_that(activity_contents, match_to("LastKey"))
        assert_that(activity_contents, match_to("Upserts"))
        assert_that(activity_contents, exist("Removals"))

    @Test(tags="qa,  stg, live")
    def test_course_node_synchronize_function(self):
        activity_contents = self.tb_test.course_node_synchronize(self.tb_test.active_book,
                                                                 self.tb_test.course_plan_key).json()
        assert_that(len(activity_contents) > 0)

    @Test(tags="qa,  stg, live")
    def test_activity_entity_status(self):
        response = self.tb_test.acitivity_entity_web(self.tb_test.book_contents.get_activity_keys())
        assert_that(response.json(), match_to("Activities"))
        assert_that(response.json(), match_to("Resources"))
        assert_that(response.status_code == 200)

    @Test(tags="qa,  stg, live")
    def test_activity_entity_function(self):
        response = self.tb_test.acitivity_entity_web(self.tb_test.book_contents.get_activity_keys())
        assert_that(
            len(jmespath.search('Activities', response.json())) == len(self.tb_test.book_contents.get_activity_keys()))
        assert_that(jmespath.search('Activities', response.json())[0], match_to("Stimulus"))
        assert_that(jmespath.search('Activities', response.json())[0], exist("Type"))
        assert_that(jmespath.search('Activities', response.json())[0], exist("Tags"))
        assert_that(jmespath.search('Activities', response.json())[0], match_to("Body"))
        assert_that(jmespath.search('Activities', response.json())[0], match_to("Key"))
        assert_that(jmespath.search('Activities', response.json())[0], exist("IsDynamicallyOrganized"))
        assert_that(jmespath.search('Activities', response.json())[0], match_to("Title"))
        assert_that(jmespath.search('Activities', response.json())[0], exist("ContentKey"))
        assert_that(jmespath.search('Activities', response.json())[0], match_to("Questions"))

    @Test(tags="qa,  stg, live")
    def test_course_unlock_status(self):
        response = self.tb_test.course_unlock(self.tb_test.active_book)
        assert_that(response.status_code == 200)

    @Test(tags="qa,  stg, live")
    def test_reward_summary_status(self):
        response = self.tb_test.query_motivation_reward_summary()
        assert_that(response.status_code == 200)

    @Test(tags="qa, stg, live")
    def test_student_progress(self):
        unlocked_lessons = self.tb_test.course_unlock(self.tb_test.active_book).json()
        self.picked_lesson = unlocked_lessons[0]
        response = self.tb_test.homework_lesson_answer(self.picked_lesson, pass_lesson=False)

        activity_nodes = self.tb_test.book_contents.get_child_nodes_by_parent_key(self.picked_lesson)
        try:
            lesson_score = jmespath.search('StudentScore',
                                           self.tb_test.lesson_score_summary([self.picked_lesson]).json()[0])
        except:
            lesson_score = 0

        for i in range(1, len(activity_nodes) + 1):
            self.tb_test.student_progress(self.picked_lesson, i, len(activity_nodes))
        response = self.tb_test.homework_lesson_answer(self.picked_lesson)

        assert_that(response.status_code == 200)

        after_lesson_score = jmespath.search('StudentScore',
                                             self.tb_test.lesson_score_summary([self.picked_lesson]).json()[0])
        assert_that((after_lesson_score - lesson_score) > 0)

    @Test(tags="qa")
    def test_student_motivation_points(self):
        # get the cleaned point lesson key and balance value
        self.picked_lesson, updated_balance = self.clean_motivation_audit(self.tb_test.user_id)
        if self.picked_lesson == None:
            self.picked_lesson = self.tb_test.course_unlock(self.tb_test.active_book).json()[0]
        activity_nodes = self.tb_test.book_contents.get_child_nodes_by_parent_key(self.picked_lesson)

        for i in range(1, len(activity_nodes) + 1):
            self.tb_test.student_progress(self.picked_lesson, i, len(activity_nodes))
        response = self.tb_test.homework_lesson_answer(self.picked_lesson)

        assert_that(len(response.json()) > 0)

        # verify the balance valued added
        new_added_points = jmespath.search("[*].Balance", response.json())
        lambda x: assert_that(x > updated_balance), new_added_points

        point_audit = self.tb_test.query_motivation_point_audit()
        lambda x: assert_that(x in jmespath.search("[*].Balance", point_audit.json())), new_added_points
        assert_that(self.picked_lesson ==
                    jmespath.search("@[?Balance==`{0}`].Identifier".format(new_added_points[0]), point_audit.json())[0])

    @Test(tags="qa, stg, live")
    def test_homework_lesson_correction(self):
        unlocked_lessons = self.tb_test.course_unlock(self.tb_test.active_book).json()
        self.picked_lesson = unlocked_lessons[0]
        print(self.picked_lesson)
        activity_nodes = self.tb_test.book_contents.get_child_nodes_by_parent_key(self.picked_lesson)
        for i in range(1, len(activity_nodes) + 1):
            self.tb_test.student_progress(unlocked_lessons[3], i, len(activity_nodes))
        response = self.tb_test.homework_lesson_answer(self.picked_lesson, pass_lesson=False)
        correction = self.tb_test.homework_lesson_correction(self.picked_lesson)
        assert_that(correction.status_code == 200)

    @Test(tags="qa,  stg, live")
    def test_homework_motivation_task_info_status(self):
        response = self.tb_test.get_homework_motivation_task_info(self.tb_test.active_book)
        assert_that(response.status_code == 200)

    @Test(tags="qa,  stg, live")
    def test_homework_motivation_task_info_function(self):
        response = self.tb_test.get_homework_motivation_task_info(self.tb_test.active_book)
        assert_that(len(response.json()) > 0)
        assert_that(response.json()[0], exist("CompletedCount"))
        assert_that(response.json()[0], match_to("Description"))
        assert_that(response.json()[0], exist("EarnedTotalPointAmount"))
        assert_that(response.json()[0], match_to("MotivationCode"))
        assert_that(response.json()[0], exist("MotivationTaskStatus"))
        assert_that(response.json()[0], match_to("Name"))
        assert_that(response.json()[0], match_to("Resources"))
        assert_that(response.json()[0], match_to("ScopeCourseKey"))
        assert_that(response.json()[0], match_to("TotalCount"))
        assert_that(response.json()[0], exist("TotalPointAmount"))
        assert_that(response.json()[0], match_to("TypeKey"))

    @Test(tags="qa, stg, live")
    def test_get_all_book(self):
        response = self.tb_test.get_all_books()
        assert_that(response.status_code == 200)

    @Test(tags="qa,  stg, live")
    def test_get_all_book_schema(self):
        response = self.tb_test.get_all_books()
        assert_that(len(response.json()) > 0)
        assert_that(response.json()[0], exist("CreatedBy"))
        assert_that(response.json()[0], match_to("CreatedStamp"))
        assert_that(response.json()[0], exist("LastUpdatedBy"))
        assert_that(response.json()[0], match_to("LastUpdatedStamp"))
        assert_that(response.json()[0], exist("State"))
        assert_that(response.json()[0], exist("ActivityKeys"))
        assert_that(response.json()[0], exist("ContentKey"))
        assert_that(response.json()[0], match_to("Name"))
        assert_that(response.json()[0], match_to("ParentNodeKey"))
        assert_that(response.json()[0], exist("TopNodeKey"))
        assert_that(response.json()[0], match_to("Code"))
        assert_that(response.json()[0], exist("Theme"))
        assert_that(response.json()[0], match_to("Type"))
        assert_that(response.json()[0], match_to("Level"))
        assert_that(response.json()[0], exist("CoursePlanKey"))
        assert_that(response.json()[0], exist("Sequence"))
        assert_that(response.json()[0], exist("Title"))
        assert_that(response.json()[0], exist("SubTitle"))
        assert_that(response.json()[0], exist("Description"))
        assert_that(response.json()[0], exist("Body"))
        for book in response.json():
            assert_that(jmespath.search("Code", book), contains_string('TBv3Bk'))

    @Test(tags="qa, stg, live")
    def test_digital_interaction_info_status(self):
        response = self.tb_test.digital_interaction_info(self.tb_test.active_book)
        assert_that(response.status_code == 200)

    @Test(tags="qa,  stg, live")
    def test_digital_interaction_info_schema(self):
        response = self.tb_test.digital_interaction_info(self.tb_test.active_book)
        assert_that(len(response.json()) > 0)
        assert_that(response.json()[0], exist("Title"))
        assert_that(response.json()[0], match_to("Key"))

    @Test(tags="qa,  stg, live")
    def test_progress_assessment_report(self):
        unlocked_lessons = self.tb_test.course_unlock(self.tb_test.active_book).json()
        response = self.tb_test.progress_assessment__report_by_unit(unlocked_lessons[0])
        assert_that(response.json(), exist("StudentId"))
        assert_that(response.json(), match_to("UnitCourseKey"))
        assert_that(jmespath.search("StudentId", response.json()), equal_to(self.tb_test.user_id))
        assert_that(jmespath.search("UnitCourseKey", response.json()), equal_to(unlocked_lessons[0]))

    @Test(tags="qa,  stg, live")
    def test_motivation_point_audit_status(self):
        response = self.tb_test.query_motivation_point_audit()
        assert_that(response.status_code == 200)
        assert_that(len(response.json()) > 0)

    @Test(tags="qa,  stg, live")
    def test_motivation_reward_summary_status(self):
        response = self.tb_test.query_motivation_reward_summary()
        assert_that(response.status_code == 200)
        assert_that(isinstance(response.json(), list))
