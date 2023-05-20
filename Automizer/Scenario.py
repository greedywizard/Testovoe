from abc import ABC, abstractmethod
from typing import final

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
        self._active_window = value

    @abstractmethod
    def _run(self):
        pass

    @final
    def Exec(self):
        self._run()

        v = self.Driver.current_window_handle

        if self.Active_Window != self.Driver.current_window_handle:
            self.Driver.switch_to.window(self.Active_Window)
