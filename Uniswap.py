import random
import time
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from Automizer import Automizer


class Uniswap:
    def __init__(self, driver: WebDriver):
        self.driver: WebDriver = driver
        self.wait = WebDriverWait(driver, 20)
        self.automizer = Automizer(driver, wait_time=15)

    @staticmethod
    def generate_half_random(target_number):
        pointer = 100
        lower_bound = int(target_number * 0.4 * pointer)  # 40% от искомого числа
        upper_bound = int(target_number * 0.6 * pointer)  # 60% от искомого числа

        random_number = random.randint(lower_bound, upper_bound)
        return random_number / pointer

    def connect_wallet(self):
        self.driver.get("https://uniswap-v3.scroll.io/#/swap")
        self.driver.refresh()
        # "Connect" кнопка
        self.automizer.click_button_by_xpath("/html/body/div[1]/div/div[2]/div[5]/main/div[3]/div[2]/button")
        # "Metamask" конпка
        self.automizer.click_button_by_id("metamask", as_mouse=False)
        # Переключение на всплвающее окно
        self.automizer.switch_to_new_window()
        # "Next"
        self.automizer.click_button_by_xpath("/html/body/div[1]/div/div[2]/div/div[3]/div[2]/button[2]")
        # "Connect"
        self.automizer.click_button_by_xpath("/html/body/div[1]/div/div[2]/div/div[2]/div[2]/div[2]/footer/button[2]")
        # Переключение на исходное окно
        self.automizer.switch_to_prev_window()
        # Кнопка около кошелька для выбор сети
        self.automizer.click_button_by_xpath("/html/body/div[1]/div/div[1]/nav/div/div[3]/div/div[3]/div/button")
        # "Scroll alpha testnet"
        self.automizer.click_button_by_xpath("/html/body/div[1]/div/div[1]/nav/div/div[3]/div/div[3]/div/div/div/button")
        # Переключение на всплвающее окно
        self.automizer.switch_to_new_window()
        # "Approve"
        self.automizer.click_button_by_xpath("/html/body/div[1]/div/div[2]/div/div[2]/div/button[2]")
        # "Switch network"
        self.automizer.click_button_by_xpath("/html/body/div[1]/div/div[2]/div/div[2]/div/button[2]")
        # Переключение на исходное окно
        self.automizer.switch_to_prev_window()

    def swap_eth_to_weth(self, value: float) -> float:
        self.driver.get("https://uniswap-v3.scroll.io/#/swap")
        self.driver.refresh()
        # Список токенов на которые переводить
        self.automizer.click_button_by_xpath("/html/body/div[1]/div/div[2]/div[5]/main/div[3]/div[1]/div/div/div/div[1]/button")
        # Выбрать токен WETH
        self.automizer.click_button_by_xpath('/html/body/reach-portal[2]/div[3]/div/div/div/div/div[3]/div[1]/div/div/div[./div[2]/div[text()="WETH"]]')
        # "I understand"
        self.automizer.click_button_by_xpath("/html/body/reach-portal[2]/div[3]/div/div/div/div/div/button[1]")
        # Рандомная половина
        val = self.generate_half_random(value)
        # Ввод количества
        self.automizer.input_by_xpath("/html/body/div[1]/div/div[2]/div[5]/main/div[2]/div[1]/div/div/div[1]/input",
                                      str(val))
        # "Warp"
        self.automizer.click_button_by_xpath("/html/body/div[1]/div/div[2]/div[5]/main/div[3]/div[2]/button")
        # Переключение на всплвающее окно
        self.automizer.switch_to_new_window()
        # "Confirm"
        self.automizer.click_button_by_xpath("/html/body/div[1]/div/div[2]/div/div[3]/div[3]/footer/button[2]")
        # Переключение на исходное окно
        self.automizer.switch_to_prev_window()

        return val

    def swap_weth_to_usdc(self):
        self.driver.get("https://uniswap-v3.scroll.io/#/swap?outputCurrency=0xA0D71B9877f44C744546D649147E3F1e70a93760")
        self.driver.refresh()

        # "I understand" кнопка
        self.automizer.click_button_by_xpath("/html/body/reach-portal[2]/div[3]/div/div/div/div/div/button[1]")
        # Открыть список монет
        self.automizer.click_button_by_xpath("/html/body/div[1]/div/div[2]/div[5]/main/div[2]/div[1]/div/div/div[1]/button")
        # Выбрать монеты WETH
        self.automizer.click_button_by_xpath("/html/body/reach-portal[2]/div[3]/div/div/div/div/div[3]/div[1]/div/div/div[./div[2]/div[text()='WETH']]")
        # "I understand" кнопка
        self.automizer.click_button_by_xpath("/html/body/reach-portal[2]/div[3]/div/div/div/div/div/button[1]")
        try:
            # Кнопка "max"
            self.automizer.click_button_by_xpath("/html/body/div[1]/div/div[2]/div[5]/main/div[2]/div[1]/div/div/div[2]/div/div[2]/button")
        except:
            return


        # Ожидаем подсчет
        time.sleep(3)
        # Проверка наличия "Allow the Uniswap Protocol to use your WETH"
        allow_button: bool = len(self.driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[2]/div[5]/main/div[3]/div[2]/div/div/button[1]")) > 0

        if allow_button:
            # "Allow the Uniswap Protocol to use your WETH"
            self.automizer.click_button_by_xpath("/html/body/div[1]/div/div[2]/div[5]/main/div[3]/div[2]/div/div/button[1]")
            # Переключение на всплвающее окно
            self.automizer.switch_to_new_window()
            # "Max"
            self.automizer.click_button_by_xpath("/html/body/div[1]/div/div[2]/div/div[7]/div/div/label/div[2]/button/span")
            # "Next"
            self.automizer.click_button_by_xpath("/html/body/div[1]/div/div[2]/div/div[9]/footer/button[2]")
            # "Approve"
            self.automizer.click_button_by_xpath("/html/body/div[1]/div/div[2]/div/div[10]/footer/button[2]")
            # Переключение на исходное окно
            self.automizer.switch_to_prev_window()
            # Ожидание подсчетов
            time.sleep(3)
            # Swap
            self.automizer.click_button_by_xpath("/html/body/div[1]/div/div[2]/div[5]/main/div[3]/div[2]/div/div/button[2]")
            # Переключение на всплвающее окно
            self.automizer.switch_to_new_window()
            #
            self.automizer.click_button_by_xpath("/html/body/div[1]/div/div[2]/div/div[3]/div[3]/footer/button[2]")
            # Переключение на исходное окно
            self.automizer.switch_to_prev_window()
        else:
            # "Swap"
            self.automizer.click_button_by_id("swap-button")
            # "Confirm swap"
            self.automizer.click_button_by_id("confirm-swap-or-send")
            # Переключение на всплвающее окно
            self.automizer.switch_to_new_window()
            # "Confirm"
            self.automizer.click_button_by_xpath("/html/body/div[1]/div/div[2]/div/div[3]/div[3]/footer/button[2]")
            # Переключение на исходное окно
            self.automizer.switch_to_prev_window()
            # "Close"
            self.automizer.click_button_by_xpath("/html/body/reach-portal[2]/div[3]/div/div/div/div/div/div[3]/button")

    def add_liquid(self):
        self.driver.get("https://uniswap-v3.scroll.io/#/add/ETH")
        self.driver.refresh()
        # Список токенов
        self.automizer.click_button_by_xpath("/html/body/div[1]/div/div[2]/div[4]/main/div[2]/div/div[1]/div/div[2]/div[3]/div/div/button")
        # выбор usdc
        self.automizer.click_button_by_xpath("/html/body/reach-portal[2]/div[3]/div/div/div/div/div[3]/div[1]/div/div/div[./div[2]/div[text()='USDC']]")
        #
        self.automizer.click_button_by_xpath("/html/body/div[1]/div/div[2]/div[4]/main/div[2]/div/div[3]/div/button")

    def swap_usdc_to_eth(self):
        self.driver.get("https://uniswap-v3.scroll.io/#/swap?outputCurrency=0xA0D71B9877f44C744546D649147E3F1e70a93760")
        self.driver.refresh()

        # "I understand" кнопка
        self.automizer.click_button_by_xpath("/html/body/reach-portal[2]/div[3]/div/div/div/div/div/button[1]")
        # Открыть список монет
        self.automizer.click_button_by_xpath("/html/body/div[1]/div/div[2]/div[5]/main/div[2]/div[1]/div/div/div[1]/button")
        # Выбрать монеты usdc
        self.automizer.click_button_by_xpath("/html/body/reach-portal[2]/div[3]/div/div/div/div/div[3]/div[1]/div/div/div[./div[2]/div[text()='USDC']]")
        # Открыть список монет
        self.automizer.click_button_by_xpath("/html/body/div[1]/div/div[2]/div[5]/main/div[3]/div[1]/div/div/div/div[1]/button")
        # Выбрать монеты eth
        self.automizer.click_button_by_xpath("/html/body/reach-portal[2]/div[3]/div/div/div/div/div[3]/div[1]/div/div/div[./div[2]/div[text()='ETH']]")
        try:
            # Кнопка "max"
            self.automizer.click_button_by_xpath("/html/body/div[1]/div/div[2]/div[5]/main/div[2]/div[1]/div/div/div[2]/div/div[2]/button")
        except:
            return


        # Ожидаем подсчет
        time.sleep(3)
        # Проверка наличия "Allow the Uniswap Protocol to use your WETH"
        allow_button: bool = len(self.driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[2]/div[5]/main/div[3]/div[2]/div/div/button[1]")) > 0

        if allow_button:
            # "Allow the Uniswap Protocol to use your WETH"
            self.automizer.click_button_by_xpath(
                "/html/body/div[1]/div/div[2]/div[5]/main/div[3]/div[2]/div/div/button[1]")
            # Переключение на всплвающее окно
            self.automizer.switch_to_new_window()
            # "Max"
            self.automizer.click_button_by_xpath("/html/body/div[1]/div/div[2]/div/div[7]/div/div/label/div[2]/button/span")
            # "Next"
            self.automizer.click_button_by_xpath("/html/body/div[1]/div/div[2]/div/div[9]/footer/button[2]")
            # "Approve"
            self.automizer.click_button_by_xpath("/html/body/div[1]/div/div[2]/div/div[10]/footer/button[2]")
            # Переключение на исходное окно
            self.automizer.switch_to_prev_window()

        # Ожидание подсчетов
        time.sleep(3)
        # "Swap"
        self.automizer.click_button_by_id("swap-button")
        # "Confirm swap"
        self.automizer.click_button_by_id("confirm-swap-or-send")
        # Переключение на всплвающее окно
        self.automizer.switch_to_new_window()
        # "Confirm"
        self.automizer.click_button_by_xpath("/html/body/div[1]/div/div[2]/div/div[3]/div[3]/footer/button[2]")
        # Переключение на исходное окно
        self.automizer.switch_to_prev_window()
        # "Close"
        self.automizer.click_button_by_xpath("/html/body/reach-portal[2]/div[3]/div/div/div/div/div/div[3]/button")

