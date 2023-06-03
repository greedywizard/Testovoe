from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from Automizer.Scenario import Scenario


def WaitElementVisible(scenario: Scenario,
                       by: By,
                       path: str,
                       hide: bool = False):
    if hide:
        scenario.Wait.until_not(EC.visibility_of_element_located((by, path)))
    else:
        scenario.Wait.until(EC.visibility_of_element_located((by, path)))
