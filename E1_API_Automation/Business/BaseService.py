from E1_API_Automation.Lib.Moutai import Moutai


class BaseService:
    def __init__(self, host, headers={}):
        self.host = host
        default_header = {"Content-Type": "application/json;charset=UTF-8"}
        self.mou_tai = Moutai(host=self.host, headers={**default_header, **headers})
        self.id_token = None
        self.access_token = None
