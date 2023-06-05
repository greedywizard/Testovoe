from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from Automizer.ExecEnvironment import ExecEnvironment


class GetElementsResult:
    def __init__(self):
        self.__elements = None

    @property
    def Elements(self) -> List[WebElement]:
        return self.__elements

    @Elements.setter
    def Elements(self, value: WebElement):
        self.__elements = value

    @property
    def ElementsCount(self) -> int:
        return len(self.__elements)


def GetElements(scenario: ExecEnvironment,
                by: By,
                path: str) -> GetElementsResult:
    result: GetElementsResult = GetElementsResult()

    result.Elements = scenario.Driver.find_elements(by, path)

    return result
