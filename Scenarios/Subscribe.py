import time
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By

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
