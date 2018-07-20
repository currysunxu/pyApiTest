import datetime
import os
from time import sleep

from ptest.decorator import AfterMethod, BeforeSuite, AfterSuite,BeforeClass,AfterClass
from ...Business.GP import GPService
from ...Settings import ENVIRONMENT

class GrammarPro():

    @BeforeClass()
    def create_gp(self):
        self.gptest = GPService(ENVIRONMENT)

    @AfterClass()
    def sign_out(self):
        self.gptest.sign_out()
        print("Logout")