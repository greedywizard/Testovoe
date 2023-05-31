from abc import ABC, abstractmethod
from typing import List, final
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait


class Scenario(ABC):
    def __init__(self, driver: WebDriver, wait: WebDriverWait):
        self._driver: WebDriver = driver
        self._wait: WebDriverWait = wait

        self._active_window: str = driver.current_window_handle

    @property
    def Driver(self) -> WebDriver:
        return self._driver

    @property
    def Wait(self) -> WebDriverWait:
        return self._wait

    @property
    def Active_Window(self):
        return self._active_window

    @Active_Window.setter
    def Active_Window(self, value: str):
        self.Driver.switch_to.window(value)
        self._active_window = value

    @final
    def Run(self, skip=False):
        if not skip:
            self._exec()

    @abstractmethod
    def _exec(self):
        pass


class Repeater:
    def __init__(self, scenario: Scenario, args=None):
        self.__args = args
        self.__scenario = scenario

    @property
    def Scenario(self) -> Scenario:
        return self.__scenario

    @property
    def Args(self):
        return self.__args


