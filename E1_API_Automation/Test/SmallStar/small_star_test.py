import jmespath
from hamcrest import assert_that
from ptest.decorator import TestClass, Test

from E1_API_Automation.Lib.HamcrestExister import exist
from E1_API_Automation.Test.SmallStar.SmallStarBase import SmallStarBase

AMOUNT =  2147483617


@TestClass()
class SmallStarTestCases(SmallStarBase):

    @Test()
    def get_content(self):
        body = {
            "Activity":{
                "UpertsOnly":True,
            },
            "BinaryData":{
                "UpertsOnly":True,
            },
            "BookKey":self.current_book_key,
            "CourseNode":{
                "UpertsOnly":False,
            },
            "DigitalArticle":{
                "UpertsOnly":False,
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
        response = self.small_star_service.synchronize_binary_data(self.current_book_key, self.course_plan_key, self.product_code,
                                                                   amount=AMOUNT)
        assert_that(len(jmespath.search('Upserts', response.json())) != 0)
        assert_that(response.json(), exist('Upserts'))
        assert_that(len(jmespath.search('Upserts[*].ResourceId', response.json())) != 0)
        assert_that(len(jmespath.search('Upserts[*].Container', response.json())) != 0)
        assert_that(jmespath.search("Upserts[*].Container", response.json())[0] == 'e1-osp-staging' )

    @Test()
    def synchronize_course_node(self):
        response = self.small_star_service.synchronize_course_node(self.current_book_key, self.course_plan_key, self.product_code, upserts_only=False, amount=AMOUNT)
        assert_that(len(jmespath.search('Upserts', response.json())) != 0)
        assert_that(response.json(), exist('Upserts'))
        assert_that(len(jmespath.search('Upserts[*].TopNodeKey', response.json())) != 0)
        assert_that(len(jmespath.search('Upserts[*].ParentNodeKey', response.json())) != 0)
        assert_that(len(jmespath.search('Upserts[*].CoursePlanKey', response.json())) != 0)

    @Test()
    def synchronize_activitiy(self):
        response = self.small_star_service.synchronize_activity(self.current_book_key, self.course_plan_key, self.product_code, amount=AMOUNT)
        assert_that(len(jmespath.search('Upserts', response.json())) != 0)
        assert_that(len(jmespath.search('Upserts[*].Title', response.json())) != 0)
        assert_that(len(jmespath.search('Upserts[*].Stimulus', response.json())) != 0)
        assert_that(len(jmespath.search('Upserts[*].Questions', response.json())) != 0)

    @Test()
    def synchronize_digital_article(self):
        response = self.small_star_service.synchronize_digital_article(self.current_book_key, self.course_plan_key, self.product_code, upserts_only=False, amount=AMOUNT)
        assert_that(len(jmespath.search('Upserts', response.json())) != 0)
        assert_that(len(jmespath.search('Upserts[*].BinaryMeta', response.json())) != 0)
        assert_that(len(jmespath.search('Upserts[*].Body.resources', response.json())) != 0)


    @Test()
    def batch_resource(self):
        binary_response = self.small_star_service.synchronize_binary_data(self.current_book_key, self.course_plan_key, self.product_code, amount=AMOUNT)
        resource_ids = jmespath.search('Upserts[*].ResourceId', binary_response.json())
        assert_that(len(resource_ids) != 0)
        batch_resource_response = self.small_star_service.batch_resource(resource_ids[0])
        assert_that(batch_resource_response.json(), exist("[0].StorageUri"))
        assert_that(batch_resource_response.json(), exist("[0].CredentialUri"))
        assert_that( "e1-osp" in jmespath.search("[0].Container", batch_resource_response.json()))
        assert_that(batch_resource_response.json(), exist("[0].Identifier"))
    @Test()
    def batch_resources(self):
        binary_response = self.small_star_service.synchronize_binary_data(self.current_book_key, self.course_plan_key, self.product_code, amount=AMOUNT)
        resource_ids = jmespath.search('Upserts[*].ResourceId', binary_response.json())
        assert_that(len(resource_ids) != 0)
        batch_response = self.small_star_service.batch_resources(resource_ids[:5])
        assert_that( "e1-osp" in jmespath.search("[0].Container", batch_response .json()))
        assert_that(len(jmespath.search('[*]', batch_response.json())) == 5)

    @Test()
    def syncronize_all_historical_activity_answer(self):
        response = self.small_star_service.synchronize_small_star_student_activity_answer(self.current_book_key, self.course_plan_key, self.product_code, amount=AMOUNT)
        assert_that(len(jmespath.search('Upserts', response.json())) != 0)
        assert_that(len(jmespath.search('Upserts[*].ActivityCourseKey', response.json())) != 0)
        assert_that(len(jmespath.search('Upserts[*].ActivityKey', response.json())) != 0)
        assert_that(len(jmespath.search('Upserts[*].QuestionKey', response.json())) != 0)
        assert_that(len(jmespath.search('Upserts[*].SubmitIdentifier', response.json())) != 0)
        assert_that(len(jmespath.search('Upserts[*].Key', response.json())) != 0)

    @Test()
    def course_unlock(self):
        response = self.small_star_service.get_small_star_unlock_course_keys(self.current_book_key)
        assert_that(len(jmespath.search('[*]', response.json())) != 0)


    @Test()
    def activity_answer(self):
        body = {
  "GroupId" : "687498",
  "ActivityCourseKey" : "7aa1a5fa-83b1-44c4-b2df-b710a5113a7f",
  "StudentId" : "43240092",
  "ActivityKey" : "2e4a418e-68a7-4681-b725-1441d77390cd",
  "Answers" : [
    {
      "Detail" : {
        "correctAnswers" : [
          {
            "test" : "0",
            "option" : "0"
          }
        ],
        "studentAnswers" : {
          "optionSelectionFull" : [
            {
              "test" : "0",
              "option" : "0"
            }
          ],
          "optionSelection" : [
            {
              "test" : "0",
              "option" : "0"
            }
          ]
        }
      },
      "TotalStar" : 1,
      "Duration" : 1.1333333333333333,
      "QuestionKey" : "3c3ced73-d97a-4407-94e5-eaf63b6aae30",
      "Score" : 1,
      "LocalStartStamp" : "2018-09-12T06:46:22.398Z",
      "LocalEndStamp" : "2018-09-12T06:46:23.774Z",
      "TotalScore" : 1,
      "Star" : 1
    },
    {
      "Detail" : {
        "correctAnswers" : [
          {
            "test" : "0",
            "option" : "0"
          }
        ],
        "studentAnswers" : {
          "optionSelectionFull" : [
            {
              "test" : "0",
              "option" : "0"
            }
          ],
          "optionSelection" : [
            {
              "test" : "0",
              "option" : "0"
            }
          ]
        }
      },
      "TotalStar" : 1,
      "Duration" : 4.4333333333333336,
      "QuestionKey" : "39147a2e-255a-442c-91de-03a20e4e5fe5",
      "Score" : 1,
      "LocalStartStamp" : "2018-09-12T06:46:24.680Z",
      "LocalEndStamp" : "2018-09-12T06:46:29.141Z",
      "TotalScore" : 1,
      "Star" : 1
    },
    {
      "Detail" : {
        "correctAnswers" : [
          {
            "test" : "0",
            "option" : "0"
          }
        ],
        "studentAnswers" : {
          "optionSelectionFull" : [
            {
              "test" : "0",
              "option" : "0"
            }
          ],
          "optionSelection" : [
            {
              "test" : "0",
              "option" : "0"
            }
          ]
        }
      },
      "TotalStar" : 1,
      "Duration" : 4.5,
      "QuestionKey" : "565737c4-0564-414f-92e0-56d9553a2fc9",
      "Score" : 1,
      "LocalStartStamp" : "2018-09-12T06:46:30.099Z",
      "LocalEndStamp" : "2018-09-12T06:46:34.645Z",
      "TotalScore" : 1,
      "Star" : 1
    }
  ]
}
        response = self.small_star_service.submit_small_star_student_answers(body)
        assert_that(response.json(), exist("SubmitIdentifier"))
        assert_that(response.json(), exist("AnswerKeys"))


