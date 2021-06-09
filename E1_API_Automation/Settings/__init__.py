import os
import yaml
from E1_API_Automation.Settings.parseyaml import read_yaml_file

current_path = os.path.dirname(__file__)
yaml_cfg = yaml.full_load(read_yaml_file(current_path))


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


EVC_DEMO_PAGE_ENVIRONMENT = get_current_env('EVCDemoPageEnvironment')
EVC_ENVIRONMENT = get_current_env('EVCEnvironment')
EVC_CONTENT_ENVIRONMENT = get_current_env('EVCContentEnvironment')
DATABASE = get_current_env('DATABASE')
CASSANDRA_DATABASE = get_current_env('CASSANDRA_DATABASE')
MONGO_DATABASE = get_current_env('MONGO_DATABASE')
MYSQL_MOCKTEST_DATABASE = get_current_env('MYSQL_MOCKTEST_DATABASE')
