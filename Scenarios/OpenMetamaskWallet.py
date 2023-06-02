from selenium.webdriver.common.by import By
import URLs
from Automizer.Logger import Logger
from Automizer.Scenario import Scenario
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
import Automizer.Actions as Actions


class OpenMetamaskWallet(Scenario):
    class Data:
        def __init__(self):
            self.seed: str = None

    def __init__(self,
                 driver: WebDriver,
                 wait: WebDriverWait,
                 data:Data):
        super().__init__(driver, wait)
        self.__data = data

    def _exec(self):
        Logger.Info("Start OpenMetamaskWallet()")

        Actions.OpenUrl(self, url=URLs.Metamask_Home)

        while True:
            try:
                Logger.Info("Try import wallet...")
                Actions.Click(self, By.ID, "onboarding__terms-checkbox")
                Actions.Click(self, By.XPATH, "//button[@data-testid='onboarding-import-wallet']")
                break
            except:
                self.Driver.refresh()

        Actions.Click(self, By.XPATH, "//button[@data-testid='metametrics-i-agree']")

        seed_arr = self.__data.seed.split(' ')
        for i in range(seed_arr.__len__()):
            Actions.Input(self, By.ID, f"import-srp__srp-word-{i}", seed_arr[i])

        Actions.Click(self, By.XPATH, "//button[@data-testid='import-srp-confirm']")

        password: str = '12345678'
        Actions.Input(self, By.XPATH, "//input[@data-testid='create-password-new']", password)
        Actions.Input(self, By.XPATH, "//input[@data-testid='create-password-confirm']", password)
        Actions.Click(self, By.XPATH, "//input[@data-testid='create-password-terms']")
        Actions.Click(self, By.XPATH, "//button[@data-testid='create-password-import']")

        while True:
            try:
                Logger.Info("Try complete import...")
                # "Got it"
                Actions.Click(self, By.XPATH, "//button[@data-testid='onboarding-complete-done']")
                break
            except:
                pass

        Actions.Click(self, By.XPATH, "//button[@data-testid='pin-extension-next']")
        Actions.Click(self, By.XPATH, "//button[@data-testid='pin-extension-done']")
