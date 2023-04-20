from selenium.webdriver import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Metamask:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def click_button(self, xpath: str) -> None:
        button: WebElement = WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(
            (By.XPATH, xpath)))
        button.click()

    def open_wallet(self, seed_phrase: str) -> None:
        self.click_button('/html/body/div[1]/div/div[2]/div/div/div/ul/li[2]/button')
        self.click_button('/html/body/div[1]/div/div[2]/div/div/div/div/button[1]')

        seed_arr = seed_phrase.split(' ')

        input_element = WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(
            (By.ID, 'import-srp__srp-word-0')))

        input_element.send_keys(seed_arr.pop(0))

        for i in seed_arr:
            input_element.send_keys(Keys.TAB, Keys.TAB)
            input_element = self.driver.switch_to.active_element
            input_element.send_keys(i)

        self.click_button('/html/body/div[1]/div/div[2]/div/div/div/div[4]/div/button')

        password: str = '12345678'
        input_element = self.driver.switch_to.active_element
        input_element.send_keys(password)
        input_element.send_keys(Keys.TAB)
        input_element = self.driver.switch_to.active_element
        input_element.send_keys(password)
        input_element.send_keys(Keys.TAB)
        check_box = self.driver.switch_to.active_element
        check_box.click()
        check_box.send_keys(Keys.TAB, Keys.TAB)
        button = self.driver.switch_to.active_element
        button.click()

        self.click_button('/html/body/div[1]/div/div[2]/div/div/div/div[2]/button')
        self.click_button('/html/body/div[1]/div/div[2]/div/div/div/div[2]/button')
        self.click_button('/html/body/div[1]/div/div[2]/div/div/div/div[2]/button')
        self.click_button('/html/body/div[2]/div/div/section/div[2]/div/button')
