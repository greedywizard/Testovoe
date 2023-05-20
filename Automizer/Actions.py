from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.webdriver import WebDriver
from Automizer.Scenario import Scenario
from abc import ABC, abstractmethod
from typing import final


class Action(ABC):
    def __init__(self, scenario: Scenario, as_script: bool, shadow_root: WebElement):
        self._as_script: bool = as_script
        self._scenario: Scenario = scenario
        self._shadow_root: WebElement = shadow_root

    @final
    def Exec(self):
        if self._scenario.Active_Window != self._scenario.Driver.current_window_handle:
            self._scenario.Driver.switch_to.window(self._scenario.Active_Window)

        if self._shadow_root is None:
            return self._run()
        else:
            return self._shadow_run()

    @abstractmethod
    def _run(self):
        pass

    @abstractmethod
    def _shadow_run(self):
        pass


class Click(Action):
    def __init__(self,
                 scenario: Scenario,
                 by: By,
                 path: str,
                 shadow_root: WebElement = None,
                 as_script: bool = False,
                 is_opening_window: bool = False):
        super().__init__(scenario, as_script, shadow_root)
        self.__is_opening_window: bool = is_opening_window
        self.__win_count: int = 1
        self.__by = by
        self.__path = path
        self.__new_window = None
        self.__old_window = None

    def _run(self):
        self.__win_count = self._scenario.Driver.window_handles.__len__()
        button: WebElement = self._scenario.Wait.until(EC.visibility_of_element_located((self.__by, self.__path)))

        if self._as_script:
            self._scenario.Driver.execute_script("arguments[0].click();", button)
        else:
            try:
                button.click()
            except ElementClickInterceptedException:
                button = self._scenario.Wait.until(EC.element_to_be_clickable((self.__by, self.__path)))
                button.click()

        if self.__is_opening_window:
            self._scenario.Wait.until(EC.number_of_windows_to_be(self.__win_count + 1))
            self.__new_window = self._scenario.Driver.window_handles[-1]
            self.__old_window = self._scenario.Driver.current_window_handle

        return self

    def _shadow_run(self):
        self.__win_count = self._scenario.Driver.window_handles.__len__()

        if self.__by != By.CSS_SELECTOR:
            raise AttributeError("Use only css selector")
        button: WebElement = self._shadow_root.find_element(self.__by, self.__path)
        button.click()

        if self.__is_opening_window:
            self._scenario.Wait.until(EC.number_of_windows_to_be(self.__win_count + 1))
            self.__new_window = self._scenario.Driver.window_handles[-1]
            self.__old_window = self._scenario.Driver.current_window_handle

        return self

    @property
    def New_Window(self) -> str:
        return self.__new_window

    @property
    def Old_Window(self) -> str:
        return self.__old_window


class GetElement(Action):
    def __init__(self,
                 scenario: Scenario,
                 by: By,
                 path: str,
                 shadow_root: WebElement = None,
                 as_script: bool = False):
        super().__init__(scenario, as_script, shadow_root)
        self.__by = by
        self.__path = path
        self._element = None

    def _run(self):
        self._scenario.Wait.until(EC.visibility_of_element_located((self.__by, self.__path)))
        return self

    def _shadow_run(self):
        pass

    @property
    def Element(self) -> WebElement:
        return self._element


class Selector(Action):
    def __init__(self,
                 scenario: Scenario,
                 by: By,
                 path: str,
                 option: str,
                 shadow_root: WebElement = None,
                 as_script: bool = False):
        super().__init__(scenario, as_script, shadow_root)
        self.__by = by
        self.__path = path
        self.__option = option

    def _run(self):
        select_element: Select = Select(self._scenario.Wait.until(EC.visibility_of_element_located((self.__by, self.__path))))
        select_element.select_by_value(self.__option)
        return self

    def _shadow_run(self):
        pass


class Input(Action):
    def __init__(self,
                 scenario: Scenario,
                 by: By,
                 path: str,
                 data: str,
                 shadow_root: WebElement = None,
                 as_script: bool = False):
        super().__init__(scenario, as_script, shadow_root)
        self.__by = by
        self.__path = path
        self.__data = data

    def _run(self):
        input_element: WebElement = self._scenario.Wait.until(EC.element_to_be_clickable((self.__by, self.__path)))
        input_element.send_keys(self.__data)
        return self

    def _shadow_run(self):
        pass


class WaitElementVisible(Action):
    def __init__(self,
                 scenario: Scenario,
                 by: By,
                 path: str,
                 data: str,
                 shadow_root: WebElement = None,
                 hide: bool = False,
                 as_script: bool = False):
        super().__init__(scenario, as_script, shadow_root)
        self.__by = by
        self.__path = path
        self.__data = data
        self.__hide = hide

    def _run(self):
        if self.__hide:
            self._scenario.Wait.until_not(EC.visibility_of_element_located((self.__by, self.__path)))
        else:
            self._scenario.Wait.until(EC.visibility_of_element_located((self.__by, self.__path)))

        return self

    def _shadow_run(self):
        pass


class OpenUrl(Action):
    def __init__(self,
                 scenario: Scenario,
                 url: str,
                 in_new_window: bool = False,
                 as_script: bool = False):
        super().__init__(scenario, as_script, None)
        self.__url = url
        self.__in_new_window = in_new_window
        self.__new_window = None
        self.__cur_window = None

    def _run(self):
        if self.__in_new_window:
            self.__cur_window = self._scenario.Driver.current_window_handle
            self._scenario.Driver.execute_script("window.open('');")
            self.__new_window = self._scenario.Driver.window_handles[-1]
            self._scenario.Driver.switch_to.window(self.__new_window)

        if not self._as_script:
            self._scenario.Driver.get(self.__url)
        else:
            self._scenario.Driver.execute_script(f"window.location.href = '{self.__url}';")

        if self.__in_new_window:
            self._scenario.Driver.switch_to.window(self.__cur_window)

        return self

    def _shadow_run(self):
        pass

    @property
    def New_Window(self) -> str:
        return self.__new_window

    @property
    def Current_Window(self) -> str:
        return self.__cur_window


def GetShadowRoot(wait: WebDriverWait, driver: WebDriver, by: By, path: str) -> WebElement:
    shadow_host = wait.until(EC.presence_of_element_located((by, path)))
    return driver.execute_script('return arguments[0].shadowRoot', shadow_host)
