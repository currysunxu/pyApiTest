from E1_API_Automation.Business.PTSkillScore import PTSkillScore, SkillCode, SubSkillCode
from hamcrest import assert_that
from E1_API_Automation.Business.TPIService import TPIService
from ...Settings import TPI_ENVIRONMENT
import jmespath
import datetime
import random


class PTReviewUtils:
    @staticmethod
    def verify_hf_allbooks_api_db_result(api_response_json, db_query_result):
        # check if all the data return from API is consistent with DB
        error_message = ''
        time_format = '%Y-%m-%d %H:%M:%S.%f'
        for i in range(len(api_response_json)):
            response_json = api_response_json[i]
            db_result = db_query_result[i]
            for key in response_json.keys():
                actual_result = response_json[key]
                expected_result = db_result[key]
                if actual_result is None:
                    actual_result = ''
                if expected_result is None:
                    expected_result = ''
                if key in ('CreatedBy', 'LastUpdatedBy', 'Key', 'ParentNodeKey', 'TopNodeKey'):
                    # the value get from the DB is UUID type
                    expected_result = str(expected_result)
                elif key in ('CreatedStamp', 'LastUpdatedStamp'):
                    actual_result = datetime.datetime.strptime(actual_result, '%Y-%m-%dT%H:%M:%S.%fZ')
                    actual_result = actual_result.strftime(time_format)
                    expected_result = expected_result.strftime(time_format)

                if str(actual_result) != str(expected_result):
                    error_message = error_message + "List[" + i + "].key:" + key + \
                                    "'s api result not equal to db value, the result return in API is:" + \
                                    str(actual_result) + ", but the value in DB is:" + str(expected_result) + ";"
        return error_message

    '''
    generate PT whole online skill, offline skill with sub skills, and generate random scores for those 
    skill/subskills, return with dictionary list
    '''
    @staticmethod
    def generate_pt_whole_skill_subskill_randomscore_list():
        skill_dic = {}

        # four online skills
        grammar_score = PTSkillScore(SkillCode.Grammar, 0, random.randint(1, 10), random.randint(10, 20))
        listening_score = PTSkillScore(SkillCode.Listening, 0, random.randint(1, 10), random.randint(10, 20))
        reading_score = PTSkillScore(SkillCode.Reading, 0, random.randint(1, 10), random.randint(10, 20))
        vocabulary_score = PTSkillScore(SkillCode.Vocabulary, 0, random.randint(1, 10), random.randint(10, 20))

        skill_dic[SkillCode.Grammar] = grammar_score
        skill_dic[SkillCode.Listening] = listening_score
        skill_dic[SkillCode.Reading] = reading_score
        skill_dic[SkillCode.Vocabulary] = vocabulary_score

        # writing skill with four sub skills
        writing_cc_score = PTSkillScore(SubSkillCode.CommunicativeCompetence, 0, random.randint(1, 10),
                                        random.randint(10, 20))
        writing_lc_score = PTSkillScore(SubSkillCode.LexicalCommand, 0, random.randint(1, 10), random.randint(10, 20))
        writing_gc_score = PTSkillScore(SubSkillCode.GrammaticalControl, 0, random.randint(1, 10),
                                        random.randint(10, 20))
        writing_punc_score = PTSkillScore(SubSkillCode.Punctuation, 0, random.randint(1, 10), random.randint(10, 20))

        writing_list = [writing_cc_score, writing_lc_score, writing_gc_score, writing_punc_score]

        skill_dic[SkillCode.Writing] = writing_list

        # speaking skill with four sub skills
        speaking_cc_score = PTSkillScore(SubSkillCode.CommunicativeCompetence, 0, random.randint(1, 10),
                                         random.randint(10, 20))
        speaking_lc_score = PTSkillScore(SubSkillCode.LexicalCommand, 0, random.randint(1, 10), random.randint(10, 20))
        speaking_gc_score = PTSkillScore(SubSkillCode.GrammaticalControl, 0, random.randint(1, 10),
                                         random.randint(10, 20))
        speaking_punc_score = PTSkillScore(SubSkillCode.Punctuation, 0, random.randint(1, 10), random.randint(10, 20))

        speaking_list = [speaking_cc_score, speaking_lc_score, speaking_gc_score, speaking_punc_score]

        skill_dic[SkillCode.Speaking] = speaking_list

        return skill_dic

    # generate body for /api/v2/OmniProgressTestAssessment/ API
    @staticmethod
    def generate_assessment_body_for_omni(pt_key, student_skill):
        assessment_body = {}
        student_result = []
        for student_id in student_skill.keys():
            student_skill_result = {}
            online_skill_results = []
            rubric_skills = []
            skill_dic = student_skill[student_id]
            for key in skill_dic.keys():
                pt_skill_score = skill_dic[key]
                if key not in (SkillCode.Speaking, SkillCode.Writing):
                    skill_score = {}
                    skill_score["SkillName"] = pt_skill_score.skillCode.value
                    skill_score["OriginScore"] = pt_skill_score.originScore
                    skill_score["OverwriteScore"] = pt_skill_score.overwriteScore
                    skill_score["TotalScore"] = pt_skill_score.totalScore
                    online_skill_results.append(skill_score)
                else:
                    rubric_skill_score = {}
                    rubric_skill_score["SkillName"] = key.value
                    if isinstance(pt_skill_score, list):
                        offline_assessment_result = []
                        for sub_skill in pt_skill_score:
                            sub_skill_score = {}
                            sub_skill_score["Key"] = sub_skill.skillCode.value
                            sub_skill_score["OriginScore"] = sub_skill.originScore
                            sub_skill_score["OverwriteScore"] = sub_skill.overwriteScore
                            sub_skill_score["TotalScore"] = sub_skill.totalScore
                            offline_assessment_result.append(sub_skill_score)
                        rubric_skill_score["OfflineAssessmentResult"] = offline_assessment_result
                        rubric_skill_score["OriginScore"] = 1
                        rubric_skill_score["OverwriteScore"] = 1
                        rubric_skill_score["TotalScore"] = 1
                    else:
                        rubric_skill_score["OriginScore"] = pt_skill_score.originScore
                        rubric_skill_score["OverwriteScore"] = pt_skill_score.overwriteScore
                        rubric_skill_score["TotalScore"] = pt_skill_score.totalScore
                    rubric_skills.append(rubric_skill_score)

            student_skill_result["StudentId"] = student_id
            student_skill_result["OnlineSkillResults"] = online_skill_results
            student_skill_result["RubricSkills"] = rubric_skills
            student_result.append(student_skill_result)

        assessment_body["PTKey"] = pt_key
        assessment_body["StudentResults"] = student_result
        return assessment_body

    # call OmniProgressTestAssessment API to update random score
    @staticmethod
    def update_random_score_with_omni_pt_assess_api(student_id, pt_key):
        # construct data to call the API
        skill_dic = PTReviewUtils.generate_pt_whole_skill_subskill_randomscore_list()
        student_skill = {}
        student_skill[student_id] = skill_dic
        omni_body = PTReviewUtils.generate_assessment_body_for_omni(pt_key, student_skill)

        # omni_body_json = json.dumps(omni_body)
        # print(omni_body_json)

        # call OmniProgressTestAssessment API to update overwritten score and total score
        tpi_service = TPIService(TPI_ENVIRONMENT)
        tpi_response = tpi_service.put_hf_student_omni_pt_assessment(omni_body)
        assert_that(tpi_response.status_code == 204)

    @staticmethod
    def verify_pt_score_with_api_response(skill_dic, assess_metas_response, unit_key):
        # verify if the data get from the StudentPaperDigitalProgressTestAssessmentMetas API are as what you constructed
        for key in skill_dic.keys():
            pt_skill_score = skill_dic[key]
            if key not in (SkillCode.Speaking, SkillCode.Writing):
                PTReviewUtils.verify_pt_score(key.value, pt_skill_score, assess_metas_response, unit_key)

            else:
                if isinstance(pt_skill_score, list):
                    for sub_skill in pt_skill_score:
                        code = key.value + '-' + sub_skill.skillCode.value
                        PTReviewUtils.verify_pt_score(code, sub_skill, assess_metas_response, unit_key)
                else:
                    PTReviewUtils.verify_pt_score(key.value, pt_skill_score, assess_metas_response, unit_key)

    @staticmethod
    def verify_pt_score(skill_code, pt_skill_score, assess_metas_response, unit_key):
        # unit_key = PTReviewData.pt_hf_user_key_book_unit[env_key]['UnitKey']
        filter_str = "@[?(Code == '{0}'|| Code == '{1}') && UnitKey == '{2}']".format(skill_code, skill_code[:1].lower()
                                                                                      + skill_code[1:], unit_key.lower()
                                                                                      )
        actual_score = jmespath.search(filter_str+".Score | [0]", assess_metas_response)
        expected_score = pt_skill_score.overwriteScore

        actual_totalscore = jmespath.search(filter_str+".TotalScore | [0]", assess_metas_response)
        expected_totalscore = pt_skill_score.totalScore

        assert_that(actual_score == expected_score, skill_code + "'s score not been saved to OSP DB correctly.")
        assert_that(actual_totalscore == expected_totalscore,
                    skill_code + "'s total score not been saved to OSP DB correctly.")

    '''
    get the expected pt assessment by skill
    '''
    @staticmethod
    def get_expected_pt_assessment_by_skill(student_pt_assessment_dict_list, from_db):
        expected_pt_assessment_by_skill_list = []
        speaking_list = []
        writing_list = []
        speaking_code = SkillCode.Speaking.value
        writing_code = SkillCode.Writing.value
        for skill_pt_score in student_pt_assessment_dict_list:
            skill_code = skill_pt_score["Code"]
            if skill_code.capitalize().startswith(speaking_code):
                speaking_list.append(skill_pt_score)
            elif skill_code.capitalize().startswith(writing_code):
                writing_list.append(skill_pt_score)
            else:
                # code must be in standardized list
                if skill_code.capitalize() not in (SkillCode.Grammar.value, SkillCode.Listening.value,
                                                   SkillCode.Reading.value, SkillCode.Vocabulary.value):
                    return None

                # the source list might from DB, or from API, DB data suite for the qa and staging testing,
                # while API data suites for the Live testing
                if from_db:
                    score = skill_pt_score["OverwrittenScore"]
                    if score is None:
                        score = skill_pt_score["OriginalScore"]
                else:
                    score = skill_pt_score["Score"]

                if score is None:
                    return None
                else:
                    score = int(score)

                total_score = skill_pt_score["TotalScore"]

                if total_score is None:
                    return None
                else:
                    total_score = int(total_score)

                expected_skill_pt_score_dict = PTReviewUtils.construct_expected_skill_pt_score_dict(skill_code, score,
                                                                                                    total_score,
                                                                                                    skill_pt_score,
                                                                                                    from_db)

                expected_pt_assessment_by_skill_list.append(expected_skill_pt_score_dict)

        # get the expected pt assessment for speaking skill
        expected_speaking_pt_score_dict = PTReviewUtils.get_expected_pt_assessment_by_subskill(speaking_code,
                                                                                               speaking_list,
                                                                                               from_db)

        if expected_speaking_pt_score_dict is None:
            return None
        else:
            expected_pt_assessment_by_skill_list.append(expected_speaking_pt_score_dict)

        # get the expected pt assessment for writing skill
        expected_writing_pt_score_dict = PTReviewUtils.get_expected_pt_assessment_by_subskill(writing_code,
                                                                                              writing_list,
                                                                                              from_db)

        if expected_writing_pt_score_dict is None:
            return None
        else:
            expected_pt_assessment_by_skill_list.append(expected_writing_pt_score_dict)

        # expected list should include all the enum codes
        if len(expected_pt_assessment_by_skill_list) != SkillCode.__len__():
            return None
        else:
            return expected_pt_assessment_by_skill_list

    '''
    get the expected pt assessment score by sub skill, for speaking and writing, the score and total score should be the 
    sum of the each sub skills 
    '''
    @staticmethod
    def get_expected_pt_assessment_by_subskill(skill_code, sub_skill_list, from_db):
        score = 0
        total_score = 0
        # if sub_skill_list not empty
        if sub_skill_list:
            # if any sub skill's score or total score is null, then, return null
            for sub_skill in sub_skill_list:
                # the source list might from DB, or from API, DB data suite for the qa and staging testing,
                # while API data suites for the Live testing
                if from_db:
                    sub_skill_score = sub_skill["OverwrittenScore"]
                    if sub_skill_score is None:
                        sub_skill_score = sub_skill["OriginalScore"]
                else:
                    sub_skill_score = sub_skill["Score"]

                if sub_skill_score is None:
                    return None
                else:
                    sub_skill_score = int(sub_skill_score)

                score = score + sub_skill_score

                sub_total_score = sub_skill["TotalScore"]

                if sub_total_score is None:
                    return None
                else:
                    sub_total_score = int(sub_total_score)

                total_score = total_score + sub_total_score

            one_sub_skill_dict = sub_skill_list[0]
            expected_skill_pt_score_dict = PTReviewUtils.construct_expected_skill_pt_score_dict(skill_code, score,
                                                                                                total_score,
                                                                                                one_sub_skill_dict,
                                                                                                from_db)

            return expected_skill_pt_score_dict
        else:
            return None

    @staticmethod
    def construct_expected_skill_pt_score_dict(skill_code, score, total_score, skill_pt_score_dict, from_db):
        expected_skill_pt_score_dict = {}

        if from_db:
            if skill_pt_score_dict["TestInstanceKey"] is None:
                pt_test_by = 0
            else:
                pt_test_by = 1
        else:
            pt_test_by = skill_pt_score_dict["PTTestBy"]

        expected_skill_pt_score_dict["StudentId"] = skill_pt_score_dict["StudentId"]
        expected_skill_pt_score_dict["Code"] = skill_code
        expected_skill_pt_score_dict["Score"] = score
        expected_skill_pt_score_dict["TotalScore"] = total_score
        expected_skill_pt_score_dict["BookKey"] = skill_pt_score_dict["BookKey"]
        expected_skill_pt_score_dict["BookCode"] = skill_pt_score_dict["BookCode"]
        expected_skill_pt_score_dict["BookName"] = skill_pt_score_dict["BookName"]
        expected_skill_pt_score_dict["UnitKey"] = skill_pt_score_dict["UnitKey"]
        expected_skill_pt_score_dict["UnitCode"] = skill_pt_score_dict["UnitCode"]
        expected_skill_pt_score_dict["UnitName"] = skill_pt_score_dict["UnitName"]
        expected_skill_pt_score_dict["PTTestBy"] = pt_test_by

        return expected_skill_pt_score_dict

    @staticmethod
    def verify_hf_pt_assessment_by_skill(api_pt_assess_by_skill_json, expected_pt_assess_by_skill):
        # check if all the data return from API is consistent with DB
        error_message = ''

        # the API return skill length should be same as the expected enum length
        if len(api_pt_assess_by_skill_json) != SkillCode.__len__():
            error_message = "API skill list length not as expected;"
            return error_message

        code_list = jmespath.search('[].Code', api_pt_assess_by_skill_json)

        # skill code must be in the expected enum list
        for skill_code in code_list:
            if skill_code.capitalize() not in SkillCode._value2member_map_:
                error_message = error_message + skill_code + " not in the expected skill code list;"

        if error_message != '':
            return error_message

        for skill_pt_assess in api_pt_assess_by_skill_json:
            for expected_skill_pt_assess in expected_pt_assess_by_skill:
                if skill_pt_assess["Code"] == expected_skill_pt_assess["Code"]:
                    for key in expected_skill_pt_assess.keys():
                        actual_result = skill_pt_assess[key]
                        expected_result = expected_skill_pt_assess[key]

                        if str(actual_result) != str(expected_result):
                            error_message = error_message + "Code" + skill_pt_assess["Code"] + "'s key:" + key + \
                                            "'s api result not equal to expected value, the result return in API is:" \
                                            + str(actual_result) + ", but the value expected is:" \
                                            + str(expected_result) + ";"
                    break

        return error_message

    @staticmethod
    def update_score_as_null(pt_review_service, student_id, test_primary_key, skill_subskill_code, is_total_score):
        print("Checking code:" + skill_subskill_code + " for is_total_score:" + str(is_total_score))
        # make sure all the score have value at first
        PTReviewUtils.update_random_score_with_omni_pt_assess_api(student_id, test_primary_key)

        # if one skill or sub skill's TotalScore is null or if original score and overwritten score are both null,
        # then the api will return 409
        if is_total_score:
            pt_review_service.update_pt_assessment_total_score(student_id, test_primary_key, skill_subskill_code)
        else:
            pt_review_service.update_pt_assessment_original_overwritten_score(student_id, test_primary_key,
                                                                              skill_subskill_code)

    @staticmethod
    def get_expected_pt_assessment_by_unit(student_pt_assessment_dict_list, from_db):
        pt_assessment_by_unit = {}
        # put same unit pt score together
        for skill_pt_score in student_pt_assessment_dict_list:
            unit_key = str(skill_pt_score["UnitKey"])
            pt_assessment_by_unit.setdefault(unit_key, []).append(skill_pt_score)

        # for each unit, calculate the expected total score and other info
        expected_pt_assessment_by_unit = []
        for unit_key in pt_assessment_by_unit.keys():
            unit_pt_assessment_dict_list = pt_assessment_by_unit[unit_key]
            unit_expected_pt_assessment_by_skill = \
                PTReviewUtils.get_expected_pt_assessment_by_skill(unit_pt_assessment_dict_list, from_db)

            # if there's some data issues which make the expected skill pt assessment as None,
            # then the expected unit total score is null
            if unit_expected_pt_assessment_by_skill is None:
                unit_total_score = None
            else:
                unit_total_accuracy = 0
                unit_skill_count = 0
                '''
                    calculate the unit total score, the formula is:
                    a. Accuracy of each skill = round((result * 100) / total)
                    b. PT total =  avg(accuracy of each skill)
                    check ticket E1SP-201 for the detailed info
                '''
                for expected_pt_assessment_by_skill in unit_expected_pt_assessment_by_skill:
                    skill_score = expected_pt_assessment_by_skill["Score"]
                    skill_total_score = expected_pt_assessment_by_skill["TotalScore"]
                    skill_accuracy = PTReviewUtils.round_up((skill_score * 100) / skill_total_score)
                    unit_total_accuracy = unit_total_accuracy + skill_accuracy
                    unit_skill_count = unit_skill_count + 1

                unit_total_score = PTReviewUtils.round_up(unit_total_accuracy/unit_skill_count)

            expected_pt_score_by_unit_dict = \
                PTReviewUtils.construct_expected_pt_score_by_unit_dict(unit_total_score,
                                                                       unit_pt_assessment_dict_list[0],
                                                                       from_db)
            expected_pt_assessment_by_unit.append(expected_pt_score_by_unit_dict)

        return expected_pt_assessment_by_unit

    '''
    in python 3 above, the round() function will not return the right value when the value is kind like 72.5, it will 
    return 72 when using round(72.5), but we expect 73. So, using following function to implement the round function
    '''
    @staticmethod
    def round_up(number):
        result = number + 0.5
        return int(result)

    @staticmethod
    def construct_expected_pt_score_by_unit_dict(total_score, unit_pt_score_dict, from_db):
        expected_pt_score_by_unit_dict = {}

        if from_db:
            if unit_pt_score_dict["TestInstanceKey"] is None:
                pt_test_by = 0
            else:
                pt_test_by = 1
        else:
            pt_test_by = unit_pt_score_dict["PTTestBy"]

        # if total_score is None:
        #     total_score = "null"

        expected_pt_score_by_unit_dict["PTTotalScore"] = total_score
        expected_pt_score_by_unit_dict["UnitKey"] = unit_pt_score_dict["UnitKey"]
        expected_pt_score_by_unit_dict["UnitCode"] = unit_pt_score_dict["UnitCode"]
        expected_pt_score_by_unit_dict["UnitName"] = unit_pt_score_dict["UnitName"]
        expected_pt_score_by_unit_dict["PTTestBy"] = pt_test_by

        return expected_pt_score_by_unit_dict

    @staticmethod
    def verify_hf_pt_assessment_by_unit(api_pt_assess_by_unit_json, expected_pt_assess_by_unit):
        # check if all the data return from API is consistent with DB
        error_message = ''

        if len(api_pt_assess_by_unit_json) != len(expected_pt_assess_by_unit):
            error_message = "the actual list length return from API not as expected!"

        for unit_pt_assess in api_pt_assess_by_unit_json:
            is_unit_key_exist = False
            actual_unit_key = str(unit_pt_assess["UnitKey"])
            for expected_unit_pt_assess in expected_pt_assess_by_unit:
                if actual_unit_key == str(expected_unit_pt_assess["UnitKey"]):
                    is_unit_key_exist = True
                    for key in expected_unit_pt_assess.keys():
                        actual_result = unit_pt_assess[key]
                        expected_result = expected_unit_pt_assess[key]

                        if str(actual_result) != str(expected_result):
                            error_message = error_message + "UnitKey" + actual_unit_key + "'s key:" + key + \
                                            "'s api result not equal to expected value, the result return in API is:" \
                                            + str(actual_result) + ", but the value expected is:" \
                                            + str(expected_result) + ";"
                    break
            if not is_unit_key_exist:
                error_message = error_message + "UnitKey" + actual_unit_key + " not exist in the expected list!"

        return error_message
