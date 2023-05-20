import URLs
from selenium.webdriver.common.by import By
from Automizer.Scenario import Scenario
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
import Automizer.Actions as Actions


class SetupMetamaskWallet(Scenario):
    def __init__(self,
                 driver: WebDriver,
                 wait: WebDriverWait):
        super().__init__(driver, wait)

    def Exec(self):
        Actions.OpenUrl(self, url=URLs.Metamask_Settings_Advance).Exec()

        Actions.Click(self, By.XPATH, "/html/body/div[1]/div/div[3]/div/div[2]/div[2]/div[2]/div[5]/div[2]/div/label/div[1]/div[1]/div[2]").Exec()
        Actions.Click(self, By.XPATH, "/html/body/div[1]/div/div[3]/div/div[1]/div[1]/div[2]").Exec()
