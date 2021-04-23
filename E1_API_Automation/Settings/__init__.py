import os
import yaml
from E1_API_Automation.Settings.parseyaml import read_yaml_file

yaml_cfg = yaml.load(read_yaml_file("E1_API_Automation/Settings/config.yaml"))


def key_to_env(key):
    envs = {
        "QA": "QA",
        "STG": "Staging",
        "STG_SG": "Staging_SG",
        "LIVE": "Live",
        "LIVE_DR": "Live",
        "LIVE_SG": "Live_SG"
    }
    return envs.get(key, None)


try:
    print(os.environ['environment'])
except Exception as e:
    os.environ['environment'] = yaml_cfg.get('Local')['LOCAL_ENV']

env_key = key_to_env(os.environ['environment'])


def get_current_env(specific_env):
    env = ''
    try:
        env = yaml_cfg.get(specific_env)[str.upper(env_key)]
    except Exception as e:
        print("{0} do not define in {1} env, just skip it, please double check if it's necessary".format(specific_env,
                                                                                                         env_key))
    finally:
        return env


ENVIRONMENT = get_current_env('Environment')
KSD_ENVIRONMENT = get_current_env('KSDEnvironment')
OSP_ENVIRONMENT = get_current_env('OSPEnvironment')
TPI_ENVIRONMENT = get_current_env('TPIEnvironment')
AUTH_ENVIRONMENT = get_current_env('AuthEnvironment')
OMNI_ENVIRONMENT = get_current_env('OMNIEnvironment')
LEARNING_RESULT_ENVIRONMENT = get_current_env('LearningResultEnvironment')
LEARNING_PROFILE_ENVIRONMENT = get_current_env('LearningProfileEnvironment')
BFF_ENVIRONMENT = get_current_env('BffEnvironment')
HOMEWORK_ENVIRONMENT = get_current_env('HomeworkEnvironment')
COURSE_GROUP_ENVIRONMENT = get_current_env('CourseGroupEnvironment')
E1TPI_ENVIRONMENT = get_current_env('E1TPIEnvironment')
CONTENT_MAP_ENVIRONMENT = get_current_env('ContentMapEnvironment')
STUDY_TIME_ENVIRONMENT = get_current_env('StudyPlanEnvironment')
CONTENT_REPO_ENVIRONMENT = get_current_env('ContentRepoEnvironment')
CONTENT_BUILDER_ENVIRONMENT = get_current_env('ContentBuilderEnvironment')
MOCK_TEST_ENVIRONMENT = get_current_env('MockTestEnvironment')
STORYBLOK_RELEASE_ENVIRONMENT = get_current_env('StoryblokReleaseEnvironment')
STORYBLOK_IMPORT_ENVIRONMENT = get_current_env('StoryblokImportEnvironment')
AUTH2_ENVIRONMENT = get_current_env('Auth2Environment')
REMEDIATION_ENVIRONMENT = get_current_env('RemediationEnvironment')
VOCAB_ENVIRONMENT = get_current_env('VocabEnvironment')
EVC_CONTENT_ENVIRONMENT = get_current_env('EVCContentEnvironment')
EVC_CDN_ENVIRONMENT = get_current_env('EVCCDNEnvironment')
EVC_DEMO_PAGE_ENVIRONMENT = get_current_env('EVCDemoPageEnvironment')
EVC_PROXY_ENVIRONMENT = get_current_env('EVCProxyEnvironment')
DATABASE = get_current_env('DATABASE')
CASSANDRA_DATABASE = get_current_env('CASSANDRA_DATABASE')
MONGO_DATABASE = get_current_env('MONGO_DATABASE')
MYSQL_MOCKTEST_DATABASE = get_current_env('MYSQL_MOCKTEST_DATABASE')
