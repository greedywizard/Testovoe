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


class SubscribeDiscord(Act):
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
        if not self._isRestore:
            Scenarios.ConnectGuild(self.s)

        Logger.Info("SubscribeDiscord()")

        Actions.OpenUrl(self.s, URLs.Guild)

        Actions.Click(self.s, By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/div[1]/button[2]")

        # Дискорд
        Actions.Click(self.s, By.XPATH, "//div[p[contains(text(), 'Discord')]]/button", window_action=WindowActions.Open)
        Actions.Input(self.s, By.ID, "uid_6", self.__static_data.discord_login)
        Actions.Input(self.s, By.ID, "uid_8", self.__static_data.discord_pass)
        Actions.Click(self.s, By.XPATH, "//button[.//div[text()='Log In']]")
        Actions.Click(self.s, By.XPATH, "//button[.//div[text()='Authorize']]", window_action=WindowActions.WaitClose)
        if Actions.GetElement(self.s, By.XPATH, "/html/body/div[18]/div[3]/div/section/header").Element:
            Logger.Info("Discord account connected yet")
            Actions.Click(self.s, By.XPATH, "//button[span[text()='Connect anyway']]", window_action=WindowActions.Open)
            Actions.Click(self.s, By.XPATH, "//button[.//div[text()='Authorize']]", window_action=WindowActions.WaitClose)
        try:
            Actions.WaitElementVisible(self.s, By.XPATH, "div[text()='Account successfully connected']")
        except TimeoutException:
            pass
