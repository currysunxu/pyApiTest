from ..Lib.Moutai import Moutai


class ProvisioningService:
    def __init__(self, host):
        self.host = host
        headers = {"Content-Type": "application/json",
                   "X-BA-Token": "4255FB70-184A-4a92-9FAC-7DA63316AB64"}
        self.mou_tai = Moutai(host=self.host, headers=headers)

    def get_app_version_by_platform_key(self, platform_key):
        return self.mou_tai.get('/api/v1/AppVersion/{0}'.format(platform_key))
