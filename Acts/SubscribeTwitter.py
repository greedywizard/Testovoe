import time
from typing import Type

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By

import Scenarios
from Automizer.Act import Act
from Automizer.Enums import WindowActions
from Automizer.Logger import Logger
import Automizer.Actions as Actions
import URLs
from Objects import DObject
from db import PipelineOptions


class SubscribeTwitter(Act[Type[PipelineOptions], DObject]):
    def __init__(self, next_act: str = None):
        super().__init__()
        self._next_act = next_act

    def _restore(self, data):
        Scenarios.OpenMetamaskWallet(self.Env, self._static_data.seed_phrase)
        Scenarios.SetupMetamaskWallet(self.Env)
        Scenarios.ConnectScroll(self.Env)
        Scenarios.ConnectUniswap(self.Env)
        Scenarios.ConnectGuild(self.Env)

    def _base(self, dyna_data):
        if not self._isRestore:
            Scenarios.ConnectGuild(self.Env)

        Logger.Info("SubscribeTwitter()")

        Actions.OpenUrl(self.Env, URLs.Guild)

        try:
            Actions.Click(self.Env, By.XPATH, "/html/body/div[4]/div[3]/div/section/div/div[3]/button")
        except:
            pass

        Actions.Click(self.Env, By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/div[1]/button[2]")

        Actions.Click(self.Env, By.XPATH, "//div[p[contains(text(), 'Twitter')]]/button", window_action=WindowActions.Open)
        Actions.Click(self.Env, By.XPATH, "//a[@data-testid='OAuth_Consent_Log_In_Button']")
        Actions.Input(self.Env, By.XPATH, "/html/body/div/div/div/div/main/div/div/div/div[2]/div[2]/div/div[5]/label/div/div[2]/div/input", self.__static_data.twitter_login)
        Actions.Click(self.Env, By.XPATH, "//span[text()='Next']")
        Actions.Input(self.Env, By.XPATH, "/html/body/div/div/div/div/main/div/div/div/div[2]/div[2]/div[1]/div/div/div/div[3]/div/label/div/div[2]/div[1]/input",
                      self._static_data.twitter_pass)
        Actions.Click(self.Env, By.XPATH, "//span[text()='Log in']")
        Actions.Click(self.Env, By.XPATH, "//div[@data-testid='OAuth_Consent_Button']", is_clickable=False, as_script=True, window_action=WindowActions.WaitClose)

        Actions.WaitElementVisible(self.Env, By.XPATH, "div[text()='Account successfully connected']")
