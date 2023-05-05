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


    def connect_metamask(self):
        self.__driver.get("https://scroll.io/alpha")
        self.__driver.refresh()

        shadow_dom = ShadowDOM(self.__driver, shadow_xpath="/html/body/onboard-v2", wait_time=3)

        # "Connect wallet" кнопка от Scroll Alpha Testnet
        self.__automizer.click_button_by_xpath("/html/body/div/div/div[1]/div[1]/div[2]/dl/div[2]/div[2]/dd/ul/li/div[2]/a")
        # "Metamask" кнопка
        shadow_dom.click_button_by_css(
            "section > div > div > div > div > div > div > div > div.scroll-container.svelte-1qwmck3 > div > div > div > div.wallet-button-container.svelte-1vlog3j > button > div")
        # Переключение на появившееся окно подтверждения
        self.__automizer.switch_to_new_window()
        # "Next" кнопка
        self.__automizer.click_button_by_xpath("//button[text()='Next']")
        # "Connect"" кнопка
        self.__automizer.click_button_by_xpath("/html/body/div[1]/div/div[2]/div/div[2]/div[2]/div[2]/footer/button[2]")
        # Перключение обратно на исходное окно
        self.__automizer.switch_to_prev_window()

    def transfer_goerli_to_alphatest(self, value: float):
        self.__driver.get("https://scroll.io/alpha/bridge")
        self.__driver.refresh()

        # Получить количество токенов
        e = float(self.__automizer.get_element_by_xpath("/html/body/div/div[1]/div[1]/div[3]/div/div[1]/div[2]/div[2]/h6").text.split(' ')[1])
        # Ввести 99.4% от максимального значения
        self.__automizer.input_by_id(':r0:', str(e * (1 - 0.6 / 100)))
        # "Send ETH to Scroll Alpha Test" кнопка
        self.__automizer.click_button_by_id(":r2:")
        # Переключиться на всплывающее окно
        self.__automizer.switch_to_new_window()
        # "Confirm" кнопка
        self.__automizer.click_button_by_xpath("/html/body/div[1]/div/div[2]/div/div[3]/div[3]/footer/button[2]")
        # Переключиться на предыдущее окно
        self.__automizer.switch_to_prev_window()

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

