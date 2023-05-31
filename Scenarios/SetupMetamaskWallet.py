import URLs
from selenium.webdriver.common.by import By

from Automizer.Logger import Logger
from Automizer.Scenario import Scenario
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
import Automizer.Actions as Actions


class SetupMetamaskWallet(Scenario):
    def __init__(self,
                 driver: WebDriver,
                 wait: WebDriverWait):
        super().__init__(driver, wait)

    def _exec(self):
        Logger.Info("SetupMetamaskWallet()")

        Actions.OpenUrl(self, url=URLs.Metamask_Settings_Advance)

        Actions.Click(self, By.XPATH, "/html/body/div[1]/div/div[3]/div/div[2]/div[2]/div[2]/div[5]/div[2]/div/label/div[1]/div[1]/div[2]")
        Actions.Click(self, By.XPATH, "/html/body/div[1]/div/div[3]/div/div[1]/div[1]/div[2]")
        Actions.Click(self, By.XPATH, "//div[@data-testid='network-display']", as_script=True)
        Actions.Click(self, By.XPATH, "//li[.//span[text()='Goerli test network']]", as_script=True)
