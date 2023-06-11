from selenium.common.exceptions import NoAlertPresentException
from Automizer.ExecEnvironment import ExecEnvironment


def AcceptAlert(env: ExecEnvironment):
    try:
        alert = env.Driver.switch_to.alert
        alert.accept()
    except NoAlertPresentException:
        # Продолжить, если нет модального диалога
        pass