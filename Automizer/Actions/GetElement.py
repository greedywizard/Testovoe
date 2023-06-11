from selenium.common import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from Automizer.ExecEnvironment import ExecEnvironment


class GetElementResult:
    def __init__(self):
        self._element = None

    @property
    def Element(self) -> WebElement:
        return self._element

    @Element.setter
    def Element(self, value: WebElement):
        self._element = value


def GetElement(env: ExecEnvironment,
               by: By,
               path: str,
               is_visible: bool = True) -> GetElementResult:
    result: GetElementResult = GetElementResult()

    attempt = 1
    while attempt <= 3:
        try:
            if is_visible:
                result.Element = env.Wait.until(EC.visibility_of_element_located((by, path)))
            else:
                result.Element = env.Wait.until(EC.presence_of_element_located((by, path)))
            break
        except TimeoutException:
            result.Element = None
        except StaleElementReferenceException:
            attempt = attempt + 1

    return result
