import os


class Environment(object):
    QA = "https://e1svc-qa.bj-englishtown.com"
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
    QA = "https://internal-osp-qa.english1.cn"
    STAGING = "https://internal-osp-stg.english1.cn"
    LIVE = "https://internal-osp.english1.cn"
    STAGING_SG = "https://internal-osp-stg.english1.com"
    LIVE_SG = "http://internal-osp.english1.com"


class TPIEnvironment(object):
    QA = "https://internal-tpi-qa.english1.cn"
    STAGING = "https://internal-tpi-stg.english1.cn"
    STAGING_SG = "https://internal-tpi-stg.english1.com"
    LIVE = "https://internal-tpi.english1.cn"
    LIVE_SG = "https://internal-tpi.english1.com"


class AuthEnvironment(object):
    QA = "https://auth-svc-qa.bj-englishtown.com"
    STAGING = "https://auth-svc-stg.ef.cn"
    STAGING_SG = "https://auth-svc-stg.ef.com"
    LIVE = "https://auth-svc.ef.cn"
    LIVE_SG = "https://auth-svc.ef.com"


class OMNIEnvironment(object):
    QA = "https://internal-ktsvc-qa.english1.cn/omni/apigateway"
    STAGING = "https://omni-apigateway-tc-staging.ef.cn"
    STAGING_SG = "http://omni-apigateway-staging-tcjp.ef.com"
    LIVE = "https://omni-apigateway-tc.ef.cn"
    LIVE_SG = "http://omni-apigateway-tcjp.ef.com"


class LearningResultEnvironment(object):
    QA = "https://internal-ktsvc-qa.english1.cn/learning-result"
    STAGING = "https://internal-ktsvc-stg.english1.cn/learning-result"
    LIVE = "https://internal-ktsvc.english1.cn/learning-result"


class BffEnvironment(object):
    QA = "https://ktsvc-qa.bj-englishtown.com"
    STAGING = "https://ktsvc-stg.ef.cn"
    LIVE = "https://ktsvc.ef.cn"


class HomeworkEnvironment(object):
    QA = "https://internal-ktsvc-qa.english1.cn/practice"
    STAGING = "https://internal-ktsvc-stg.english1.cn/practice"
    LIVE = "https://internal-ktsvc.english1.cn/practice"


class CourseGroupEnvironment(object):
    QA = "https://internal-ktsvc-qa.english1.cn/course-group"
    STAGING = "https://internal-ktsvc-stg.english1.cn/course-group"
    LIVE = "https://internal-ktsvc.english1.cn/course-group"


class ContentMapEnvironment(object):
    QA = "https://internal-ktsvc-qa.english1.cn/content-map"
    STAGING = "https://internal-ktsvc-stg.english1.cn/content-map"
    LIVE = "https://internal-ktsvc.english1.cn/content-map"


class ContentRepoEnvironment(object):
    QA = "https://internal-ktsvc-qa.english1.cn/content-repo"
    STAGING = "https://internal-ktsvc-stg.english1.cn/content-repo"
    LIVE = "https://internal-ktsvc.english1.cn/content-repo"


class ContentBuilderEnvironment(object):
    QA = "https://internal-ktsvc-qa.english1.cn/content-builder"
    STAGING = "https://internal-ktsvc-stg.english1.cn/content-builder"
    LIVE = "https://internal-ktsvc.english1.cn/content-builder"


class MockTestEnvironment(object):
    QA = "https://ktsvc-qa.bj-englishtown.com/mseb"
    STAGING = "https://ktsvc-stg.ef.cn/mseb"
    LIVE = "https://ktsvc.ef.cn/mseb"


class StoryblokReleaseEnvironment(object):
    QA = "https://internal-ktsvc-qa.english1.cn/storyblok-release"
    STAGING = "https://internal-ktsvc-stg.english1.cn/storyblok-release"
    LIVE = "https://internal-ktsvc.english1.cn/storyblok-release"


class StoryblokImportEnvironment(object):
    QA = "https://internal-ktsvc-qa.english1.cn/storyblok-import"
    LIVE = "https://internal-ktsvc.english1.cn/storyblok-import"


class E1TPIEnvironment(object):
    STAGING = "https://e1tpi-staging.ef.cn"
    STAGING_SG = "https://e1tpi-staging.ef.com"
    LIVE = "https://e1tpi.ef.cn"
    LIVE_SG = "https://e1tpi.ef.com"


