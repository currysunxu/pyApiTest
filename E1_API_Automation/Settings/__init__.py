import os


class Environment(object):
    QA = "https://e1svc-qa.ef.cn"
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


class TPIEnvironment(object):
    QA = "http://internal-e1tpi-qa.ef.com"
    STAGING = "http://internal-tpi-staging-cn.ef.com"
    STAGING_SG = "http://internal-tpi-staging.ef.com"
    LIVE = "http://internal-tpi-cn.ef.com"
    LIVE_SG = "http://internal-tpi.ef.com"


class AuthEnvironment(object):
    QA = "https://auth-svc-qa.ef.cn"
    STAGING = "https://auth-svc-stg.ef.cn"
    STAGING_SG = "https://auth-svc-stg.ef.com"
    LIVE = "https://auth-svc.ef.cn"
    LIVE_SG = "https://auth-svc.ef.com"


class OMNIEnvironment(object):
    QA = "http://internal-ktsvc-qa-cn.ef.com/omni/apigateway"
    STAGING = "http://omni-apigateway-staging-tccn.ef.com"
    STAGING_SG = "http://omni-apigateway-tcjp.ef.com"
    LIVE = "http://omni-apigateway-tccn.ef.com"


class LearningResultEnvironment(object):
    QA = "http://internal-ktsvc-qa-cn.ef.com/learning-result"


class BffEnvironment(object):
    QA = "https://ktsvc-qa.ef.cn"


class HomeworkEnvironment(object):
    QA = "http://internal-ktsvc-qa-cn.ef.com/homework"


class ContentMapEnvironment(object):
    QA = "http://internal-ktsvc-qa-cn.ef.com/content-map"


class ContentRepoEnvironment(object):
    QA = "http://internal-ktsvc-qa-cn.ef.com/content-repo"


class KidsEVCEnvironment(object):
    QA = "https://study-qa.ef.cn"


class MockTestEnvironment(object):
    QA = "https://ktsvc-qa.ef.cn/mseb"

try:
    print(os.environ['environment'])
except:
    os.environ['environment'] = 'QA'


if os.environ['environment'] == 'QA':
    ENVIRONMENT = Environment.QA
    OSP_ENVIRONMENT = OSPEnvironment.QA
    TPI_ENVIRONMENT = TPIEnvironment.QA
    AUTH_ENVIRONMENT = AuthEnvironment.QA
    OMNI_ENVIRONMENT = OMNIEnvironment.QA
    LEARNING_RESULT_ENVIRONMENT = LearningResultEnvironment.QA
    BFF_ENVIRONMENT = BffEnvironment.QA
    HOMEWORK_ENVIRONMENT = HomeworkEnvironment.QA
    CONTENT_MAP_ENVIRONMENT = ContentMapEnvironment.QA
    CONTENT_REPO_ENVIRONMENT = ContentRepoEnvironment.QA
    KIDS_EVC_ENVIRONMENT = KidsEVCEnvironment.QA
    MOCK_TEST_ENVIRONMENT = MockTestEnvironment.QA
    env_key = 'QA'
    DATABASE = {
        "Server": "10.163.24.105,1433",
        "User": "SchoolUser",
        "Password": "#Bugsfor$!"
    }
    CASSANDRA_DATABASE = {
        "Server": "10.178.86.216",
        "User": "cassandra",
        "Password": "cassandra"
    }
    MONGO_DATABASE = {
        "Server": "10.179.243.73:27017,10.179.243.72:27017,10.179.243.66:27017",
        "User": "svcuser",
        "Password": "Efef@123!"
    }


elif os.environ['environment'] == 'STG':
    ENVIRONMENT = Environment.STAGING
    OSP_ENVIRONMENT = OSPEnvironment.STAGING
    TPI_ENVIRONMENT = TPIEnvironment.STAGING
    AUTH_ENVIRONMENT = AuthEnvironment.STAGING
    OMNI_ENVIRONMENT = OMNIEnvironment.STAGING
    env_key = 'Staging'
    DATABASE = {
        "Server": "CNE1STGDB01.e1ef.com,1434",
        "User": "TBV3",
        "Password": "#Bugsfor$"
    }

elif os.environ['environment'] == 'STG_SG':
    ENVIRONMENT = Environment.STAGING_SG
    OSP_ENVIRONMENT = OSPEnvironment.STAGING_SG
    TPI_ENVIRONMENT = TPIEnvironment.STAGING_SG
    AUTH_ENVIRONMENT = AuthEnvironment.STAGING_SG
    OMNI_ENVIRONMENT = OMNIEnvironment.STAGING_SG
    env_key = 'Staging_SG'
    DATABASE = {
        "Server": "SGE1STGDB01.e1ef.com,1434",
        "User": "TBV3",
        "Password": "#Bugsfor$"
    }


elif os.environ['environment'] == 'LIVE':
    ENVIRONMENT = Environment.LIVE
    OSP_ENVIRONMENT = OSPEnvironment.LIVE
    TPI_ENVIRONMENT = TPIEnvironment.LIVE
    AUTH_ENVIRONMENT = AuthEnvironment.LIVE
    OMNI_ENVIRONMENT = OMNIEnvironment.LIVE
    env_key = 'Live'
    DATABASE = {
        "Server": "",
        "User": "",
        "Password": ""
    }

elif os.environ['environment'] == 'LIVE_SG':
    ENVIRONMENT = Environment.LIVE_SG
    OSP_ENVIRONMENT = OSPEnvironment.LIVE_SG
    TPI_ENVIRONMENT = TPIEnvironment.LIVE_SG
    AUTH_ENVIRONMENT = AuthEnvironment.LIVE_SG
    OMNI_ENVIRONMENT = OMNIEnvironment.LIVE
    env_key = 'Live_SG'
    DATABASE = {
        "Server": "",
        "User": "",
        "Password": ""
    }
