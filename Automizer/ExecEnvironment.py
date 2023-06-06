from abc import ABC, abstractmethod
from typing import List, final
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait


class ExecEnvironment:
    def __init__(self, driver: WebDriver, wait: WebDriverWait):
        self._driver: WebDriver = driver
        self._wait: WebDriverWait = wait
        self._active_window: str = driver.current_window_handle
        self._prev_window: str = None
        self._new_window: str = None

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

    @property
    def Previous_Window(self):
        return self._prev_window

    @Previous_Window.setter
    def Previous_Window(self, value: str):
        self._prev_window = value

    @property
    def New_Window(self):
        return self._new_window

    @New_Window.setter
    def New_Window(self, value: str):
        self._new_window = value
