from ..Lib.Moutai import Moutai
import jmespath


class OMNIService:
    def __init__(self, host):
        self.host = host
        headers = {"Content-Type": "application/json", "X-ODIN-AppId": "grammarpro",
                   "X-ODIN-AppSecret": "U2FsdGVkX19SgIpGnlaC1bhAza7MSywQ4DDTcvlWmJ0="}
        self.mou_tai = Moutai(host=self.host, headers=headers)

    def get_customer_id(self, user_name, password):
        user_info = {
            "UserName": user_name,
            "Password": password,
        }

        result = self.mou_tai.set_request_context("post", user_info, "/api/v1/customer")
        customer_id = jmespath.search("CustomerId", result.json())
        return customer_id

