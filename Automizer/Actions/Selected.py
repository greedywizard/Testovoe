from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from Automizer.Scenario import Scenario


class SelectedResult:
    pass


def Selected(scenario: Scenario,
             by: By,
             path: str,
             option: str) -> SelectedResult:
    result: SelectedResult = SelectedResult()

    select_element: Select = Select(scenario.Wait.until(EC.visibility_of_element_located((by, path))))
    select_element.select_by_value(option)

    return result
