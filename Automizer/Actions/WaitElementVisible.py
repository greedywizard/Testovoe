from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from Automizer.Scenario import Scenario


class WaitElementVisibleResult:
    pass


def WaitElementVisible(scenario: Scenario,
                       by: By,
                       path: str,
                       hide: bool = False) -> WaitElementVisibleResult:
    result: WaitElementVisibleResult = WaitElementVisibleResult()

    if hide:
        scenario.Wait.until_not(EC.visibility_of_element_located((by, path)))
    else:
        scenario.Wait.until(EC.visibility_of_element_located((by, path)))

    return result
