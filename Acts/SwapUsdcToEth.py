import time
from typing import Type

from selenium.webdriver.common.by import By

import Scenarios
from Automizer.Act import Act
from Automizer.Enums import WindowActions
from Automizer.Logger import Logger
import Automizer.Actions as Actions
import URLs
from Objects import DObject
from db import PipelineOptions


class SwapUsdcToEth(Act[Type[PipelineOptions], DObject]):
    def __init__(self, next_act: str = None):
        super().__init__()
        self._next_act = next_act

    def _restore(self, data):
        Scenarios.OpenMetamaskWallet(self.Env, self._static_data.seed_phrase)
        Scenarios.SetupMetamaskWallet(self.Env)
        Scenarios.ConnectScroll(self.Env)
        Scenarios.ConnectUniswap(self.Env)

    def _base(self, dyna_data):
        Logger.Info("SwapUsdcToEth()")

        Actions.OpenUrl(self.Env, URLs.Uniswap_Swap)

        Actions.Click(self.Env, By.XPATH, "/html/body/div[1]/div/div[2]/div[5]/main/div[2]/div[1]/div/div/div[1]/button")
        Actions.Input(self.Env, By.ID, "token-search-input", "0xA0D71B9877f44C744546D649147E3F1e70a93760")
        Actions.Click(self.Env, By.XPATH, "//div[text()='USD Coin']")

        try:
            # I understand
            Actions.Click(self.Env, By.XPATH, "/html/body/reach-portal[2]/div[3]/div/div/div/div/div/button[1]")
        except:
            pass

        Actions.Click(self.Env, By.XPATH, "/html/body/div[1]/div/div[2]/div[5]/main/div[3]/div[1]/div/div/div/div[1]/button")
        Actions.Input(self.Env, By.ID, "token-search-input", "Ether")
        Actions.Click(self.Env, By.XPATH, "//div[text()='Ether']")

        try:
            # Кнопка "max"
            Actions.Click(self.Env, By.XPATH, "//button[text()='Max']")
        except:
            Logger.Error("Cant click 'Max-Button'. balance can be 0.0")
            return

        # Ожидание подсчетов
        time.sleep(3)

        if Actions.ExistElement(self.Env, By.XPATH, "/html/body/div[1]/div/div[2]/div[5]/main/div[3]/div[2]/div/div/button[1]"):
            self._approve()
        else:
            Actions.Click(self.Env, By.ID, "swap-button", as_script=True)

        Actions.Click(self.Env, By.ID, "confirm-swap-or-send", window_action=WindowActions.Open)
        Actions.Click(self.Env, By.XPATH, "//button[@data-testid='page-container-footer-next']", window_action=WindowActions.WaitClose)

        Actions.WaitElementVisible(self.Env, By.XPATH, "//p[contains(text(), 'Pending')]")
        Actions.WaitElementVisible(self.Env, By.XPATH, "//p[contains(text(), 'Pending')]", hide=True)

    def _approve(self):
        Actions.Click(self.Env, By.XPATH, "/html/body/div[1]/div/div[2]/div[5]/main/div[3]/div[2]/div/div/button[1]", window_action=WindowActions.Open)
        Actions.Click(self.Env, By.XPATH, "//button[text()='Max']")
        Actions.Click(self.Env, By.XPATH, "//button[@data-testid='page-container-footer-next']")
        Actions.Click(self.Env, By.XPATH, "//button[@data-testid='page-container-footer-next']", window_action=WindowActions.WaitClose)

        # Ожидание подсчетов
        while True:
            try:
                Logger.Info("Waiting calc WETH to USDC...")
                Actions.GetElement(self.Env, By.XPATH, "//button[@data-testid='web3-status-connected']")
                break
            except:
                pass

        while True:
            try:
                Logger.Info("Waiting Approve")
                Actions.Click(self.Env, By.ID, "swap-button", as_script=True)
                break
            except:
                pass
