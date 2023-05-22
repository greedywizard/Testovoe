from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from Automizer.Scenario import Scenario


def AcceptAlert(scenario: Scenario):
    alert = scenario.Driver.switch_to.alert
    alert.accept()