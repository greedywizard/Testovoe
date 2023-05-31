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

    def _exec(self, args=None):
        Logger.Info("CreateSecondAccount()")

        Actions.OpenUrl(self, URLs.Metamask_NewAccount)

        # Ввести название
        Actions.Input(self, By.XPATH, "/html/body/div[1]/div/div[3]/div/div/div[2]/input", "scroll2")
        # Получить значение из input
        Actions.GetElement(self, By.XPATH, "/html/body/div[1]/div/div[3]/div/div/div[2]/input[@value='scroll2']")
        # "Create"
        Actions.Click(self, By.XPATH, "//button[text()='Create']", as_script=True)
