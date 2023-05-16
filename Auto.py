import time
from selenium.webdriver import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchWindowException, ElementNotInteractableException


class Automizer:
    def __init__(self, driver: WebDriver, wait_time: int):
        self.__driver: WebDriver = driver
        self.__wait: WebDriverWait = WebDriverWait(driver, wait_time)
        self.__prev_window = None

    def get(self, url: str) -> None:
        self.__driver.execute_script(f"window.location.href = '{url}';")

    def always_false(self) -> bool:
        return False

    def __exist(self, by: str, path: str):
        self.__wait.until_not(EC.visibility_of_element_located((by, path)))

    def element_hided_by_xpath(self, path: str):
        self.__exist(By.XPATH, path)

    # Click buttons
    def __click(self, by: str, path: str, as_mouse: bool):
        button: WebElement = self.__wait.until(EC.visibility_of_element_located((by, path)))

        if as_mouse:
            try:
                button.click()
            except ElementClickInterceptedException:
                button = self.__wait.until(EC.element_to_be_clickable((by, path)))
                button.click()
        else:
            self.__driver.execute_script("arguments[0].click();", button)

    def click_button_by_xpath(self, xpath: str, as_mouse: bool = True) -> None:
        self.__click(By.XPATH, xpath, as_mouse)

    def click_button_by_css(self, css: str, as_mouse: bool = True) -> None:
        self.__click(By.CSS_SELECTOR, css, as_mouse)

    def click_button_by_id(self, id, as_mouse: bool = True) -> None:
        self.__click(By.ID, id, as_mouse)

    # Get elements
    def __get_element(self, by: str, path: str) -> WebElement:
        return self.__wait.until(EC.visibility_of_element_located((by, path)))

    def get_element_by_xpath(self, xpath: str) -> WebElement:
        return self.__get_element(By.XPATH, xpath)

    def get_element_by_css(self, css: str) -> WebElement:
        return self.__get_element(By.CSS_SELECTOR, css)

    def get_element_by_id(self, id) -> WebElement:
        return self.__get_element(By.ID, id)

    def get_element_by_class_name(self, name) -> WebElement:
        return self.__get_element(By.CLASS_NAME, name)

    #Inputs
    def __input(self, by: str, finder: str, value: str):
        input_element = self.__wait.until(EC.element_to_be_clickable((by, finder)))
        time.sleep(1)
        input_element.send_keys(value)

    def input_by_xpath(self, xpath: str, value: str) -> None:
        self.__input(By.XPATH, xpath, value)

    def input_by_css(self, css: str, value: str) -> None:
        self.__input(By.CSS_SELECTOR, css, value)

    def input_by_id(self, id, value: str) -> None:
        self.__input(By.ID, id, value)

    #Select
    def __select(self, by: str, path: str, option: str):
        select_selement: Select = Select(self.__wait.until(EC.visibility_of_element_located((by, path))))
        select_selement.select_by_value(option)

    def select_by_id(self, path: str, option: str):
        self.__select(By.ID, path, option)

    def select_by_xpath(self, path: str, option: str):
        self.__select(By.XPATH, path, option)

    # Switch window
    def switch_to_new_window(self, count: int = 2) -> str:
        current_window = self.__driver.current_window_handle
        self.__prev_window = current_window

        self.__wait.until(EC.number_of_windows_to_be(count))
        self.__driver.switch_to.window(self.__driver.window_handles[-1])

        return current_window

    def switch_to_prev_window(self) -> None:
        try:
            self.__driver.close()
        except NoSuchWindowException:
            pass
        finally:
            self.__driver.switch_to.window(self.__prev_window)
