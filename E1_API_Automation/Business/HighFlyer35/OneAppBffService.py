import time

import requests

from E1_API_Automation.Business.BaseService import BaseService
from E1_API_Automation.Business.HighFlyer35.HighFlyerUtils.Hf35BffUtils import Hf35BffUtils
from E1_API_Automation.Business.Utils.CommonUtils import CommonUtils

import jmespath


class OneAppBffService(BaseService):

    def login(self, user_name, password):
        user_info = {
            "username": user_name,
            "password": password
        }

        athentication_result = self.mou_tai.post("/auth2/api/v1/login", user_info)
        accessToken = jmespath.search('accessToken', athentication_result.json())
        self.access_token = accessToken
        self.mou_tai.headers['EF-Access-Token'] = accessToken
        self.id_token = jmespath.search('idToken', athentication_result.json())
        return athentication_result

    # def get_auth_token(self):
    #     token_value = self.mou_tai.headers.pop('X-EF-TOKEN')
    #     return token_value

    def submit_new_attempt_with_negative_auth_token(self, attempt_json, negative_token):
        self.set_negative_token(negative_token)
        attempt_result = self.mou_tai.post("/mega/api/v1/homework/attempts", attempt_json)
        return attempt_result

    def submit_new_attempt(self, attempt_json):
        attempt_result = self.mou_tai.post("/mega/api/v1/homework/attempts", attempt_json)
        return attempt_result

    def get_bootstrap_controller(self, platform):
        if platform:
            return self.mou_tai.get("/mega/api/v1/bootstrap?platform={0}".format(platform))
        else:
            return self.mou_tai.get("/mega/api/v1/bootstrap")

    def get_unlock_progress_controller(self, book_content_id):
        return self.mou_tai.get("/mega/api/v1/unlocked-progress?bookContentId={0}".format(book_content_id))

    def get_the_best_attempt(self, book_content_id):
        api_url = '/mega/api/v1/homework/attempts/best?bookContentId={0}'.format(book_content_id)
        return self.mou_tai.get(api_url)

    def get_course_structure(self):
        return self.mou_tai.get("/mega/api/v1/course/structure")

    def get_course_structure_with_negative_token(self, negative_token):
        self.set_negative_token(negative_token)
        return self.mou_tai.get("/mega/api/v1/course/structure")

    def get_book_structure(self, content_id, tree_revision):
        return self.mou_tai.get("/mega/api/v1/books/{0}/structure?treeRevision={1}".format(content_id, tree_revision))

    def get_book_structure_with_negative_token(self, content_id, tree_revision, negative_token):
        self.set_negative_token(negative_token)
        return self.mou_tai.get("/mega/api/v1/books/{0}/structure?treeRevision={1}".format(content_id, tree_revision))

    def get_homework_activities(self, content_body_from_content_repo):
        api_url = "/mega/api/v1/activities"
        return self.mou_tai.post(api_url, content_body_from_content_repo)

    def get_homework_activity_asset_group(self, unit_content_revision, unit_content_id, unit_schema_version):
        api_url = "/mega/api/v1/homework/content-groups?unitContentRevision=%s&unitContentId=%s&unitSchemaVersion=%s" \
                  % (unit_content_revision, unit_content_id, unit_schema_version)
        return self.mou_tai.get(api_url)

    def get_handout_content_groups(self, book_content_id, book_content_revision, book_schema_version):
        api_url = "/mega/api/v1/handout/content-groups?bookContentId=%s&bookContentRevision=%s&bookSchemaVersion=%s" \
                  % (book_content_id, book_content_revision, book_schema_version)
        return self.mou_tai.get(api_url)

    def get_vocab_content_groups(self, book_content_id, book_content_revision, book_schema_version):
        api_url = "/mega/api/v1/vocab/content-groups?unitContentId=%s&unitContentRevision=%s&unitSchemaVersion=%s" \
                  % (book_content_id, book_content_revision, book_schema_version)
        return self.mou_tai.get(api_url)

    def get_handout_ecas(self, eca_filter_body):
        api_url = "/mega/api/v1/eca"
        return self.mou_tai.post(api_url, eca_filter_body)

    def get_homework_activities_with_negative_token(self, inserted_content_body, negative_token):
        self.set_negative_token(negative_token)
        return self.get_homework_activities(inserted_content_body)

    def get_homework_activities_group_with_negative_token(self, unitContentRevision, unitContentId, negative_token):
        self.set_negative_token(negative_token)
        return self.get_homework_activity_asset_group(unitContentRevision, unitContentId, 1)

    def set_negative_token(self, negative_token):
        if negative_token == "":
            self.mou_tai.headers['EF-Access-Token'] = ""
        elif negative_token == "noToken":
            self.mou_tai.headers.pop('EF-Access-Token')
        elif negative_token == "invalid":
            self.mou_tai.headers['EF-Access-Token'] = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9"
        elif negative_token == "expired":
            # expired token
            self.mou_tai.headers[
                'EF-Access-Token'] = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJqdGkiOiI2Y2QzMjEwMy05MDg4LTRiM2EtYmY1Ni1mZjE0ZjJhZjQ3MTUiLCJzdWIiOiIxMDAyIiwiaWF0IjoxNTgyNjE0NTYwLCJleHAiOjE1ODI2MjUzNjAsImNvcnJlbGF0aW9uX2lkIjoiY2Q5YWQ0ZjgtMjBmMy00YWUzLWE0YzEtMWZiOTBiMjEwOWY2IiwicmVmX2lkIjoiYWQ2MWRlMTQtMzUxMC00YjMxLTk1OTUtMzIyZWJmZjE1ZDMwIn0.sfl4sm7ON58rpUkxZ4g_PPMTb8bp1Vi4CIfYke8DxAfL0nNuQUR6fTfVCeHp71hf7GRPpnGIkgyhCX16aQMIMBZtVQWtYy_35EaCuKHCXoWUeAc6M7TJTp3qAW8UyvxX9Vh1aNvVPWWmWWI2OtvCKs1CLDRCOnVp9pDz2mm-3vUZ2IWeq1Di53tq1L2hp_DLQIK5LveLqHbGb9zesniHfVKVsPae-rOx2154Ffw6-YLxA_HJXlsgci5EQX4eYzlfcyH4jBj_u68IgZA8UflJ3ok_HkBXl2vWCOptEgq74O1o6N1qNBkHjLZZPIyI2CS79KENHYAoNln2lcEVkqjrtA"

    def get_online_pl_class(self, scope, course_type_level_code=''):
        # get online pl class api need both X-EF-TOKEN and EF-Access-Token
        self.mou_tai.headers['X-EF-TOKEN'] = self.id_token
        api_url = "/mega/api/v1/classes/online-pl?scope={0}&courseTypeLevelCode={1}".format(scope,
                                                                                            course_type_level_code)
        return self.mou_tai.get(api_url)

    def get_online_gl_class(self):
        # get online gl class api need both X-EF-TOKEN and EF-Access-Token
        self.mou_tai.headers['X-EF-TOKEN'] = self.id_token
        api_url = "/mega/api/v1/classes/online-gl"
        return self.mou_tai.get(api_url)

    def get_privacy_policy_document(self):
        # don't need any token
        access_token = self.mou_tai.headers.pop('EF-Access-Token')
        api_url = "/mega/api/v1/privacy-policy-document"
        api_response = self.mou_tai.get(api_url)
        # set back the access token, when sign pp agreement, it needed
        self.mou_tai.headers['EF-Access-Token'] = access_token
        return api_response

    def post_privacy_policy_agreement(self, privacy_document_id):
        body = {
            "privacyDocumentId": privacy_document_id
        }
        api_url = "/mega/api/v1/privacy-policy-agreement"
        return self.mou_tai.post(api_url, body)

    def post_vocab_progress(self, word_attempt_list):
        word_attempt_insert_dict_list = Hf35BffUtils.construct_word_attempts_dict(word_attempt_list)
        return self.mou_tai.post("/mega/api/v1/vocab/attempts", word_attempt_insert_dict_list)

    def get_vocab_progress(self, book_content_id):
        api_url = '/mega/api/v1/vocab/progress?bookContentId={0}'.format(book_content_id)
        return self.mou_tai.get(api_url)

    def get_reader_content_groups(self, relevant_content_id, relevant_content_revision):
        api_url = "/mega/api/v1/reader/content-groups?relevantContentId=%s&relevantContentRevision=%s" \
                  % (relevant_content_id, relevant_content_revision)
        return self.mou_tai.get(api_url)

    def get_reader_progress(self, student_id, relevant_content_id):
        api_url = "/mega/api/v1/reader/progress?studentId=%s&relevantContentId=%s" \
                  % (student_id, relevant_content_id)
        return self.mou_tai.get(api_url)

    def get_reader_level_focused(self, student_id, dafault_reader_level_content_id):
        api_url = "/mega/api/v1/reader/levels/focused?studentId=%s&defaultReaderLevelContentId=%s" \
                  % (student_id, dafault_reader_level_content_id)
        return self.mou_tai.get(api_url)

    def post_reader_progress(self, attempt_json):
        # self.set_negative_token(negative_token)
        attempt_result = self.mou_tai.post("/mega/api/v1/reader/attempts", attempt_json)
        return attempt_result

    def get_weekly_plan(self, start_time):
        api_url = '/mega/api/v1/plans/weekly?startAt={0}'.format(start_time)
        return self.mou_tai.get(api_url)

    def get_content_path(self, content_path):
        api_url = '/mega/api/v1/plans?contentPath={0}'.format(content_path)
        return self.mou_tai.get(api_url)

    def get_rewards_by_content_path(self, content_path):
        api_url = '/mega/api/v1/rewards/earned-stamps?contentPath={0}'.format(content_path)
        return self.mou_tai.get(api_url)

    def get_media(self, media_url):
        api_url = '/media/api/v1/assets/{0}'.format(media_url)
        i = 0
        # retry three times if exception happens
        while i < 3:
            try:
                get_media_response = self.mou_tai.get(api_url, timeout=5)
                return get_media_response
            except requests.exceptions.RequestException:
                i += 1
                time.sleep(1)

    def get_bootstrap_controller_v2(self, platform):
        return self.mou_tai.get("/mega/api/v2/bootstrap?platform={0}".format(platform))

    def get_book_structure_v2(self, content_path):
        encoded_content_path = CommonUtils.encode_url_content_path(content_path)
        return self.mou_tai.get("/mega/api/v2/books/{0}/structure".format(encoded_content_path))

    def get_book_structure_v3(self, content_path):
        encoded_content_path = CommonUtils.encode_url_content_path(content_path)
        return self.mou_tai.get("/mega/api/v3/books/{0}/structure".format(encoded_content_path))

    def get_student_context(self):
        return self.mou_tai.get("/mega/api/v1/student/context")

    # hardcode reservationId and sessionId from staging env
    def post_class_online_enter(self, onlinePlatform, reservation_id, session_id):
        body = {
            "onlinePlatform": onlinePlatform,
            "reservationId": reservation_id,
            "sessionId": session_id
        }
        api_url = "/mega/api/v1/classes/online/enter"
        if onlinePlatform is "NULL_BODY":
            body = {}
        return self.mou_tai.post(api_url, body)

    def get_online_class_id(self, reservation_id):
        return self.mou_tai.get("/mega/api/v1/classes/online/{0}".format(reservation_id))

    def post_pt_deep_link_enter(self, ptKey):
        self.mou_tai.headers['x-ef-token'] = self.id_token
        body = {
            "testContentId": ptKey
        }
        api_url = "/mega/api/v1/progress-test/enter"
        return self.mou_tai.post(api_url, body)

    def post_mt_enter(self):
        body = {}
        api_url = "/mega/api/v1/mock-test/enter"
        return self.mou_tai.post(api_url, body)

    def get_remediation_by_pt_key_and_instance_key(self, pt_instance_key, pt_key):
        api_url = "/mega/api/v1/remediation/content-groups?testInstanceId={0}&testId={1}".format(pt_instance_key,
                                                                                                 pt_key)
        return self.mou_tai.get(api_url)

    def post_best_remediation_attempts(self, attempts):
        api_url = "/mega/api/v1/remediation/attempts"
        return self.mou_tai.post(api_url, attempts)

    def get_best_remediation_attempts(self, pt_instance_key):
        api_url = "/mega/api/v1/remediation/attempts/best?testInstanceId={0}".format(pt_instance_key)
        return self.mou_tai.get(api_url)

    def get_flashcard_content_group(self, book_content_id, book_content_revision, schema_version):
        api_url = "/mega/api/v1/flashcard/content-groups?bookContentId={0}&bookContentRevision={1}&bookSchemaVersion={2}".format(
            book_content_id, book_content_revision, schema_version)
        return self.mou_tai.get(api_url)

    def get_ss_unit_quiz_content_group(self, test_id):
        api_url = "/mega/api/v1/unit-quiz/content-groups/{0}".format(test_id)
        return self.mou_tai.get(api_url)

    def post_ss_submit_unit_quiz_attempts(self, attempts):
        api_url = "/mega/api/v1/unit-quiz/attempts"
        return self.mou_tai.post(api_url, attempts)

    def get_ss_unit_quiz_attempts_details(self, test_id):
        api_url = "/mega/api/v1/unit-quiz/attempts/{0}".format(test_id)
        return self.mou_tai.get(api_url)