import E1_API_Automation.Settings
import requests
import E1_API_Automation.Lib.Utils
import jmespath

class EducationRegion:
    Shanghai = '61AEF09D-AFA0-4FC2-96AD-93C72D390653'
    Beijing = '8EF7CCD2-8C58-4BC6-8A35-B3FCAE4D0F0D'
    Shenzhen = '568CD462-C9D5-48FD-84E8-FE07CAE65EBC'
    Chongqing = 'A1460327-3FEB-4B3B-BC86-DFABA078663F'
    Foshan = '3120FADB-9800-4394-B272-9F658F7CEA55'
    Guangzhou = '163B7979-6413-4194-892D-51726D8EFDE5'
    Fuzhou = '22777B07-1296-4F5A-81FA-D14100EF2FE4'

class ShanghaiGradeKey:
    Gth2 = ['2th', '593f86f2-1e21-48bb-ac12-0d1dfba071c8']
    Gth3 = ['3th', 'e8fee4e0-c180-4e07-b37a-cf91d12df2b4']
    Gth4 = ['4th', '0d05b8bc-62f5-422a-a196-719fe8ab4483']
    Gth5 = ['5th', '9459e5bb-1449-4432-b4b6-84c964959b24']
    Gth6 = ['6th', '7e1025c7-8ea5-4942-ab6b-249d01cb844f']
    Gth7 = ['7th', 'a668a326-a716-4fa5-a2f6-7b1c54712766']
    Gth8 = ['8th', '5da62ca5-f332-419e-b3db-111da15635bd']
    Gth9 = ['9th', '3d5b9a07-f9f5-4ad5-b5a9-e4d383220fed']
    Gth10 = ['10th', '0f9f5634-d6f4-4428-ab02-7bb81f3c289a']
    Gth11 = ['11th', '5760982d-77bc-42d4-8998-0c072e30a9e6']
    Gth12 = ['12th', 'd3a5cd6d-b791-476c-b77c-6c8aa9c85c52']


class ResetGPGradeTool:
    if E1_API_Automation.Settings.env_key == 'QA':
        search_url = 'http://10.163.28.151//User/UserSource/QA?rand=0.14291181323741897&PageId=0'
        reset_url = 'http://10.163.28.151/User/SaveStudentProfile?userKey=%s&rand=0.17256526783407744&PageId=0'
    else:
        search_url = 'http://10.163.28.151//User/UserSource/STAGING?rand=0.14291181323741897&PageId=0'
        reset_url = 'http://10.163.28.151/User/SaveStudentProfile/STAGING-CN?userKey=%s&rand=0.17256526783407744&PageId=0'
    tool_url = 'http://10.163.28.151'
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
        target_value = ShanghaiGradeKey.Gth3[1]
        if current_grade == ShanghaiGradeKey.Gth3[0]:
            target_value = ShanghaiGradeKey.Gth4[1]
        data_info = {
            'Birthday': '12/27/2003 4:00:00 PM',
            'EducationGradeKey': target_value,
            'EducationRegionKey': EducationRegion.Shanghai,
            'StartPointGradeKey': target_value
        }
        s = requests.session()
        data = s.post(url=url, data=data_info, cookies=self.cookie).content.decode('utf-8')