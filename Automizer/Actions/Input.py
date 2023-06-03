from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from Automizer.Scenario import Scenario


def Input(scenario: Scenario,
          by: By,
          path: str,
          data: str):
    input_element: WebElement = scenario.Wait.until(EC.presence_of_element_located((by, path)) and EC.element_to_be_clickable((by, path)))
    input_element.send_keys(data)
