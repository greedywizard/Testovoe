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


class SwapUsdcToEth(Act):
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
        Logger.Info("SwapUsdcToEth()")

        Actions.OpenUrl(self.s, URLs.Uniswap_Swap)

        Actions.Click(self.s, By.XPATH, "/html/body/div[1]/div/div[2]/div[5]/main/div[2]/div[1]/div/div/div[1]/button")
        Actions.Input(self.s, By.ID, "token-search-input", "0xA0D71B9877f44C744546D649147E3F1e70a93760")
        Actions.Click(self.s, By.XPATH, "//div[text()='USD Coin']")

        try:
            # I understand
            Actions.Click(self.s, By.XPATH, "/html/body/reach-portal[2]/div[3]/div/div/div/div/div/button[1]")
        except:
            pass

        Actions.Click(self.s, By.XPATH, "/html/body/div[1]/div/div[2]/div[5]/main/div[3]/div[1]/div/div/div/div[1]/button")
        Actions.Input(self.s, By.ID, "token-search-input", "Ether")
        Actions.Click(self.s, By.XPATH, "//div[text()='Ether']")

        try:
            # Кнопка "max"
            Actions.Click(self.s, By.XPATH, "//button[text()='Max']")
        except:
            Logger.Error("Cant click 'Max-Button'. balance can be 0.0")
            return

        if Actions.ExistElement(self.s, By.XPATH, "/html/body/div[1]/div/div[2]/div[5]/main/div[3]/div[2]/div/div/button[1]"):
            self._approve()
        else:
            Actions.Click(self.s, By.ID, "swap-button")

        Actions.Click(self.s, By.ID, "confirm-swap-or-send", window_action=WindowActions.Open)
        Actions.Click(self.s, By.XPATH, "//button[@data-testid='page-container-footer-next']", window_action=WindowActions.WaitClose)
        # "Close"
        Actions.Click(self.s, By.XPATH, "/html/body/reach-portal[2]/div[3]/div/div/div/div/div/div[3]/button")

    def _approve(self):
        Actions.Click(self.s, By.XPATH, "/html/body/div[1]/div/div[2]/div[5]/main/div[3]/div[2]/div/div/button[1]", window_action=WindowActions.Open)
        Actions.Click(self.s, By.XPATH, "//button[text()='Max']")
        Actions.Click(self.s, By.XPATH, "//button[@data-testid='page-container-footer-next']")
        Actions.Click(self.s, By.XPATH, "//button[@data-testid='page-container-footer-next']", window_action=WindowActions.WaitClose)

        # Ожидание подсчетов
        while True:
            try:
                Logger.Info("Waiting calc WETH to USDC...")
                Actions.GetElement(self.s, By.XPATH, "//button[@data-testid='web3-status-connected']")
                break
            except:
                pass

        while True:
            try:
                Logger.Info("Waiting Approve")
                Actions.Click(self.s, By.ID, "swap-button", is_visible=False)
                break
            except:
                pass
