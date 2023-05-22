from selenium.common.exceptions import NoAlertPresentException
from Automizer.Scenario import Scenario


def AcceptAlert(scenario: Scenario):
    try:
        alert = scenario.Driver.switch_to.alert
        alert.accept()
    except NoAlertPresentException:
        # Продолжить, если нет модального диалога
        pass