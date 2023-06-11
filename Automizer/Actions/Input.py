from selenium.common import InvalidElementStateException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from Automizer.ExecEnvironment import ExecEnvironment


def Input(env: ExecEnvironment,
          by: By,
          path: str,
          data: str):
    input_element = None

    attempt = 1
    while attempt <= 3:
        try:
            input_element: WebElement = env.Wait.until(EC.visibility_of_element_located((by, path)) and EC.element_to_be_clickable((by, path)))
            break
        except StaleElementReferenceException:
            attempt = attempt + 1

    try:
        input_element.clear()
    except InvalidElementStateException:
        pass

    input_element.send_keys(data)
