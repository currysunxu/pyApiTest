from E1_API_Automation.Test_Data.AuthData import AuthProduct
import jmespath
import json


class AuthUtils:
    @staticmethod
    def get_expected_product(product_key):
        if product_key not in (AuthProduct.SSV2.value, AuthProduct.GP.value):
            expected_value = product_key[0:2]
        elif product_key == AuthProduct.SSV2.value:
            expected_value = "SSLEGACY"
        elif product_key == AuthProduct.GP.value:
            expected_value = "GL"
        return expected_value

    @staticmethod
    def get_expected_gp_purchase_type(student_profile):
        student_profile_json = json.loads(student_profile)
        student_status = jmespath.search("StudentStatus", student_profile_json)
        if student_status == 1:
            expected_gp_purchase_type = "SUBSCRIBE"
        elif student_status == 4:
            expected_gp_purchase_type = "TRIAL"
        return expected_gp_purchase_type