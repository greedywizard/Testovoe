import time
from typing import Type

from selenium.webdriver.common.by import By

import Scenarios
from Automizer.Act import Act
from Automizer.Enums import WindowActions
from Automizer.Logger import Logger
import Automizer.Actions as Actions
import URLs
from Exceptions import NoGoerliBalanceException
from Objects import DObject
from db import PipelineOptions


class TransferGoerliToAlphaTestnet(Act[Type[PipelineOptions], DObject]):
    def __init__(self, next_act: str = None):
        super().__init__()
        self._next_act = next_act

    def _restore(self, dyna_data):
        Scenarios.OpenMetamaskWallet(self.Env, self._static_data.seed_phrase)
        Scenarios.SetupMetamaskWallet(self.Env)
        Scenarios.ConnectScroll(self.Env)
        Scenarios.ConnectUniswap(self.Env)

    def _base(self, dyna_data: DObject):
        Logger.Info("TransferGoerliToAlphaTestnet()")

        Actions.OpenUrl(self.Env, URLs.Scroll_Bridge)

        time.sleep(2)

        if Actions.GetElement(self.Env, By.XPATH, "/html/body/div/div/div[2]/div/div[1]/div[2]/div[1]/p").Element.text == 'Scroll Alpha Testnet':
            Actions.Click(self.Env, By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/button", window_action=WindowActions.Open)
            if Actions.ExistElement(self.Env, By.XPATH, "//button[text()='Approve']"):
                Actions.Click(self.Env, By.XPATH, "//button[text()='Approve']")
            Actions.Click(self.Env, By.XPATH, "//button[text()='Switch network']", window_action=WindowActions.WaitClose)

        res = Actions.GetElement(self.Env, By.XPATH, "//div[1]//h6[contains(text(), 'Balance')]")
        balance = float(res.Element.text.split(' ')[1]) * 0.9

        if balance == 0.0:
            Logger.Info("There is no Goerli balance")
            self._next_act = None
            Actions.OpenUrl(self.Env, URLs.Metamask_Settings_Advance)
            Actions.Click(self.Env, By.XPATH, "//button[text()='Clear activity tab data']")
            raise NoGoerliBalanceException

        Actions.Input(self.Env, By.ID, ":r0:", str(balance))
        Actions.Click(self.Env, By.ID, ":r2:", window_action=WindowActions.Open)
        Actions.Click(self.Env, By.XPATH, "//button[@data-testid='page-container-footer-next']", window_action=WindowActions.WaitClose)
