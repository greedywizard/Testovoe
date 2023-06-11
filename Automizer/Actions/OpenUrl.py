from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from Automizer.ExecEnvironment import ExecEnvironment


class OpenUrlResult:
    def __init__(self):
        self.__old_window = None
        self.__new_window = None

    @property
    def New_Window(self) -> str:
        return self.__new_window

    @property
    def Old_Window(self) -> str:
        return self.__old_window

    @New_Window.setter
    def New_Window(self, value: str):
        self.__new_window = value

    @Old_Window.setter
    def Old_Window(self, value: str):
        self.__old_window = value


def OpenUrl(env: ExecEnvironment,
            url: str,
            in_new_window: bool = False,
            as_script: bool = False) -> OpenUrlResult:
    result: OpenUrlResult = OpenUrlResult()

    if in_new_window:
        result.Old_Window = env.Driver.current_window_handle
        env.Driver.execute_script("window.open('');")
        result.New_Window = env.Driver.window_handles[-1]
        env.Driver.switch_to.window(result.New_Window)

    if not as_script:
        env.Driver.get(url)
    else:
        env.Driver.execute_script(f"window.location.href = '{url}';")

    return result
