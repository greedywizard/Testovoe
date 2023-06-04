import time
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By

from Automizer.Enums import WindowActions
from Automizer.Logger import Logger
from Automizer.Scenario import Scenario
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
import Automizer.Actions as Actions
import URLs


class Subscribe(Scenario):
    class Data:
        def __init__(self):
            self.discord_login = None
            self.discord_pass = None
            self.twitter_login = None
            self.twitter_pass = None

    def __init__(self,
                 driver: WebDriver,
                 wait: WebDriverWait,
                 data: Data):
        super().__init__(driver, wait)
        self.__data = data

    def _exec(self):
        Logger.Info("Subscribe()")

        Actions.OpenUrl(self, URLs.Guild)

        Actions.Click(self, By.XPATH, "//span[text()='Connect to a wallet']")
        res = Actions.Click(self, By.XPATH, "//span[text()='MetaMask']", window_action=WindowActions.Open)
        self.Active_Window = res.New_Window
        Actions.Click(self, By.XPATH, "//button[text()='Next']")
        Actions.Click(self, By.XPATH, "//button[text()='Connect']", window_action=WindowActions.WaitClose)
        self.Active_Window = res.Old_Window
        res = Actions.Click(self, By.XPATH, "//span[text()='Verify account']", window_action=WindowActions.Open)
        self.Active_Window = res.New_Window
        Actions.Click(self, By.XPATH, "//button[@data-testid='page-container-footer-next']", window_action=WindowActions.WaitClose)
        self.Active_Window = res.Old_Window
        Actions.Click(self, By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/div[1]/button[2]")

        # Дискорд
        res = Actions.Click(self, By.XPATH, "//div[p[contains(text(), 'Discord')]]/button", window_action=WindowActions.Open)
        self.Active_Window = res.New_Window
        Actions.Input(self, By.ID, "uid_6", self.__data.discord_login)
        Actions.Input(self, By.ID, "uid_8", self.__data.discord_pass)
        Actions.Click(self, By.XPATH, "//button[.//div[text()='Log In']]")
        Actions.Click(self, By.XPATH, "//button[.//div[text()='Authorize']]", window_action=WindowActions.WaitClose)
        self.Active_Window = res.Old_Window

        res = Actions.Click(self, By.XPATH, "//div[p[contains(text(), 'Twitter')]]/button", window_action=WindowActions.Open)
        self.Active_Window = res.New_Window
        Actions.Click(self, By.XPATH, "//a[@data-testid='OAuth_Consent_Log_In_Button']")
        Actions.Input(self, By.XPATH, "/html/body/div/div/div/div/main/div/div/div/div[2]/div[2]/div/div[5]/label/div/div[2]/div/input", self.__data.twitter_login)
        Actions.Click(self, By.XPATH, "//span[text()='Next']")
        Actions.Input(self, By.XPATH, "/html/body/div/div/div/div/main/div/div/div/div[2]/div[2]/div[1]/div/div/div/div[3]/div/label/div/div[2]/div[1]/input",
                      self.__data.twitter_pass)
        Actions.Click(self, By.XPATH, "//span[text()='Log in']")
        Actions.Click(self, By.XPATH, "//div[@data-testid='OAuth_Consent_Button']", window_action=WindowActions.WaitClose)
        self.Active_Window = res.Old_Window
