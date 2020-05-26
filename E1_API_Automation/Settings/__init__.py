import os


class Environment(object):
    QA = "https://e1svc-qa.ef.cn"
    STAGING = "https://e1svc-staging.ef.cn"
    LIVE = "https://e1svc.ef.cn"
    STAGING_SG = "https://e1svc-staging.ef.com"
    LIVE_SG = "https://e1svc.ef.com"

class KSDEnvironment(object):
    QA = "https://study-qa.ef.cn"
    STAGING = "https://study-staging.ef.cn"
    LIVE = "https://study.ef.cn"
    STAGING_SG = "https://study-staging.ef.com"
    LIVE_SG = "https://study.ef.com"

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
    STAGING = "https://internal-ktsvc-stg-cn.ef.com/learning-result"
    LIVE = "https://internal-ktsvc-cn.ef.com/learning-result"


class BffEnvironment(object):
    QA = "https://ktsvc-qa.ef.cn"
    STAGING = "https://ktsvc-stg.ef.cn"
    LIVE = "https://ktsvc.ef.cn"


class HomeworkEnvironment(object):
    QA = "http://internal-ktsvc-qa-cn.ef.com/practice"
    STAGING = "https://internal-ktsvc-stg-cn.ef.com/practice"
    LIVE = "https://internal-ktsvc-cn.ef.com/practice"


class CourseGroupEnvironment(object):
    QA = "http://internal-ktsvc-qa-cn.ef.com/course-group"
    STAGING = "https://internal-ktsvc-stg-cn.ef.com/course-group"
    LIVE = "https://internal-ktsvc-cn.ef.com/course-group"


class ContentMapEnvironment(object):
    QA = "http://internal-ktsvc-qa-cn.ef.com/content-map"
    STAGING = "https://internal-ktsvc-stg-cn.ef.com/content-map"
    LIVE = "https://internal-ktsvc-cn.ef.com/content-map"


class ContentRepoEnvironment(object):
    QA = "http://internal-ktsvc-qa-cn.ef.com/content-repo"
    STAGING = "https://internal-ktsvc-stg-cn.ef.com/content-repo"
    LIVE = "https://internal-ktsvc-cn.ef.com/content-repo"


class MockTestEnvironment(object):
    QA = "https://ktsvc-qa.ef.cn/mseb"
    STAGING = "https://ktsvc-stg.ef.cn/mseb"
    Live = "https://ktsvc.ef.cn/mseb"


class E1TPIEnvironment(object):
    STAGING = "https://e1tpi-staging.ef.cn"
    STAGING_SG = "https://e1tpi-staging.ef.com"
    LIVE = "https://e1tpi.ef.cn"
    LIVE_SG = "https://e1tpi.ef.com"

try:
    print(os.environ['environment'])
except:
    os.environ['environment'] = 'QA'

if os.environ['environment'] == 'QA':
    ENVIRONMENT = Environment.QA
    KSD_ENVIRONMENT = KSDEnvironment.QA
    OSP_ENVIRONMENT = OSPEnvironment.QA
    TPI_ENVIRONMENT = TPIEnvironment.QA
    AUTH_ENVIRONMENT = AuthEnvironment.QA
    OMNI_ENVIRONMENT = OMNIEnvironment.QA
    LEARNING_RESULT_ENVIRONMENT = LearningResultEnvironment.QA
    BFF_ENVIRONMENT = BffEnvironment.QA
    HOMEWORK_ENVIRONMENT = HomeworkEnvironment.QA
    COURSE_GROUP_ENVIRONMENT = CourseGroupEnvironment.QA
    CONTENT_MAP_ENVIRONMENT = ContentMapEnvironment.QA
    CONTENT_REPO_ENVIRONMENT = ContentRepoEnvironment.QA
    MOCK_TEST_ENVIRONMENT = MockTestEnvironment.QA
    env_key = 'QA'
    DATABASE = {
        "Server": "10.163.24.105,1433",
        "User": "SchoolUser",
        "Password": "#Bugsfor$!"
    }
    CASSANDRA_DATABASE = {
        "Server": "CNEDTECHSTG-CASSANDRA-2471745a408b9ef8.elb.cn-north-1.amazonaws.com.cn",
        "KeySpace": "kids_qa",
        "User": "result_app",
        "Password": "GE^&%*!yrP@$^|cLmFH"
    }
    MONGO_DATABASE = {
        "Server": "10.179.243.73:27017,10.179.243.72:27017,10.179.243.66:27017",
        "User": "svcuser",
        "Password": "Efef@123!"
    }
    MYSQL_MOCKTEST_DATABASE = {
        "Server": "cnedtechpdmysqlstg.c4qxob5ca5uq.rds.cn-north-1.amazonaws.com.cn:3306",
        "User":"edtechmysqluser",
        "Password": "edtechdbuserstg123"
    }


