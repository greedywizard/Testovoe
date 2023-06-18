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


class RemoveLiquidEthUSDC(Act[Type[PipelineOptions], DObject]):
    def __init__(self, next_act: str):
        super().__init__()
        self._next_act = next_act

    def _restore(self, data):
        Scenarios.OpenMetamaskWallet(self.Env, self._static_data.seed_phrase)
        Scenarios.SetupMetamaskWallet(self.Env)
        Scenarios.ConnectScroll(self.Env)
        Scenarios.ConnectUniswap(self.Env)

    def _base(self, dyna_data):
        Logger.Info("RemoveLiquid()")
        time.sleep(15)
        Actions.OpenUrl(self.Env, URLs.Uniswap_ETH_Liquid_Pool)

        Actions.Click(self.Env, By.XPATH, "/html/body/div[1]/div/div[2]/div[5]/div/div/main/a[.//div[1]/div[1]/div[text()[2] = 'USDC' and text()[4] = 'ETH']]")
        # Убрать ликвидность
        Actions.Click(self.Env, By.XPATH, "//a[text()='Remove Liquidity']")
        Actions.Click(self.Env, By.XPATH, "//button[text()='Max']")
        Actions.Click(self.Env, By.XPATH, "//button[text()='Remove']")
        Actions.Click(self.Env, By.XPATH, "/html/body/reach-portal[3]/div[3]/div/div/div/div/div/div[2]/button", window_action=WindowActions.Open)
        Actions.Click(self.Env, By.XPATH, "//button[@data-testid='page-container-footer-next']", window_action=WindowActions.WaitClose)
        while True:
            Logger.Info("Wait")
            e = Actions.GetElement(self.Env, By.XPATH, "//div[text()='Success']").Element
            if e:
                break
