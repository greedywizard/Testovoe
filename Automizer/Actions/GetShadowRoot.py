from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from Automizer.ExecEnvironment import ExecEnvironment


class GetShadowRootResult:
    def __init__(self):
        self.__element = None

    @property
    def Element(self) -> WebElement:
        return self.__element

    @Element.setter
    def Element(self, value: WebElement):
        self.__element = value


def GetShadowRoot(env: ExecEnvironment,
                  by: By,
                  path: str) -> GetShadowRootResult:
    result: GetShadowRootResult = GetShadowRootResult()

    shadow_host = None
    attempt = 1
    while attempt <= 3:
        try:
            shadow_host = env.Wait.until(EC.presence_of_element_located((by, path)))
            break
        except StaleElementReferenceException:
            attempt = attempt + 1

    result.Element = env.Driver.execute_script('return arguments[0].shadowRoot', shadow_host)

    return result

