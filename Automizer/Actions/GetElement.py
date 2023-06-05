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


def GetElement(scenario: ExecEnvironment,
               by: By,
               path: str) -> GetElementResult:
    result: GetElementResult = GetElementResult()
    result.Element = scenario.Wait.until(EC.visibility_of_element_located((by, path)))

    return result
