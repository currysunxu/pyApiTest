import string

from E1_API_Automation.Business.PTSkillScore import PTSkillScore, SkillCode, SubSkillCode
from hamcrest import assert_that
from E1_API_Automation.Business.TPIService import TPIService
from E1_API_Automation.Business.OMNIService import CourseGroupStatus, CourseGroupInfo
from E1_API_Automation.Business.PTReviewService import PTReviewService
from E1_API_Automation.Business.OSPService import OSPService
from E1_API_Automation.Lib.db_mssql import MSSQLHelper
from E1_API_Automation.Test_Data.PTReviewData import PtWebSQLString
from ...Settings import DATABASE
import jmespath
import datetime
import random
import json


class PTReviewUtils:
    @staticmethod
    def verify_allbooks_by_course_api_db_result(api_response_json, db_query_result):
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
                elif key in ('Body'):
                    if expected_result != '':
                        expected_result = json.loads(expected_result)

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
        tpi_service = TPIService()
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
        expected_skill_score_list = []
        speaking_list = []
        writing_list = []
        speaking_code = SkillCode.Speaking.value
        writing_code = SkillCode.Writing.value
        test_by = 1
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
                        # if one of the grammer/vocabulary/reading/listening's OverwrittenScore have value, means it's paper test
                        # modified by E1SP-405
                        test_by = 0
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

                expected_skill_score = PTReviewUtils.construct_expected_skill_score(skill_code, score, total_score)
                expected_skill_score_list.append(expected_skill_score)

        # get the expected pt assessment for speaking skill
        expected_speaking_pt_score_dict = PTReviewUtils.get_expected_pt_assessment_by_subskill(speaking_code,
                                                                                               speaking_list,
                                                                                               from_db)

        if expected_speaking_pt_score_dict is None:
            return None
        else:
            expected_skill_score_list.append(expected_speaking_pt_score_dict)

        # get the expected pt assessment for writing skill
        expected_writing_pt_score_dict = PTReviewUtils.get_expected_pt_assessment_by_subskill(writing_code,
                                                                                              writing_list,
                                                                                              from_db)

        if expected_writing_pt_score_dict is None:
            return None
        else:
            expected_skill_score_list.append(expected_writing_pt_score_dict)

        if len(expected_skill_score_list) != SkillCode.__len__():
            return None
        else:
            return PTReviewUtils.construct_expected_skill_pt_score_result(list(filter(lambda d:d["Code"] in ("grammar","listening","Reading","Vocabulary"),student_pt_assessment_dict_list))[0],
                                                                          expected_skill_score_list,
                                                                          from_db, test_by)

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

            expected_skill_pt_score_dict = PTReviewUtils.construct_expected_skill_score(skill_code, score, total_score)

            return expected_skill_pt_score_dict
        else:
            return None

    @staticmethod
    def construct_expected_skill_score(skill_code, score, total_score):
        expected_skill_score = {}
        expected_skill_score["Code"] = skill_code
        expected_skill_score["Score"] = score
        expected_skill_score["TotalScore"] = total_score

        return expected_skill_score

    @staticmethod
    def construct_expected_skill_pt_score_result(skill_pt_score_dict, expected_skill_score_list, from_db, test_by):
        expected_skill_pt_score_dict = {}

        if from_db:
            pt_key = skill_pt_score_dict["TestPrimaryKey"]
            # if skill_pt_score_dict["TestInstanceKey"] is None:
            #     pt_test_by = 0
            # else:
            #     pt_test_by = 1
            pt_test_by = test_by
        else:
            pt_test_by = skill_pt_score_dict["PTTestBy"]
            # if it's live env, there's no such field in the StudentPaperDigitalProgressTestAssessmentMetas API,
            # so, can't get this value for verification
            pt_key = ""

        expected_skill_pt_score_dict["StudentId"] = skill_pt_score_dict["StudentId"]
        expected_skill_pt_score_dict["BookKey"] = skill_pt_score_dict["BookKey"]
        expected_skill_pt_score_dict["BookCode"] = skill_pt_score_dict["BookCode"]
        expected_skill_pt_score_dict["BookName"] = skill_pt_score_dict["BookName"]
        expected_skill_pt_score_dict["UnitKey"] = skill_pt_score_dict["UnitKey"]
        expected_skill_pt_score_dict["UnitCode"] = skill_pt_score_dict["UnitCode"]
        expected_skill_pt_score_dict["UnitName"] = skill_pt_score_dict["UnitName"]
        expected_skill_pt_score_dict["PTKey"] = pt_key
        expected_skill_pt_score_dict["PTTestBy"] = pt_test_by
        expected_skill_pt_score_dict["PTInstanceKey"] = skill_pt_score_dict["TestInstanceKey"] if from_db else skill_pt_score_dict["PTInstanceKey"]
        if from_db:
            if skill_pt_score_dict["OverwrittenScore"] and skill_pt_score_dict["OriginalScore"]:
                expected_skill_pt_score_dict["IsOverwritten"] = True
            elif skill_pt_score_dict["OverwrittenScore"] and skill_pt_score_dict["OriginalScore"] is None:
                expected_skill_pt_score_dict["IsOverwritten"] = False

        # calculate the PTTotalScore
        unit_total_accuracy = 0
        unit_skill_count = 0
        '''
            calculate the unit total score, the formula is:
            a. Accuracy of each skill = round((result * 100) / total)
            b. PT total =  avg(accuracy of each skill)
            check ticket E1SP-201 for the detailed info
        '''
        for expected_skill_score in expected_skill_score_list:
            skill_score = expected_skill_score["Score"]
            skill_total_score = expected_skill_score["TotalScore"]
            skill_accuracy = PTReviewUtils.round_up((skill_score * 100) / skill_total_score)
            unit_total_accuracy = unit_total_accuracy + skill_accuracy
            unit_skill_count = unit_skill_count + 1

        unit_total_score = PTReviewUtils.round_up(unit_total_accuracy / unit_skill_count)

        expected_skill_pt_score_dict["PTTotalScore"] = unit_total_score
        expected_skill_pt_score_dict["SkillScores"] = expected_skill_score_list

        return expected_skill_pt_score_dict

    @staticmethod
    def verify_hf_pt_assessment_by_skill(api_pt_assess_by_skill_json, expected_pt_assess_by_skill):
        # check if all the data return from API is consistent with DB
        error_message = ''

        for key in api_pt_assess_by_skill_json.keys():
            if key != 'SkillScores' and key !='PTInstanceKey' and key !='IsOverwritten' and key !='TestKind' :
                actual_value = api_pt_assess_by_skill_json[key]
                expected_value = expected_pt_assess_by_skill[key]

                if key == 'PTKey' and expected_value == '':
                    if str(actual_value) is None or str(actual_value) == '':
                        error_message = error_message + "PTKey's value in Live Env should not be None;"
                else:
                    if str(actual_value) != str(expected_value):
                        error_message = error_message + "key:" + key + \
                                        "'s api value not equal to expected value, the value in API is:" \
                                        + str(actual_value) + ", but the value expected is:" \
                                        + str(expected_value) + ";"
            else:
                # the API return skill length should be same as the expected enum length
                if len(api_pt_assess_by_skill_json["SkillScores"]) != SkillCode.__len__():
                    error_message = "API SkillScores length not as expected;"
                    return error_message

                code_list = jmespath.search('SkillScores[].Code', api_pt_assess_by_skill_json)

                expected_code_list = [SkillCode.Grammar.value, SkillCode.Vocabulary.value, SkillCode.Listening.value,
                                      SkillCode.Reading.value, SkillCode.Writing.value, SkillCode.Speaking.value]

                # skill code must be in the expected enum list, and with order like E1SP-300 mentioned
                for i in range(len(code_list)):
                    actual_skill_code = code_list[i].capitalize()
                    expected_skill_code = expected_code_list[i]
                    if actual_skill_code != expected_skill_code:
                        error_message = error_message + actual_skill_code \
                                        + " not consistent with the expected skill code order or not " \
                                          "in the expected code list;"

                if error_message != '':
                    return error_message

                for skill_score in api_pt_assess_by_skill_json["SkillScores"]:
                    for expected_skill_score in expected_pt_assess_by_skill["SkillScores"]:
                        if skill_score["Code"] == expected_skill_score["Code"]:
                            for skill_score_key in expected_skill_score.keys():
                                actual_result = skill_score[skill_score_key]
                                expected_result = expected_skill_score[skill_score_key]

                                if str(actual_result) != str(expected_result):
                                    error_message = error_message + "Code" + skill_score["Code"] + "'s key:" + \
                                                    skill_score_key + "'s api result not equal to expected value, " \
                                                                      "the result return in API is:" \
                                                    + str(actual_result) + ", but the value expected is:" \
                                                    + str(expected_result) + ";"
                            break

        return error_message

    @staticmethod
    def update_score_as_null(student_id, test_primary_key, skill_subskill_code, is_total_score):
        print("Checking code:" + skill_subskill_code + " for is_total_score:" + str(is_total_score))
        # make sure all the score have value at first
        PTReviewUtils.update_random_score_with_omni_pt_assess_api(student_id, test_primary_key)

        # if one skill or sub skill's TotalScore is null or if original score and overwritten score are both null,
        # then the api will return 200 after E1SP-814
        if is_total_score:
            PTReviewService.update_pt_assessment_total_score(student_id, test_primary_key, skill_subskill_code)
        else:
            PTReviewService.update_pt_assessment_original_overwritten_score(student_id, test_primary_key,
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

                # according to E1SP-405, PTTestBy value is decided by four skill's overwrittenscore
                test_by = 1
                for unit_pt_assessment_dict in unit_pt_assessment_dict_list:
                    skill_code = unit_pt_assessment_dict["Code"]
                    if skill_code.capitalize() in (SkillCode.Grammar.value, SkillCode.Listening.value,
                                                    SkillCode.Reading.value, SkillCode.Vocabulary.value):
                        over_written_score = None
                        if from_db:
                            over_written_score = unit_pt_assessment_dict["OverwrittenScore"]

                        if over_written_score is not None:
                            test_by = 0
            else:
                unit_total_score = unit_expected_pt_assessment_by_skill["PTTotalScore"]
                test_by = unit_expected_pt_assessment_by_skill["PTTestBy"]

            expected_pt_score_by_unit_dict = \
                PTReviewUtils.construct_expected_pt_score_by_unit_dict(unit_total_score,
                                                                       list(filter(lambda d:d["Code"] in ("grammar","listening","Reading","Vocabulary"),unit_pt_assessment_dict_list))[0],
                                                                       from_db, test_by)
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
    def construct_expected_pt_score_by_unit_dict(total_score, unit_pt_score_dict, from_db, test_by):
        expected_pt_score_by_unit_dict = {}

        if from_db:
            # if unit_pt_score_dict["TestInstanceKey"] is None:
            #     pt_test_by = 0
            # else:
            #     pt_test_by = 1
            pt_test_by = test_by
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

    @staticmethod
    def get_expected_default_available_books(groups_json):
        hf_course_groups = jmespath.search("groups[?program == 'High Flyers']", groups_json)

        hf_course_status_map = {}
        all_course_list = []
        for hf_course_group in hf_course_groups:
            course_type_code = 'HF'+ hf_course_group["programLevel"]
            course_group_status = hf_course_group["status"]
            is_current_group = False

            if course_group_status in (CourseGroupStatus.Past.value, CourseGroupStatus.Current.value):
                course_group = CourseGroupInfo(course_type_code, course_group_status, is_current_group)

                hf_course_status_map.setdefault(course_group_status, []).append(course_group)
                all_course_list.append(course_group)

        priority_first_key = CourseGroupStatus.Current.value
        priority_second_key = CourseGroupStatus.Past.value

        default_course = None
        if priority_first_key in hf_course_status_map.keys():
            default_course = PTReviewUtils.get_default_course(hf_course_status_map[priority_first_key], True)
        elif priority_second_key in hf_course_status_map.keys():
            default_course = PTReviewUtils.get_default_course(hf_course_status_map[priority_second_key], True)


        if default_course is not None:
            default_course.set_is_default_course(True)

        return all_course_list

    @staticmethod
    def get_default_course(course_group_list, is_get_highest):
        default_course = course_group_list[0]
        for i in range(1, len(course_group_list)):
            if is_get_highest:
                if default_course.courseTypeCode < course_group_list[i].courseTypeCode:
                    default_course = course_group_list[i]
            else:
                if default_course.courseTypeCode > course_group_list[i].courseTypeCode:
                    default_course = course_group_list[i]
        return default_course

    @staticmethod
    def verify_enrolled_groups_with_state(default_available_course_api_json, expected_course_list):
        error_message = ''

        if len(default_available_course_api_json) != len(expected_course_list):
            error_message = "the actual result list length return from EnrolledGroupsWithState API are not expected!"
            return error_message

        for actual_course in default_available_course_api_json:
            product_code = actual_course["ProductLevelCode"]
            is_default = actual_course["IsDefaultProductLevel"]
            is_course_exist = False
            for expected_course in expected_course_list:
                expected_course_code = expected_course.courseTypeCode
                if product_code == expected_course_code:
                    is_course_exist = True
                    if str(is_default) != str(expected_course.isDefaultCourse):
                        error_message = error_message + product_code + "'s IsDefaultProductLevel value not as expected!"

                    break

            if not is_course_exist:
                error_message = error_message + product_code + " not exist in the expected list!"

        return error_message

    @staticmethod
    def verify_resource_url(actual_resource_json, resource_list):
        error_message = ''

        if len(actual_resource_json) != len(resource_list):
            error_message = "the actual result list length return from Resource/Batch API are not expected!"
            return error_message

        for i in range(len(resource_list)):
            expected_identifier = resource_list[i]
            expected_url = '/' + expected_identifier
            actual_resource_url = actual_resource_json[i]
            actual_identifier = actual_resource_url["Identifier"]
            actual_credential_Uri = actual_resource_url["CredentialUri"]

            is_resource_exist = False
            if actual_identifier == expected_identifier and expected_url in actual_credential_Uri:
                is_resource_exist = True

            if not is_resource_exist:
                error_message = error_message + actual_identifier + " not exist in the expected list!"

        return error_message

    @staticmethod
    def get_expected_ptr_bff_result_by_book_unit(api_pt_assess_by_skill_json):
        expected_ptr_result_by_book_unit = {}
        expected_ptr_result_by_book_unit['id'] = api_pt_assess_by_skill_json['PTKey']
        expected_ptr_result_by_book_unit['name'] = api_pt_assess_by_skill_json['UnitName']
        expected_ptr_result_by_book_unit['bookName'] = api_pt_assess_by_skill_json['BookName']
        expected_ptr_result_by_book_unit['ptKey'] = api_pt_assess_by_skill_json['PTKey']
        expected_ptr_result_by_book_unit['ptInstanceKey'] = api_pt_assess_by_skill_json['PTInstanceKey']
        expected_ptr_result_by_book_unit['__typename'] = 'Test'


        if api_pt_assess_by_skill_json['PTTestBy'] == 0:
            test_type = 'paper'
        elif api_pt_assess_by_skill_json['PTTestBy'] == 1:
            test_type = 'digital'
        else :
            test_type = 'web'

        expected_ptr_result_by_book_unit['type'] = test_type

        invalid = False
        if api_pt_assess_by_skill_json['PTTotalScore'] is None:
            invalid = True

        expected_ptr_result_by_book_unit['invalid'] = invalid
        expected_ptr_result_by_book_unit['score'] = api_pt_assess_by_skill_json['PTTotalScore']

        skill_score_list = api_pt_assess_by_skill_json['SkillScores']
        ptr_skills = []

        for i in range(len(skill_score_list)):
            ptr_skill = {}
            ptr_skill_type = {}
            ptr_skill_result = {}
            skill_score = skill_score_list[i]
            ptr_skill_type['id'] = skill_score['Code']
            ptr_skill_type['name'] = skill_score['Code']
            ptr_skill_result['score'] = skill_score['Score']
            ptr_skill_result['totalScore'] = skill_score['TotalScore']
            ptr_skill['type'] = ptr_skill_type
            ptr_skill['result'] = ptr_skill_result

            ptr_skills.append(ptr_skill)
        expected_ptr_result_by_book_unit['skills'] = ptr_skills
        return expected_ptr_result_by_book_unit

    # verify pt review bff result by book and unit body
    @staticmethod
    def verify_ptr_bff_graphql_by_book_unit(ptr_bff_graphql_response_json, expected_ptr_result_by_book_unit):
        actual_ptr_bff_graphql_result_by_book_unit = ptr_bff_graphql_response_json['data']['test']

        error_message = ''
        for key in actual_ptr_bff_graphql_result_by_book_unit.keys():
            actual_value = actual_ptr_bff_graphql_result_by_book_unit[key]
            expected_value = expected_ptr_result_by_book_unit[key]

            if key != 'skills':
                if key == 'score':
                    actual_value = int(actual_value)

                if str(actual_value) != str(expected_value):
                    error_message = error_message + " Key:" + key + \
                                    "'s api result not equal to expected value, the result return in API is:" \
                                    + str(actual_value) + ", but the value expected is:" \
                                    + str(expected_value) + ";"
            else:
                if len(actual_value) != len(expected_value):
                    error_message = error_message + " skills result length not as expected!"
                else:
                    for i in range(len(actual_value)):
                        actual_skill = actual_value[i]
                        expected_skill = expected_value[i]

                        for skill_key in actual_skill.keys():
                            for sub_key in actual_skill[skill_key].keys():
                                actual_value_in_skill = actual_skill[skill_key][sub_key]
                                expected_value_in_skill = expected_skill[skill_key][sub_key]
                                if 'score' in sub_key.lower():
                                    actual_value_in_skill = int(actual_value_in_skill)

                                if str(actual_value_in_skill) != str(expected_value_in_skill):
                                    error_message = error_message + " Key:" + skill_key + "[" + sub_key + "]" + \
                                                    "'s api result not equal to expected value, the result return in API is:" \
                                                    + str(actual_value_in_skill) + ", but the value expected is:" \
                                                    + str(expected_value_in_skill) + ";"
        return error_message

    # get expected pt review bff result by book body
    @staticmethod
    def get_expected_ptr_bff_result_by_book(student_id, course, book_key, book_info_dict):
        osp_service = OSPService()
        tpi_service = TPIService()
        if course == 'HF':
            course = 'highflyers'

        if book_info_dict is None and book_key is not None:
            response = osp_service.get_all_books_by_course(course)
            book_info_json = response.json()
            book_info_dict = jmespath.search("[?Key=='{0}']".format(book_key.lower()), book_info_json)[0]
        elif book_info_dict is not None and book_key is None:
            book_key = book_info_dict['Key']
        else:
            # if book_key and book_info_dict are both None, then return None, not acceptable
            return None

        default_available_course_result = tpi_service.post_enrolled_groups_with_state(student_id, course)

        api_pt_assess_by_unit_response = osp_service.post_hf_student_pt_assess_by_unit(student_id, book_key)
        api_pt_assess_by_unit_list = api_pt_assess_by_unit_response.json()

        book_name = book_info_dict['Name']
        book_code = book_info_dict['Code']

        default_available_course_info = \
            jmespath.search("[?ProductLevelCode=='{0}']".format(book_code), default_available_course_result.json())

        is_current = False
        is_active = False
        if default_available_course_info is not None and len(default_available_course_info) > 0:
            is_current = default_available_course_info[0]['IsDefaultProductLevel']
            is_active = True

        ptr_bff_test_by_unit_list = []

        for i in range(len(api_pt_assess_by_unit_list)):
            ptr_bff_test_by_unit = {}
            api_pt_assess_by_unit = api_pt_assess_by_unit_list[i]
            ptr_bff_test_by_unit['id'] = api_pt_assess_by_unit['ProgressTestKey']
            ptr_bff_test_by_unit['name'] = api_pt_assess_by_unit['UnitName']

            if api_pt_assess_by_unit['PTTestBy'] == 0:
                test_type = 'paper'
            elif api_pt_assess_by_unit['PTTestBy'] == 1:
                test_type = 'digital'
            else :
                test_type = 'web'


            invalid = True
            score = None
            if api_pt_assess_by_unit['PTTotalScore'] is not None:
                invalid = False
                score = api_pt_assess_by_unit['PTTotalScore']

            # ptr_bff_test_by_unit['invalid'] = invalid remove during PTWeb
            ptr_bff_test_by_unit['type'] = test_type
            ptr_bff_test_by_unit['score'] = score
            ptr_bff_test_by_unit['date'] = None

            ptr_bff_test_by_unit_list.append(ptr_bff_test_by_unit)

        ptr_bff_book_dict = {}
        ptr_bff_book_dict['id'] = book_key.lower()
        ptr_bff_book_dict['code'] = book_code
        ptr_bff_book_dict['title'] = book_name
        ptr_bff_book_dict['tests'] = ptr_bff_test_by_unit_list
        ptr_bff_book_dict['isCurrent'] = is_current
        ptr_bff_book_dict['isActive'] = is_active
        ptr_bff_book_cover = {}
        ptr_bff_book_cover['url'] = book_code
        ptr_bff_book_cover['alt'] = book_code
        ptr_bff_book_dict['cover'] = ptr_bff_book_cover
        ptr_bff_book_dict['__typename'] = book_name.split(" ")[0:][0]
        return ptr_bff_book_dict

    # verify pt review bff result for unit level body
    @staticmethod
    def verify_ptr_bff_graphql_by_book(actual_ptr_bff_graphql_result_by_book, expected_ptr_result_by_book):
        # actual_ptr_bff_graphql_result_by_book = ptr_bff_graphql_response_json['data']['book']

        error_message = ''
        for key in actual_ptr_bff_graphql_result_by_book.keys():
            actual_value = actual_ptr_bff_graphql_result_by_book[key]
            expected_value = expected_ptr_result_by_book[key]

            if key != 'tests' and key != 'cover':
                if str(actual_value) != str(expected_value):
                    error_message = error_message + " Key:" + key + \
                                    "'s api result not equal to expected value, the result return in API is:" \
                                    + str(actual_value) + ", but the value expected is:" \
                                    + str(expected_value) + ";"
            elif key == 'cover':
                for sub_key in actual_value.keys():
                    actual_cover_value = actual_value[sub_key]
                    expected_cover_value = expected_value[sub_key]

                    if str(actual_cover_value) != str(expected_cover_value):
                        error_message = error_message + " Key in cover:" + key + \
                                        "'s api result not equal to expected value, the result return in API is:" \
                                        + str(actual_cover_value) + ", but the value expected is:" \
                                        + str(expected_cover_value) + ";"

            else:
                # for tests field verification
                if len(actual_value) != len(expected_value):
                    error_message = error_message + " unit result length not as expected!"
                else:
                    for i in range(len(actual_value)):
                        actual_unit = actual_value[i]
                        expected_unit = expected_value[i]

                        for unit_dict_key in actual_unit.keys():
                            if unit_dict_key not in ['ptKey','status','__typename','ptInstanceKey']:
                                actual_tests_unit_value = actual_unit[unit_dict_key]
                                expected_tests_unit_value = expected_unit[unit_dict_key]

                                if unit_dict_key == 'score' and actual_tests_unit_value is not None:
                                    actual_tests_unit_value = int(actual_tests_unit_value)

                                if str(actual_tests_unit_value) != str(expected_tests_unit_value):
                                    error_message = error_message + " Key in tests result:" + unit_dict_key + \
                                                    "'s api result not equal to expected value, the result return in API is:" \
                                                    + str(actual_tests_unit_value) + ", but the value expected is:" \
                                                    + str(expected_tests_unit_value) + ";"
        return error_message

    # get expected pt review bff result by studentid body, for all courses
    @staticmethod
    def get_expected_ptr_bff_result_all_course(student_id, course):
        osp_service = OSPService()
        if course == 'HF':
            course = 'highflyers'

        response = osp_service.get_all_books_by_course(course)
        book_info_json = response.json()

        expected_ptr_bff_graphql_result = {}
        expected_ptr_bff_all_books_list = []
        for i in range(len(book_info_json)):
            book_info_dict = book_info_json[i]
            expected_ptr_bff_book_result = \
                PTReviewUtils.get_expected_ptr_bff_result_by_book(student_id, course, None, book_info_dict)
            expected_ptr_bff_all_books_list.append(expected_ptr_bff_book_result)

        expected_ptr_bff_graphql_result['id'] = student_id
        expected_ptr_bff_graphql_result['books'] = expected_ptr_bff_all_books_list
        return expected_ptr_bff_graphql_result

    @staticmethod
    def verify_ptr_bff_graphql_all_course(ptr_bff_graphql_response_json, expected_ptr_bff_graphql_result):
        actual_ptr_bff_result = ptr_bff_graphql_response_json['data']['viewer']

        error_message = ''
        if str(actual_ptr_bff_result['id']) != str(expected_ptr_bff_graphql_result['id']):
            error_message = error_message + " id's value not as expected!"

        actual_ptr_bff_result_books = actual_ptr_bff_result['books']
        expected_ptr_bff_result_books = expected_ptr_bff_graphql_result['books']

        if len(actual_ptr_bff_result_books) != len(expected_ptr_bff_result_books):
            error_message = error_message + " books' value length not as expected!"
        else:
            for i in range(len(actual_ptr_bff_result_books)):
                actual_ptr_bff_result_by_book = actual_ptr_bff_result_books[i]
                expected_ptr_bff_result_by_book = expected_ptr_bff_result_books[i]
                error_message = error_message + \
                                PTReviewUtils.verify_ptr_bff_graphql_by_book(actual_ptr_bff_result_by_book,
                                                                             expected_ptr_bff_result_by_book)
        return error_message

    @staticmethod
    def construct_expected_pt_web_create_entity(pt_key,student_id):
        expected_pt_web_entity = {}
        expected_pt_web_entity['TeacherId'] = ''.join(random.sample(string.digits, 4))
        expected_pt_web_entity['ProgressTestKey'] = pt_key
        expected_pt_web_entity['GroupId'] = ''.join(random.sample(string.digits, 4))
        expected_pt_web_entity['StudentIdCollection'] = student_id
        expected_pt_web_entity['SchoolCode'] = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        return expected_pt_web_entity

    @staticmethod
    def get_pt_instance_key_from_db(pt_key):
        ms_sql_server = MSSQLHelper(DATABASE, 'OnlineSchoolPlatform')
        return ms_sql_server.exec_query(PtWebSQLString.get_pt_instance_key_sql.format(pt_key))

    @staticmethod
    def set_pt_paper_version_from_db(pt_key,student_id):
        skills =['Speaking-PUNCTUATION','Writing-PUNCTUATION','listening','vocabulary','grammar','reading']
        try:
            ms_sql_server = MSSQLHelper(DATABASE, 'OnlineSchoolPlatform')
            pt_num = ms_sql_server.exec_query(PtWebSQLString.get_pt_instance_key_sql.format(pt_key))
            test_metadata_key = ms_sql_server.exec_query(PtWebSQLString.get_pt_metadata_key_sql.format(pt_key,student_id))
            if len(pt_num) is 0:
                if len(test_metadata_key) is not 0:
                    ms_sql_server.exec_non_query(PtWebSQLString.delete_pt_paper_version_sql.format(pt_key,student_id))
                for skill in skills:
                        ms_sql_server.exec_non_query(PtWebSQLString.insert_pt_paper_version_sql.format(student_id,pt_key,skill))
        except Exception as e:
            print(e)

    @staticmethod
    def set_student_pt_state_to_inital_value(student_id,pt_instance_key):
        try:
            ms_sql_server = MSSQLHelper(DATABASE, 'OnlineSchoolPlatform')
            update_result = ms_sql_server.exec_non_query(PtWebSQLString.reset_student_pt_state_sql.format(student_id,pt_instance_key))
            print("reset student progress test status:",update_result)
        except Exception as e:
            print(e)

    @staticmethod
    def get_student_pt_state(student_id, pt_instance_key):
        try:
            ms_sql_server = MSSQLHelper(DATABASE, 'OnlineSchoolPlatform')
            progress_test_state = ms_sql_server.exec_query(
                PtWebSQLString.get_student_pt_state_sql.format(student_id, pt_instance_key))
            print("reset student progress test status:", progress_test_state)
            return progress_test_state
        except Exception as e:
            print(e)