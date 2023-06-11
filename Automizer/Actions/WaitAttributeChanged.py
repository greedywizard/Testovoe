from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, JavascriptException, StaleElementReferenceException
from Automizer.ExecEnvironment import ExecEnvironment


def WaitAttributeChanged(env: ExecEnvironment,
                         by: By,
                         path: str,
                         attribute: str,
                         attr_value: str,
                         equal: bool = False):
    attempt = 1
    while attempt <= 3:
        try:
            element = env.Wait.until(EC.visibility_of_element_located((by, path)))
            break
        except StaleElementReferenceException:
            attempt = attempt + 1

    if equal:
        try:
            env.Wait.until(lambda x: element.get_attribute(attribute) == attr_value)
        except JavascriptException:
            env.Wait.until(lambda x: env.Driver.execute_script(f"return arguments[0].{attribute};", element) == attr_value)

    else:
        try:
            env.Wait.until(lambda x: element.get_attribute(attribute) != attr_value)
        except JavascriptException:
            env.Wait.until(lambda x: env.Driver.execute_script(f"return arguments[0].{attribute};", element) != attr_value)
