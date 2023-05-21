from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from Automizer.Scenario import Scenario


class ClickResult:
    def __init__(self):
        self._new_window = None
        self._old_window = None

    @property
    def New_Window(self) -> str:
        return self._new_window

    @New_Window.setter
    def New_Window(self, value: str):
        self._new_window = value

    @property
    def Old_Window(self) -> str:
        return self._old_window

    @Old_Window.setter
    def Old_Window(self, value: str):
        self._old_window = value


def Click(scenario: Scenario,
          by: By,
          path: str,
          as_script: bool = False,
          shadow_root: WebElement = None,
          is_opening_window: bool = False) -> ClickResult:
    result: ClickResult = ClickResult()
    win_count = scenario.Driver.window_handles.__len__()

    def _run():
        button: WebElement = scenario.Wait.until(EC.visibility_of_element_located((by, path)))

        if as_script:
            scenario.Driver.execute_script("arguments[0].click();", button)
        else:
            try:
                button.click()
            except ElementClickInterceptedException:
                button = scenario.Wait.until(EC.element_to_be_clickable((by, path)))
                button.click()

    def _shadow_run():
        if by != By.CSS_SELECTOR:
            raise AttributeError("Use only css selector")
        button: WebElement = shadow_root.find_element(by, path)
        button.click()

    if shadow_root is None:
        _run()
    else:
        _shadow_run()

    if is_opening_window:
        scenario.Wait.until(EC.number_of_windows_to_be(win_count + 1))
        result.Old_Window = scenario.Driver.current_window_handle
        result.New_Window = scenario.Driver.window_handles[-1]

    return result
