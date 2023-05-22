import time
from random import random
from selenium.webdriver.common.by import By
from Automizer.Scenario import Scenario, ScenarioResult
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
import Automizer.Actions as Actions
import URLs


class SwapUsdcToEth(Scenario):
    def __init__(self,
                 driver: WebDriver,
                 wait: WebDriverWait):
        super().__init__(driver, wait)

    def Exec(self, args=None):
        result: ScenarioResult = ScenarioResult()

        Actions.OpenUrl(self, URLs.Uniswap_Swap_Usdc)

        try:
            # "I understand" кнопка
            Actions.Click(self, By.XPATH, "/html/body/reach-portal[2]/div[3]/div/div/div/div/div/button[1]")
        except:
            pass

        # Открыть список монет
        Actions.Click(self, By.XPATH, "/html/body/div[1]/div/div[2]/div[5]/main/div[2]/div[1]/div/div/div[1]/button")
        # Выбрать монеты usdc
        Actions.Click(self, By.XPATH, "/html/body/reach-portal[2]/div[3]/div/div/div/div/div[3]/div[1]/div/div/div[./div[2]/div[text()='USDC']]")
        # Открыть список монет
        Actions.Click(self, By.XPATH, "/html/body/div[1]/div/div[2]/div[5]/main/div[3]/div[1]/div/div/div/div[1]/button")
        # Выбрать монеты eth
        Actions.Click(self, By.XPATH, "/html/body/reach-portal[2]/div[3]/div/div/div/div/div[3]/div[1]/div/div/div[./div[2]/div[text()='ETH']]")
        try:
            # Кнопка "max"
            Actions.Click(self, By.XPATH, "//button[text()='Max']")
        except:
            return


        # Ожидаем подсчет
        time.sleep(3)
        # Проверка наличия "Allow the Uniswap Protocol to use your USDC"
        allow_button: bool = Actions.GetElements(self, By.XPATH, "//button[.//div/div[text()='Allow the Uniswap Protocol to use your USDC']]").ElementsCount > 0

        if allow_button:
            # "Allow the Uniswap Protocol to use your WETH"
            res = Actions.Click(self, By.XPATH, "//button[.//div/div[text()='Allow the Uniswap Protocol to use your USDC']]", is_opening_window=True)
            # Переключение на всплвающее окно
            self.Active_Window = res.New_Window
            # "Max"
            Actions.Click(self, By.XPATH, "//button[text()='Max']")
            # "Next"
            Actions.Click(self, By.XPATH, "//button[text()='Next']")
            # "Approve"
            Actions.Click(self, By.XPATH, "//button[text()='Approve']")
            # Переключение на исходное окно
            self.Active_Window = res.Old_Window

        # Ожидание подсчетов
        while True:
            try:
                Actions.Click(self, By.XPATH, "//div[text()='You can now trade USDC']")
                break
            except:
                pass
        # "Swap"
        Actions.Click(self, By.ID, "swap-button")
        # "Confirm swap"
        res = Actions.Click(self, By.ID, "confirm-swap-or-send", is_opening_window=True)
        # Переключение на всплвающее окно
        self.Active_Window = res.New_Window
        # "Confirm"
        Actions.Click(self, By.XPATH, "/html/body/div[1]/div/div[2]/div/div[3]/div[3]/footer/button[2]")
        # Переключение на исходное окно
        self.Active_Window = res.Old_Window
        # "Close"
        Actions.Click(self, By.XPATH, "/html/body/reach-portal[2]/div[3]/div/div/div/div/div/div[3]/button")

        return result
