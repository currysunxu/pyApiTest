import jmespath
import requests
import xlrd

from E1_API_Automation.Lib.Moutai import Moutai, Token


class UnlockService():
    def __init__(self, host):
        self.host = host
        self.mou_tai = Moutai(host=self.host, token=Token("X-BA-TOKEN", "Token"))

    def sslogin(self, user_name, password):
        user_info = {
            "UserName": user_name,
            "Password": password,
            "DeviceId": "",
            "DeviceType": "",
            "Platform": 0
        }
        return self.mou_tai.set_request_context("post", user_info, "/api/v2/Authentication/SS/")

    def tblogin(self, user_name, password):
        user_info = {
            "UserName": user_name,
            "Password": password,
            "DeviceId": "",
            "DeviceType": "",
            "Platform": 0
        }
        return self.mou_tai.set_request_context("post", user_info, "/api/v2/Authentication/TBV3/")


def read_excel_key(file, sheet_id, col_id):
    keys = []
    ExcelFile = xlrd.open_workbook(file)
    sheet = ExcelFile.sheet_by_index(sheet_id)
    accounts_list = sheet.col_values(col_id)
    for accounts in accounts_list:
        keys.append(accounts)

    return keys


def ss_unlock_service(student_id, keys, env):
    urlcn = 'http://internal-tpi-staging.ef.cn/api/v2/SmallStarUnlock/'
    urlsg = 'http://internal-tpi-staging.ef.cn/api/v2/SmallStarUnlock/'
    header = {'Content-Type': 'application/json', "X-BA-TOKEN": "97096cec-091a-486a-9cef-4c1097a33a46"}
    data = {"StudentIdCollection": student_id,
            "CourseKeys": keys
            }
    if env == 'cn':
        return requests.put(urlcn, json=data, verify=False, headers=header)
    elif env == 'sg':
        return requests.put(urlsg, json=data, verify=False, headers=header)


def tb_unlock_service(student_id, keys, env):
    urlcn = 'http://internal-tpi-staging-cn.ef.cn/api/v2/TrailblazerUnlock/'
    urlsg = 'http://internal-tpi-staging-cn.ef.cn/api/v2/TrailblazerUnlock/'
    header = {'Content-Type': 'application/json', "X-BA-TOKEN": "97096cec-091a-486a-9cef-4c1097a33a46"}
    data = {"StudentIdCollection": student_id,
            "CourseKeys": keys
            }
    if env == 'cn':
        return requests.put(urlcn, json=data, verify=False, headers=header)
    elif env == 'sg':
        return requests.put(urlsg, json=data, verify=False, headers=header)


def unlock_service_by_read_excel_or_by_specific_key_list(product_name, env, username, password, keys, sheet_number=0,
                                                         col_num=2):
    student_id_list = []
    service = UnlockService('https://e1svc-staging.ef.cn')
    if product_name == 'ss3':
        student_id = service.sslogin(username, password).json()  # replace student id which you'd like to unlock
        single_ss3_student_id = jmespath.search("UserInfo.UserId",
                                                student_id)
        student_id_list.append(single_ss3_student_id)

        try:
            keys = read_excel_key(keys, sheet_number, col_num)

        except:
            keys = keys
        ss_unlock_service(student_id_list, keys, env)

    elif product_name == 'tb3':
        student_id = service.tblogin(username, password).json()  # replace student id which you'd like to unlock
        single_tb_student_id = jmespath.search("UserInfo.UserId",
                                               student_id)
        student_id_list.append(single_tb_student_id)
        try:
            keys = read_excel_key(keys, sheet_number, col_num)

        except:
            keys = keys
        tb_unlock_service(student_id_list, keys, env)


if __name__ == '__main__':
    product_name = 'ss3'  # ss3, tb3
    env = 'cn'  # cn , sg
    username = 'ss3.cn.02'
    password = '12345'
    # KEY=r'C:\Users\robinyonghao.wang\Desktop\studentTestAccounts.xlsx'
    KEY = ['080BF3B5-24D0-E811-814A-02BC62143FC0']
    unlock_service_by_read_excel_or_by_specific_key_list(product_name, env, username, password, KEY, sheet_number=0,
                                                         col_num=2)

    """
    
    :param product name : ss3 or tb3 
    :param env : cn or sg
    :param username : account username
    :param password : account password
    :param key : Two method to pass the keys to API
                    1. By excel, add excel file address in you PC, comment second line of KEY.
                    2. By specific keys list: It's a list, you can add mutiple keys in the list and comment first line of KEY.
    :param Sheet number: The sheet number in excel, default is first sheet.
    :param Column number: Column number which keys list in the sheet, default value is third column.

    """
