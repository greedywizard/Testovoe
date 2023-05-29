from selenium.webdriver.common.by import By

from Automizer.Logger import Logger
from Automizer.Scenario import Scenario, ScenarioResult
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
import Automizer.Actions as Actions
import URLs


class WaitTransferGoerliToAlpha(Scenario):
    def __init__(self,
                 driver: WebDriver,
                 wait: WebDriverWait):
        super().__init__(driver, wait)

    def Exec(self, args=None):
        Logger.Info("WaitTransferGoerliToAlpha()")
        result: ScenarioResult = ScenarioResult()

        Actions.OpenUrl(self, URLs.Scroll_Bridge)

        Actions.Click(self, By.XPATH, '//*[@id="root"]/div/div[1]/div[1]/div/button[2]')

        while True:
            try:
                Logger.Info("Waiting success transfer...")
                Actions.GetElement(self, By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div/table/tbody/tr[1]/td[1]/div/div[1]/span[text()='Success']")
                Actions.GetElement(self, By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div/table/tbody/tr[1]/td[1]/div/div[2]/span[text()='Success']")
                break
            except:
                pass

        return result
