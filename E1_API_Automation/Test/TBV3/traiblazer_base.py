import datetime
import os
from time import sleep

from ptest.decorator import AfterMethod, BeforeSuite, AfterSuite,BeforeClass,AfterClass
from ...Business.TrailblazerV3 import TrailbazerService

from ...Settings import ENVIRONMENT


class TraiblazerBaseClass():

    @BeforeClass()
    def create_tb(self):
        self.tb_test = TrailbazerService(ENVIRONMENT)

    @AfterClass()
    def sign_out(self):
        self.tb_test.sign_out()
        print("Logout")