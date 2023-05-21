from selenium.webdriver.common.by import By

import URLs
from Automizer.Scenario import Scenario
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
import Automizer.Actions as Actions


class OpenMetamaskWallet(Scenario):
    def __init__(self,
                 driver: WebDriver,
                 wait: WebDriverWait,
                 seed_phrase: str):
        super().__init__(driver, wait)
        self.__sp = seed_phrase

    def Exec(self):
        Actions.OpenUrl(self, url=URLs.Metamask_Home)

        while True:
            try:
                Actions.Click(self, By.ID, "onboarding__terms-checkbox")
                Actions.Click(self, By.XPATH, "//button[@data-testid='onboarding-import-wallet']")
                break
            except:
                self.Driver.refresh()

        Actions.Click(self, By.XPATH, "//button[@data-testid='metametrics-i-agree']")

        seed_arr = self.__sp.split(' ')
        for i in range(seed_arr.__len__()):
            Actions.Input(self, By.ID, f"import-srp__srp-word-{i}", seed_arr[i])

        Actions.Click(self, By.XPATH, "//button[@data-testid='import-srp-confirm']")

        password: str = '12345678'
        Actions.Input(self, By.XPATH, "//input[@data-testid='create-password-new']", password)
        Actions.Input(self, By.XPATH, "//input[@data-testid='create-password-confirm']", password)
        # Чекбокс
        Actions.Click(self, By.XPATH, "//input[@data-testid='create-password-terms']")
        # "Import"
        Actions.Click(self, By.XPATH, "//button[@data-testid='create-password-import']")

        while True:
            try:
                # "Got it"
                Actions.Click(self, By.XPATH, "//button[@data-testid='onboarding-complete-done']")
                break
            except:
                pass

        Actions.Click(self, By.XPATH, "//button[@data-testid='pin-extension-next']")
        Actions.Click(self, By.XPATH, "//button[@data-testid='pin-extension-done']")
