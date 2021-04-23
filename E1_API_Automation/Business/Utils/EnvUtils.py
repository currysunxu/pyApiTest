from E1_API_Automation.Settings import env_key


class EnvUtils:
    @staticmethod
    def is_env_live() -> bool:
        return env_key == 'Live'

    @staticmethod
    def is_env_live_sg() -> bool:
        return env_key == 'Live_SG'

    @staticmethod
    def is_env_qa() -> bool:
        return env_key == 'QA'

    @staticmethod
    def is_env_stg() -> bool:
        return env_key == 'Staging'

    @staticmethod
    def is_env_stg_sg() -> bool:
        return env_key == 'Staging_SG'
