from E1_API_Automation.Lib.Moutai import Moutai
import jmespath


class Hf35BffService:
    def __init__(self, host):
        self.host = host
        self.mou_tai = Moutai(host=self.host, headers={"Content-Type": "application/json;charset=UTF-8"})

    def login(self, user_name, password):
        user_info = {
            "username": user_name,
            "password": password,
        }

        athentication_result = self.mou_tai.post("/auth2/api/v1/login", user_info)
        accessToken = jmespath.search('accessToken', athentication_result.json())
        self.mou_tai.headers['EF-Access-Token'] = accessToken
        return athentication_result

    def get_auth_token(self):
        token_value = self.mou_tai.headers.pop('X-EF-TOKEN')
        return token_value

    def submit_new_attempt_with_negative_auth_token(self, attempt_json, negative_token):
        self.set_negative_token(negative_token)
        attempt_result = self.mou_tai.post("/hf3/api/v1/homework/attempts", attempt_json)
        return attempt_result

    def submit_new_attempt(self, attempt_json):
        attempt_result = self.mou_tai.post("/hf3/api/v1/homework/attempts", attempt_json)
        return attempt_result

    def get_bootstrap_controller(self, platform):
        if platform:
            return self.mou_tai.get("/hf3/api/v1/bootstrap?platform={0}".format(platform))
        else:
            return self.mou_tai.get("/hf3/api/v1/bootstrap")

    def get_unlock_progress_controller(self, book_content_id):
        return self.mou_tai.get("/hf3/api/v1/unlocked-progress?bookContentId={0}".format(book_content_id))

    def get_the_best_attempt(self, book_content_id):
        api_url = '/hf3/api/v1/homework/attempts/best?bookContentId={0}'.format(book_content_id)
        return self.mou_tai.get(api_url)

    def get_course_structure(self):
        return self.mou_tai.get("/hf3/api/v1/course/structure")

    def get_course_structure_with_negative_token(self, negative_token):
        self.set_negative_token(negative_token)
        return self.mou_tai.get("/hf3/api/v1/course/structure")

    def get_book_structure(self, content_id, tree_revision):
        return self.mou_tai.get("/hf3/api/v1/books/{0}/structure?treeRevision={1}".format(content_id, tree_revision))

    def get_book_structure_with_negative_token(self, content_id, tree_revision, negative_token):
        self.set_negative_token(negative_token)
        return self.mou_tai.get("/hf3/api/v1/books/{0}/structure?treeRevision={1}".format(content_id, tree_revision))

    def get_homework_activities(self, content_body_from_content_repo):
        api_url = "/hf3/api/v1/activities"
        return self.mou_tai.post(api_url, content_body_from_content_repo)

    def get_homework_activity_asset_group(self, unit_content_revision, unit_content_id, unit_schema_version):
        api_url = "/hf3/api/v1/homework/content-groups?unitContentRevision=%s&unitContentId=%s&unitSchemaVersion=%s" \
                  % (unit_content_revision, unit_content_id, unit_schema_version)
        return self.mou_tai.get(api_url)

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
            self.mou_tai.headers['EF-Access-Token'] = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJqdGkiOiI2Y2QzMjEwMy05MDg4LTRiM2EtYmY1Ni1mZjE0ZjJhZjQ3MTUiLCJzdWIiOiIxMDAyIiwiaWF0IjoxNTgyNjE0NTYwLCJleHAiOjE1ODI2MjUzNjAsImNvcnJlbGF0aW9uX2lkIjoiY2Q5YWQ0ZjgtMjBmMy00YWUzLWE0YzEtMWZiOTBiMjEwOWY2IiwicmVmX2lkIjoiYWQ2MWRlMTQtMzUxMC00YjMxLTk1OTUtMzIyZWJmZjE1ZDMwIn0.sfl4sm7ON58rpUkxZ4g_PPMTb8bp1Vi4CIfYke8DxAfL0nNuQUR6fTfVCeHp71hf7GRPpnGIkgyhCX16aQMIMBZtVQWtYy_35EaCuKHCXoWUeAc6M7TJTp3qAW8UyvxX9Vh1aNvVPWWmWWI2OtvCKs1CLDRCOnVp9pDz2mm-3vUZ2IWeq1Di53tq1L2hp_DLQIK5LveLqHbGb9zesniHfVKVsPae-rOx2154Ffw6-YLxA_HJXlsgci5EQX4eYzlfcyH4jBj_u68IgZA8UflJ3ok_HkBXl2vWCOptEgq74O1o6N1qNBkHjLZZPIyI2CS79KENHYAoNln2lcEVkqjrtA"