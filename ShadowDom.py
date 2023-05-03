from selenium.webdriver import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver


class ShadowDOM:
    def __init__(self, driver: WebDriver, shadow_xpath: str, wait_time: int):
        self.driver: WebDriver = driver
        self.wait: WebDriverWait = WebDriverWait(self.driver, wait_time)
        shadow_host = self.wait.until(EC.presence_of_element_located((By.XPATH, shadow_xpath)))
        self.shadow_root = self.driver.execute_script('return arguments[0].shadowRoot', shadow_host)

    def click_button_by_css(self, selector):
        button: WebElement = self.shadow_root.find_element(By.CSS_SELECTOR, selector)
        button.click()
