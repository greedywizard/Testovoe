import random
import time
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from Automizer import Automizer


class Uniswap:
    def __init__(self, driver: WebDriver):
        self.__driver: WebDriver = driver
        self.__wait = WebDriverWait(driver, 20)
        self.__automizer = Automizer(driver, wait_time=15)




    def swap_eth_to_weth(self, value: float) -> float:
        self.__driver.get("https://uniswap-v3.scroll.io/#/swap")

        # Список токенов на которые переводить
        self.__automizer.click_button_by_xpath("/html/body/div[1]/div/div[2]/div[5]/main/div[3]/div[1]/div/div/div/div[1]/button")
        # Выбрать токен WETH
        self.__automizer.click_button_by_xpath('/html/body/reach-portal[2]/div[3]/div/div/div/div/div[3]/div[1]/div/div/div[./div[2]/div[text()="WETH"]]')
        # "I understand"
        self.__automizer.click_button_by_xpath("/html/body/reach-portal[2]/div[3]/div/div/div/div/div/button[1]")
        # Рандомная половина
        val = self.generate_half_random(value)
        # Ввод количества
        self.__automizer.input_by_xpath("/html/body/div[1]/div/div[2]/div[5]/main/div[2]/div[1]/div/div/div[1]/input",
                                        str(val))
        # "Warp"
        self.__automizer.click_button_by_xpath("/html/body/div[1]/div/div[2]/div[5]/main/div[3]/div[2]/button")
        # Переключение на всплвающее окно
        self.__automizer.switch_to_new_window()
        # "Confirm"
        self.__automizer.click_button_by_xpath("//button[text()='Confirm']")
        # Переключение на исходное окно
        self.__automizer.switch_to_prev_window()

        return val

    def swap_weth_to_usdc(self):
        self.__driver.get("https://uniswap-v3.scroll.io/#/swap?outputCurrency=0xA0D71B9877f44C744546D649147E3F1e70a93760")

        try:
            # "I understand" кнопка
            self.__automizer.click_button_by_xpath("//button[text()='I understand']")
        except:
            pass

        # Открыть список монет
        self.__automizer.click_button_by_xpath("/html/body/div[1]/div/div[2]/div[5]/main/div[2]/div[1]/div/div/div[1]/button")
        # Выбрать монеты WETH
        self.__automizer.click_button_by_xpath("/html/body/reach-portal[2]/div[3]/div/div/div/div/div[3]/div[1]/div/div/div[./div[2]/div[text()='WETH']]")
        # "I understand" кнопка
        self.__automizer.click_button_by_xpath("//button[text()='I understand']")
        try:
            # Кнопка "max"
            self.__automizer.click_button_by_xpath("//button[text()='Max']")
        except:
            return

        # Ожидаем подсчет
        time.sleep(3)
        # Проверка наличия "Allow the Uniswap Protocol to use your WETH"
        allow_button: bool = len(self.__driver.find_elements(By.XPATH, "//button[.//div/div[text()='Allow the Uniswap Protocol to use your WETH']]")) > 0
        uwrap_button: bool = len(self.__driver.find_elements(By.XPATH, "//button[text()='Unwrap']"))

        if allow_button:
            # "Allow the Uniswap Protocol to use your WETH"
            self.__automizer.click_button_by_xpath("//button[.//div/div[text()='Allow the Uniswap Protocol to use your WETH']]")
            # Переключение на всплвающее окно
            self.__automizer.switch_to_new_window()
            # "Max"
            self.__automizer.click_button_by_xpath("//button[text()='Max']")
            # "Next"
            self.__automizer.click_button_by_xpath("//button[text()='Next']")
            # "Approve"
            self.__automizer.click_button_by_xpath("//button[text()='Approve']")
            # Переключение на исходное окно
            self.__automizer.switch_to_prev_window()
            # Ожидание подсчетов
            while True:
                try:
                    self.__automizer.get_element_by_xpath("//div[text()='You can now trade WETH']")
                    break
                except:
                    pass
            # Swap
            self.__automizer.click_button_by_xpath("//button[.//div[text()='Swap']]")
            # Переключение на всплвающее окно
            self.__automizer.switch_to_new_window()
            #
            self.__automizer.click_button_by_xpath("//button[text()='Confirm']")
            # Переключение на исходное окно
            self.__automizer.switch_to_prev_window()
        else:
            # "Swap"
            self.__automizer.click_button_by_id("swap-button")
            # "Confirm swap"
            self.__automizer.click_button_by_id("confirm-swap-or-send")
            # Переключение на всплвающее окно
            self.__automizer.switch_to_new_window()
            # "Confirm"
            self.__automizer.click_button_by_xpath("//button[text()='Confirm']")
            # Переключение на исходное окно
            self.__automizer.switch_to_prev_window()
            # "Close"
            self.__automizer.click_button_by_xpath("/html/body/reach-portal[2]/div[3]/div/div/div/div/div/div[3]/button")

    def add_liquid(self):
        self.__driver.get("https://uniswap-v3.scroll.io/#/add/ETH")

        # Список токенов
        self.__automizer.click_button_by_xpath("/html/body/div[1]/div/div[2]/div[4]/main/div[2]/div/div[1]/div/div[2]/div[3]/div/div/button")
        # выбор usdc
        self.__automizer.click_button_by_xpath("/html/body/reach-portal[2]/div[3]/div/div/div/div/div[3]/div[1]/div/div/div[./div[2]/div[text()='USDC']]")
        #
        self.__automizer.click_button_by_xpath("/html/body/div[1]/div/div[2]/div[4]/main/div[2]/div/div[3]/div/button")

        self.__automizer.click_button_by_xpath("/html/body/div[1]/div/div[2]/div[4]/main/div[2]/div/div[1]/div/div[3]/div/div[2]/button[3]")
        self.__automizer.click_button_by_xpath("//button[.//div[text()='Full Range']]")
        self.__automizer.click_button_by_xpath("//button[.//div[text()='I understand']]")
        self.__automizer.click_button_by_xpath("/html/body/div[1]/div/div[2]/div[4]/main/div[2]/div/div[2]/div/div/div[3]/div/div[2]/div/div[2]/button")
        self.__automizer.click_button_by_xpath("//button[text()='Approve USDC']")
        # Переключение на всплвающее окно
        self.__automizer.switch_to_new_window()
        # "Max"
        self.__automizer.click_button_by_xpath("//button[text()='Max']")
        # "Next"
        self.__automizer.click_button_by_xpath("//button[text()='Next']")
        # "Approve"
        self.__automizer.click_button_by_xpath("//button[text()='Approve']")
        # Переключение на исходное окно
        self.__automizer.switch_to_prev_window()

    def swap_usdc_to_eth(self):
        self.__driver.get("https://uniswap-v3.scroll.io/#/swap?outputCurrency=0xA0D71B9877f44C744546D649147E3F1e70a93760")

        try:
            # "I understand" кнопка
            self.__automizer.click_button_by_xpath("/html/body/reach-portal[2]/div[3]/div/div/div/div/div/button[1]")
        except:
            pass

        # Открыть список монет
        self.__automizer.click_button_by_xpath("/html/body/div[1]/div/div[2]/div[5]/main/div[2]/div[1]/div/div/div[1]/button")
        # Выбрать монеты usdc
        self.__automizer.click_button_by_xpath("/html/body/reach-portal[2]/div[3]/div/div/div/div/div[3]/div[1]/div/div/div[./div[2]/div[text()='USDC']]")
        # Открыть список монет
        self.__automizer.click_button_by_xpath("/html/body/div[1]/div/div[2]/div[5]/main/div[3]/div[1]/div/div/div/div[1]/button")
        # Выбрать монеты eth
        self.__automizer.click_button_by_xpath("/html/body/reach-portal[2]/div[3]/div/div/div/div/div[3]/div[1]/div/div/div[./div[2]/div[text()='ETH']]")
        try:
            # Кнопка "max"
            self.__automizer.click_button_by_xpath("//button[text()='Max']")
        except:
            return


        # Ожидаем подсчет
        time.sleep(3)
        # Проверка наличия "Allow the Uniswap Protocol to use your USDC"
        allow_button: bool = len(self.__driver.find_elements(By.XPATH, "//button[.//div/div[text()='Allow the Uniswap Protocol to use your USDC']]")) > 0

        if allow_button:
            # "Allow the Uniswap Protocol to use your WETH"
            self.__automizer.click_button_by_xpath("//button[.//div/div[text()='Allow the Uniswap Protocol to use your USDC']]")
            # Переключение на всплвающее окно
            self.__automizer.switch_to_new_window()
            # "Max"
            self.__automizer.click_button_by_xpath("//button[text()='Max']")
            # "Next"
            self.__automizer.click_button_by_xpath("//button[text()='Next']")
            # "Approve"
            self.__automizer.click_button_by_xpath("//button[text()='Approve']")
            # Переключение на исходное окно
            self.__automizer.switch_to_prev_window()

        # Ожидание подсчетов
        while True:
            try:
                self.__automizer.get_element_by_xpath("//div[text()='You can now trade USDC']")
                break
            except:
                pass
        # "Swap"
        self.__automizer.click_button_by_id("swap-button")
        # "Confirm swap"
        self.__automizer.click_button_by_id("confirm-swap-or-send")
        # Переключение на всплвающее окно
        self.__automizer.switch_to_new_window()
        # "Confirm"
        self.__automizer.click_button_by_xpath("/html/body/div[1]/div/div[2]/div/div[3]/div[3]/footer/button[2]")
        # Переключение на исходное окно
        self.__automizer.switch_to_prev_window()
        # "Close"
        self.__automizer.click_button_by_xpath("/html/body/reach-portal[2]/div[3]/div/div/div/div/div/div[3]/button")

