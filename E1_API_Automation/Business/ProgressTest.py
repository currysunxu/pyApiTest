import jmespath

from ..Lib.Moutai import Moutai, Token


class PTService():
    def __init__(self, host):
        self.host = host
        self.mou_tai = Moutai(host=self.host, token=Token("X-BA-TOKEN", "Token"))

    def stuff_login(self, username, password):
        user_info = {
            "Platform": 1,
            "UserName": username,
            "Password": password,

        }

        return self.mou_tai.set_request_context("post", user_info, "/api/v2/Authentication/Staff/")

    def get_web_socket_url(self):
        return self.mou_tai.get('/api/v2/ProgressTestWebSocket/CND')

    def get_books_info(self, product_name):
        if product_name == "tb":
            return self.mou_tai.get('/api/v2/ProgressTestBooks/1')
        elif product_name == "ss":
            return self.mou_tai.get('/api/v2/ProgressTestBooks/SmallStar')

    def post_content_info(self, book_key_list, product_name):
        global product_code
        if product_name == "tb":
            product_code = "PT"
        elif product_name == "ss":
            product_code = "SSPT"

        data = {"BookKeys": book_key_list,
                "ProductCode": product_code
                }
        return self.mou_tai.post('/api/v2/ProgressTestContent/Product', data)

    def get_book_key_list(self, product_name):
        book_info = self.get_books_info(product_name)
        book_key_list = jmespath.search("[].Key", book_info.json())
        return book_key_list, product_name

    def query_school_info(self, region_key):
        data = {"Region": region_key}

        return self.mou_tai.post('/api/v2/SchoolInfo/', data)

    def get_course_schedule(self, teacher_id, school_code, date):
        data = {
            "Day": date[0]["day"],
            "TeacherId": teacher_id,
            "Year": date[0]["year"],
            "SchoolCode": school_code,
            "Month": date[0]["month"]
        }
        return self.mou_tai.post('/api/v2/CourseSchedule/', data)

    def get_root_course_info(self, key):
        data = {"RootCourseKey": key}
        return self.mou_tai.post('/api/v2/ProgressTest/', data)

    def post_courseNode_sync(self, book_key):
        data = {
            "BookKey": book_key
        }
        return self.mou_tai.post('/api/v2/CourseNode/Synchronize', data)

    def post_activity_sync(self, book_key):
        data = {
            "BookKey": book_key
        }
        return self.mou_tai.post('/api/v2/Activity/Synchronize', data)

    def post_binary_data_sync(self, book_key):
        data = {
            "BookKey": book_key
        }
        return self.mou_tai.post('/api/v2/BinaryData/Synchronize', data)

    def sign_out(self):
        return self.mou_tai.delete(url="/api/v2/Token/")
