import time
from selenium.webdriver import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchWindowException, ElementNotInteractableException
from Scenario import Scenario
from abc import ABC


class Action(ABC):
    def __init__(self, scenario: Scenario, as_script: bool = False):
        self._as_script: bool = as_script
        self._scenario: Scenario = scenario

    def Exec(self):
        pass


class Click(Action):
    def __init__(self,
                 scenario: Scenario,
                 by: By,
                 path: str,
                 as_script: bool = False):
        super().__init__(scenario, as_script)
        self.__by = by
        self.__path = path

    def Exec(self):
        button: WebElement = self._scenario.Wait.until(EC.visibility_of_element_located((self.__by, self.__path)))

        if self._as_script:
            self._scenario.Driver.execute_script("arguments[0].click();", button)
        else:
            try:
                button.click()
            except ElementClickInterceptedException:
                button = self._scenario.Wait.until(EC.element_to_be_clickable((self.__by, self.__path)))
                button.click()


class GetElement(Action):
    pass


class WaitAnimation(Action):
    pass


class