from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from Automizer.ExecEnvironment import ExecEnvironment


def Selector(env: ExecEnvironment,
             by: By,
             path: str,
             option: str):
    attempt = 1
    while attempt <= 3:
        try:
            select_element: Select = Select(env.Wait.until(EC.visibility_of_element_located((by, path))))
            select_element.select_by_value(option)
            break
        except StaleElementReferenceException:
            attempt = attempt + 1
