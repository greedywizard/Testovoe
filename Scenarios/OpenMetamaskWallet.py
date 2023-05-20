from selenium.webdriver.common.by import By
from Automizer.Scenario import Scenario
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
import Automizer.Actions as Actions
import URLs

class OpenMetamaskWallet(Scenario):
    def __init__(self,
                 driver: WebDriver,
                 wait: WebDriverWait,
                 seed_phrase: str):
        super().__init__(driver, wait)
        self.__sp = seed_phrase

    def Exec(self):
        Actions.OpenUrl(self, url=URLs.Metamask_Home).Exec()

        while True:
            try:
                Actions.Click(self, By.ID, "onboarding__terms-checkbox").Exec()
                Actions.Click(self, By.XPATH, "//button[@data-testid='onboarding-import-wallet']").Exec()
                break
            except:
                self.Driver.refresh()

        Actions.Click(self, By.XPATH, "//button[@data-testid='metametrics-i-agree']").Exec()

        seed_arr = self.__sp.split(' ')
        for i in range(seed_arr.__len__()):
            Actions.Input(self, By.ID, f"import-srp__srp-word-{i}", seed_arr[i]).Exec()

        Actions.Click(self, By.XPATH, "//button[@data-testid='import-srp-confirm']").Exec()

        password: str = '12345678'
        Actions.Input(self, By.XPATH, "//input[@data-testid='create-password-new']", password).Exec()
        Actions.Input(self, By.XPATH, "//input[@data-testid='create-password-confirm']", password).Exec()
        # Чекбокс
        Actions.Click(self, By.XPATH, "//input[@data-testid='create-password-terms']").Exec()
        # "Import"
        Actions.Click(self, By.XPATH, "//button[@data-testid='create-password-import']").Exec()

        while True:
            try:
                # "Got it"
                Actions.Click(self, By.XPATH, "//button[@data-testid='onboarding-complete-done']").Exec()
                break
            except:
                pass

        Actions.Click(self, By.XPATH, "//button[@data-testid='pin-extension-next']").Exec()
        Actions.Click(self, By.XPATH, "//button[@data-testid='pin-extension-done']").Exec()
