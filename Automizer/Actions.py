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


class Click(Action):
    def __init__(self,
                 scenario: Scenario,
                 as_script: bool = False,
                 is_opening_window: bool = False):
        super().__init__(scenario, as_script)
        self.__is_opening_window: bool = is_opening_window
        self.__win_count: int = 1
        self.__new_window = None

    def Exec(self, by: By, path: str):
        button: WebElement = self._scenario.Wait.until(EC.visibility_of_element_located((by, path)))
        self.__win_count = self._scenario.Driver.window_handles.__len__()

        if self._scenario.Active_Window != self._scenario.Driver.current_window_handle:
            self._scenario.Driver.switch_to.window(self._scenario.Active_Window)

        if self._as_script:
            self._scenario.Driver.execute_script("arguments[0].click();", button)
        else:
            try:
                button.click()
            except ElementClickInterceptedException:
                button = self._scenario.Wait.until(EC.element_to_be_clickable((by, path)))
                button.click()

        if self.__is_opening_window:
            self._scenario.Wait.until(EC.number_of_windows_to_be(self.__win_count + 1))
            self.__new_window = self._scenario.Driver.window_handles[-1]

        return self

    @property
    def New_Window(self) -> str:
        return self.__new_window


class GetElement(Action):
    def __init__(self,
                 scenario: Scenario,
                 as_script: bool = False):
        super().__init__(scenario, as_script)
        self._element = None

    def Exec(self, b: By, path: str):
        self._scenario.Wait.until(EC.visibility_of_element_located((b, path)))
        return self

    @property
    def Element(self) -> WebElement:
        return self._element


class Selector(Action):
    pass

