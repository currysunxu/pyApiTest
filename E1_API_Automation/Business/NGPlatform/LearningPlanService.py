from E1_API_Automation.Lib.Moutai import Moutai
from E1_API_Automation.Business.NGPlatform.NGPlatformUtils.LearningPlanUtils import LearningPlanUtils


class LearningPlanService:
    def __init__(self, host):
        self.host = host
        headers = {"Content-Type": "application/json",
                   "X-EF-ACCESS": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJhY2Nlc3MtdG9rZW4iLCJhcHBfaWQiOiI2MDEyNDc0Ny0wZDg3LTQ0ZDItOWI0Yy0zODMzN2NlZDZiNmYiLCJhcHBfbmFtZSI6InBsYXRmb3JtLXBsYW4tc3ZjIiwidHlwZSI6InNlcnZpY2UiLCJyb2xlcyI6bnVsbCwiYWNscyI6bnVsbCwiaWF0IjoxNTYzMjEzNDY4LCJleHAiOjQ3MTg4ODcwNjh9.mh17_pPXb1NQwK3Et3Z-vomdtps3Hao4FNb7d0qTfWfAunPbhqYIkJvKNJF2icEs98DOLwj0nsJcQUkwjH1SvAa6bnmg9DWD63aCzTS7VvzUpPjlIOMMpwPWca9uuZrij8p8kU-BXEn_o0w20_OzAO_AGMfCEMgBAHEekZhNW6-mauj7oOAMLcYnpaO_7tJjbFIyWs2uxSG2cF9Wza_TMb3jINY0Wl3DRVv2nkCVSnoQ2zS1bNhgJ5A9oV1Mtzsr7Uv235qH_ij-mkCpe2bJ6u4d3ey-_1dHmJmcUdU0cIFsGddvrA6UtKoyaDBXkcZcFdzc1TYrIhiSJ7iKOFKOuw"}
        self.mou_tai = Moutai(host=self.host, headers=headers)

    def post_learning_plan_insert(self, learning_plan):
        learning_plan_insert_dict = LearningPlanUtils.construct_learning_plan_dict(learning_plan)
        print(str(learning_plan_insert_dict))
        api_response = self.mou_tai.post("/api/v1/plans/", learning_plan_insert_dict)
        # get the system_key for entity after insert API
        if api_response.status_code == 200:
            if api_response.json() is not None and len(api_response.json())>0:
                LearningPlanUtils.get_learning_plan_system_key(api_response.json(),
                                                               learning_plan)
        return api_response

    def post_learning_plan_batch_insert(self, learning_plan_list):
        learning_plan_batch_insert_dict = LearningPlanUtils.construct_batch_learning_plan_dict(learning_plan_list)
        print(str(learning_plan_batch_insert_dict))
        api_response = self.mou_tai.post("/api/v1/plans/batch", learning_plan_batch_insert_dict)
        # get the system_key for entity list after insert API
        if api_response.status_code == 200:
            if api_response.json() is not None and len(api_response.json())>0:
                LearningPlanUtils.get_learning_plan_system_key(api_response.json(),
                                                               learning_plan_list)

        return api_response

    def put_learning_plan(self, learning_plan):
        learning_plan_update_dict = LearningPlanUtils.construct_learning_plan_dict(learning_plan)
        print(str(learning_plan_update_dict))
        return self.mou_tai.put("/api/v1/plans/", learning_plan_update_dict)

    def get_partition_plan_without_limit_page(self, learning_plan):
        api_url = '/api/v1/plans/{0}/{1}/{2}'.format(learning_plan.product_id, learning_plan.bucket_id,
                                                     learning_plan.plan_business_key)
        return self.mou_tai.get(api_url)

    def get_partition_plan_with_limit(self, learning_plan, limit):
        if limit is None:
            limit = ''
        api_url = '/api/v1/plans/{0}/{1}/{2}?limit={3}'.format(learning_plan.product_id, learning_plan.bucket_id,
                                                               learning_plan.plan_business_key, limit)
        return self.mou_tai.get(api_url)

    def get_partition_plan_with_limit_page(self, learning_plan, limit, page):
        if limit is None:
            limit = ''
        if page is None:
            page = ''

        api_url = '/api/v1/plans/{0}/{1}/{2}?limit={3}&page={4}'.format(learning_plan.product_id,
                                                                        learning_plan.bucket_id,
                                                                        learning_plan.plan_business_key, limit, page)
        return self.mou_tai.get(api_url)

    def get_user_plan_without_limit_page(self, learning_plan):
        api_url = '/api/v1/plans/{0}/{1}/{2}?studentkey={3}'.format(learning_plan.product_id, learning_plan.bucket_id,
                                                                    learning_plan.plan_business_key,
                                                                    learning_plan.student_key)
        return self.mou_tai.get(api_url)

    def get_user_plan_with_limit(self, learning_plan, limit):
        if limit is None:
            limit = ''

        api_url = '/api/v1/plans/{0}/{1}/{2}?studentkey={3}&limit={4}'.format(learning_plan.product_id,
                                                                              learning_plan.bucket_id,
                                                                              learning_plan.plan_business_key,
                                                                              learning_plan.student_key, limit)
        return self.mou_tai.get(api_url)

    def get_user_plan_with_limit_page(self, learning_plan, limit, page):
        if limit is None:
            limit = ''
        if page is None:
            page = ''

        api_url = '/api/v1/plans/{0}/{1}/{2}?studentkey={3}&limit={4}&page={5}'.format(learning_plan.product_id,
                                                                                       learning_plan.bucket_id,
                                                                                       learning_plan.plan_business_key,
                                                                                       learning_plan.student_key,
                                                                                       limit, page)
        return self.mou_tai.get(api_url)

    def get_specific_plan(self, learning_plan):
        api_url = '/api/v1/plans/{0}/{1}/{2}?studentkey={3}&systemkey={4}'.format(learning_plan.product_id,
                                                                                  learning_plan.bucket_id,
                                                                                  learning_plan.plan_business_key,
                                                                                  learning_plan.student_key,
                                                                                  learning_plan.system_key)
        return self.mou_tai.get(api_url)

    def delete_plan_by_partition(self, learning_plan):
        api_url = '/api/v1/plans/{0}/{1}/{2}'.format(learning_plan.product_id, learning_plan.bucket_id,
                                                     learning_plan.plan_business_key)
        return self.mou_tai.delete(api_url)

    def delete_user_plan(self, learning_plan):
        api_url = '/api/v1/plans/{0}/{1}/{2}?studentkey={3}'.format(learning_plan.product_id,
                                                                    learning_plan.bucket_id,
                                                                    learning_plan.plan_business_key,
                                                                    learning_plan.student_key)
        return self.mou_tai.delete(api_url)

    def delete_specific_plan(self, learning_plan):
        api_url = '/api/v1/plans/{0}/{1}/{2}?studentkey={3}&systemkey={4}'.format(learning_plan.product_id,
                                                                                  learning_plan.bucket_id,
                                                                                  learning_plan.plan_business_key,
                                                                                  learning_plan.student_key,
                                                                                  learning_plan.system_key)
        return self.mou_tai.delete(api_url)

