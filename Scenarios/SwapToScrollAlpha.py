import time
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from Automizer.Scenario import Scenario, ScenarioResult
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
import Automizer.Actions as Actions
import URLs


class SwapToScrollAlpha(Scenario):
    def __init__(self,
                 driver: WebDriver,
                 wait: WebDriverWait):
        super().__init__(driver, wait)

    def Exec(self, args=None):
        result: ScenarioResult = ScenarioResult()

        Actions.OpenUrl(self, URLs.Metamask_Home)

        # Открыть свиписок сетей
        Actions.Click(self, By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div/div', as_script=True)
        # Выбрать сеть goerli
        Actions.Click(self, By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/li[.//span[text()="Scroll Alpha"]]', as_script=True)

        return result
