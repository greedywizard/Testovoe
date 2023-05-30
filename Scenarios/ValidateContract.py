import time
from selenium.common import NoAlertPresentException
from selenium.webdriver.common.by import By

from Automizer.Enums import WindowActions
from Automizer.Logger import Logger
from Automizer.Scenario import Scenario, ScenarioResult
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
import Automizer.Actions as Actions
import URLs


class ValidateContract(Scenario):
    def __init__(self,
                 driver: WebDriver,
                 wait: WebDriverWait):
        super().__init__(driver, wait)

    def Exec(self, args=None):
        Logger.Info("ValidateContract()")
        result: ScenarioResult = ScenarioResult()

        res = Actions.OpenUrl(self, f"https://blockscout.scroll.io/address/{args['address']}/verify-via-flattened-code/new", in_new_window=True)

        Actions.AcceptAlert(self)
        # Выбор компилятора
        Actions.Selector(self, By.ID, "smart_contract_compiler_version", args["compile_version"])
        # "Publish"
        Actions.Click(self, By.XPATH, "//button[text()='Verify & publish']")
        while True:
            Logger.Info("Publishing...")
            try:
                Actions.WaitElementVisible(self, By.ID, 'loading', hide=True)
                break
            except:
                pass

        self.Active_Window = res.Old_Window

        return result
