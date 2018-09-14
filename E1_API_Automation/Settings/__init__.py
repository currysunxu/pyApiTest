import os


class Environment(object):
    QA = "http://e1svc-qa.ef.cn"
    STAGING = "https://e1svc-staging.ef.cn"
    LIVE = "https://e1svc.ef.cn"


# os.environ['environment'] = 'LIVE'


if os.environ['environment'] == 'QA':
    ENVIRONMENT = Environment.QA
    env_key = 'QA'

elif os.environ['environment'] == 'STG':
    ENVIRONMENT = Environment.STAGING
    env_key = 'Staging'

elif os.environ['environment'] == 'LIVE':
    ENVIRONMENT = Environment.LIVE
    env_key = 'Live'
