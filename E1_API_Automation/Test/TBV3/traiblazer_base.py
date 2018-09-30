import datetime
import os
from time import sleep

from ptest.decorator import AfterMethod, BeforeSuite, AfterSuite, BeforeClass, AfterClass
from ...Business.TrailblazerV3 import TrailbazerService

from ...Settings import ENVIRONMENT, env_key
from ...Test_Data.TBData import TBUsers


class TraiblazerBaseClass():
    @BeforeClass()
    def create_tb(self):
        self.tb_test = TrailbazerService(ENVIRONMENT, TBUsers.tb_user[env_key]['username'],
                                         TBUsers.tb_user[env_key]['password'])
        self.picked_lesson = None

    @AfterClass()
    def sign_out(self):
        # reset the lesson score to zero
        response = self.tb_test.homework_lesson_answer(self.picked_lesson, pass_lesson=False)
        self.tb_test.sign_out()
        print("Logout")
