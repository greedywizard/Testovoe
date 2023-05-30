import time

from selenium.common import NoAlertPresentException
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By

from Automizer.Logger import Logger
from Automizer.Scenario import Scenario, ScenarioResult
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
import Automizer.Actions as Actions
import URLs


class AddToken(Scenario):
    def __init__(self,
                 driver: WebDriver,
                 wait: WebDriverWait):
        super().__init__(driver, wait)

    def Exec(self, args=None):
        Logger.Info("AddToken()")
        result: ScenarioResult = ScenarioResult()

        Actions.OpenUrl(self, URLs.Metamask_ImportToken)

        Actions.AcceptAlert(self)

        Actions.Input(self, By.ID, "custom-address", args["address"])

        while True:
            Logger.Info("Importing token...")
            try:
                symbol = Actions.GetElement(self, By.ID, "custom-symbol").Element.text
                if not symbol or symbol is None:
                    break
                else:
                    time.sleep(3)
            except:
                pass

        Actions.Click(self, By.XPATH, "//button[text()='Add custom token']", as_script=True)

        return result
