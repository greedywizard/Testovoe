import random
import time

from selenium.common import NoAlertPresentException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from Automizer import Automizer


class Metamask:
    link_ext = "chrome-extension://iahmedeapmodoedininhafpahbolpnoi"

    def __init__(self, driver: WebDriver):
        self.__driver: WebDriver = driver
        self.__wait = WebDriverWait(driver, 10)
        self.__automizer = Automizer(driver, wait_time=15)
        
    def add_test_networks(self):
        self.__driver.get(f'{self.link_ext}/home.html#settings/networks')

        self.__automizer.click_button_by_xpath("//button[text()='Add a network']")
        self.__automizer.click_button_by_xpath("//div[./a/h6[text()='Add a network manually']]")

        # добавить сеть
        # Network name
        input_element = self.__driver.switch_to.active_element
        input_element.send_keys('Scroll Alpha Testnet')
        # New RPC URL
        input_element.send_keys(Keys.TAB)
        input_element = self.__driver.switch_to.active_element
        input_element.send_keys('https://alpha-rpc.scroll.io/l2')
        # Chain ID
        input_element.send_keys(Keys.TAB, Keys.TAB)
        input_element = self.__driver.switch_to.active_element
        input_element.send_keys('534353')
        # Currency symbol
        input_element.send_keys(Keys.TAB)
        input_element = self.__driver.switch_to.active_element
        input_element.send_keys('ETH')
        # Currency symbol
        input_element.send_keys(Keys.TAB)
        input_element = self.__driver.switch_to.active_element
        input_element.send_keys('https://blockscout.scroll.io')

        self.__automizer.click_button_by_xpath("//button[text()='Save']")
        self.__automizer.click_button_by_xpath('/html/body/div[2]/div/div/section/div/div/button[1]')

    def swap_to_sat(self):
        self.__driver.get(f"{self.link_ext}/home.html")

        # Открыть свиписок сетей
        self.__automizer.click_button_by_xpath('/html/body/div[1]/div/div[1]/div/div[2]/div/div', as_mouse=False)
        # Выбрать сеть goerli
        self.__automizer.click_button_by_xpath('/html/body/div[1]/div/div[2]/div/div[2]/li[.//span[text()="Scroll Alpha"]]', as_mouse=False)

    def check_balance(self) -> float:
        self.__driver.get(f"{self.link_ext}/home.html")

        # Открыть свиписок сетей
        self.__automizer.click_button_by_xpath('/html/body/div[1]/div/div[1]/div/div[2]/div/div', as_mouse=False)
        # Выбрать сеть goerli
        self.__automizer.click_button_by_xpath('/html/body/div[1]/div/div[2]/div/div[2]/li[.//span[text()="Goerli test network"]]', as_mouse=False)

        self.__automizer.get_element_by_xpath("//span[text()='Connecting to Goerli test network']")

        while True:
            try:
                self.__automizer.element_hided_by_xpath("//span[text()='Connecting to Goerli test network']")
                break
            except:
                pass
        #Connecting to Goerli test network

        # Получить количество монет
        e: WebElement = self.__automizer.get_element_by_xpath('/html/body/div[1]/div/div[3]/div/div/div/div[3]/div/div[./div[2]/button/h2/span[text()="GoerliETH"]]')
        v = float(e.find_element(By.CLASS_NAME, 'asset-list-item__token-value').text)

        if v == 0.0:
            return 0.0
        else:
            return v

    def clear_account(self):
        self.__driver.get(f'{self.link_ext}/home.html#settings/advanced')

        self.__automizer.click_button_by_xpath('/html/body/div[1]/div/div[3]/div/div[2]/div[2]/div[2]/div[3]/div[2]/div/button', as_mouse=False)
        self.__automizer.click_button_by_xpath('/html/body/div[1]/div/span/div[1]/div/div/div[2]/button[2]', as_mouse=False)

    def add_token(self, address):
        self.__driver.get(f'{self.link_ext}/home.html#import-token')
        try:
            # Проверьте наличие модального диалога и примите его, если он есть
            alert = self.__driver.switch_to.alert
            alert.accept()
        except NoAlertPresentException:
            # Продолжить, если нет модального диалога
            pass
        pass

        self.__automizer.input_by_id("custom-address", address)

        while True:
            try:
                symbol = self.__automizer.get_element_by_id("custom-symbol").text
                if not symbol or symbol is None:
                    break
                else:
                    time.sleep(3)
            except:
                pass

        self.__automizer.click_button_by_xpath("//button[text()='Add custom token']", as_mouse=False)

    def create_sencond_account(self):
        self.__driver.get(f"{self.link_ext}/home.html#new-account")

        # Ввести название
        self.__automizer.input_by_xpath("/html/body/div[1]/div/div[3]/div/div/div[2]/input", "scroll2")
        # Получить значение из input
        self.__automizer.get_element_by_xpath("/html/body/div[1]/div/div[3]/div/div/div[2]/input[@value='scroll2']")
        # "Create"
        self.__automizer.click_button_by_xpath("//button[text()='Create']", as_mouse=False)

    def send_to_2_account_and_revert(self):
        self.__driver.get(f"{self.link_ext}/home.html")

        self.__automizer.click_button_by_xpath("//button[@data-testid='account-menu-icon']", as_mouse=False)
        #
        self.__automizer.click_button_by_xpath("/html/body/div[1]/div/div[3]/div[4]/div/button[1]", as_mouse=False)

        self.__automizer.click_button_by_xpath("//button[.//span[text()='Send']]", as_mouse=False)
        # Открыть список аккаунтов
        self.__automizer.click_button_by_xpath("//a[text()='Transfer between my accounts']", as_mouse=False)
        # Выбрать 2 аккаунт
        self.__automizer.click_button_by_xpath("//div[text()='scroll2']", as_mouse=False)
        #
        max_value = float(self.__automizer.get_element_by_class_name("currency-display-component__text").text)
        rand_value = 0.0

        if max_value >= 0.0015:
            rand_value = random.randint(5, 15)/10000
        else:
            rand_value = max_value

        # Ввести значения
        self.__automizer.input_by_xpath("/html/body/div[1]/div/div[3]/div/div[3]/div/div[2]/div[2]/div[1]/div/div/div[1]/input", str(rand_value))

        while True:
            try:
                #  "Next"
                self.__automizer.click_button_by_xpath("/html/body/div[1]/div/div[3]/div/div[4]/footer/button[2]", as_mouse=False)
                #  "Confirm"
                self.__automizer.click_button_by_xpath("/html/body/div[1]/div/div[3]/div/div[3]/div[3]/footer/button[2]", as_mouse=False)
                break
            except Exception as e:
                print(e)
                pass

        while True:
            try:
                # Открыть информацию о
                self.__automizer.click_button_by_xpath("/html/body/div[1]/div/div[3]/div/div/div/div[3]/div/div/div/div/div[1]", as_mouse=False)
                if self.__automizer.get_element_by_xpath("/html/body/div[2]/div/div/section/div[2]/div/div[2]/div[1]/div[2]/div").text == "Confirmed":
                    break
                self.__automizer.click_button_by_xpath("/html/body/div[2]/div/div/section/div[1]/div/button", as_mouse=False)
            except:
                pass

        # Выбрать 2 аккаунт
        self.__automizer.click_button_by_xpath("/html/body/div[1]/div/div[1]/div/div[2]/button/div", as_mouse=False)
        # Выбрать scroll2
        self.__automizer.click_button_by_xpath("//button/div[3]/div[text()='scroll2']", as_mouse=False)

        self.__driver.get(f"{self.link_ext}/home.html#send")

        # Открыть список аккаунтов
        self.__automizer.click_button_by_xpath("/html/body/div[1]/div/div[3]/div/div[3]/div/div/a", as_mouse=False)
        # Выбрать 2 аккаунт
        self.__automizer.click_button_by_xpath("//div[.//div[2]/div[text()='Account 1']]", as_mouse=False)

        while True:
            try:
                # Ввести значения
                self.__automizer.input_by_xpath("/html/body/div[1]/div/div[3]/div/div[3]/div/div[2]/div[2]/div[1]/div/div/div[1]/input", str(rand_value/2))
                #  "Next"
                self.__automizer.click_button_by_xpath("//button[text()='Next']", as_mouse=False)
                #  "Confirm"
                self.__automizer.click_button_by_xpath("//button[text()='Confirm']", as_mouse=False)
                break
            except:
                pass

        while True:
            try:
                self.__automizer.click_button_by_xpath("/html/body/div[1]/div/div[3]/div/div/div/div[3]/div/div/div/div/div[1]", as_mouse=False)
                if self.__automizer.get_element_by_xpath("/html/body/div[2]/div/div/section/div[2]/div/div[2]/div[1]/div[2]/div").text == "Confirmed":
                    break
                self.__automizer.click_button_by_xpath("/html/body/div[2]/div/div/section/div[1]/div/button", as_mouse=False)
            except:
                pass

