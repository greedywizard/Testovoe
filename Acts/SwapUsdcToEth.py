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

        Actions.OpenUrl(self.s, URLs.Uniswap_Swap_Usdc)

        try:
            # "I understand" кнопка
            Actions.Click(self.s, By.XPATH, "/html/body/reach-portal[2]/div[3]/div/div/div/div/div/button[1]")
        except:
            pass

        # Открыть список монет
        Actions.Click(self.s, By.XPATH, '//*[@id="swap-currency-input"]/div/div[1]/button')
        # Выбрать монеты usdc
        Actions.Click(self.s, By.XPATH, "//div[text()='USDC']")
        # Открыть список монет
        Actions.Click(self.s, By.XPATH, '//*[@id="swap-currency-output"]/div/div[1]/button')
        # Выбрать монеты eth
        Actions.Click(self.s, By.XPATH, "//div[text()='ETH']")
        try:
            # Кнопка "max"
            Actions.Click(self.s, By.XPATH, "//button[text()='Max']")
        except:
            Logger.Error("Cant click 'Max-Button'. balance can be 0.0")
            return

        # Ожидаем подсчет
        time.sleep(3)
        # Проверка наличия "Allow the Uniswap Protocol to use your USDC"
        allow_button: bool = Actions.GetElements(self.s, By.XPATH, "//button[.//div/div[text()='Allow the Uniswap Protocol to use your USDC']]").ElementsCount > 0

        if allow_button:
            while True:
                try:
                    Actions.Click(self.s, By.XPATH, "//button[.//div/div[text()='Allow the Uniswap Protocol to use your USDC']]", window_action=WindowActions.Open)
                    break
                except:
                    pass
            Actions.Click(self.s, By.XPATH, "//button[text()='Max']")
            Actions.Click(self.s, By.XPATH, "//button[text()='Next']")
            Actions.Click(self.s, By.XPATH, "//button[text()='Approve']", window_action=WindowActions.WaitClose)

            # Ожидание подсчетов
            while True:
                try:
                    Logger.Info("Waiting calc WETH to USDC...")
                    Actions.GetElement(self.s, By.XPATH, "//button[@data-testid='web3-status-connected']")
                    break
                except:
                    pass

            Actions.Click(self.s, By.XPATH, "//button[.//div[text()='Swap']]")
        else:
            Actions.Click(self.s, By.ID, "swap-button")

        Actions.Click(self.s, By.ID, "confirm-swap-or-send", window_action=WindowActions.Open)
        Actions.Click(self.s, By.XPATH, "//button[@data-testid='page-container-footer-next']", window_action=WindowActions.WaitClose)
        # "Close"
        Actions.Click(self.s, By.XPATH, "/html/body/reach-portal[2]/div[3]/div/div/div/div/div/div[3]/button")
