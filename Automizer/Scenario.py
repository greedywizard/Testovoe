from abc import ABC
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait


class Scenario(ABC):
    def __init__(self, driver: WebDriver, wait: WebDriverWait):
        self._driver: WebDriver = driver
        self._wait: WebDriverWait = wait

    @property
    def Driver(self) -> WebDriver:
        return self._driver

    @property
    def Wait(self) -> WebDriverWait:
        return self._wait
