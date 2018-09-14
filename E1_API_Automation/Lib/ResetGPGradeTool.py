import requests

import E1_API_Automation.Lib.Utils
import E1_API_Automation.Settings
from ..Test_Data.GPData import EducationRegion, ShanghaiGradeKey


class ResetGPGradeTool:
    if E1_API_Automation.Settings.env_key == 'QA':
        search_url = 'http://internal-e1pss-qa.ef.com//User/UserSource/QA?rand=0.14291181323741897&PageId=0'
        reset_url = 'http://internal-e1pss-qa.ef.com/User/SaveStudentProfile?userKey=%s&rand=0.17256526783407744&PageId=0'
        tool_url = 'http://internal-e1pss-qa.ef.com'
    elif E1_API_Automation.Settings.env_key == 'Staging':
            search_url = 'http://internal-e1pss-qa.ef.com/User/UserSource/STAGING?rand=0.14291181323741897&PageId=0'
            reset_url = 'http://internal-e1pss-qa.ef.com/User/SaveStudentProfile/STAGING-CN?userKey=%s&rand=0.17256526783407744&PageId=0'
            tool_url = 'http://internal-e1pss-qa.ef.com'
    elif E1_API_Automation.Settings.env_key == 'Live':
            search_url = 'https://pssportal.ef.cn/User/UserSource/PROD?rand=0.9001314632136694&PageId=0'
            reset_url = 'https://pssportal.ef.cn/User/SaveStudentProfile/PROD-CN?userKey=%s&rand=0.36498686749677756&PageId=0'
            tool_url = 'https://pssportal.ef.cn'

    login_user = ("qa.testauto@ef.com", "test@456")

    def __init__(self):

        self.cookie = self.login(self.login_user[0], self.login_user[1])

    def login(self, username, password):
        user_data = {
            "UserName": username,
            "Password": password
        }
        session = requests.session()
        r = session.post(self.tool_url, user_data)
        if r.status_code == 200:
            cookie = requests.utils.dict_from_cookiejar(session.cookies)
            return cookie
        return None

    def get_user_key(self, student_id):
        search_url = self.search_url
        s = requests.session()
        data_info = {
            "PageIndex": 1,
            "PageSize": 10,
            "OrderBy": '',
            "SortCol": 0,
            "Where[StudentId]": student_id
        }
        data = s.post(url=search_url, data=data_info, cookies=self.cookie).content.decode('utf-8')
        user_key = data[data.index('profile') + 9:data.index('profile') + 45]
        user_current_grade = E1_API_Automation.Lib.Utils.get_html_tagvalues(data, '/table/tbody/tr/td')[2]
        print(user_current_grade)
        return user_key, user_current_grade

    def reset_grade(self, student_id):
        url = self.reset_url
        user_key, current_grade = self.get_user_key(student_id)
        url = url % user_key
        target_value = ShanghaiGradeKey.Gth4[1]
        if current_grade == ShanghaiGradeKey.Gth4[0]:
            target_value = ShanghaiGradeKey.Gth5[1]
        data_info = {
            'Birthday': '12/27/2003 4:00:00 PM',
            'EducationGradeKey': target_value,
            'EducationRegionKey': EducationRegion.city_list['Shanghai'],
            'StartPointGradeKey': target_value
        }
        s = requests.session()
        data = s.post(url=url, data=data_info, cookies=self.cookie).content.decode('utf-8')
