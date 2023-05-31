from selenium.webdriver.common.by import By

from Automizer.Enums import WindowActions
from Automizer.Logger import Logger
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

    def _exec(self, args=None):
        Logger.Info("TransferGoerliToAlphaTestnet()")

        Actions.OpenUrl(self, URLs.Scroll_Bridge)

        res = Actions.GetElement(self, By.XPATH, "//div[1]//h6[contains(text(), 'Balance')]")
        balance = float(res.Element.text.split(' ')[1])/100

        if balance == 0.0:
            raise ValueError

        Actions.Input(self, By.ID, ":r0:", str(balance))
        res = Actions.Click(self, By.ID, ":r2:", window_action=WindowActions.Open)
        self.Active_Window = res.New_Window
        Actions.Click(self, By.XPATH, "//button[@data-testid='page-container-footer-next']", window_action=WindowActions.WaitClose)
        self.Active_Window = res.Old_Window
