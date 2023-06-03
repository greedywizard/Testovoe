import time
from selenium.webdriver.common.by import By

from Automizer.Enums import WindowActions
from Automizer.Logger import Logger
from Automizer.Scenario import Scenario
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
import Automizer.Actions as Actions
import URLs


class SwapWethToUsdc(Scenario):
    def __init__(self,
                 driver: WebDriver,
                 wait: WebDriverWait):
        super().__init__(driver, wait)

    def _exec(self):
        Logger.Info("SwapWethToUsdc()")
        Actions.OpenUrl(self, URLs.Uniswap_Swap_Usdc)

        try:
            Actions.Click(self, By.XPATH, "//button[text()='I understand']")
        except:
            return

        # Открыть список монет
        Actions.Click(self, By.XPATH, '//*[@id="swap-currency-output"]/div/div[1]/button')
        # Выбрать USDC
        Actions.Click(self, By.XPATH, "//div[text()='USDC']")

        # Открыть список монет
        Actions.Click(self, By.XPATH, "/html/body/div[1]/div/div[2]/div[5]/main/div[2]/div[1]/div/div/div[1]/button")
        # Выбрать монеты WETH
        Actions.Click(self, By.XPATH, "/html/body/reach-portal[2]/div[3]/div/div/div/div/div[3]/div[1]/div/div/div[./div[2]/div[text()='WETH']]")
        Actions.Click(self, By.XPATH, "//button[text()='I understand']")
        try:
            Actions.Click(self, By.XPATH, "//button[text()='Max']")
        except:
            Logger.Error("Cant click 'Max-Button'. balance can be 0.0")
            return

        # Ожидаем подсчет
        time.sleep(3)
        # Проверка наличия "Allow the Uniswap Protocol to use your WETH"
        allow_button: bool = Actions.GetElements(self, By.XPATH, "//button[.//div/div[text()='Allow the Uniswap Protocol to use your WETH']]").ElementsCount > 0

        if allow_button:
            res = Actions.Click(self, By.XPATH, "//button[.//div/div[text()='Allow the Uniswap Protocol to use your WETH']]", window_action=WindowActions.Open)

            self.Active_Window = res.New_Window
            Actions.Click(self, By.XPATH, "//button[text()='Max']")
            Actions.Click(self, By.XPATH, "//button[text()='Next']")
            Actions.Click(self, By.XPATH, "//button[text()='Approve']", window_action=WindowActions.WaitClose)
            self.Active_Window = res.Old_Window

            # Ожидание подсчетов
            while True:
                try:
                    Logger.Info("Waiting calc WETH to USDC...")
                    Actions.GetElement(self, By.XPATH, "//button[@data-testid='web3-status-connected']")
                    # "/html/body/div[1]/div/div[1]/nav/div/div[3]/div/span/button/div/p"
                    # Actions.Click(self, By.XPATH, "//div[text()='You can now trade WETH']")
                    break
                except:
                    pass
            # Swap
            res = Actions.Click(self, By.XPATH, "//button[.//div[text()='Swap']]", window_action=WindowActions.Open)
            self.Active_Window = res.New_Window
            Actions.Click(self, By.XPATH, "//button[text()='Confirm']", window_action=WindowActions.WaitClose)
            self.Active_Window = res.Old_Window
        else:
            Actions.Click(self, By.ID, "swap-button")

        res = Actions.Click(self, By.ID, "confirm-swap-or-send", window_action=WindowActions.Open)
        self.Active_Window = res.New_Window
        Actions.Click(self, By.XPATH, "//button[text()='Confirm']", window_action=WindowActions.WaitClose)
        self.Active_Window = res.Old_Window
        # "Close"
        Actions.Click(self, By.XPATH, "/html/body/reach-portal[2]/div[3]/div/div/div/div/div/div[3]/button")