class StudyPlanEnvironment(object):
    QA = "https://internal-ktsvc-qa.english1.cn/study-plan"
    STAGING = "https://internal-ktsvc-stg.english1.cn/study-plan"
    LIVE = "https://internal-ktsvc-english1.cn/study-plan"


class LearningProfileEnvironment(object):
    STAGING = "https://e1-evc-booking-integration-stg.ef.com"
    LIVE = "https://e1-evc-booking-integration.ef.com"


class EVCContentEnvironment(object):
    STAGING = "https://evc-content-staging.bj-englishtown.com"
    LIVE = "https://evc-content.bj-englishtown.com"


class EVCCDNEnvironment(object):
    STAGING = "https://evc-fe-staging.bj-englishtown.com"
    LIVE = "https://evc-fe.bj-englishtown.com"


class EVCDemoPageEnvironment(object):
    STAGING = "https://evc-ts-staging.ef.com.cn"
    LIVE = "https://evc-ts.ef.com.cn/"


class EVCProxyEnvironment:
    STAGING = {
        "CN": "evc-ts-staging.ef.com.cn",
        "US": "evc-tv-to-ts-staging.ef.com",
        "UK": "evc-tf-to-ts-staging.ef.com",
        "SG": "evc-tsg-to-ts-staging.ef.com"
    }

    LIVE = {
        "CN": "evc-ts.ef.com.cn",
        "US": "evc-tv-to-ts.ef.com",
        "UK": "evc-tf-to-ts.ef.com",
        "SG": "evc-tsg-to-ts.ef.com"
    }

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
    STUDY_TIME_ENVIRONMENT = StudyPlanEnvironment.QA
    CONTENT_REPO_ENVIRONMENT = ContentRepoEnvironment.QA
    CONTENT_BUILDER_ENVIRONMENT = ContentBuilderEnvironment.QA
    MOCK_TEST_ENVIRONMENT = MockTestEnvironment.QA
    STORYBLOK_RELEASE_ENVIRONMENT = StoryblokReleaseEnvironment.QA
    STORYBLOK_IMPORT_ENVIRONMENT = StoryblokImportEnvironment.QA
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
        "User": "edtechmysqluser",
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
    STUDY_TIME_ENVIRONMENT = StudyPlanEnvironment.STAGING
    CONTENT_REPO_ENVIRONMENT = ContentRepoEnvironment.STAGING
    CONTENT_BUILDER_ENVIRONMENT = ContentBuilderEnvironment.STAGING
    MOCK_TEST_ENVIRONMENT = MockTestEnvironment.STAGING
    STORYBLOK_RELEASE_ENVIRONMENT = StoryblokReleaseEnvironment.STAGING
    LEARNING_PROFILE_ENVIRONMENT = LearningProfileEnvironment.STAGING
    EVC_CONTENT_ENVIRONMENT = EVCContentEnvironment.STAGING
    EVC_CDN_ENVIRONMENT = EVCCDNEnvironment.STAGING
    EVC_DEMO_PAGE_ENVIRONMENT = EVCDemoPageEnvironment.STAGING
    EVC_PROXY_ENVIRONMENT = EVCProxyEnvironment.STAGING
    env_key = 'Staging'
    DATABASE = {
        "Server": "10.163.24.124,1434",
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
        "User": "edtechmysqluser",
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
    STUDY_TIME_ENVIRONMENT = StudyPlanEnvironment.LIVE
    CONTENT_REPO_ENVIRONMENT = ContentRepoEnvironment.LIVE
    CONTENT_BUILDER_ENVIRONMENT = ContentBuilderEnvironment.LIVE
    MOCK_TEST_ENVIRONMENT = MockTestEnvironment.LIVE
    STORYBLOK_RELEASE_ENVIRONMENT = StoryblokReleaseEnvironment.LIVE
    STORYBLOK_IMPORT_ENVIRONMENT = StoryblokImportEnvironment.LIVE
    LEARNING_PROFILE_ENVIRONMENT = LearningProfileEnvironment.LIVE
    EVC_CONTENT_ENVIRONMENT = EVCContentEnvironment.LIVE
    EVC_CDN_ENVIRONMENT = EVCCDNEnvironment.LIVE
    EVC_DEMO_PAGE_ENVIRONMENT = EVCDemoPageEnvironment.LIVE
    EVC_PROXY_ENVIRONMENT = EVCProxyEnvironment.LIVE
    env_key = 'Live'
    DATABASE = {
        "Server": "",
        "User": "",
        "Password": ""
    }
    MYSQL_MOCKTEST_DATABASE = {
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
