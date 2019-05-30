import os


class Environment(object):
    QA = "http://e1svc-qa.ef.cn"
    STAGING = "https://e1svc-staging.ef.cn"
    LIVE = "https://e1svc.ef.cn"
    STAGING_SG = "https://e1svc-staging.ef.com"
    LIVE_SG = "https://e1svc.ef.com"


class OSPEnvironment(object):
    QA = "http://internal-e1osp-qa.ef.com"
    STAGING = "http://internal-osp-staging-cn.ef.com"
    LIVE = "http://internal-osp-cn.ef.com"
    STAGING_SG = "http://internal-osp-staging.ef.com"
    LIVE_SG = "http://internal-osp.ef.com"


try:
    print(os.environ['environment'])
except:
    os.environ['environment'] = 'LIVE'


if os.environ['environment'] == 'QA':
    ENVIRONMENT = Environment.QA
    OSP_ENVIRONMENT = OSPEnvironment.QA
    env_key = 'QA'
    DATABASE = {
        "Server": "10.163.24.105,1433",
        "User": "SchoolUser",
        "Password": "#Bugsfor$!"
    }


elif os.environ['environment'] == 'STG':
    ENVIRONMENT = Environment.STAGING
    OSP_ENVIRONMENT = OSPEnvironment.STAGING
    env_key = 'Staging'
    DATABASE = {
        "Server": "CNE1STGDB01.e1ef.com,1434",
        "User": "TBV3",
        "Password": "#Bugsfor$"
    }

elif os.environ['environment'] == 'STG_SG':
    ENVIRONMENT = Environment.STAGING_SG
    OSP_ENVIRONMENT = OSPEnvironment.STAGING_SG
    env_key = 'Staging_SG'
    DATABASE = {
        "Server": "SGE1STGDB01.e1ef.com,1434",
        "User": "TBV3",
        "Password": "#Bugsfor$"
    }


elif os.environ['environment'] == 'LIVE':
    ENVIRONMENT = Environment.LIVE
    OSP_ENVIRONMENT = OSPEnvironment.LIVE
    env_key = 'Live'
    DATABASE = {
        "Server": "",
        "User": "",
        "Password": ""
    }

elif os.environ['environment'] == 'LIVE_SG':
    ENVIRONMENT = Environment.LIVE_SG
    OSP_ENVIRONMENT = OSPEnvironment.LIVE_SG
    env_key = 'Live_SG'
    DATABASE = {
        "Server": "",
        "User": "",
        "Password": ""
    }
