from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from Automizer.ExecEnvironment import ExecEnvironment


def Selector(scenario: ExecEnvironment,
             by: By,
             path: str,
             option: str):
    select_element: Select = Select(scenario.Wait.until(EC.visibility_of_element_located((by, path))))
    select_element.select_by_value(option)
