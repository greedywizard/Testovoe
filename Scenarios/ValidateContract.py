import time
from selenium.common import NoAlertPresentException
from selenium.webdriver.common.by import By
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
        result: ScenarioResult = ScenarioResult()

        res = Actions.OpenUrl(self, f"https://blockscout.scroll.io/address/{args['address']}/verify-via-flattened-code/new", in_new_window=True)
        try:
            Actions.AcceptAlert(self)
        except NoAlertPresentException:
            # Продолжить, если нет модального диалога
            pass

        # Выбор компилятора
        Actions.Selected(self, By.ID, "smart_contract_compiler_version", args["compile_version"])
        # "Publish"
        Actions.Click(self, By.XPATH, "/html/body/div[1]/main/section/div[2]/form/div[14]/button[text()='Verify & publish']")
        self.Active_Window = res.Old_Window

        return result
