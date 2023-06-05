from typing import Type

from selenium.webdriver.common.by import By

import Scenarios
from Automizer.Act import Act
from Automizer.Logger import Logger
from Automizer.ExecEnvironment import ExecEnvironment
import Automizer.Actions as Actions
import URLs
from db import PipelineOptions


class WaitTransferGoerliToAlpha(Act):
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
        Logger.Info("WaitTransferGoerliToAlpha()")
        Actions.OpenUrl(self.s, URLs.Scroll_Bridge)

        Actions.Click(self.s, By.XPATH, '//*[@id="root"]/div/div[1]/div[1]/div/button[2]')

        while True:
            try:
                Logger.Info("Waiting success transfer...")
                Actions.GetElement(self.s, By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div/table/tbody/tr[1]/td[1]/div/div[1]/span[text()='Success']")
                Actions.GetElement(self.s, By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div/table/tbody/tr[1]/td[1]/div/div[2]/span[text()='Success']")
                break
            except:
                pass

        return
