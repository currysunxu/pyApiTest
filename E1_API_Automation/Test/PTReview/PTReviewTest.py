from ptest.decorator import TestClass, Test
from E1_API_Automation.Business.PTReviewService import PTReviewService
from E1_API_Automation.Business.Utils.PTReviewUtils import PTReviewUtils
from E1_API_Automation.Business.TPIService import TPIService
from ...Settings import OSP_ENVIRONMENT, TPI_ENVIRONMENT, env_key
from ...Test_Data.PTReviewData import PTReviewData
from E1_API_Automation.Business.Utils.EnvUtils import EnvUtils
from E1_API_Automation.Business.PTSkillScore import SkillCode, SubSkillCode
from hamcrest import assert_that
import jmespath
import json


@TestClass()
class PTReviewTestCases:

    @Test(tags="qa, stg, live")
    def test_get_hf_all_books(self):
        pt_review_service = PTReviewService(OSP_ENVIRONMENT)
        response = pt_review_service.get_hf_all_books_url()
        api_response_json = response.json()
        code_list = jmespath.search('[].Code', api_response_json)

        expected_code_list = ['HFC', 'HFD', 'HFE', 'HFF', 'HFG', 'HFH', 'HFI', 'HFJ']
        assert_that(code_list == expected_code_list, "Code returned is not as expected.")

        # if it's not Live environment, then do the rest verification with DB
        if not EnvUtils.is_env_live():
            # get the result from DB
            db_query_result = pt_review_service.get_hf_all_books_from_db()

            # the list length should be equal for the response list and DB list
            assert_that(len(api_response_json) == len(db_query_result))

            # check if all the data return from API is consistent with DB
            error_message = PTReviewUtils.verify_hf_allbooks_api_db_result(api_response_json, db_query_result)
            assert_that(error_message == '', error_message)

    '''
    test the OmniProgressTestAssessment API, verify if the score have been saved correctly
    '''
    @Test(tags="qa, stg")
    def test_save_total_score_with_omni_api(self):
        student_id = list(PTReviewData.pt_hf_user_key_book_unit[env_key].keys())[0]
        pt_key = PTReviewData.pt_hf_user_key_book_unit[env_key][student_id]['TestPrimaryKey']
        book_key = PTReviewData.pt_hf_user_key_book_unit[env_key][student_id]['BookKey']
        unit_key = PTReviewData.pt_hf_user_key_book_unit[env_key][student_id]['UnitKey']

        # construct data to call the API
        skill_dic = PTReviewUtils.generate_pt_whole_skill_subskill_randomscore_list()
        student_skill = {}
        student_skill[student_id] = skill_dic

        omni_body = PTReviewUtils.generate_assessment_body_for_omni(pt_key, student_skill)

        omni_body_json = json.dumps(omni_body)
        print(omni_body_json)

        # call OmniProgressTestAssessment API to update overwritten score and total score
        tpi_service = TPIService(TPI_ENVIRONMENT)
        tpi_response = tpi_service.put_hf_student_omni_pt_assessment(omni_body)
        assert_that(tpi_response.status_code == 204)

        pt_review_service = PTReviewService(OSP_ENVIRONMENT)
        # call StudentPaperDigitalProgressTestAssessmentMetas API to get all the records from DB
        assess_metas = pt_review_service.post_hf_student_pt_assess_metas(student_id, book_key)
        assert_that(assess_metas.status_code == 200)
        assess_metas_response = assess_metas.json()

        # verify if the data get from the StudentPaperDigitalProgressTestAssessmentMetas API are as what you constructed
        PTReviewUtils.verify_pt_score_with_api_response(skill_dic, assess_metas_response, unit_key)

    '''
    the case to test the StudentProgressTestAssessmentMetasGroupBySkill API, 
    for QA and staging: if the skill & sub skill's overwritten score is not null, it will get the value of 
    overwritten score as score in the API
    for Live: get the info directly with StudentPaperDigitalProgressTestAssessmentMetas API, then do the rest check
    '''
    @Test(tags="qa, stg, live")
    def test_pt_assessment_by_skill_api(self):
        student_id = list(PTReviewData.pt_hf_user_key_book_unit[env_key].keys())[0]
        test_primary_key = PTReviewData.pt_hf_user_key_book_unit[env_key][student_id]['TestPrimaryKey']
        book_key = PTReviewData.pt_hf_user_key_book_unit[env_key][student_id]['BookKey']
        unit_key = PTReviewData.pt_hf_user_key_book_unit[env_key][student_id]['UnitKey']

        pt_review_service = PTReviewService(OSP_ENVIRONMENT)
        if not EnvUtils.is_env_live():
            # make sure all the score have value at first
            PTReviewUtils.update_random_score_with_omni_pt_assess_api(student_id, test_primary_key)
            hf_pt_assess = pt_review_service.get_hf_pt_assessment_from_db(student_id, book_key, unit_key)
            from_db = True
        else:
            assess_metas = pt_review_service.post_hf_student_pt_assess_metas(student_id, book_key)
            hf_pt_assess = jmespath.search("@[?UnitKey == '{0}']".format(unit_key.lower()), assess_metas.json())
            from_db = False
        expected_pt_assess_by_skill = PTReviewUtils.get_expected_pt_assessment_by_skill(hf_pt_assess, from_db)
        api_pt_assess_by_skill = pt_review_service.post_hf_student_pt_assess_by_skill(student_id, book_key, unit_key)
        if expected_pt_assess_by_skill is None:
            assert_that(api_pt_assess_by_skill.status_code == 409)
        else:
            assert_that(api_pt_assess_by_skill.status_code == 200)
            api_pt_assess_by_skill_json = api_pt_assess_by_skill.json()
            print(api_pt_assess_by_skill_json)
            error_message = PTReviewUtils.verify_hf_pt_assessment_by_skill(api_pt_assess_by_skill_json,
                                                                           expected_pt_assess_by_skill)
            assert_that(error_message == '', error_message)

    '''
    the case to test the StudentProgressTestAssessmentMetasGroupBySkill API, 
    if the skill & sub skill's overwritten score is null, it will get the value of original score as score in the API 
    '''
    @Test(tags="qa, stg")
    def test_pt_assessment_by_skill_api_for_originalscore(self):
        student_id = list(PTReviewData.pt_hf_user_key_book_unit[env_key].keys())[0]
        test_primary_key = PTReviewData.pt_hf_user_key_book_unit[env_key][student_id]['TestPrimaryKey']
        book_key = PTReviewData.pt_hf_user_key_book_unit[env_key][student_id]['BookKey']
        unit_key = PTReviewData.pt_hf_user_key_book_unit[env_key][student_id]['UnitKey']

        pt_review_service = PTReviewService(OSP_ENVIRONMENT)

        # make sure all the score have value at first
        PTReviewUtils.update_random_score_with_omni_pt_assess_api(student_id, test_primary_key)
        # update user's original score as overwritten score, and over written score as null to test if the API will get
        # original score when overwritten score as null
        pt_review_service.update_pt_assessment_original_with_value(student_id, test_primary_key)
        # get value from DB
        hf_pt_assess = pt_review_service.get_hf_pt_assessment_from_db(student_id, book_key, unit_key)
        # get the expected skill score list
        expected_pt_assess_by_skill = PTReviewUtils.get_expected_pt_assessment_by_skill(hf_pt_assess, True)
        # call the by skill API
        api_pt_assess_by_skill = pt_review_service.post_hf_student_pt_assess_by_skill(student_id, book_key, unit_key)
        assert_that(api_pt_assess_by_skill.status_code == 200)
        api_pt_assess_by_skill_json = api_pt_assess_by_skill.json()
        # verify the API return result with expected value
        error_message = PTReviewUtils.verify_hf_pt_assessment_by_skill(api_pt_assess_by_skill_json,
                                                                       expected_pt_assess_by_skill)
        assert_that(error_message == '', error_message)
        # revert the orignal score column value
        pt_review_service.update_pt_assessment_original_with_null(student_id, test_primary_key)

    '''
    test the unit API, to check if the return result is as expected
    '''
    @Test(tags="qa, stg, live")
    def test_pt_assessment_by_unit_api(self):
        student_id = list(PTReviewData.pt_hf_user_key_book_unit[env_key].keys())[0]
        test_primary_key = PTReviewData.pt_hf_user_key_book_unit[env_key][student_id]['TestPrimaryKey']
        book_key = PTReviewData.pt_hf_user_key_book_unit[env_key][student_id]['BookKey']

        pt_review_service = PTReviewService(OSP_ENVIRONMENT)
        if not EnvUtils.is_env_live():
            # make sure all the score have value at first
            PTReviewUtils.update_random_score_with_omni_pt_assess_api(student_id, test_primary_key)
            hf_pt_assess = pt_review_service.get_hf_pt_assessment_by_book_from_db(student_id, book_key)
            from_db = True
        else:
            assess_metas = pt_review_service.post_hf_student_pt_assess_metas(student_id, book_key)
            hf_pt_assess = assess_metas.json()
            from_db = False
        # get the expected pt assessment list
        expected_pt_assess_by_unit = PTReviewUtils.get_expected_pt_assessment_by_unit(hf_pt_assess, from_db)
        # call the unit API
        api_pt_assess_by_unit = pt_review_service.post_hf_student_pt_assess_by_unit(student_id, book_key)
        assert_that(api_pt_assess_by_unit.status_code == 200)
        api_pt_assess_by_unit_json = api_pt_assess_by_unit.json()
        # do the verification
        error_message = PTReviewUtils.verify_hf_pt_assessment_by_unit(api_pt_assess_by_unit_json,
                                                                      expected_pt_assess_by_unit)
        assert_that(error_message == '', error_message)

    '''
    update skill/subskill original score or total score to check if skill level API will return with 409, 
    and the PTTotalScore is null for Unit API 
    '''
    @staticmethod
    def update_score_as_null_then_verify(pt_review_service, student_id, test_primary_key, book_key,
                                         unit_key, skill_subskill_code, is_total_score):
        # update the pt score as null
        PTReviewUtils.update_score_as_null(pt_review_service, student_id, test_primary_key, skill_subskill_code,
                                           is_total_score)

        # call the skill API, and do the verification, the API will return with 409 for not valid data
        api_pt_assess_by_skill = pt_review_service.post_hf_student_pt_assess_by_skill(student_id, book_key,
                                                                                      unit_key)
        assert_that(api_pt_assess_by_skill.status_code == 409)

        # call the unit API, and do the verification, the pttotalscore should be null for this unit
        hf_pt_assess = pt_review_service.get_hf_pt_assessment_by_book_from_db(student_id, book_key)
        # the expected unit pt assessment will have PTTotalScore as null as the data in DB is not valid for the logic
        expected_pt_assess_by_unit = PTReviewUtils.get_expected_pt_assessment_by_unit(hf_pt_assess, True)
        # call the unit API
        api_pt_assess_by_unit = pt_review_service.post_hf_student_pt_assess_by_unit(student_id, book_key)
        assert_that(api_pt_assess_by_unit.status_code == 200)
        api_pt_assess_by_unit_json = api_pt_assess_by_unit.json()
        error_message = PTReviewUtils.verify_hf_pt_assessment_by_unit(api_pt_assess_by_unit_json,
                                                                      expected_pt_assess_by_unit)
        assert_that(error_message == '', error_message)

    '''
    test the skill and unit API when skill/subskill original score and overwritten score are both null
    '''
    @Test(tags="qa, stg")
    def test_pt_assessment_by_skill_unit_for_null_score(self):
        student_id = list(PTReviewData.pt_hf_user_key_book_unit[env_key].keys())[0]
        test_primary_key = PTReviewData.pt_hf_user_key_book_unit[env_key][student_id]['TestPrimaryKey']
        book_key = PTReviewData.pt_hf_user_key_book_unit[env_key][student_id]['BookKey']
        unit_key = PTReviewData.pt_hf_user_key_book_unit[env_key][student_id]['UnitKey']
        pt_review_service = PTReviewService(OSP_ENVIRONMENT)

        for skill in SkillCode.__members__:
            if skill in (SkillCode.Speaking.value, SkillCode.Writing.value):
                for sub_skill in SubSkillCode.__members__:
                    sub_skill_code = skill + "-" + sub_skill
                    # update original score and overwritten score as null for each sub skill to check
                    # if the skill API return with 409, and also check the Unit API
                    self.update_score_as_null_then_verify(pt_review_service, student_id, test_primary_key,
                                                          book_key, unit_key, sub_skill_code, False)
            else:
                # update original score and overwritten score as null for each skill to check if skill and unit API
                self.update_score_as_null_then_verify(pt_review_service, student_id, test_primary_key, book_key,
                                                      unit_key, skill, False)

        # make all the data valid after test
        PTReviewUtils.update_random_score_with_omni_pt_assess_api(student_id, test_primary_key)

    '''
    test the skill and unit API when skill/subskill total score is null
    '''
    @Test(tags="qa, stg")
    def test_pt_assessment_by_skill_unit_for_null_totalscore(self):
        student_id = list(PTReviewData.pt_hf_user_key_book_unit[env_key].keys())[0]
        test_primary_key = PTReviewData.pt_hf_user_key_book_unit[env_key][student_id]['TestPrimaryKey']
        book_key = PTReviewData.pt_hf_user_key_book_unit[env_key][student_id]['BookKey']
        unit_key = PTReviewData.pt_hf_user_key_book_unit[env_key][student_id]['UnitKey']
        pt_review_service = PTReviewService(OSP_ENVIRONMENT)

        for skill in SkillCode.__members__:
            if skill in (SkillCode.Speaking.value, SkillCode.Writing.value):
                for sub_skill in SubSkillCode.__members__:
                    sub_skill_code = skill + "-" + sub_skill
                    # update total score as null for each sub skill to check if the skill API return with 409,
                    # and also check the Unit API
                    self.update_score_as_null_then_verify(pt_review_service, student_id, test_primary_key,
                                                          book_key, unit_key, sub_skill_code, True)
            else:
                # update original score and overwritten score as null for each skill to check if skill and unit API
                self.update_score_as_null_then_verify(pt_review_service, student_id, test_primary_key, book_key,
                                                      unit_key, skill, True)

        # make all the data valid after test
        PTReviewUtils.update_random_score_with_omni_pt_assess_api(student_id, test_primary_key)


