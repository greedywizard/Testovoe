import time
from selenium.common import NoAlertPresentException
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from Automizer.Enums import WindowActions
from Automizer.Logger import Logger
from Automizer.Scenario import Scenario, ScenarioResult
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
import Automizer.Actions as Actions
import URLs


class AddLiquid(Scenario):
    def __init__(self,
                 driver: WebDriver,
                 wait: WebDriverWait):
        super().__init__(driver, wait)

    def Exec(self, args=None):
        Logger.Info("AddLiquid()")
        result: ScenarioResult = ScenarioResult()

        Actions.OpenUrl(self, URLs.Uniswap_ETH_Liquid)

        Actions.Click(self, By.XPATH, "//span[text()='Select a token']")
        Actions.Click(self, By.XPATH, "//div[text()='USDC']")

        Actions.Click(self, By.XPATH, '//*[@id="root"]/div/div[2]/div[4]/main/div[2]/div/div[1]/div/div[3]/div/div[2]/button[1]')
        Actions.Click(self, By.XPATH, '//*[@id="root"]/div/div[2]/div[4]/main/div[2]/div/div[4]/div[2]/div/div/div/div[2]/button')
        Actions.Click(self, By.XPATH, '//*[@id="root"]/div/div[2]/div[4]/main/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[3]/button')
        Actions.Click(self, By.XPATH, "//button[text()='MAX']")
        res = Actions.Click(self, By.XPATH, "//button[text()='Approve USDC']", window_action=WindowActions.Open)
        self.Active_Window = res.New_Window
        Actions.Click(self, By.XPATH, "//button[text()='Max']")
        Actions.Click(self, By.XPATH, "//button[@data-testid='page-container-footer-next']")
        Actions.Click(self, By.XPATH, "//button[@data-testid='page-container-footer-next']", window_action=WindowActions.WaitClose)
        self.Active_Window = res.Old_Window

        return result
