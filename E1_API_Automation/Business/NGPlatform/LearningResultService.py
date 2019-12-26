from E1_API_Automation.Lib.Moutai import Moutai
from E1_API_Automation.Business.NGPlatform.NGPlatformUtils.LearningResultUtils import LearningResultUtils


class LearningResultService:
    def __init__(self, host):
        self.host = host
        # headers = {"Content-Type": "application/json",
        #            "X-EF-ACCESS": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJhY2Nlc3MtdG9rZW4iLCJhcHBfaWQiOiI2MDEyNDc0Ny0wZDg3LTQ0ZDItOWI0Yy0zODMzN2NlZDZiNmYiLCJhcHBfbmFtZSI6InBsYXRmb3JtLXBsYW4tc3ZjIiwidHlwZSI6InNlcnZpY2UiLCJyb2xlcyI6bnVsbCwiYWNscyI6bnVsbCwiaWF0IjoxNTYzMjEzNDY4LCJleHAiOjQ3MTg4ODcwNjh9.mh17_pPXb1NQwK3Et3Z-vomdtps3Hao4FNb7d0qTfWfAunPbhqYIkJvKNJF2icEs98DOLwj0nsJcQUkwjH1SvAa6bnmg9DWD63aCzTS7VvzUpPjlIOMMpwPWca9uuZrij8p8kU-BXEn_o0w20_OzAO_AGMfCEMgBAHEekZhNW6-mauj7oOAMLcYnpaO_7tJjbFIyWs2uxSG2cF9Wza_TMb3jINY0Wl3DRVv2nkCVSnoQ2zS1bNhgJ5A9oV1Mtzsr7Uv235qH_ij-mkCpe2bJ6u4d3ey-_1dHmJmcUdU0cIFsGddvrA6UtKoyaDBXkcZcFdzc1TYrIhiSJ7iKOFKOuw"}
        self.mou_tai = Moutai(host=self.host)

    def post_learning_result_insert(self, learning_result):
        learning_result_insert_dict = LearningResultUtils.construct_learning_result_dict(learning_result)
        return self.mou_tai.post("/api/v1/results/", learning_result_insert_dict)

    def get_partition_result_without_limit(self, learning_result):
        api_url = '/api/v1/results/{0}/{1}'.format(learning_result.product, learning_result.student_key)
        return self.mou_tai.get(api_url)

    def get_partition_result_with_limit(self, learning_result, limit):
        if limit is None:
            limit = ''
        api_url = '/api/v1/results/{0}/{1}?limit={2}'.format(learning_result.product,
                                                             learning_result.student_key, limit)
        return self.mou_tai.get(api_url)

    def get_user_result_without_limit(self, learning_result):
        api_url = '/api/v1/results/{0}/{1}?productmodule={2}'.format(learning_result.product,
                                                                       learning_result.student_key,
                                                                       learning_result.product_module)
        return self.mou_tai.get(api_url)

    def get_user_result_with_limit(self, learning_result, limit):
        if limit is None:
            limit = ''

        api_url = '/api/v1/results/{0}/{1}?productmodule={2}&limit={3}'.format(learning_result.product,
                                                                                 learning_result.student_key,
                                                                                 learning_result.product_module,
                                                                                 limit)
        return self.mou_tai.get(api_url)

    def get_specific_result(self, learning_result):
        api_url = '/api/v1/results/{0}/{1}?productmodule={2}&businesskey={3}'.format(learning_result.product,
                                                                                         learning_result.student_key,
                                                                                         learning_result.product_module,
                                                                                         learning_result.business_key)
        return self.mou_tai.get(api_url)
