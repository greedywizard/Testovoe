import time
from selenium.common import NoAlertPresentException
from selenium.webdriver.common.by import By

from Automizer.Logger import Logger
from Automizer.Scenario import Scenario, ScenarioResult
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
import Automizer.Actions as Actions
import URLs
import random
import string
from selenium.common import NoAlertPresentException
from selenium.webdriver.common.by import By
from Automizer.Scenario import Scenario, ScenarioResult
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait


class CreateToken(Scenario):
    def __init__(self,
                 driver: WebDriver,
                 wait: WebDriverWait):
        super().__init__(driver, wait)

    def Exec(self, args=None):
        Logger.Info("CreateToken()")
        result: ScenarioResult = ScenarioResult()

        Actions.OpenUrl(self, URLs.OpenZeppelin_Wizard)

        Actions.AcceptAlert(self)

        iframe = Actions.GetElement(self, By.XPATH, "/html/body/div[1]/main/div/article/oz-wizard/iframe")
        self.Driver.switch_to.frame(iframe)
        # "Mintable"
        Actions.Click(self, By.XPATH, "/html/body/div/div[2]/div[1]/div[1]/section[2]/div/label[1]/input")
        # очистить поле
        Actions.GetElement(self, By.XPATH, "/html/body/div/div[2]/div[1]/div[1]/section[1]/div/label[2]/input").Element.clear()
        # 3 рандомные буквы
        random_letter = ''.join(random.choices(string.ascii_uppercase, k=3))
        result.ResultData["name"] = random_letter
        Actions.Input(self, By.XPATH, "/html/body/div/div[2]/div[1]/div[1]/section[1]/div/label[2]/input", random_letter)
        # много денях
        Actions.Input(self, By.XPATH, "/html/body/div/div[2]/div[1]/div[1]/section[1]/label/input", str(2124221))
        # Получить код контракта
        result.ResultData["code"] = Actions.GetElement(self, By.XPATH, "/html/body/div/div[2]/div[2]/pre/code").Element.text
        self.Driver.switch_to.default_content()

        return result
