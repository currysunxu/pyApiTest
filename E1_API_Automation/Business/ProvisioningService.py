from E1_API_Automation.Business.BaseService import BaseService


class ProvisioningService(BaseService):
    def __init__(self, host):
        super().__init__(host, {"X-BA-Token": "4255FB70-184A-4a92-9FAC-7DA63316AB64"})

    def get_app_version_by_platform_key(self, platform_key):
        return self.mou_tai.get('/api/v1/AppVersion/{0}'.format(platform_key))
