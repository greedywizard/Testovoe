import time
from selenium.webdriver import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchWindowException, \
    StaleElementReferenceException


class Automizer:
    def __init__(self, driver: WebDriver, wait_time: int):
        self.driver: WebDriver = driver
        self.wait: WebDriverWait = WebDriverWait(driver, wait_time)
        self.prev_window = None

    def always_false(self) -> bool:
        return False

    # Click buttons
    def __click(self, by: str, path: str, as_mouse: bool):
        button: WebElement = self.wait.until(EC.visibility_of_element_located(
            (by, path)))

        if as_mouse:
            try:
                button.click()
            except ElementClickInterceptedException:
                button = self.wait.until(EC.element_to_be_clickable(
                    (by, path)))
                button.click()
        else:
            self.driver.execute_script("arguments[0].click();", button)

    def click_button_by_xpath(self, xpath: str, as_mouse: bool = True) -> None:
        self.__click(By.XPATH, xpath, as_mouse)

    def click_button_by_css(self, css: str, as_mouse: bool = True) -> None:
        self.__click(By.CSS_SELECTOR, css, as_mouse)

    def click_button_by_id(self, id, as_mouse: bool = True) -> None:
        self.__click(By.ID, id, as_mouse)

    # Get elements
    def __get_element(self, by: str, path: str) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located((by, path)))

    def get_element_by_xpath(self, xpath: str) -> WebElement:
        return self.__get_element(By.XPATH, xpath)

    def get_element_by_css(self, css: str) -> WebElement:
        return self.__get_element(By.CSS_SELECTOR, css)

    def get_element_by_id(self, id) -> WebElement:
        return self.__get_element(By.ID, id)

    #Inputs
    def __input(self, by: str, finder: str, value: str):
        input_element = self.wait.until(EC.element_to_be_clickable((by, finder)))
        #self.wait.until(EC.visibility_of(input_element))
        time.sleep(1)
        input_element.send_keys(value)

    def input_by_xpath(self, xpath: str, value: str) -> None:
        self.__input(By.XPATH, xpath, value)

    def input_by_css(self, css: str, value: str) -> None:
        self.__input(By.CSS_SELECTOR, css, value)

    def input_by_id(self, id, value: str) -> None:
        self.__input(By.ID, id, value)

    # Switch window
    def switch_to_new_window(self, number: int = 2, count: int = 2) -> str:
        current_window = self.driver.current_window_handle
        self.prev_window = current_window

        self.wait.until(EC.number_of_windows_to_be(count))
        self.driver.switch_to.window(self.driver.window_handles[number - 1])

        return current_window

    def switch_to_prev_window(self) -> None:
        try:
            self.driver.close()
        except NoSuchWindowException:
            pass
        finally:
            self.driver.switch_to.window(self.prev_window)
