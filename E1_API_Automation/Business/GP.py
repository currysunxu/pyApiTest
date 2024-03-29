import jmespath
from hamcrest import assert_that

from E1_API_Automation.Business.BaseService import BaseService
from E1_API_Automation.Test_Data.GPData import ShanghaiGradeKey, MoscowGradeKey, EducationRegion
from ..Lib.ResetGPGradeTool import ResetGPGradeTool
from E1_API_Automation.Settings import env_key
from E1_API_Automation.Test_Data.GPData import GP_user


class GPService(BaseService):
    def __init__(self):
        super().__init__("Environment", {"X-BA-TOKEN": "Token"})

    def login(self, user_name, password):
        user_info = {
            "UserName": user_name,
            "Password": password,
            "Platform": 0
        }
        return self.mou_tai.set_request_context("post", user_info, "/api/v2/Authentication/GP/")

    def get_student_profile(self):
        return self.mou_tai.get("/api/v2/StudentProfile/")

    def get_student_profile_gp(self):
        return self.mou_tai.get("/api/v2/StudentProfile/GP")

    def sign_out(self):
        return self.mou_tai.delete(url="/api/v2/Token/")

    def post_access_token(self):
        return self.mou_tai.post("/api/v2/xAPI/AccessToken/")

    def get_local_privacy_policy(self, culture_code):
        return self.mou_tai.get(
            "/api/v2/PrivacyPolicy/StudentPrivacyPolicyAgreement/?product=7&cultureCode={}".format(culture_code))

    def get_local_language_student_report(self, culture_code):
        return self.mou_tai.get("/api/v2/StudentReport/{}".format(culture_code))

    def get_en_student_report(self):
        return self.mou_tai.get("/api/v2/StudentReport/en-US")

    def get_custom_test(self):
        return self.mou_tai.get("/api/v2/CustomTest")

    def get_module_latest(self):
        return self.mou_tai.get("/api/v2/StudentDiagnosticTest/ModuleLatest")

    def get_student_progress(self):
        return self.mou_tai.get("/api/v2/StudentProgress")

    def post_students_lesson_progress(self, module_info):
        return self.mou_tai.post("/api/v2/StudentRemediationProgress", module_info)

    def post_students_lesson_activity(self, module_info):
        return self.mou_tai.post("/api/v2/ActivityEntity/Web/", module_info)

    def get_available_grade(self, region_key, culture_code):
        return self.mou_tai.get("/api/v2/AvailableGradeList/?regionKey={0}&cultureCode={1}".format(region_key,
                                                                                                   culture_code))

    def post_quiz_start(self, lesson_key):
        return self.mou_tai.post("/api/v2/RemediationLesson/Start/", lesson_key)

    def post_quiz_save(self, submit_answer):
        return self.mou_tai.post("/api/v2/RemediationLesson/Save/", submit_answer)

    def put_dt_start(self):
        return self.mou_tai.put("/api/v2/StudentDiagnosticTest/Start/")

    def put_dt_save(self, submit_answer):
        return self.mou_tai.put("/api/v2/StudentDiagnosticTest/Save/", submit_answer)

    def get_region_and_grade(self, market_region=1, culture_code='zh-CN'):
        return self.mou_tai.get(
            "/api/v2/RegionAndGrade/?marketRegion={0}&cultureCode={1}".format(market_region, culture_code))

    def put_custom_test_start(self, module_list):
        return self.mou_tai.put("/api/v2/CustomTest/Start/", module_list)

    def put_custom_test_save(self, test_answer):
        return self.mou_tai.put("/api/v2/CustomTest/Save/", test_answer)

    def put_student_profile_save(self, submit_data):
        return self.mou_tai.put("/api/v2/StudentProfile/Save/", submit_data)

    def setup_student_profile(self, grade_level='1st', culture_code='en-US'):
        student_id, grade_city, region_grade = self.find_student_region_grade()
        # student_id = jmespath.search('UserId', self.get_student_profile_gp().json())
        grade_key = jmespath.search("[?Name=='{0}'].Key".format(grade_level), region_grade)[0]
        self.reset_grade(student_id, grade_city, region_grade)

        submit_data = {"Birthday": "2003-12-30T16:00:00.340Z",
                       "EducationRegionKey": grade_city,
                       "EducationGradeKey": grade_key,
                       "CultureCode": culture_code,
                       "StartPointGradeKey": grade_key,
                       "PreferLanguageCode": culture_code}

        profile_save = self.put_student_profile_save(submit_data)
        assert_that(profile_save.status_code == 204)

    def get_new_recommend_module(self):
        student_progress = self.get_student_progress().json()
        new_module_list = jmespath.search("DiagnosticTestProgress.NextDiagnosticTest.New",
                                          student_progress)
        return new_module_list

    def get_custom_test_answer(self, module_list):

        question_list = self.put_custom_test_start(module_list[:4]).json()
        ct_key = jmespath.search('CustomTestKey', question_list)
        submit_data = {}
        module_activity_answers = []
        submit_data['CustomTestKey'] = ct_key
        for module in jmespath.search('Modules', question_list):
            module_key = jmespath.search('ModuleKey', module)
            for activity in jmespath.search('Activitys', module):
                activity_type = jmespath.search('Type', activity)
                activity_key = jmespath.search('Key', activity)
                for question in jmespath.search('Questions', activity):
                    question_key = jmespath.search('Key', question)
                    submit_question = self.set_submit_question(question_key)
                    submit_question['Score'] = 0
                    module_activity_answer = self.set_module_activity_answer(activity_key, activity_type, module_key,
                                                                             submit_question)
                    module_activity_answers.append(module_activity_answer)

        submit_data['StudentModuleActivityAnswer'] = module_activity_answers

        return submit_data

    def find_student_region_grade(self):
        student_profie = self.get_student_profile_gp().json()
        student_id = jmespath.search('UserId', self.get_student_profile_gp().json())
        student_market_region = jmespath.search('MarketRegion', self.get_student_profile_gp().json())
        region_json = self.get_region_and_grade(student_market_region, 'en-US').json()

        # get student's region first city key
        grade_city = jmespath.search("[:1].Region.Key", region_json)[0]

        # get student's region first city grade info
        region_grade = jmespath.search("[:1].Grades[].Grade", region_json)
        return (student_id, grade_city, region_grade)

    def get_dt_submit_answer(self, failed_module_number, first_time=True):

        student_id, grade_city, region_grade = self.find_student_region_grade()

        if first_time:
            self.reset_grade(student_id, grade_city, region_grade)

        question_list = self.put_dt_start().json()
        response_code = self.put_dt_start()
        if response_code.status_code == 200:
            dt_key = jmespath.search('DiagnosticTestKey', question_list)
            failed_module_list, module_activity_answers = [], []
            submit_data = {'DiagnosticTestKey': dt_key, 'Studentid': student_id}

            for index, module in enumerate(jmespath.search('Modules', question_list)):
                module_key = jmespath.search('ModuleKey', module)
                for activity in jmespath.search('Activitys', module):
                    activity_type = jmespath.search('Type', activity)
                    activity_key = jmespath.search('Key', activity)
                    for question in jmespath.search('Questions', activity):
                        question_key = jmespath.search('Key', question)
                        submit_question = self.set_submit_question(question_key)
                        if index + 1 > failed_module_number:
                            submit_question['Score'] = 1
                        else:
                            submit_question['Score'] = 0
                            failed_module_list.append(module_key)

                        module_activity_answer = self.set_module_activity_answer(activity_key, activity_type,
                                                                                 module_key,
                                                                                 submit_question)
                        module_activity_answers.append(module_activity_answer)

            submit_data['StudentModuleActivityAnswer'] = module_activity_answers
            failed_module = list(set(failed_module_list))
            return submit_data, failed_module, response_code.status_code
        else:
            return response_code.status_code

    def set_submit_question(self, question_key):
        submit_question = {}
        submit_question['Attempts'] = None
        submit_question['Detail'] = {"modelData": None}
        submit_question['Duration'] = None
        submit_question['key'] = None
        submit_question['LocalEndStamp'] = None
        submit_question['LocalStartStamp'] = None
        submit_question['QuestionKey'] = question_key
        submit_question['Star'] = None
        submit_question['TotalScore'] = 1
        submit_question['TotalStar'] = None
        return submit_question

    def set_module_activity_answer(self, activity_key, activity_type, module_key, submit_question):
        module_activity_answer = {}
        module_activity_answer['QuestionAnswer'] = submit_question
        module_activity_answer['ActivityKey'] = activity_key
        module_activity_answer['ModuleKey'] = module_key
        module_activity_answer['TemplateType'] = activity_type
        return module_activity_answer

    def reset_grade(self, student_id, grade_city, region_grade):
        reset_dt = ResetGPGradeTool()
        reset_dt.reset_grade(student_id, grade_city, region_grade)

    def save_all_module_quiz_answer(self):
        student_progress = self.get_student_progress().json()
        module_key = jmespath.search("DiagnosticTestProgress.NextDiagnosticTest.NeedToBeVerified", student_progress)
        for single_module_key in module_key:
            self.save_submit_quiz_answer(single_module_key)

    def save_lower_grade_quiz_answer(self):
        student_progress = self.get_student_progress().json()
        module_key = jmespath.search("RemediationProgress.LessThanSelectedGradeModules[].ModuleKey", student_progress)
        if module_key is not None:
            self.save_submit_quiz_answer(module_key[0], False)

    def get_quiz_start_info(self):
        student_progress = self.get_student_progress().json()
        print(student_progress)
        module_key = jmespath.search("RemediationProgress.Recommended[0].ModuleKey", student_progress)
        lesson_key = jmespath.search("RemediationProgress.Recommended[0].Lessons[2].LessonKey", student_progress)
        submit_data = {"ModuleKey": module_key, "LessonKey": lesson_key}
        return submit_data

    def get_lesson_activity_key(self):
        student_progress = self.get_student_progress().json()
        print(student_progress)
        activity_key = jmespath.search("RemediationProgress.Recommended[0].Lessons[0].ActivityKeys", student_progress)
        return activity_key

    def save_submit_quiz_answer(self, single_module_key, Remediation=True):
        student_id = jmespath.search('UserId', self.get_student_profile_gp().json())
        submit_data = {}
        for lesson_number in range(1, 5):
            student_progress = self.get_student_progress().json()
            if Remediation == True:
                module_json = jmespath.search(
                    "RemediationProgress.Recommended[?ModuleKey=='" + single_module_key + "']",
                    student_progress)
            else:
                module_json = jmespath.search(
                    "RemediationProgress.LessThanSelectedGradeModules[?ModuleKey=='" + single_module_key + "']",
                    student_progress)

            single_activity_list, single_lesson_key = self.get_lesson_key_and_single_activity_list(lesson_number,
                                                                                                   module_json)
            question_key_list = self.post_students_lesson_activity(single_activity_list).json()
            submit_json = {"ModuleKey": single_module_key, "LessonKey": single_lesson_key}
            remediation_key = self.set_remediation_key(submit_json)
            submit_data['StudentRemediationKey'] = remediation_key
            submit_data['StudentId'] = student_id

            student_module_lesson_answers = []
            for activity in single_activity_list:
                activity_type = jmespath.search("Activities[?Key=='" + activity + "'].Type", question_key_list)[0]

                question_key, question_list = self.get_question_key_and_list(activity, question_key_list)
                questions = [x for x in question_list if x in question_key]

                for question in questions:
                    question_answer = self.set_question_answer(question)
                    student_module_lesson_answer = self.set_student_module_lesson_answer(activity,
                                                                                         activity_type,
                                                                                         single_module_key,
                                                                                         question_answer,
                                                                                         single_lesson_key)
                    student_module_lesson_answers.append(student_module_lesson_answer)
            submit_data['StudentModuleLessonAnswer'] = student_module_lesson_answers

            self.post_quiz_save(submit_data)

    def set_remediation_key(self, submit_json):
        remediation_key = self.post_quiz_start(submit_json).json()
        return remediation_key

    def get_lesson_key_and_single_activity_list(self, lesson_number, module_json):
        single_lesson_key = jmespath.search(
            "[].Lessons[?Sequence==`" + str(lesson_number) + "`].LessonKey[]",
            module_json)[0]
        single_activity_list = jmespath.search(
            "[].Lessons[?Sequence==`" + str(lesson_number) + "`].ActivityKeys[][]",
            module_json)
        return single_activity_list, single_lesson_key

    def get_question_key_and_list(self, activity, question_key_list):
        question_list = jmespath.search("Activities[?Key=='" + activity + "'].Questions[].Key",
                                        question_key_list)
        question_key = jmespath.search("Activities[?Body.tags.ActivitySubType=='Review'].Questions[].Key",
                                       question_key_list)
        return question_key, question_list

    def set_student_module_lesson_answer(self, activity, activity_type, single_module_key, question_answer,
                                         single_lesson_key):
        student_module_lesson_answer = {}
        student_module_lesson_answer['QuestionAnswer'] = question_answer
        student_module_lesson_answer['ActivityKey'] = activity
        student_module_lesson_answer['ModuleKey'] = single_module_key
        student_module_lesson_answer['LessonKey'] = single_lesson_key
        student_module_lesson_answer['TemplateType'] = activity_type
        return student_module_lesson_answer

    def set_question_answer(self, question):
        question_answer = {}
        question_answer['Attempts'] = None
        question_answer['Detail'] = {"modelData": None}
        question_answer['Duration'] = None
        question_answer['key'] = None
        question_answer['LocalEndStamp'] = None
        question_answer['LocalStartStamp'] = None
        question_answer['QuestionKey'] = question
        question_answer['Score'] = 1
        question_answer['Star'] = None
        question_answer['TotalScore'] = 1
        question_answer['TotalStar'] = None
        return question_answer

    def finish_first_dt(self, failed_module_number, first_time=True):
        submit_json = self.get_dt_submit_answer(failed_module_number, first_time)
        response = self.put_dt_save(submit_json[0])
        assert_that(response.status_code == 204)
        if failed_module_number != 0:
            self.save_all_module_quiz_answer()

    def finish_not_first_dt(self, failed_module_number, first_time=False, loop=1):
        for times in range(loop):
            submit_json = self.get_dt_submit_answer(failed_module_number, first_time)
            response = self.put_dt_save(submit_json[0])
            assert_that(response.status_code == 204)
            if failed_module_number != 0 and loop % 2 == 0:
                self.save_all_module_quiz_answer()

    def get_mapping(self, culture_code):
        all_module_info = self.get_all_module_info(culture_code)
        grade_ids = jmespath.search("[*].GradeOrdinal", all_module_info)
        mapping = []
        for grade_id in grade_ids:
            module_key_list = jmespath.search("[?GradeOrdinal==`" + str(grade_id) + "`].Modules[].Key",
                                              all_module_info)
            for module_key in module_key_list:
                difficulty_level = jmespath.search("[*].Modules[?Key=='" + module_key + "'].DifficultyLevel[]",
                                                   all_module_info)
                list = (grade_id, difficulty_level[0], module_key,)
                mapping.append(list)

        return mapping

    def search_mapping(self, search_value, expected_output, mapping):
        result = []
        for single_mapping in mapping:
            if search_value in (single_mapping[0], single_mapping[1], single_mapping[2]):
                if expected_output == 'key':
                    return single_mapping[2]
                elif expected_output == 'grade_id':
                    return single_mapping[0]
                elif expected_output == 'level':
                    return single_mapping[1]
                elif expected_output == 'levelWithGrade':
                    result.append(single_mapping[1])
                continue

            else:
                continue

        if expected_output == 'levelWithGrade':
            return result

    def search_module_key_by_gradeid(self, lists, module_info):
        if type(lists) == int:
            module_key_list = jmespath.search("[?GradeOrdinal==`" + str(lists) + "`].Modules[].Key", module_info)
            return module_key_list
        if type(lists) == list:
            all_first_module_keys = []
            for grade_id in lists:
                module_key_list = jmespath.search("[?GradeOrdinal==`" + str(grade_id) + "`].Modules[].Key", module_info)
                all_first_module_keys = all_first_module_keys + module_key_list

            return all_first_module_keys

    def get_mapping_result_set(self, lists, expected_output, mapping):
        results = []
        for search_value in lists:
            result = self.search_mapping(search_value, expected_output, mapping)
            if isinstance(result, list):
                results = results + result
            else:
                results.append(result)
        if expected_output == 'key':
            return results
        else:
            results_list = list(set(results))
            return results_list

    def get_all_module_info(self, culture_code):

        # get student's region and grade key from student's profile info
        student_id, grade_city, region_grade = self.find_student_region_grade()

        all_module_info = self.get_available_grade(grade_city, culture_code).json()
        return all_module_info

    def get_new_recommended_module(self, culture_code, failed_module_number):
        student_progress = self.get_student_progress().json()
        latest_dt_modules = jmespath.search("DiagnosticTestProgress.UserDiagnosticTestScoreSummary[*].ModuleKey",
                                            student_progress)
        mapping = self.get_mapping(culture_code)
        all_module_info = self.get_all_module_info(culture_code)
        dt_included_grade = self.get_mapping_result_set(latest_dt_modules, 'grade_id', mapping)

        dt_included_grade_key = self.search_module_key_by_gradeid(dt_included_grade, all_module_info)
        new_list = [x for x in dt_included_grade_key if x not in latest_dt_modules]

        if len(new_list) < (5 - failed_module_number):
            if failed_module_number < 3:
                return self.get_higher_grade_module(all_module_info, dt_included_grade, failed_module_number, mapping,
                                                    new_list)

            else:
                return self.get_lower_grade_module(all_module_info, dt_included_grade, failed_module_number, mapping,
                                                   new_list)
        if len(new_list) >= (5 - failed_module_number):
            return self.get_same_grade_modules(failed_module_number, mapping, new_list, dt_included_grade)

    def get_same_grade_modules(self, failed_module_number, mapping, new_list, dt_included_grade):
        new_list_diff_level = self.get_mapping_result_set(new_list, 'level', mapping)
        grades = self.get_mapping_result_set(new_list, 'grade_id', mapping)
        start_grade = [x for x in dt_included_grade if x not in grades]

        culture_code = GP_user.GPDTUsers[env_key]['culture_code']

        # if it's for ru-RU, when grade is middle grade testing, that is grade 6,
        # the module will cross grade 5, 6 and 7, need to have specific logic for it
        if len(grades) > 1 and len(start_grade) == 1 and culture_code == 'ru-RU':
            lower_grade = []
            higher_grade = []
            for grade_value in grades:
                if grade_value < start_grade[0]:
                    lower_grade.append(grade_value)
                else:
                    higher_grade.append(grade_value)

            '''
            when failed_module_number = 3, means the DT score equal to 40, the expected module which need to do test 
            again should be the module in grade 5;
            if the failed_module_number = 4, means the DT Score lower than 40, the expected module which need to do test
             again  should be the module in grade 5;
            when failed_module_number = 2, means the DT Score higher than 40, the expected module which need to do test 
            again should be all the left modules which haven't took test
            '''
            if failed_module_number > 2:
                lower_grade_level = self.get_mapping_result_set(lower_grade, 'levelWithGrade', mapping)
                new_list_lower_grade_diff_level = [x for x in new_list_diff_level if x in lower_grade_level]
                new_list_diff_level = new_list_lower_grade_diff_level
                new_list_diff_level.sort()
                new_list_diff_level.reverse()
            else:
                new_list_diff_level.sort()
        else:
            if grades < start_grade:
                new_list_diff_level.sort()
                new_list_diff_level.reverse()
            else:
                new_list_diff_level.sort()
        recommend_modules_level = new_list_diff_level[:(5 - failed_module_number)]
        recommend_modules = self.get_mapping_result_set(recommend_modules_level, 'key', mapping)
        return recommend_modules

    def get_lower_grade_module(self, all_module_info, dt_included_grade, failed_module_number, mapping, new_list):
        next_grade = dt_included_grade[0] - 1
        next_grade_module_key_list = self.search_module_key_by_gradeid(next_grade, all_module_info)
        if next_grade_module_key_list == []:
            return self.get_higher_grade_module(all_module_info, dt_included_grade, failed_module_number, mapping,
                                                new_list)
        else:
            next_grade_difficulty_level = self.get_mapping_result_set(next_grade_module_key_list, 'level', mapping)
            next_grade_difficulty_level.sort()
            next_grade_difficulty_level.reverse()
            next_grade_real_level = next_grade_difficulty_level[:(5 - failed_module_number - len(new_list))]
            next_grade_module_id = self.get_mapping_result_set(next_grade_real_level, 'key', mapping)
            expected_new_module_key = new_list + next_grade_module_id
            return expected_new_module_key

    def get_higher_grade_module(self, all_module_info, dt_included_grade, failed_module_number, mapping, new_list):
        next_grade = dt_included_grade[-1] + 1
        next_grade_module_key_list = self.search_module_key_by_gradeid(next_grade, all_module_info)
        if next_grade_module_key_list == []:
            if dt_included_grade[-1] == len(all_module_info):
                dt_included_grade.pop()
            return self.get_higher_grade_module(all_module_info, dt_included_grade, failed_module_number, mapping,
                                                new_list)
        else:
            next_grade_difficulty_level = self.get_mapping_result_set(next_grade_module_key_list, 'level', mapping)
            next_grade_difficulty_level.sort()
            next_grade_real_level = next_grade_difficulty_level[:(5 - failed_module_number - len(new_list))]
            next_grade_module_id = self.get_mapping_result_set(next_grade_real_level, 'key', mapping)
            expected_new_module_key = new_list + next_grade_module_id
            return expected_new_module_key

    def get_all_activity_keys(self):
        student_progress = self.get_student_progress().json()
        activity_keys = jmespath.search("RemediationProgress.LessThanSelectedGradeModules[].Lessons[].ActivityKeys[]",
                                        student_progress)
        if activity_keys is None:
            activity_keys = jmespath.search(
                "RemediationProgress.RemediationModulesResult[].Lessons[].ActivityKeys[]", student_progress)
        activity_keys = list(set(activity_keys))
        return activity_keys

    def get_and_verify_video_resource(self, activity_keys):
        api_response = self.post_students_lesson_activity(activity_keys)
        video_resource_ids = jmespath.search("Resources[?Mime=='video/mp4'].ResourceId", api_response.json())
        video_resource_ids = list(set(video_resource_ids))
        expected_datas = [
            {
                "Width": 640,
                "Height": 360
            },
            {
                "Width": 856,
                "Height": 480
            },
            {
                "Width": 1280,
                "Height": 720
            },
            {
                "Width": 1920,
                "Height": 1080
            }
        ]
        for video_resource_id in video_resource_ids:
            video_resource_items = jmespath.search("Resources[?ResourceId=='" + video_resource_id + "']",
                                                   api_response.json())
            assert_that(len(video_resource_items) >= 4,
                        "video resource must have more then 4 records in the api response")

            # for each resource, check if each resource will have four type width*height,
            # and length and duration should more than 0
            for expected_data in expected_datas:
                filter_str = "@[?(Width == `{0}` && Height == `{1}` && Quality == '{2}' && Length > `0` && Duration > `0`)]" \
                    .format(expected_data['Width'], expected_data['Height'],
                            str(expected_data['Width']) + 'x' + str(expected_data['Height']))
                resource_item = jmespath.search(filter_str, video_resource_items)
                assert_that(resource_item is not None)
