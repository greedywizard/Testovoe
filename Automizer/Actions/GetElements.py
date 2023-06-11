from typing import List

from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from Automizer.ExecEnvironment import ExecEnvironment
from selenium.webdriver.support import expected_conditions as EC


class GetElementsResult:
    def __init__(self):
        self.__elements = []

    @property
    def Elements(self) -> List[WebElement]:
        return self.__elements

    @Elements.setter
    def Elements(self, value: WebElement):
        self.__elements = value

    @property
    def ElementsCount(self) -> int:
        return len(self.__elements)


def GetElements(env: ExecEnvironment,
                by: By,
                path: str) -> GetElementsResult:
    result: GetElementsResult = GetElementsResult()

    attempt = 1
    while attempt <= 3:
        try:
            result.Elements = env.Wait.until(EC.presence_of_all_elements_located((by, path)))
            break
        except StaleElementReferenceException:
            attempt = attempt + 1
        except:
            result.Elements = []

    return result
