import random
import string

from selenium.common import NoAlertPresentException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from Automizer import Automizer


class Openzeppelin:
    def __init__(self, driver: WebDriver):
        self.__driver: WebDriver = driver
        self.__wait = WebDriverWait(driver, 10)
        self.__automizer = Automizer(driver, wait_time=15)

    def create_contract(self) -> (str, str):
        self.__driver.get(f"https://docs.openzeppelin.com/contracts/4.x/wizard")

        try:
            # Проверьте наличие модального диалога и примите его, если он есть
            alert = self.__driver.switch_to.alert
            alert.accept()
        except NoAlertPresentException:
            # Продолжить, если нет модального диалога
            pass


        iframe = self.__automizer.get_element_by_xpath("/html/body/div[1]/main/div/article/oz-wizard/iframe")
        self.__driver.switch_to.frame(iframe)
        # "Mintable"
        self.__automizer.click_button_by_xpath("/html/body/div/div[2]/div[1]/div[1]/section[2]/div/label[1]/input")
        # очистить поле
        self.__automizer.get_element_by_xpath("/html/body/div/div[2]/div[1]/div[1]/section[1]/div/label[2]/input").clear()
        # 3 рандомные буквы
        random_letter = ''.join(random.choices(string.ascii_uppercase, k=3))
        self.__automizer.input_by_xpath("/html/body/div/div[2]/div[1]/div[1]/section[1]/div/label[2]/input", random_letter)
        # много денях
        self.__automizer.input_by_xpath("/html/body/div/div[2]/div[1]/div[1]/section[1]/label/input", str(121002102))
        # Получить код контракта
        code: str = self.__automizer.get_element_by_xpath("/html/body/div/div[2]/div[2]/pre/code").text
        self.__driver.switch_to.default_content()

        return code, random_letter
