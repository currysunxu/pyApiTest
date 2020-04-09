from E1_API_Automation.Settings import env_key


class EnvUtils:
    @staticmethod
    def is_env_live():
        return env_key.startswith('Live')

    @staticmethod
    def is_env_qa():
        return env_key == 'QA'
