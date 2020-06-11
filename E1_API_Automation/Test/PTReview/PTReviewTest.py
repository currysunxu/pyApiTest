from ptest.decorator import TestClass, Test
from E1_API_Automation.Business.PTReviewService import PTReviewService
from E1_API_Automation.Business.OSPService import OSPService
from E1_API_Automation.Business.PTReviewBFFService import PTReviewBFFService
from E1_API_Automation.Business.Utils.PTReviewUtils import PTReviewUtils
from E1_API_Automation.Business.TPIService import TPIService
from E1_API_Automation.Business.OMNIService import OMNIService
from ...Settings import OSP_ENVIRONMENT, TPI_ENVIRONMENT, OMNI_ENVIRONMENT, ENVIRONMENT, env_key
from ...Test_Data.PTReviewData import PTReviewData, PTDATA
from E1_API_Automation.Business.Utils.EnvUtils import EnvUtils
from E1_API_Automation.Business.PTSkillScore import SkillCode, SubSkillCode
from hamcrest import assert_that, equal_to
import jmespath
import json


@TestClass()
class PTReviewTestCases:

    @Test(tags="qa, stg, live")
    def test_get_all_books_by_course(self):
        osp_service = OSPService(OSP_ENVIRONMENT)
        # verify all the three courses
        course_code_list = ['highflyers', 'frontrunner', 'trailblazers']
        for course_code in course_code_list:
            print("Verify course:" + course_code)
            response = osp_service.get_all_books_by_course(course_code)
            assert_that(response.status_code == 200)
            api_response_json = response.json()
            code_list = jmespath.search('[].Code', api_response_json)

            if course_code == 'highflyers':
                expected_code_list = ['HFC', 'HFD', 'HFE', 'HFF', 'HFG', 'HFH', 'HFI', 'HFJ']
                assert_that(code_list == expected_code_list, "HF code returned is not as expected.")
            elif course_code == 'frontrunner':
                assert_that(len(api_response_json) == 16, "frontrunner return list length should be 16")
            elif course_code == 'trailblazers':
                # the value will be used in DB query
                course_code = 'TB'
                expected_code_list = ['TBv3Bk1', 'TBv3Bk2', 'TBv3Bk3', 'TBv3Bk4', 'TBv3Bk5', 'TBv3Bk6', 'TBv3Bk7',
                                      'TBv3Bk8']
                assert_that(code_list == expected_code_list, "TB code returned is not as expected.")

            # if it's not Live environment, then do the rest verification with DB
            if not EnvUtils.is_env_live():
                # get the result from DB
                db_query_result = PTReviewService.get_all_books_by_course_from_db(course_code)

                # the list length should be equal for the response list and DB list
                assert_that(len(api_response_json) == len(db_query_result))

                # check if all the data return from API is consistent with DB
                error_message = PTReviewUtils.verify_allbooks_by_course_api_db_result(api_response_json,
                                                                                      db_query_result)
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

        osp_service = OSPService(OSP_ENVIRONMENT)
        # call StudentPaperDigitalProgressTestAssessmentMetas API to get all the records from DB
        assess_metas = osp_service.post_hf_student_pt_assess_metas(student_id, book_key)
        assert_that(assess_metas.status_code == 200)
        assess_metas_response = assess_metas.json()

        # verify if the data get from the StudentPaperDigitalProgressTestAssessmentMetas API are as what you constructed
        PTReviewUtils.verify_pt_score_with_api_response(skill_dic, assess_metas_response, unit_key)

    # test the omni API for multiple user
    @Test(tags="qa")
    def test_save_total_score_with_omni_api_multiple_user(self):
        student_skill = {}
        for student_id in PTReviewData.pt_hf_user_key_book_unit[env_key].keys():
            # the pt_key, book_key, unit_key will be same for omni api to support multiple user
            pt_key = PTReviewData.pt_hf_user_key_book_unit[env_key][student_id]['TestPrimaryKey']
            # construct data to call the API
            skill_dic = PTReviewUtils.generate_pt_whole_skill_subskill_randomscore_list()
            student_skill[student_id] = skill_dic

        omni_body = PTReviewUtils.generate_assessment_body_for_omni(pt_key, student_skill)

        omni_body_json = json.dumps(omni_body)
        print(omni_body_json)

        # call OmniProgressTestAssessment API to update overwritten score and total score
        tpi_service = TPIService(TPI_ENVIRONMENT)
        tpi_response = tpi_service.put_hf_student_omni_pt_assessment(omni_body)
        assert_that(tpi_response.status_code == 204)

        osp_service = OSPService(OSP_ENVIRONMENT)
        for student_id in PTReviewData.pt_hf_user_key_book_unit[env_key].keys():
            book_key = PTReviewData.pt_hf_user_key_book_unit[env_key][student_id]['BookKey']
            unit_key = PTReviewData.pt_hf_user_key_book_unit[env_key][student_id]['UnitKey']
            # call StudentPaperDigitalProgressTestAssessmentMetas API to get all the records from DB
            assess_metas = osp_service.post_hf_student_pt_assess_metas(student_id, book_key)
            assert_that(assess_metas.status_code == 200)
            assess_metas_response = assess_metas.json()
            # verify if the data get from the StudentPaperDigitalProgressTestAssessmentMetas API are as what you constructed
            PTReviewUtils.verify_pt_score_with_api_response(student_skill[student_id], assess_metas_response, unit_key)

    '''
    the case to test the StudentProgressTestAssessmentMetasGroupBySkill API, 
    for QA and staging: if the skill & sub skill's overwritten score is not null, it will get the value of 
    overwritten score as score in the API
    for Live: get the info directly with StudentPaperDigitalProgressTestAssessmentMetas API, then do the rest check
    '''

    @Test(tags="qa, stg, live")
    def test_pt_assessment_by_skill_api(self):
        student_id  = list(PTReviewData.pt_hf_user_key_book_unit[env_key].keys())[0]
        test_primary_key = PTReviewData.pt_hf_user_key_book_unit[env_key][student_id]['TestPrimaryKey']
        book_key = PTReviewData.pt_hf_user_key_book_unit[env_key][student_id]['BookKey']
        unit_key = PTReviewData.pt_hf_user_key_book_unit[env_key][student_id]['UnitKey']

        osp_service = OSPService(OSP_ENVIRONMENT)
        if not EnvUtils.is_env_live():
            # make sure all the score have value at first
            PTReviewUtils.update_random_score_with_omni_pt_assess_api(student_id, test_primary_key)
            hf_pt_assess = PTReviewService.get_hf_pt_assessment_from_db(student_id, book_key, unit_key)
            from_db = True
        else:
            assess_metas = osp_service.post_hf_student_pt_assess_metas(student_id, book_key)
            hf_pt_assess = jmespath.search("@[?UnitKey == '{0}']".format(unit_key.lower()), assess_metas.json())
            from_db = False
        expected_pt_assess_by_skill = PTReviewUtils.get_expected_pt_assessment_by_skill(hf_pt_assess, from_db)
        api_pt_assess_by_skill = osp_service.post_hf_student_pt_assess_by_skill(student_id, book_key, unit_key)
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

        osp_service = OSPService(OSP_ENVIRONMENT)

        # make sure all the score have value at first
        PTReviewUtils.update_random_score_with_omni_pt_assess_api(student_id, test_primary_key)
        # update user's original score as overwritten score, and over written score as null to test if the API will get
        # original score when overwritten score as null
        PTReviewService.update_pt_assessment_original_with_value(student_id, test_primary_key)
        # get value from DB
        hf_pt_assess = PTReviewService.get_hf_pt_assessment_from_db(student_id, book_key, unit_key)
        # get the expected skill score list
        expected_pt_assess_by_skill = PTReviewUtils.get_expected_pt_assessment_by_skill(hf_pt_assess, True)
        # call the by skill API
        api_pt_assess_by_skill = osp_service.post_hf_student_pt_assess_by_skill(student_id, book_key, unit_key)
        assert_that(api_pt_assess_by_skill.status_code == 200)
        api_pt_assess_by_skill_json = api_pt_assess_by_skill.json()
        # verify the API return result with expected value
        error_message = PTReviewUtils.verify_hf_pt_assessment_by_skill(api_pt_assess_by_skill_json,
                                                                       expected_pt_assess_by_skill)
        assert_that(error_message == '', error_message)
        # revert the orignal score column value
        PTReviewService.update_pt_assessment_original_with_null(student_id, test_primary_key)

    '''
    test the unit API, to check if the return result is as expected
    '''

    @Test(tags="qa, stg, live")
    def test_pt_assessment_by_unit_api(self):
        student_id = list(PTReviewData.pt_hf_user_key_book_unit[env_key].keys())[0]
        test_primary_key = PTReviewData.pt_hf_user_key_book_unit[env_key][student_id]['TestPrimaryKey']
        book_key = PTReviewData.pt_hf_user_key_book_unit[env_key][student_id]['BookKey']

        osp_service = OSPService(OSP_ENVIRONMENT)

        if not EnvUtils.is_env_live():
            # make sure all the score have value at first
            PTReviewUtils.update_random_score_with_omni_pt_assess_api(student_id, test_primary_key)
            hf_pt_assess = PTReviewService.get_hf_pt_assessment_by_book_from_db(student_id, book_key)
            from_db = True
        else:
            assess_metas = osp_service.post_hf_student_pt_assess_metas(student_id, book_key)
            hf_pt_assess = assess_metas.json()
            from_db = False
        # get the expected pt assessment list
        expected_pt_assess_by_unit = PTReviewUtils.get_expected_pt_assessment_by_unit(hf_pt_assess, from_db)
        # call the unit API
        api_pt_assess_by_unit = osp_service.post_hf_student_pt_assess_by_unit(student_id, book_key)
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
    def update_score_as_null_then_verify(osp_service, student_id, test_primary_key, book_key,
                                         unit_key, skill_subskill_code, is_total_score):
        # update the pt score as null
        PTReviewUtils.update_score_as_null(student_id, test_primary_key, skill_subskill_code,
                                           is_total_score)

        # call the skill API, and do the verification, the API will return with 409 for not valid data
        api_pt_assess_by_skill = osp_service.post_hf_student_pt_assess_by_skill(student_id, book_key,
                                                                                unit_key)
        assert_that(api_pt_assess_by_skill.status_code == 409)

        # call the unit API, and do the verification, the pttotalscore should be null for this unit
        hf_pt_assess = PTReviewService.get_hf_pt_assessment_by_book_from_db(student_id, book_key)
        # the expected unit pt assessment will have PTTotalScore as null as the data in DB is not valid for the logic
        expected_pt_assess_by_unit = PTReviewUtils.get_expected_pt_assessment_by_unit(hf_pt_assess, True)
        # call the unit API
        api_pt_assess_by_unit = osp_service.post_hf_student_pt_assess_by_unit(student_id, book_key)
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

        osp_service = OSPService(OSP_ENVIRONMENT)

        for skill in SkillCode.__members__:
            if skill in (SkillCode.Speaking.value, SkillCode.Writing.value):
                for sub_skill in SubSkillCode.__members__:
                    sub_skill_code = skill + "-" + sub_skill
                    # update original score and overwritten score as null for each sub skill to check
                    # if the skill API return with 409, and also check the Unit API
                    self.update_score_as_null_then_verify(osp_service, student_id, test_primary_key,
                                                          book_key, unit_key, sub_skill_code, False)
            else:
                # update original score and overwritten score as null for each skill to check if skill and unit API
                self.update_score_as_null_then_verify(osp_service, student_id, test_primary_key, book_key,
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

        osp_service = OSPService(OSP_ENVIRONMENT)

        for skill in SkillCode.__members__:
            if skill in (SkillCode.Speaking.value, SkillCode.Writing.value):
                for sub_skill in SubSkillCode.__members__:
                    sub_skill_code = skill + "-" + sub_skill
                    # update total score as null for each sub skill to check if the skill API return with 409,
                    # and also check the Unit API
                    self.update_score_as_null_then_verify(osp_service, student_id, test_primary_key,
                                                          book_key, unit_key, sub_skill_code, True)
            else:
                # update original score and overwritten score as null for each skill to check if skill and unit API
                self.update_score_as_null_then_verify(osp_service, student_id, test_primary_key, book_key,
                                                      unit_key, skill, True)

        # make all the data valid after test
        PTReviewUtils.update_random_score_with_omni_pt_assess_api(student_id, test_primary_key)

    @Test(tags="qa, stg")
    def test_enrolled_groups_with_state_api(self):
        omni_service = OMNIService(OMNI_ENVIRONMENT)
        tpi_service = TPIService(TPI_ENVIRONMENT)
        customer_list = PTReviewData.ptr_hf_user[env_key]
        for customer in customer_list:
            user_name = customer["username"]
            password = customer["password"]
            print("Verify user:" + user_name)
            customer_id = omni_service.get_customer_id(user_name, password)
            groups_response = omni_service.get_customer_groups(customer_id)
            expected_course_list = PTReviewUtils.get_expected_default_available_books(groups_response.json())
            actual_default_available_course_result = tpi_service.post_enrolled_groups_with_state(customer_id,
                                                                                                 'highflyers')
            assert_that(actual_default_available_course_result.status_code == 200)
            error_message = \
                PTReviewUtils.verify_enrolled_groups_with_state(actual_default_available_course_result.json(),
                                                                expected_course_list)
            assert_that(error_message == '', user_name + "'s verification failed:" + error_message)

    @Test(tags="qa, stg")
    def test_resource_url_lessthan_50(self):
        pt_review_service = PTReviewService(ENVIRONMENT)
        resource_list = PTReviewData.ptr_resource_list[env_key]
        # make sure options API return 200
        recource_url_options_response = pt_review_service.options_resource_batch()
        assert_that(recource_url_options_response.status_code == 200)

        recource_url_response = pt_review_service.post_resource_batch(resource_list)
        assert_that(recource_url_response.status_code == 200)
        error_message = PTReviewUtils.verify_resource_url(recource_url_response.json(), resource_list)
        assert_that(error_message == '', "Resource API verification failed:" + error_message)

    @Test(tags="qa, stg")
    def test_resource_url_exceed_50(self):
        pt_review_service = PTReviewService(ENVIRONMENT)
        resource_list = PTReviewData.ptr_resource_list[env_key]

        original_length = len(resource_list)
        loop_num, remainder = divmod(51, original_length)

        # mock resouce list to make the size = 51,  API will not filter out the duplicate resouce key
        exceed_fifty_resouce_list = []
        for i in range(loop_num):
            exceed_fifty_resouce_list.extend(resource_list)

        if remainder > 0:
            exceed_fifty_resouce_list.extend(resource_list[:remainder])

        recource_url_response = pt_review_service.post_resource_batch(exceed_fifty_resouce_list)
        assert_that(recource_url_response.status_code == 403)
        response_message = recource_url_response.json()['Message']
        assert_that('Reason: the max length of keys is 50' in response_message)

    # test pt review bff graphql API by book and unit
    @Test(tags="qa, stg, live")
    def test_ptr_bff_graphql_by_book_unit(self):
        pt_review_bff_service = PTReviewBFFService(ENVIRONMENT)
        pt_review_bff_service.login()
        osp_service = OSPService(OSP_ENVIRONMENT)
        course_code = 'HF'
        student_id = PTReviewData.ptr_bff_data[env_key]['HF']['StudentId']
        book_key = PTReviewData.ptr_bff_data[env_key]['HF']['BookKey']
        unit_key = PTReviewData.ptr_bff_data[env_key]['HF']['UnitKey']
        ptr_bff_graphql_response = pt_review_bff_service.post_ptr_graphql_by_book_unit(course_code, book_key, unit_key)
        assert_that(ptr_bff_graphql_response.status_code == 200)

        api_pt_assess_by_skill_response = osp_service.post_hf_student_pt_assess_by_skill(student_id, book_key, unit_key)
        expected_ptr_result_by_skill = \
            PTReviewUtils.get_expected_ptr_bff_result_by_book_unit(api_pt_assess_by_skill_response.json())

        error_message = PTReviewUtils.verify_ptr_bff_graphql_by_book_unit(ptr_bff_graphql_response.json(),
                                                                          expected_ptr_result_by_skill)
        assert_that(error_message == '', error_message)

    # test pt review bff graphql API by book
    @Test(tags="qa, stg, live")
    def test_ptr_bff_graphql_by_book(self):
        pt_review_bff_service = PTReviewBFFService(ENVIRONMENT)
        pt_review_bff_service.login()
        student_id = PTReviewData.ptr_bff_data[env_key]['HF']['StudentId']
        book_key = PTReviewData.ptr_bff_data[env_key]['HF']['BookKey']
        course_code = 'HF'
        ptr_bff_graphql_response = pt_review_bff_service.post_ptr_graphql_by_book(course_code, book_key)
        print(ptr_bff_graphql_response.json())
        assert_that(ptr_bff_graphql_response.status_code == 200)

        expected_ptr_result_by_book = \
            PTReviewUtils.get_expected_ptr_bff_result_by_book(student_id, course_code, book_key, None)

        actual_ptr_bff_graphql_result_by_book = ptr_bff_graphql_response.json()['data']['book']
        error_message = PTReviewUtils.verify_ptr_bff_graphql_by_book(actual_ptr_bff_graphql_result_by_book,
                                                                     expected_ptr_result_by_book)
        assert_that(error_message == '', error_message)

    # test pt review bff graphql API for all course
    @Test(tags="qa, stg,live")
    def test_ptr_bff_graphql_all_course(self):
        pt_review_bff_service = PTReviewBFFService(ENVIRONMENT)
        pt_review_bff_service.login()
        student_id = PTReviewData.ptr_bff_data[env_key]['HF']['StudentId']
        course_code = 'HF'
        ptr_bff_graphql_response = pt_review_bff_service.post_ptr_graphql_by_student(course_code)
        assert_that(ptr_bff_graphql_response.status_code == 200)

        expected_ptr_result_all_course = \
            PTReviewUtils.get_expected_ptr_bff_result_all_course(student_id, course_code)

        error_message = PTReviewUtils.verify_ptr_bff_graphql_all_course(ptr_bff_graphql_response.json(),
                                                                        expected_ptr_result_all_course)
        assert_that(error_message == '', error_message)

    @Test(tags="qa,stg")
    def test_pt_web_osp_create_pt_entity(self):
        osp_service = OSPService(OSP_ENVIRONMENT)
        pt_key = PTDATA.pt_web_data[env_key]['HFF']['TestPrimaryKey']
        student_id = PTDATA.pt_web_data[env_key]['HFF']['StudentId']
        expected_entity_dict = PTReviewUtils.construct_expected_pt_web_create_entity(pt_key, student_id)
        actual_result = osp_service.put_create_progress_test_entity(expected_entity_dict)
        assert_that(actual_result.status_code == 200)
        print(actual_result.json())
        assert_that(actual_result.json()["TeacherId"], equal_to(expected_entity_dict["TeacherId"]))
        assert_that(actual_result.json()["ProgressTestKey"], equal_to(expected_entity_dict["ProgressTestKey"].lower()))
        assert_that(actual_result.json()["GroupId"], equal_to(expected_entity_dict["GroupId"]))
        assert_that(actual_result.json()["SchoolCode"], equal_to(expected_entity_dict["SchoolCode"]))
        assert_that(actual_result.json()["Name"], equal_to("Progress Test"))
        pt_instance_key = PTReviewUtils.get_pt_instance_key_from_db(pt_key)
        pt_instance_key = str(pt_instance_key)[str(pt_instance_key).find("'") + 1:str(pt_instance_key).find(")") - 1]
        assert_that(actual_result.json()["ProgressTestInstanceKey"], equal_to(pt_instance_key))
        assert_that(len(actual_result.json()) == 11, "response fields numbers is invalid,please check whether add or "
                                                     "remove any fields")

    @Test(tags="qa,stg")
    def test_pt_web_osp_query_test_by_student_and_book(self):
        osp_service = OSPService(OSP_ENVIRONMENT)
        student_id = PTDATA.pt_web_data[env_key]['HFF']['StudentId']
        book_key = PTDATA.pt_web_data[env_key]['HFF']['BookKey']
        pt_key = PTDATA.pt_web_data[env_key]['HFF']['TestPrimaryKey']
        unit_key = PTDATA.pt_web_data[env_key]['HFF']['UnitKey']
        actual_result = osp_service.post_query_pt_by_student_book_state(student_id, book_key)
        assert_that(actual_result.status_code == 200)
        print(actual_result.json())
        assert_that(actual_result.json()[0]["StudentId"], equal_to(str(student_id)))
        assert_that(actual_result.json()[0]["ProgressTestKey"], equal_to(pt_key.lower()))
        assert_that(actual_result.json()[0]["UnitKey"], equal_to(unit_key.lower()))
        pt_instance_key = PTReviewUtils.get_pt_instance_key_from_db(pt_key)
        pt_instance_key = str(pt_instance_key)[str(pt_instance_key).find("'") + 1:str(pt_instance_key).find(")") - 1]
        assert_that(actual_result.json()[0]["ProgressTestInstanceKey"], equal_to(pt_instance_key))
        assert_that(len(actual_result.json()[0]) == 6, "response fields numbers is invalid,please check whether add or "
                                                       "remove any fields")

    @Test(tags="qa,stg")
    def test_pt_web_osp_query_test_by_test_result(self):
        osp_service = OSPService(OSP_ENVIRONMENT)
        student_id = PTDATA.pt_web_data[env_key]['HFD']['StudentId']
        book_key = PTDATA.pt_web_data[env_key]['HFD']['BookKey']
        pt_key = PTDATA.pt_web_data[env_key]['HFD']['TestPrimaryKey']
        unit_key = PTDATA.pt_web_data[env_key]['HFD']['UnitKey']
        actual_result = osp_service.post_query_pt_test_result_by_student_book(student_id, book_key)
        assert_that(actual_result.status_code == 200)
        print(" response is : %s" % (json.dumps(actual_result.json(), indent=4)))
        assert_that(actual_result.json()[0]["PTTotalScore"], equal_to(None))
        assert_that(actual_result.json()[0]["UnitKey"], equal_to(unit_key.lower()))
        assert_that(actual_result.json()[0]["ProgressTestKey"], equal_to(pt_key.lower()))
        assert_that(len(actual_result.json()[0]) == 8,
                    "response fields numbers is invalid,please check whether add or remove any fields")

    @Test(tags="qa,stg,live")
    def test_pt_web_tpi_create_pt_entity(self):
        tpi_service = TPIService(TPI_ENVIRONMENT)
        pt_key = PTDATA.pt_web_data[env_key]['HFF']['TestPrimaryKey']
        student_id = PTDATA.pt_web_data[env_key]['HFF']['StudentId']
        expected_entity_dict = PTReviewUtils.construct_expected_pt_web_create_entity(pt_key, student_id)
        actual_result = tpi_service.pt_web_unlock(expected_entity_dict)
        assert_that(actual_result.status_code == 200)
        print(json.dumps(actual_result.json(), indent=4))
        assert_that(actual_result.json()["TeacherId"], equal_to(expected_entity_dict["TeacherId"]))
        assert_that(actual_result.json()["ProgressTestKey"], equal_to(expected_entity_dict["ProgressTestKey"].lower()))
        assert_that(actual_result.json()["GroupId"], equal_to(expected_entity_dict["GroupId"]))
        assert_that(actual_result.json()["SchoolCode"], equal_to(expected_entity_dict["SchoolCode"]))
        assert_that(actual_result.json()["Name"], equal_to("Progress Test"))
        if not EnvUtils.is_env_live():
            pt_instance_key = PTReviewUtils.get_pt_instance_key_from_db(pt_key)
            pt_instance_key = str(pt_instance_key)[str(pt_instance_key).find("'") + 1:str(pt_instance_key).find(")") - 1]
            assert_that(actual_result.json()["ProgressTestInstanceKey"], equal_to(pt_instance_key))
        assert_that(len(actual_result.json()) == 11, "response fields numbers is invalid,please check whether add or "
                                                     "remove any fields")

    @Test(tags="qa,stg")
    def test_pt_web_unlock_pt_after_paper_version_should_403(self):
        osp_service = OSPService(OSP_ENVIRONMENT)
        pt_key = PTDATA.pt_web_data[env_key]['HFJ3']['TestPrimaryKey']
        student_id = PTDATA.pt_web_data[env_key]['HFJ3']['StudentId']
        PTReviewUtils.set_pt_paper_version_from_db(pt_key, student_id)
        expected_entity_dict = PTReviewUtils.construct_expected_pt_web_create_entity(pt_key, student_id)
        actual_result = osp_service.put_create_progress_test_entity(expected_entity_dict)
        assert_that(actual_result.status_code == 403)
        print(actual_result.json())

    @Test(tags="qa,stg")
    def test_pt_web_multiple_students_can_take_test_after_one_of_them_commit(self):
        pt_key = PTDATA.pt_web_data[env_key]['HFC4']['TestPrimaryKey']
        students_ids = PTDATA.pt_web_data[env_key]['HFC4']['StudentId']
        tpi_service = TPIService(TPI_ENVIRONMENT)
        expected_entity_dict = PTReviewUtils.construct_expected_pt_web_create_entity(pt_key, students_ids)
        actual_result = tpi_service.pt_web_unlock(expected_entity_dict)
        pt_instance_key = PTReviewUtils.get_pt_instance_key_from_db(pt_key)
        try:
            assert_that(actual_result.status_code == 200)
            print(json.dumps(actual_result.json(), indent=4))
            assert_that(actual_result.json()["TeacherId"], equal_to(expected_entity_dict["TeacherId"]))
            assert_that(actual_result.json()["ProgressTestKey"],
                        equal_to(expected_entity_dict["ProgressTestKey"].lower()))
            osp_service = OSPService(OSP_ENVIRONMENT)
            pt_instance_key = str(pt_instance_key)[
                              str(pt_instance_key).find("'") + 1:str(pt_instance_key).find(")") - 1]
            commit_response = osp_service.put_commit_progress_test_hc(students_ids[0], pt_instance_key)
            print(commit_response.status_code)
            assert_that(commit_response.status_code == 204)
            othe_ther_student_pt_state = PTReviewUtils.get_student_pt_state(students_ids[1],pt_instance_key)
            assert_that(othe_ther_student_pt_state[0][0],equal_to(1))
        finally:
            print("Finally reset student progress test status by update db")
            PTReviewUtils.set_student_pt_state_to_inital_value(students_ids[0], pt_instance_key)







