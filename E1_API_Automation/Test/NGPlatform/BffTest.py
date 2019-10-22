#!/usr/bin/env python
#-*-coding:utf-8-*-

#author:Curry
#date:2019/10/14


from E1_API_Automation.Business.AuthService import AuthService
from E1_API_Automation.Business.NGPlatform.BffService import BffService
from E1_API_Automation.Settings import BFF_ENVIRONMENT,env_key,AUTH_ENVIRONMENT
from E1_API_Automation.Test_Data.BffData import BffUsers,BffProduct
from hamcrest import assert_that, equal_to
from ptest.decorator import TestClass, Test



@TestClass()
class BffTest:

	@Test(tag='qa')
	def test_bff_auth_login_valid_username(self):
		bff_service = BffService(BFF_ENVIRONMENT)
		product_keys = BffUsers.BffUserPw[env_key].keys()
		for key in product_keys:
			user_name = BffUsers.BffUserPw[env_key][key][0]['username']
			password = BffUsers.BffUserPw[env_key][key][0]['password']
			if key.__contains__('HF'):
				print("HF user is : %s"%(user_name))
				response = bff_service.login(user_name, password)
				print("Bff login response is : %s"%(response.__str__()))
				id_token = bff_service.get_auth_token()
				print("Bff login Token is : %s"%(id_token))
				assert_that((not id_token.__eq__("")) and id_token.__str__() is not None)

	@Test(tag='qa')
	def test_bff_auth_login_invalid_username(self):
		bff_service = BffService(BFF_ENVIRONMENT)
		key = BffProduct.HFV35.value
		user_name = BffUsers.BffUserPw[env_key][key][0]['password']
		password = BffUsers.BffUserPw[env_key][key][0]['password']
		response = bff_service.login(user_name,password)
		print("Bff login response is : %s"%(response.__str__()))
		assert_that(response.status_code, equal_to(404))

	@Test(tag='qa')
	def test_bff_auth_login_not_HF_username(self):
		bff_service = BffService(BFF_ENVIRONMENT)
		product_keys = BffUsers.BffUserPw[env_key].keys()
		for key in product_keys:
			user_name = BffUsers.BffUserPw[env_key][key][0]['username']
			password = BffUsers.BffUserPw[env_key][key][0]['password']
			response = bff_service.login(user_name, password)
			print(
				"Product:" + key + ";UserName:" + user_name )
			if not key.__contains__('HF'):
				print("status: %s, message: %s"%(str(response.json()['status']),response.json()['message']))
				assert_that(response.status_code, equal_to(401))
				assert_that((response.json()['error'].__eq__("Unauthorized")))


	@Test(tag='qa')
	def test_submit_new_attempt_without_auth_token(self):
		bff_service = BffService(BFF_ENVIRONMENT)
		response=bff_service.submit_new_attempt_with_negative_auth_token()
		print("Bff login response is : %s" % (response.__str__()))
		assert_that(response.status_code, equal_to(400))
		assert_that((response.json()['error'].__eq__("Bad Request")))

	@Test(tag='qa')
	def test_submit_new_attempt_with_invalid_auth_token(self):
		bff_service = BffService(BFF_ENVIRONMENT)
		response=bff_service.submit_new_attempt_with_negative_auth_token("invalid")
		print("Bff login response is : %s" % (response.__str__()))
		assert_that(response.status_code, equal_to(401))
		assert_that((response.json()['error'].__eq__("Unauthorized")))








