from selenium.common.exceptions import NoAlertPresentException
from Automizer.ExecEnvironment import ExecEnvironment


def AcceptAlert(scenario: ExecEnvironment):
    try:
        alert = scenario.Driver.switch_to.alert
        alert.accept()
    except NoAlertPresentException:
        # Продолжить, если нет модального диалога
        pass