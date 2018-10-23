from ptest.decorator import AfterMethod, BeforeSuite, AfterSuite,BeforeClass,AfterClass
from E1_API_Automation.Business.ProgressTest import PTService
from ...Settings import ENVIRONMENT


class ProgressTestClass():

    @BeforeClass()
    def create_pt(self):
        self.pttest = PTService(ENVIRONMENT)

    @AfterClass()
    def sign_out(self):
        self.pttest.sign_out()
        print("Logout")