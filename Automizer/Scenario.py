from abc import ABC, abstractmethod
from typing import List

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

    @abstractmethod
    def Exec(self, args=None) -> 'ScenarioResult':
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


class ScenarioResult:
    def __init__(self):
        self.__result = dict()
        self.__args = None
        self.__pre_scenarios = None

    @property
    def PreScenarios(self) -> List[Repeater]:
        return self.__pre_scenarios

    @PreScenarios.setter
    def PreScenarios(self, value: List[Repeater]):
        self.__pre_scenarios = value

    @property
    def ResultData(self) -> dict:
        return self.__result

