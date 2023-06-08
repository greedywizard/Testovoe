from selenium.common import InvalidElementStateException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from Automizer.ExecEnvironment import ExecEnvironment


def Input(scenario: ExecEnvironment,
          by: By,
          path: str,
          data: str):
    input_element: WebElement = scenario.Wait.until(EC.visibility_of_element_located((by, path)) and EC.element_to_be_clickable((by, path)))
    try:
        input_element.clear()
    except InvalidElementStateException:
        pass
    input_element.send_keys(data)
