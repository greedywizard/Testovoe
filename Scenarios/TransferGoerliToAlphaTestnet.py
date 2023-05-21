from selenium.webdriver.common.by import By
from Automizer.Scenario import Scenario
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
import Automizer.Actions as Actions
import URLs


class TransferGoerliToAlphaTestnet(Scenario):
    def __init__(self,
                 driver: WebDriver,
                 wait: WebDriverWait):
        super().__init__(driver, wait)

    def Exec(self):
        Actions.OpenUrl(self, URLs.Scroll_Bridge).Exec()

        return self
