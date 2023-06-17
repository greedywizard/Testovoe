import time
from typing import Type

from selenium.webdriver.common.by import By

import Scenarios
from Automizer.Act import Act
from Automizer.Enums import WindowActions
from Automizer.Logger import Logger
from Automizer.ExecEnvironment import ExecEnvironment
import Automizer.Actions as Actions
import URLs
from db import PipelineOptions


class TransferGoerliToAlphaTestnet(Act):
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
        Scenarios.ConnectUniswap(self.s)

    def _base(self, dyna_data):
        Logger.Info("TransferGoerliToAlphaTestnet()")
        try:
            Actions.OpenUrl(self.s, URLs.Scroll_Bridge)

            if Actions.GetElement(self.s, By.XPATH, "/html/body/div/div/div[2]/div/div[1]/div[2]/div[1]/p").Element.text == 'Scroll Alpha Testnet':
                Actions.Click(self.s, By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/button", window_action=WindowActions.Open)
                if Actions.ExistElement(self.s, By.XPATH, "//button[text()='Approve']"):
                    Actions.Click(self.s, By.XPATH, "//button[text()='Approve']")
                Actions.Click(self.s, By.XPATH, "//button[text()='Switch network']", window_action=WindowActions.WaitClose)

            res = Actions.GetElement(self.s, By.XPATH, "//div[1]//h6[contains(text(), 'Balance')]")
            balance = float(res.Element.text.split(' ')[1]) / 100

            if balance == 0.0:
                raise ValueError

            Actions.Input(self.s, By.ID, ":r0:", str(balance))
            Actions.Click(self.s, By.ID, ":r2:", window_action=WindowActions.Open)
            Actions.Click(self.s, By.XPATH, "//button[@data-testid='page-container-footer-next']", window_action=WindowActions.WaitClose)

        except ValueError:
            Logger.Info("There is no Goerli balance")
            print('clear account')
