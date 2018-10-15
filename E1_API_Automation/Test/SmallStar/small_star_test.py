import jmespath
from hamcrest import assert_that
from ptest.decorator import TestClass, Test

from E1_API_Automation.Business.SchoolCourse import CourseBook
from E1_API_Automation.Lib.HamcrestExister import exist
from E1_API_Automation.Settings import ENVIRONMENT, Environment
from E1_API_Automation.Test.SmallStar.SmallStarBase import SmallStarBase

AMOUNT = 500  # 210000#2147483617


@TestClass()
class SmallStarTestCases(SmallStarBase):

    @Test()
    def get_content(self):
        body = {
            "Activity": {
                "UpertsOnly": True,
            },
            "BinaryData": {
                "UpertsOnly": True,
            },
            "BookKey": self.current_book_key,
            "CourseNode": {
                "UpertsOnly": False,
            },
            "DigitalArticle": {
                "UpertsOnly": False,
            },
            "ProductCode": self.product_code
        }
        response = self.small_star_service.fetch_content_update_summary(body)
        assert_that(response.json(), exist('BinaryDataAmount'))
        assert_that(response.json(), exist('ActivityQuestionAmount'))
        assert_that(response.json(), exist('ActivityStimulusAmount'))
        assert_that(response.json(), exist('ActivityAmount'))
        assert_that(response.json(), exist('AcademicElementAmount'))
        assert_that(response.json(), exist('CourseNodeAmount'))
        assert_that(response.json(), exist('DigitalArticleAmount'))
        assert_that(response.json(), exist('BinaryDataSize'))

    @Test()
    def synchronize_binary_data(self):
        response = self.small_star_service.synchronize_binary_data(self.current_book_key, self.course_plan_key,
                                                                   amount=AMOUNT)
        assert_that(len(jmespath.search('Upserts', response.json())) != 0)
        assert_that(response.json(), exist('Upserts'))
        assert_that(len(jmespath.search('Upserts[*].ResourceId', response.json())) != 0)
        assert_that(len(jmespath.search('Upserts[*].Container', response.json())) != 0)
        assert_that("e1-osp" in jmespath.search("Upserts[*].Container", response.json())[0])
        self.check_content_with_last_stamp_and_key(response, self.small_star_service.synchronize_binary_data,
                                                   'ResourceId')

    @Test()
    def synchronize_course_node(self):
        response = self.small_star_service.synchronize_course_node(self.current_book_key, self.course_plan_key,
                                                                   upserts_only=False, amount=AMOUNT)
        assert_that(len(jmespath.search('Upserts', response.json())) != 0)
        assert_that(response.json(), exist('Upserts'))
        assert_that(len(jmespath.search('Upserts[*].TopNodeKey', response.json())) != 0)
        assert_that(len(jmespath.search('Upserts[*].ParentNodeKey', response.json())) != 0)
        assert_that(len(jmespath.search('Upserts[*].CoursePlanKey', response.json())) != 0)
        self.check_content_with_last_stamp_and_key(response, self.small_star_service.synchronize_course_node, "Key")

    @Test()
    def synchronize_activity(self):
        response = self.small_star_service.synchronize_activity(self.current_book_key, self.course_plan_key,
                                                                amount=AMOUNT)
        assert_that(len(jmespath.search('Upserts', response.json())) != 0)
        assert_that(len(jmespath.search('Upserts[*].Title', response.json())) != 0)
        assert_that(len(jmespath.search('Upserts[*].Stimulus', response.json())) != 0)
        assert_that(len(jmespath.search('Upserts[*].Questions', response.json())) != 0)
        self.check_content_with_last_stamp_and_key(response, self.small_star_service.synchronize_activity,
                                                   "Stimulus[0].Key")

    @Test()
    def synchronize_digital_article(self):
        response = self.small_star_service.synchronize_digital_article(self.current_book_key, self.course_plan_key,
                                                                       upserts_only=False,
                                                                       amount=AMOUNT)
        assert_that(len(jmespath.search('Upserts', response.json())) != 0)
        assert_that(len(jmespath.search('Upserts[*].BinaryMeta', response.json())) != 0)
        assert_that(len(jmespath.search('Upserts[*].Body.resources', response.json())) != 0)
        self.check_content_with_last_stamp_and_key(response, self.small_star_service.synchronize_digital_article,
                                                   'BinaryMeta', )

    @Test()
    def batch_resource(self):
        binary_response = self.small_star_service.synchronize_binary_data(self.current_book_key, self.course_plan_key,
                                                                          amount=AMOUNT)
        resource_ids = jmespath.search('Upserts[*].ResourceId', binary_response.json())
        assert_that(len(resource_ids) != 0)
        batch_resource_response = self.small_star_service.batch_resource(resource_ids[0])
        assert_that(batch_resource_response.json(), exist("[0].StorageUri"))
        assert_that(batch_resource_response.json(), exist("[0].CredentialUri"))
        assert_that("e1-osp" in jmespath.search("[0].Container", batch_resource_response.json()))
        assert_that(batch_resource_response.json(), exist("[0].Identifier"))

    @Test()
    def batch_resources(self):
        binary_response = self.small_star_service.synchronize_binary_data(self.current_book_key, self.course_plan_key,
                                                                          amount=AMOUNT)
        resource_ids = jmespath.search('Upserts[*].ResourceId', binary_response.json())
        assert_that(len(resource_ids) != 0)
        batch_response = self.small_star_service.batch_resources(resource_ids[:5])
        assert_that("e1-osp" in jmespath.search("[0].Container", batch_response.json()))
        assert_that(len(jmespath.search('[*]', batch_response.json())) == 5)

    @Test()
    def synchronize_all_historical_activity_answer(self):
        response = self.small_star_service.synchronize_small_star_student_activity_answer(self.current_book_key,
                                                                                          self.course_plan_key,
                                                                                          amount=AMOUNT)
        assert_that(len(jmespath.search('Upserts', response.json())) != 0)
        assert_that(len(jmespath.search('Upserts[*].ActivityCourseKey', response.json())) != 0)
        assert_that(len(jmespath.search('Upserts[*].ActivityKey', response.json())) != 0)
        assert_that(len(jmespath.search('Upserts[*].QuestionKey', response.json())) != 0)
        assert_that(len(jmespath.search('Upserts[*].SubmitIdentifier', response.json())) != 0)
        assert_that(len(jmespath.search('Upserts[*].Key', response.json())) != 0)
        self.check_content_with_last_stamp_and_key(response,
                                                   self.small_star_service.synchronize_small_star_student_activity_answer,
                                                   'Key')

    @Test()
    def course_unlock(self):
        response = self.small_star_service.get_small_star_unlock_course_keys(self.current_book_key)
        assert_that(len(jmespath.search('[*]', response.json())) != 0)

    @Test()
    def activity_answer(self):
        un_lock_lesson_keys = self.small_star_service.get_small_star_unlock_course_keys(self.current_book_key).json()
        response, submit_activity_key = self.small_star_service.submit_small_star_student_answers(self.product_code,
                                                                                                  self.group_id,
                                                                                                  self.current_book_key,
                                                                                                  un_lock_lesson_keys[
                                                                                                      0],
                                                                                                  self.course_plan_key,
                                                                                                  self.user_id, True)
        assert_that(response.json(), exist("SubmitIdentifier"))
        assert_that(response.json(), exist("AnswerKeys"))
        self.reset_activity_anwser(un_lock_lesson_keys[0])

    def reset_activity_anwser(self, lesson_key):
        response, submit_activity_key = self.small_star_service.submit_small_star_student_answers(self.product_code,
                                                                                                  self.group_id,
                                                                                                  self.current_book_key,
                                                                                                  lesson_key,
                                                                                                  self.course_plan_key,
                                                                                                  self.user_id, False)

    def check_content_with_last_stamp_and_key(self, response, synchronize_function, item_to_be_checked):
        last_key, last_stamp = self.get_last_stamp_and_key(response)
        second_response = synchronize_function(self.current_book_key, self.course_plan_key,
                                               amount=AMOUNT,
                                               last_synchronized_key=last_key,
                                               last_Synchronized_Stamp=last_stamp)
        assert_that(len(jmespath.search('Upserts[*].%s' % item_to_be_checked, second_response.json())) != 0)

    def get_last_stamp_and_key(self, response):
        last_stamp = jmespath.search('LastStamp', response.json())
        last_key = jmespath.search('LastKey', response.json())
        return last_key, last_stamp

    @Test()
    def synchronize_activity_answer(self):
        un_lock_lesson_keys = self.small_star_service.get_small_star_unlock_course_keys(self.current_book_key).json()
        response, submit_activity_key = self.small_star_service.submit_small_star_student_answers(self.product_code,
                                                                                                  self.group_id,
                                                                                                  self.current_book_key,
                                                                                                  un_lock_lesson_keys[
                                                                                                      0],
                                                                                                  self.course_plan_key,
                                                                                                  self.user_id, True)

        historical_activity_answer = self.small_star_service.synchronize_small_star_student_activity_answer(
            self.current_book_key,
            self.course_plan_key,
            amount=2147483617)

        activity_keys = jmespath.search('Upserts[*].ActivityKey', historical_activity_answer.json())

        assert_that(submit_activity_key[0] in activity_keys)

        result = jmespath.search("Upserts[?ActivityKey=='{}']".format(submit_activity_key[0]),
                                 historical_activity_answer.json())[-1]

        assert_that(result['TotalScore'] == result['Score'])
