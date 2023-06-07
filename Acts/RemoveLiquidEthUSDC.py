import time
from typing import Type

from selenium.common import ElementNotInteractableException
from selenium.webdriver.common.by import By

import Scenarios
from Automizer.Act import Act
from Automizer.Enums import WindowActions
from Automizer.Logger import Logger
from Automizer.ExecEnvironment import ExecEnvironment
import Automizer.Actions as Actions
import URLs
from db import PipelineOptions


class RemoveLiquidEthUSDC(Act):
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
        Logger.Info("RemoveLiquid()")

        Actions.OpenUrl(self.s, URLs.Uniswap_ETH_Liquid_Pool)

        Actions.Click(self.s, By.XPATH, "/html/body/div[1]/div/div[2]/div[5]/div/div/main/a[2]")
        # Убрать ликвидность
        Actions.Click(self.s, By.XPATH, "//a[text()='Remove Liquidity']")
        Actions.Click(self.s, By.XPATH, "//button[text()='Max']")
        Actions.Click(self.s, By.XPATH, "//button[text()='Remove']")
        Actions.Click(self.s, By.XPATH, "/html/body/reach-portal[3]/div[3]/div/div/div/div/div/div[2]/button", window_action=WindowActions.Open)
        Actions.Click(self.s, By.XPATH, "//button[@data-testid='page-container-footer-next']", window_action=WindowActions.WaitClose)
        while True:
            Logger.Info("Wait")
            e = Actions.GetElement(self.s, By.XPATH, "//div[text()='Success']").Element
            if e:
                break
