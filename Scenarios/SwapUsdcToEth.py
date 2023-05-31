import time
from random import random
from selenium.webdriver.common.by import By

from Automizer.Enums import WindowActions
from Automizer.Logger import Logger
from Automizer.Scenario import Scenario
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
import Automizer.Actions as Actions
import URLs


class SwapUsdcToEth(Scenario):
    def __init__(self,
                 driver: WebDriver,
                 wait: WebDriverWait):
        super().__init__(driver, wait)

    def _exec(self, args=None):
        Logger.Info("SwapUsdcToEth()")

        Actions.OpenUrl(self, URLs.Uniswap_Swap_Usdc)

        try:
            # "I understand" кнопка
            Actions.Click(self, By.XPATH, "/html/body/reach-portal[2]/div[3]/div/div/div/div/div/button[1]")
        except:
            pass

        # Открыть список монет
        Actions.Click(self, By.XPATH, '//*[@id="swap-currency-input"]/div/div[1]/button')
        # Выбрать монеты usdc
        Actions.Click(self, By.XPATH, "//div[text()='USDC']")
        # Открыть список монет
        Actions.Click(self, By.XPATH, '//*[@id="swap-currency-output"]/div/div[1]/button')
        # Выбрать монеты eth
        Actions.Click(self, By.XPATH, "//div[text()='ETH']")
        try:
            # Кнопка "max"
            Actions.Click(self, By.XPATH, "//button[text()='Max']")
        except:
            Logger.Error("Cant click 'Max-Button'. balance can be 0.0")
            return

        # Ожидаем подсчет
        time.sleep(3)
        # Проверка наличия "Allow the Uniswap Protocol to use your USDC"
        allow_button: bool = Actions.GetElements(self, By.XPATH, "//button[.//div/div[text()='Allow the Uniswap Protocol to use your USDC']]").ElementsCount > 0

        if allow_button:
            # "Allow the Uniswap Protocol to use your WETH"
            res = Actions.Click(self, By.XPATH, "//button[.//div/div[text()='Allow the Uniswap Protocol to use your USDC']]", window_action=WindowActions.Open)
            # Переключение на всплвающее окно
            self.Active_Window = res.New_Window
            # "Max"
            Actions.Click(self, By.XPATH, "//button[text()='Max']")
            # "Next"
            Actions.Click(self, By.XPATH, "//button[text()='Next']")
            # "Approve"
            Actions.Click(self, By.XPATH, "//button[text()='Approve']", window_action=WindowActions.WaitClose)
            # Переключение на исходное окно
            self.Active_Window = res.Old_Window

        # Ожидание подсчетов
            while True:
                try:
                    Logger.Info("Waiting calc WETH to USDC...")
                    Actions.GetElement(self, By.XPATH, "//button[@data-testid='web3-status-connected']")
                    break
                except:
                    pass

            res = Actions.Click(self, By.XPATH, "//button[.//div[text()='Swap']]", window_action=WindowActions.Open)
            self.Active_Window = res.New_Window
            Actions.Click(self, By.XPATH, "//button[text()='Confirm']", window_action=WindowActions.WaitClose)
            self.Active_Window = res.Old_Window
        else:
            Actions.Click(self, By.ID, "swap-button")

        # "Confirm swap"
        res = Actions.Click(self, By.ID, "confirm-swap-or-send", window_action=WindowActions.Open)
        # Переключение на всплвающее окно
        self.Active_Window = res.New_Window
        # "Confirm"
        Actions.Click(self, By.XPATH, "/html/body/div[1]/div/div[2]/div/div[3]/div[3]/footer/button[2]", window_action=WindowActions.WaitClose)
        # Переключение на исходное окно
        self.Active_Window = res.Old_Window
        # "Close"
        Actions.Click(self, By.XPATH, "/html/body/reach-portal[2]/div[3]/div/div/div/div/div/div[3]/button")
