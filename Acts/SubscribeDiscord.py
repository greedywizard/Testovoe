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


class SubscribeDiscord(Act[Type[PipelineOptions], DObject]):
    def __init__(self, next_act: str = None):
        super().__init__()
        self._next_act = next_act

    def _restore(self, data):
        Scenarios.OpenMetamaskWallet(self.Env, self._static_data.seed_phrase)
        Scenarios.SetupMetamaskWallet(self.Env)
        Scenarios.ConnectScroll(self.Env)
        Scenarios.ConnectGuild(self.Env)

    def _base(self, dyna_data):
        if not self._isRestore:
            Scenarios.ConnectGuild(self.Env)

        Logger.Info("SubscribeDiscord()")

        Actions.OpenUrl(self.Env, URLs.Guild)

        Actions.Click(self.Env, By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/div[1]/button[2]")

        # Дискорд
        Actions.Click(self.Env, By.XPATH, "//div[p[contains(text(), 'Discord')]]/button", window_action=WindowActions.Open)
        Actions.Input(self.Env, By.ID, "uid_6", self._static_data.discord_login)
        Actions.Input(self.Env, By.ID, "uid_8", self._static_data.discord_pass)
        Actions.Click(self.Env, By.XPATH, "//button[.//div[text()='Log In']]")
        Actions.Click(self.Env, By.XPATH, "//button[.//div[text()='Authorize']]", window_action=WindowActions.WaitClose)
        if Actions.GetElement(self.Env, By.XPATH, "/html/body/div[18]/div[3]/div/section/header").Element:
            Logger.Info("Discord account connected yet")
            Actions.Click(self.Env, By.XPATH, "//button[span[text()='Connect anyway']]", window_action=WindowActions.Open)
            Actions.Click(self.Env, By.XPATH, "//button[.//div[text()='Authorize']]", window_action=WindowActions.WaitClose)
        try:
            Actions.WaitElementVisible(self.Env, By.XPATH, "div[text()='Account successfully connected']")
        except TimeoutException:
            pass
