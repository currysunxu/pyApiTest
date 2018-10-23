import jmespath
from ptest.assertion import assert_that
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
                "DeviceId": "9F4B30E5-9289-4C1A-B40F-81EDD3435079",
                "DeviceType": 2
            }

        return self.mou_tai.set_request_context("post", user_info, "/api/v2/Authentication/Staff/")


    def get_web_socket_url(self):
        return self.mou_tai.get('/api/v2/ProgressTestWebSocket/CND')

    def get_books_info(self):
        return self.mou_tai.get('/api/v2/ProgressTestBooks/1')

    def post_content_info(self,book_key_list):
        data={"BookKeys":book_key_list,"ProductCode" : "PT"}
        return self.mou_tai.post('/api/v2/ProgressTestContent/Product', data)

    def get_book_key_list(self):
        book_info=self.get_books_info()
        book_key_list=jmespath.search("[].Key",book_info.json())
        return book_key_list


    def query_school_info(self,region_key):
        data={"Region" : region_key}

        return self.mou_tai.post('/api/v2/SchoolInfo/',data)

    def get_course_schedule(self,teacher_id):
        data={
              "Day" : 2,
              "TeacherId" : teacher_id,
              "Year" : 2018,
              "SchoolCode" : "CND",
              "Month" : 10
            }
        return self.mou_tai.post('/api/v2/CourseSchedule/', data)

    def get_root_course_info(self,key):
        data={"RootCourseKey": key}
        return self.mou_tai.post('/api/v2/ProgressTest/',data)

    def post_courseNode_sync(self,book_key):
        data={
              "BookKey" : book_key,
              "ProductCode" : "PT",
              "UpsertsOnly" : 0
            }
        return self.mou_tai.post('/api/v2/CourseNode/Synchronize', data)

    def post_activity_sync(self,book_key):
        data={
              "BookKey" : book_key,
              "ProductCode" : "PT",
              "UpsertsOnly" : 1
            }
        return self.mou_tai.post('/api/v2/Activity/Synchronize', data)

    def post_binary_data_sync(self,book_key):
        data={
              "BookKey" : book_key,
              "ProductCode" : "PT",
              "UpsertsOnly" : 1
            }
        return self.mou_tai.post('/api/v2/BinaryData/Synchronize', data)


    def sign_out(self):
        return self.mou_tai.delete(url="/api/v2/Token/")
