from E1_API_Automation.Lib.Moutai import Moutai
from E1_API_Automation.Business.HFV35.HFV35Utils.LearningPlanUtils import LearningPlanUtils


class LearningPlanService:
    def __init__(self, host):
        self.host = host
        headers = {"Content-Type": "application/json",
                   "X-EF-ACCESS": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJhY2Nlc3MtdG9rZW4iLCJhcHBfaWQiOiI2MDEyNDc0Ny0wZDg3LTQ0ZDItOWI0Yy0zODMzN2NlZDZiNmYiLCJhcHBfbmFtZSI6InBsYXRmb3JtLXBsYW4tc3ZjIiwidHlwZSI6InNlcnZpY2UiLCJyb2xlcyI6bnVsbCwiYWNscyI6bnVsbCwiaWF0IjoxNTYzMjEzNDY4LCJleHAiOjQ3MTg4ODcwNjh9.mh17_pPXb1NQwK3Et3Z-vomdtps3Hao4FNb7d0qTfWfAunPbhqYIkJvKNJF2icEs98DOLwj0nsJcQUkwjH1SvAa6bnmg9DWD63aCzTS7VvzUpPjlIOMMpwPWca9uuZrij8p8kU-BXEn_o0w20_OzAO_AGMfCEMgBAHEekZhNW6-mauj7oOAMLcYnpaO_7tJjbFIyWs2uxSG2cF9Wza_TMb3jINY0Wl3DRVv2nkCVSnoQ2zS1bNhgJ5A9oV1Mtzsr7Uv235qH_ij-mkCpe2bJ6u4d3ey-_1dHmJmcUdU0cIFsGddvrA6UtKoyaDBXkcZcFdzc1TYrIhiSJ7iKOFKOuw"}
        self.mou_tai = Moutai(host=self.host, headers=headers)

    def post_learning_plan_insert(self, learning_plan):
        learning_plan_insert_dict = LearningPlanUtils.construct_learning_plan_dict(learning_plan)
        print(str(learning_plan_insert_dict))
        return self.mou_tai.post("/api/v1/plans/", learning_plan_insert_dict)

