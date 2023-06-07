import time
from typing import Type

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By

import Scenarios
from Automizer.Act import Act
from Automizer.Enums import WindowActions
from Automizer.Logger import Logger
from Automizer.ExecEnvironment import ExecEnvironment
import Automizer.Actions as Actions
import URLs
from db import PipelineOptions


class SubscribeTwitter(Act):
    def __init__(self, driver, wait, data: Type[PipelineOptions], next_point=None, restore_point=None):
        super().__init__(next_point, restore_point)
        self.__driver = driver
        self.__wait = wait
        self.__static_data = data
        self.s = ExecEnvironment(self.__driver, self.__wait)

    def _restore(self, data):
        Scenarios.OpenMetamaskWallet(self.s, self.__static_data.seed_phrase)
        Scenarios.SetupMetamaskWallet(self.s)
        Scenarios.ConnectScroll(self.s)
        Scenarios.ConnectGuild(self.s)

    def _base(self, dyna_data):
        Logger.Info("SubscribeTwitter()")

        Actions.OpenUrl(self.s, URLs.Guild)

        Actions.Click(self.s, By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/div[1]/button[2]")

        Actions.Click(self.s, By.XPATH, "//div[p[contains(text(), 'Twitter')]]/button", window_action=WindowActions.Open)
        Actions.Click(self.s, By.XPATH, "//a[@data-testid='OAuth_Consent_Log_In_Button']")
        Actions.Input(self.s, By.XPATH, "/html/body/div/div/div/div/main/div/div/div/div[2]/div[2]/div/div[5]/label/div/div[2]/div/input", self.__static_data.twitter_login)
        Actions.Click(self.s, By.XPATH, "//span[text()='Next']")
        Actions.Input(self.s, By.XPATH, "/html/body/div/div/div/div/main/div/div/div/div[2]/div[2]/div[1]/div/div/div/div[3]/div/label/div/div[2]/div[1]/input",
                      self.__static_data.twitter_pass)
        Actions.Click(self.s, By.XPATH, "//span[text()='Log in']")
        Actions.Click(self.s, By.XPATH, "//div[@data-testid='OAuth_Consent_Button']", is_clickable=False, as_script=True, window_action=WindowActions.WaitClose)
        try:
            Actions.WaitElementVisible(self.s, By.XPATH, "div[text()='Account successfully connected']")
        except TimeoutException:
            pass
