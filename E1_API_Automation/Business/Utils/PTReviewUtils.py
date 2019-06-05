from E1_API_Automation.Business.PTSkillScore import PTSkillScore, SkillCode, SubSkillCode
from ...Test_Data.PTReviewData import PTReviewData
from ...Settings import env_key
from hamcrest import assert_that
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

    @staticmethod
    def verify_pt_score_with_api_response(skill_dic, assess_metas_response):
        # verify if the data get from the StudentPaperDigitalProgressTestAssessmentMetas API are as what you constructed
        for key in skill_dic.keys():
            pt_skill_score = skill_dic[key]
            if key not in (SkillCode.Speaking, SkillCode.Writing):
                PTReviewUtils.verify_pt_score(key.value, pt_skill_score, assess_metas_response)

            else:
                if isinstance(pt_skill_score, list):
                    for sub_skill in pt_skill_score:
                        code = key.value + '-' + sub_skill.skillCode.value
                        PTReviewUtils.verify_pt_score(code, sub_skill, assess_metas_response)
                else:
                    PTReviewUtils.verify_pt_score(key.value, pt_skill_score, assess_metas_response)

    @staticmethod
    def verify_pt_score(skill_code, pt_skill_score, assess_metas_response):
        unit_key = PTReviewData.pt_hf_user_key_book_unit[env_key]['UnitKey']
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