elif os.environ['environment'] == 'STG':
    ENVIRONMENT = Environment.STAGING
    KSD_ENVIRONMENT = KSDEnvironment.STAGING
    OSP_ENVIRONMENT = OSPEnvironment.STAGING
    TPI_ENVIRONMENT = TPIEnvironment.STAGING
    AUTH_ENVIRONMENT = AuthEnvironment.STAGING
    OMNI_ENVIRONMENT = OMNIEnvironment.STAGING
    E1TPI_ENVIRONMENT = E1TPIEnvironment.STAGING
    LEARNING_RESULT_ENVIRONMENT = LearningResultEnvironment.STAGING
    BFF_ENVIRONMENT = BffEnvironment.STAGING
    HOMEWORK_ENVIRONMENT = HomeworkEnvironment.STAGING
    COURSE_GROUP_ENVIRONMENT = CourseGroupEnvironment.STAGING
    CONTENT_MAP_ENVIRONMENT = ContentMapEnvironment.STAGING
    CONTENT_REPO_ENVIRONMENT = ContentRepoEnvironment.STAGING
    MOCK_TEST_ENVIRONMENT = MockTestEnvironment.STAGING
    env_key = 'Staging'
    DATABASE = {
        "Server": "CNE1STGDB01.e1ef.com,1434",
        "User": "TBV3",
        "Password": "#Bugsfor$"
    }
    CASSANDRA_DATABASE = {
        "Server": "CNEDTECHSTG-CASSANDRA-2471745a408b9ef8.elb.cn-north-1.amazonaws.com.cn",
        "KeySpace": "kids_stg",
        "User": "result_app",
        "Password": "GE^&%*!yrP@$^|cLmFH"
    }
    MYSQL_MOCKTEST_DATABASE = {
        "Server": "cnedtechpdmysqlstg.c4qxob5ca5uq.rds.cn-north-1.amazonaws.com.cn:3306",
        "User":"edtechmysqluser",
        "Password": "edtechdbuserstg123"
    }

elif os.environ['environment'] == 'STG_SG':
    ENVIRONMENT = Environment.STAGING_SG
    KSD_ENVIRONMENT = KSDEnvironment.STAGING_SG
    OSP_ENVIRONMENT = OSPEnvironment.STAGING_SG
    TPI_ENVIRONMENT = TPIEnvironment.STAGING_SG
    AUTH_ENVIRONMENT = AuthEnvironment.STAGING_SG
    OMNI_ENVIRONMENT = OMNIEnvironment.STAGING_SG
    E1TPI_ENVIRONMENT = E1TPIEnvironment.STAGING_SG
    env_key = 'Staging_SG'
    DATABASE = {
        "Server": "SGE1STGDB01.e1ef.com,1434",
        "User": "TBV3",
        "Password": "#Bugsfor$"
    }


elif os.environ['environment'] == 'LIVE':
    ENVIRONMENT = Environment.LIVE
    KSD_ENVIRONMENT = KSDEnvironment.LIVE
    OSP_ENVIRONMENT = OSPEnvironment.LIVE
    TPI_ENVIRONMENT = TPIEnvironment.LIVE
    AUTH_ENVIRONMENT = AuthEnvironment.LIVE
    OMNI_ENVIRONMENT = OMNIEnvironment.LIVE
    E1TPI_ENVIRONMENT = E1TPIEnvironment.LIVE
    LEARNING_RESULT_ENVIRONMENT = LearningResultEnvironment.LIVE
    BFF_ENVIRONMENT = BffEnvironment.LIVE
    HOMEWORK_ENVIRONMENT = HomeworkEnvironment.LIVE
    COURSE_GROUP_ENVIRONMENT = CourseGroupEnvironment.LIVE
    CONTENT_MAP_ENVIRONMENT = ContentMapEnvironment.LIVE
    CONTENT_REPO_ENVIRONMENT = ContentRepoEnvironment.LIVE
    env_key = 'Live'
    DATABASE = {
        "Server": "",
        "User": "",
        "Password": ""
    }

elif os.environ['environment'] == 'LIVE_SG':
    ENVIRONMENT = Environment.LIVE_SG
    KSD_ENVIRONMENT = KSDEnvironment.LIVE_SG
    OSP_ENVIRONMENT = OSPEnvironment.LIVE_SG
    TPI_ENVIRONMENT = TPIEnvironment.LIVE_SG
    AUTH_ENVIRONMENT = AuthEnvironment.LIVE_SG
    OMNI_ENVIRONMENT = OMNIEnvironment.LIVE
    E1TPI_ENVIRONMENT = E1TPIEnvironment.LIVE_SG
    env_key = 'Live_SG'
    DATABASE = {
        "Server": "",
        "User": "",
        "Password": ""
    }
