from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By

from Automizer.ExecEnvironment import ExecEnvironment


def ExistElement(env: ExecEnvironment,
                 by: By,
                 path: str) -> bool:
    attempt = 1
    while attempt <= 3:
        try:
            v = env.Driver.find_element(by, path)
            if v.is_displayed():
                return True
            else:
                return False
        except NoSuchElementException:
            return False
        except StaleElementReferenceException:
            attempt = attempt + 1
