from E1_API_Automation.Business.AuthService import AuthService, AuthPlatform, AuthDeviceType
from E1_API_Automation.Test_Data.AuthData import AuthUsers, AuthProduct
from hamcrest import assert_that
from ptest.decorator import TestClass, Test
from E1_API_Automation.Settings import AUTH_ENVIRONMENT, env_key
from E1_API_Automation.Business.Utils.AuthUtils import AuthUtils
from E1_API_Automation.Business.Utils.EnvUtils import EnvUtils
from ...Lib.HamcrestMatcher import match_to
import jmespath


@TestClass()
class AuthTestCases:

    @Test(tags="qa, stg, live")
    def test_login_logout(self):
        auth_service = AuthService(AUTH_ENVIRONMENT)
        product_keys = AuthUsers.AuthUsers[env_key].keys()

        # verify login for all the product user with all the supported platform and device type
        for key in product_keys:
            user_name = AuthUsers.AuthUsers[env_key][key][0]['username']
            password = AuthUsers.AuthUsers[env_key][key][0]['password']
            for auth_platform in AuthPlatform:
                for auth_device_type in AuthDeviceType:
                    # verify if login works
                    print(
                        "Product:" + key + ";UserName:" + user_name +
                        ";Platform:" + auth_platform.value + ";DeviceType:" + auth_device_type.value)
                    login_response = auth_service.login(user_name,
                                                        password,
                                                        auth_platform.value,
                                                        auth_device_type.value)
                    assert_that(login_response.status_code == 200)
                    # verify if logout works
                    sign_out_response = auth_service.sign_out()
                    assert_that(sign_out_response.status_code == 200)

    @Test(tags="qa, stg, live")
    def test_legacy_logout(self):
        auth_service = AuthService(AUTH_ENVIRONMENT)
        product_keys = AuthUsers.AuthUsers[env_key].keys()

        # test the legacy logout for all the products
        for key in product_keys:
            user_name = AuthUsers.AuthUsers[env_key][key][0]['username']
            password = AuthUsers.AuthUsers[env_key][key][0]['password']
            auth_service.login(user_name, password)
            customer_id = auth_service.get_custom_id()
            legacy_sign_out_response = auth_service.legacy_sign_out(customer_id)
            assert_that(legacy_sign_out_response.status_code == 200)

    @Test(tags="qa, stg, live")
    def test_products(self):
        auth_service = AuthService(AUTH_ENVIRONMENT)
        product_keys = AuthUsers.AuthUsers[env_key].keys()

        # test the product API for all the products
        for key in product_keys:
            user_list = AuthUsers.AuthUsers[env_key][key]

            for user in user_list:
                user_name = user['username']
                password = user['password']
                print("Checking the product of :" + key + ";UserName:" + user_name)
                auth_service.login(user_name, password)
                product_response = auth_service.get_user_products()
                assert_that(product_response.status_code == 200)
                expected_value = AuthUtils.get_expected_product(key)
                is_progress_test_exist = False
                if key != AuthProduct.GP.value:
                    product_content = jmespath.search("[0]", product_response.json())
                    assert_that(product_content['value'] == expected_value)
                    assert_that(product_content['level'] == 'PRODUCT')
                    assert_that(product_content['identity'] == 'HOMEWORK')
                    assert_that(product_content['purchaseType'] == 'SUBSCRIBE')
                    assert_that(product_content['isActived'])
                    assert_that(product_content['isCurrentGroup'])
                    if key not in (AuthProduct.SSV2.value , AuthProduct.SSV3.value):
                        is_progress_test_exist = True
                else:
                    product_content = jmespath.search("[?identity == 'GRAMMARPRO'] | [0]", product_response.json())
                    assert_that(product_content['value'] == expected_value)
                    assert_that(product_content['level'] == 'PRODUCT')
                    # if it's not Live environment, then do the rest verification with DB
                    if not EnvUtils.is_env_live_cn() and not EnvUtils.is_env_live_sg() :
                        customer_id = auth_service.get_custom_id()
                        student_profile = auth_service.get_student_profile_from_db(customer_id)
                        expected_gp_purchase_type = AuthUtils.get_expected_gp_purchase_type(student_profile[0][0])
                        assert_that(product_content['purchaseType'] == expected_gp_purchase_type)
                    else:
                        assert_that(product_content, match_to("purchaseType"))

                product_content = jmespath.search("[?identity == 'PROGRESSTEST'] | [0]",
                                                  product_response.json())
                if is_progress_test_exist:
                    assert_that(product_content['value'] == expected_value)
                    assert_that(product_content['level'] == 'PRODUCT')
                    assert_that(product_content['description'] == expected_value)
                else:
                    assert_that(product_content is None, "PROGRESSTEST product should not present in Auth ACL!")
