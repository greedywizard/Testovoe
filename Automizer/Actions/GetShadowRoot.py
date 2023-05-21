from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from Automizer.Scenario import Scenario


def GetShadowRoot(scenario: Scenario,
                  by: By,
                  path: str) -> WebElement:
    shadow_host = scenario.Wait.until(EC.presence_of_element_located((by, path)))
    return scenario.Driver.execute_script('return arguments[0].shadowRoot', shadow_host)
