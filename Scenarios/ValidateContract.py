import time
from selenium.common import NoAlertPresentException
from selenium.webdriver.common.by import By

from Automizer.Enums import WindowActions
from Automizer.Logger import Logger
from Automizer.Scenario import Scenario
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
import Automizer.Actions as Actions


class ValidateContract(Scenario):
    class Data:
        def __init__(self):
            self.compile_version: str = None
            self.address: str = None

    def __init__(self,
                 driver: WebDriver,
                 wait: WebDriverWait,
                 data: Data):
        super().__init__(driver, wait)
        self.__data = data

    def _exec(self):
        Logger.Info("ValidateContract()")

        res = Actions.OpenUrl(self, f"https://blockscout.scroll.io/address/{self.__data.address}/verify-via-flattened-code/new", in_new_window=True)

        Actions.AcceptAlert(self)
        # Выбор компилятора
        Actions.Selector(self, By.ID, "smart_contract_compiler_version", self.__data.compile_version)
        time.sleep(1)
        # "Publish"
        Actions.Click(self, By.XPATH, "//button[text()='Verify & publish']")
        while True:
            Logger.Info("Publishing...")
            try:
                # self.Driver.refresh()
                Actions.WaitElementVisible(self, By.ID, "loading", hide=True)
                break
            except:
                pass

        self.Driver.close()
        self.Active_Window = res.Old_Window
