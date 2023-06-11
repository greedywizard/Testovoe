from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from Automizer.ExecEnvironment import ExecEnvironment


def WaitElementVisible(env: ExecEnvironment,
                       by: By,
                       path: str,
                       hide: bool = False):
    attempt = 1
    while attempt <= 3:
        try:
            if hide:
                env.Wait.until_not(EC.visibility_of_element_located((by, path)))
            else:
                env.Wait.until(EC.visibility_of_element_located((by, path)))
            break
        except StaleElementReferenceException:
            attempt = attempt + 1
