import os


class Environment(object):
    QA = "http://e1svc-qa.ef.cn"
    STAGING = "https://e1svc-staging.ef.cn"
    LIVE = "https://e1svc.ef.cn"
    STAGING_SG = "https://e1svc-staging.ef.com"
    LIVE_SG = "https://e1svc.ef.com"


# os.environ['environment'] = 'QA'


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

elif os.environ['environment'] == 'STG_SG':
    ENVIRONMENT = Environment.STAGING_SG
    env_key = 'Staging_SG'


elif os.environ['environment'] == 'LIVE':
    ENVIRONMENT = Environment.LIVE
    env_key = 'Live'

elif os.environ['environment'] == 'LIVE_SG':
    ENVIRONMENT = Environment.LIVE_SG
    env_key = 'Live_SG'