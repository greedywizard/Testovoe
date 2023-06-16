from selenium.common import InvalidElementStateException, StaleElementReferenceException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from Automizer.ExecEnvironment import ExecEnvironment


def PressKey(env: ExecEnvironment, by: By, path: str, key: Keys):
    input_element = None

    attempt = 1
    while attempt <= 3:
        try:
            input_element: WebElement = env.Wait.until(EC.visibility_of_element_located((by, path)) and EC.element_to_be_clickable((by, path)))
            break
        except StaleElementReferenceException:
            attempt = attempt + 1

    input_element.send_keys(key)
