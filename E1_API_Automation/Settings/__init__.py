import os


class Environment(object):
    QA = "http://e1svc-qa.ef.cn"
    STAGING = "https://e1svc-staging.ef.cn"


# os.environ['environment'] = 'STG'


if os.environ['environment'] == 'QA':
    ENVIRONMENT = Environment.QA
    env_key = 'QA'

elif os.environ['environment'] == 'STG':
    ENVIRONMENT = Environment.STAGING
    env_key = 'Staging'
