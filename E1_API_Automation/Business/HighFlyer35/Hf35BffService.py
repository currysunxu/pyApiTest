from E1_API_Automation.Lib.Moutai import Moutai
import jmespath


class Hf35BffService:
    def __init__(self, host):
        self.host = host
        self.mou_tai = Moutai(host=self.host, headers={"Content-Type": "application/json;charset=UTF-8"})

    def login(self, user_name, password):
        user_info = {
            "userName": user_name,
            "password": password,
        }

        athentication_result = self.mou_tai.post("/hf3/api/v1/auth/login", user_info)
        idToken = jmespath.search('idToken', athentication_result.json())
        self.mou_tai.headers['X-EF-TOKEN'] = idToken
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

    def get_unlock_progress_controller(self):
        return self.mou_tai.get("hf3/api/v1/unlocked-progress")

    def get_the_best_attempt(self, student_id, book_content_id):
        api_url = '/hf3/api/v1/homework/attempts/best?studentId={0}&bookContentId={1}'.format(student_id,
                                                                                              book_content_id)
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

    def get_homework_activity_asset_group(self, unitContentRevision, unitContentId):
        api_url = "/hf3/api/v1/homework/content-groups?unitContentRevision=%s&unitContentId=%s" % (
        unitContentRevision, unitContentId)
        return self.mou_tai.get(api_url)

    def get_homework_activities_with_negative_token(self, inserted_content_body, negative_token):
        self.set_negative_token(negative_token)
        return self.get_homework_activities(inserted_content_body)

    def get_homework_activities_group_with_negative_token(self, unitContentRevision, unitContentId, negative_token):
        self.set_negative_token(negative_token)
        return self.get_homework_activity_asset_group(unitContentRevision, unitContentId)

    def set_negative_token(self, negative_token):
        if negative_token == "":
            self.mou_tai.headers['X-EF-TOKEN'] = ""
        elif negative_token == "noToken":
            self.mou_tai.headers.pop('X-EF-TOKEN')
        else:
            self.mou_tai.headers['X-EF-TOKEN'] = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9"
