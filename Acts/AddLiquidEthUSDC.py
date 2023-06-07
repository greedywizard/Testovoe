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


class AddLiquidEthUSDC(Act):
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
        Logger.Info("AddLiquid()")

        Actions.OpenUrl(self.s, URLs.Uniswap_ETH_Liquid)

        Actions.Click(self.s, By.XPATH, "/html/body/div[1]/div/div[2]/div[4]/main/div[2]/div/div[1]/div/div[2]/div[1]/div/div/button")
        Actions.Click(self.s, By.XPATH, "//div[text()='ETH']")
        Actions.Click(self.s, By.XPATH, "/html/body/div[1]/div/div[2]/div[4]/main/div[2]/div/div[1]/div/div[2]/div[3]/div/div/button")
        Actions.Click(self.s, By.XPATH, "//div[text()='USDC']")

        Actions.Click(self.s, By.XPATH, '//*[@id="root"]/div/div[2]/div[4]/main/div[2]/div/div[1]/div/div[3]/div/div[2]/button[1]')
        Actions.Click(self.s, By.XPATH, '//*[@id="root"]/div/div[2]/div[4]/main/div[2]/div/div[4]/div[2]/div/div/div/div[2]/button')
        Actions.Click(self.s, By.XPATH, '//*[@id="root"]/div/div[2]/div[4]/main/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[3]/button')
        Actions.Click(self.s, By.XPATH, "//button[text()='MAX']")

        if Actions.GetElement(self.s, By.XPATH, "//button[text()='Approve USDC']").Element:
            Actions.Click(self.s, By.XPATH, "//button[text()='Approve USDC']", window_action=WindowActions.Open)
            Actions.Click(self.s, By.XPATH, "//button[text()='Max']")
            Actions.Click(self.s, By.XPATH, "//button[@data-testid='page-container-footer-next']")
            Actions.Click(self.s, By.XPATH, "//button[@data-testid='page-container-footer-next']", window_action=WindowActions.WaitClose)

        Actions.Click(self.s, By.XPATH, "//button[div[text()='Preview']]")
        Actions.Click(self.s, By.XPATH, "//button[div[text()='Add']]", window_action=WindowActions.Open)
        Actions.Click(self.s, By.XPATH, "//button[@data-testid='page-container-footer-next']", window_action=WindowActions.WaitClose)
        while True:
            e = Actions.GetElement(self.s, By.XPATH, "//div[text()='Success']").Element
            if e:
                break

        Actions.Click(self.s, By.XPATH, "/html/body/reach-portal[2]/div[3]/div/div/div/div/div/div[3]/button")
        Actions.Click(self.s, By.XPATH, "/html/body/div[1]/div/div[2]/div[5]/div/div/main/a[2]")
