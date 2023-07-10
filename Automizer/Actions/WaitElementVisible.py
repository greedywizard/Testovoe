from selenium.common import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from Automizer.ExecEnvironment import ExecEnvironment


def WaitElementVisible(env: ExecEnvironment,
                       by: By,
                       path: str,
                       is_visible: bool = True,
                       only_dom: bool = False) -> bool:
    attempt = 1

    while attempt <= 3:
        try:
            if only_dom:
                if is_visible:
                    env.Wait.until(EC.presence_of_element_located((by, path)))
                else:
                    env.Wait.until_not(EC.presence_of_element_located((by, path)))
            else:
                if is_visible:
                    env.Wait.until(EC.visibility_of_element_located((by, path)))
                else:
                    env.Wait.until(EC.invisibility_of_element_located((by, path)))
            break
        except StaleElementReferenceException:
            attempt = attempt + 1
        except TimeoutException:
            return not is_visible

    return is_visible
