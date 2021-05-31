from ptest.decorator import BeforeClass, AfterClass

from E1_API_Automation.Business.ProgressTest import PTService


class ProgressTestClass():

    @BeforeClass()
    def create_pt(self):
        self.PTService = PTService()

    @AfterClass()
    def sign_out(self):
        self.PTService.sign_out()
        print("Logout")
