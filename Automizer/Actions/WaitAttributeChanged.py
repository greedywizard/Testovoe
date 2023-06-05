from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, JavascriptException
from Automizer.ExecEnvironment import ExecEnvironment


def WaitAttributeChanged(scenario: ExecEnvironment,
                         by: By,
                         path: str,
                         attribute: str,
                         attr_value: str,
                         equal: bool = False):
    element = scenario.Wait.until(EC.visibility_of_element_located((by, path)))

    if equal:
        try:
            scenario.Wait.until(lambda x: element.get_attribute(attribute) == attr_value)
        except JavascriptException:
            scenario.Wait.until(lambda x: scenario.Driver.execute_script(f"return arguments[0].{attribute};", element) == attr_value)

    else:
        try:
            scenario.Wait.until(lambda x: element.get_attribute(attribute) != attr_value)
        except JavascriptException:
            scenario.Wait.until(lambda x: scenario.Driver.execute_script(f"return arguments[0].{attribute};", element) != attr_value)
