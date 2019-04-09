import os


class Environment(object):
    QA = "http://e1svc-qa.ef.cn"
    STAGING = "https://e1svc-staging.ef.cn"
    LIVE = "https://e1svc.ef.cn"
    STAGING_SG = "https://e1svc-staging.ef.com"
    LIVE_SG = "https://e1svc.ef.com"


try:
    print(os.environ['environment'])
except:
    os.environ['environment'] = 'LIVE'


if os.environ['environment'] == 'QA':
    ENVIRONMENT = Environment.QA
    env_key = 'QA'
    DATABASE = {
        "Server": "10.163.24.105,1433",
        "User": "SchoolUser",
        "Password": "#Bugsfor$!"
    }


elif os.environ['environment'] == 'STG':
    ENVIRONMENT = Environment.STAGING
    env_key = 'Staging'
    DATABASE = {
        "Server": "",
        "User": "",
        "Password": ""
    }

elif os.environ['environment'] == 'STG_SG':
    ENVIRONMENT = Environment.STAGING_SG
    env_key = 'Staging_SG'
    DATABASE = {
        "Server": "",
        "User": "",
        "Password": ""
    }


elif os.environ['environment'] == 'LIVE':
    ENVIRONMENT = Environment.LIVE
    env_key = 'Live'
    DATABASE = {
        "Server": "",
        "User": "",
        "Password": ""
    }

elif os.environ['environment'] == 'LIVE_SG':
    ENVIRONMENT = Environment.LIVE_SG
    env_key = 'Live_SG'
    DATABASE = {
        "Server": "",
        "User": "",
        "Password": ""
    }
