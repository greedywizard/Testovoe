from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException

from Automizer.Logger import Logger
from Automizer.ExecEnvironment import ExecEnvironment
from Automizer.Enums import WindowActions


class ClickResult:
    def __init__(self):
        self.__new_window = None
        self.__old_window = None

    @property
    def New_Window(self) -> str:
        return self.__new_window

    @New_Window.setter
    def New_Window(self, value: str):
        self.__new_window = value

    @property
    def Prev_Window(self) -> str:
        return self.__old_window

    @Prev_Window.setter
    def Prev_Window(self, value: str):
        self.__old_window = value


def Click(env: ExecEnvironment,
          by: By,
          path: str,
          as_script: bool = False,
          is_visible: bool = True,
          is_clickable: bool = True,
          shadow_root: WebElement = None,
          window_action: WindowActions = None) -> ClickResult:
    """
    Имитирует нажатие на элемент
    """

    result: ClickResult = ClickResult()
    win_count = env.Driver.window_handles.__len__()

    def _run():
        if is_visible:
            button = env.Wait.until(EC.visibility_of_element_located((by, path)))
        else:
            button = env.Wait.until(EC.presence_of_element_located((by, path)))

        if is_clickable and not button.is_enabled():
            button = env.Wait.until(EC.element_to_be_clickable((by, path)))

        if not button:
            raise ElementClickInterceptedException

        try:
            if as_script:
                env.Driver.execute_script("arguments[0].click();", button)
            else:
                button.click()
        except ElementClickInterceptedException:
            button = env.Wait.until(EC.element_to_be_clickable((by, path)))
            if as_script:
                env.Driver.execute_script("arguments[0].click();", button)
            else:
                button.click()

    def _shadow_run():
        if by != By.CSS_SELECTOR:
            raise AttributeError("Use only css selector")
        button: WebElement = shadow_root.find_element(by, path)
        button.click()

    attempt = 1
    while attempt <= 3:
        try:
            if shadow_root is None:
                _run()
            else:
                _shadow_run()
            break
        except StaleElementReferenceException:
            attempt = attempt + 1

    if window_action == WindowActions.Open:
        try:
            env.Wait.until(EC.number_of_windows_to_be(win_count + 1))
        except:
            pass
        result.Prev_Window = env.Driver.current_window_handle
        result.New_Window = env.Driver.window_handles[-1]
        env.Active_Window = result.New_Window
        env.Previous_Window = result.Prev_Window
        env.New_Window = result.New_Window

    if window_action == WindowActions.WaitClose:
        env.Wait.until(EC.number_of_windows_to_be(win_count - 1))
        env.Active_Window = env.Previous_Window

    return result
