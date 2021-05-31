import datetime
import os
from time import sleep

from ptest.decorator import AfterMethod, BeforeSuite, AfterSuite,BeforeClass,AfterClass
from ...Business.GP import GPService


class GrammarProBaseClass():

    @BeforeClass()
    def create_gp(self):
        self.gptest = GPService()

    @AfterMethod()
    def sign_out(self):
        self.gptest.sign_out()
        print("Logout")