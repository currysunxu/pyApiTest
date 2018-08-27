class Environment(object):
    QA = "http://e1svc-qa.ef.cn"
    STAGING = "https://e1svc-staging.ef.cn"

ENVIRONMENT = Environment.STAGING

if ENVIRONMENT == Environment.QA:
    SIS_SERVICE = 'https://internal-e1-evc-booking-qa-cn.ef.com'
    env_key = 'QA'
elif ENVIRONMENT == Environment.STAGING:
    env_key ='Staging'
    SIS_SERVICE = 'http://internal-e1-evc-booking-stg-cn.ef.com'