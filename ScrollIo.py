import time

from selenium.webdriver import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, NoAlertPresentException

from Automizer import Automizer
from ShadowDom import ShadowDOM


class ScrollIo:
    def __init__(self, driver: WebDriver):
        self.__driver: WebDriver = driver
        self.__wait = WebDriverWait(driver, 20)
        self.__automizer = Automizer(driver, wait_time=15)

    def transfer_goerli_to_alphatest(self, value: float):
        self.__driver.get("https://scroll.io/alpha/bridge")

        # Ввести 99.4% от максимального значения
        self.__automizer.input_by_id(':r0:', str(value * (1 - 0.6 / 100)))
        # "Send ETH to Scroll Alpha Test" кнопка
        self.__automizer.click_button_by_id(":r2:")
        # Переключиться на всплывающее окно
        self.__automizer.switch_to_new_window()
        # "Confirm" кнопка
        self.__automizer.click_button_by_xpath("//button[text()='Confirm']")
        # Переключиться на предыдущее окно
        self.__automizer.switch_to_prev_window()

        while True:
            try:
                self.__automizer.get_element_by_xpath("/html/body/div/div/div[1]/div[3]/div/div/table/tbody/tr[1]/td[1]/div/div[1]/span[text()='Success']")
                self.__automizer.get_element_by_xpath("/html/body/div/div/div[1]/div[3]/div/div/table/tbody/tr/td[1]/div/div[2]/span[text()='Success']")
                break
            except:
                pass

    def validate_contract(self, compiler: str, address: str):
        self.__driver.execute_script("window.open('');")
        self.__automizer.switch_to_new_window()
        self.__driver.get(f"https://blockscout.scroll.io/address/{address}/verify-via-flattened-code/new")
        try:
            # Проверьте наличие модального диалога и примите его, если он есть
            alert = self.__driver.switch_to.alert
            alert.accept()
        except NoAlertPresentException:
            # Продолжить, если нет модального диалога
            pass

        # Выбор компилятора
        self.__automizer.select_by_id("smart_contract_compiler_version", compiler)
        # "Publish"
        self.__automizer.click_button_by_xpath("/html/body/div[1]/main/section/div[2]/form/div[14]/button[text()='Verify & publish']")
        self.__automizer.switch_to_prev_window()
