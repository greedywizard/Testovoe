from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from Automizer.ExecEnvironment import ExecEnvironment


def ExistElement(env: ExecEnvironment,
                 by: By,
                 path: str) -> bool:
    try:
        v = env.Driver.find_element(by, path)
        if v.is_displayed():
            return True
        else:
            return False
    except NoSuchElementException:
        return False
