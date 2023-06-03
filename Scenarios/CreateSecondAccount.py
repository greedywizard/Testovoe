from selenium.webdriver.common.by import By
from Automizer.Logger import Logger
from Automizer.Scenario import Scenario
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
import Automizer.Actions as Actions
import URLs


class CreateSecondAccount(Scenario):
    def __init__(self,
                 driver: WebDriver,
                 wait: WebDriverWait):
        super().__init__(driver, wait)

    def _exec(self):
        Logger.Info("CreateSecondAccount()")

        Actions.OpenUrl(self, URLs.Metamask_NewAccount)

        Actions.Input(self, By.XPATH, "/html/body/div[1]/div/div[3]/div/div/div[2]/input", "scroll2")

        while True:
            try:
                Actions.WaitAttributeChanged(self, By.XPATH, "/html/body/div[1]/div/div[3]/div/div/div[2]/input", "value", "scroll2", True)
                break
            except:
                pass

        Actions.Click(self, By.XPATH, "//button[text()='Create']")
