import os


class Environment(object):
    QA = "http://e1svc-qa.ef.cn"
    STAGING = "https://e1svc-staging.ef.cn"
    STAGING_SG = "https://e1svc-staging.ef.com"


# os.environ['environment'] = 'STG_SG'


if os.environ['environment'] == 'QA':
    ENVIRONMENT = Environment.QA
    env_key = 'QA'

elif os.environ['environment'] == 'STG':
    ENVIRONMENT = Environment.STAGING
    env_key = 'Staging'

elif os.environ['environment'] == 'STG_SG':
    ENVIRONMENT = Environment.STAGING_SG
    env_key = 'Staging_SG'