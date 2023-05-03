import time

from selenium.webdriver import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException

from Automizer import Automizer
from ShadowDom import ShadowDOM


class ScrollIo:
    def __init__(self, driver: WebDriver):
        self.driver: WebDriver = driver
        self.wait = WebDriverWait(driver, 20)
        self.automizer = Automizer(driver, wait_time=15)


    def connect_metamask(self):
        self.driver.get("https://scroll.io/alpha")
        self.driver.refresh()

        shadow_dom = ShadowDOM(self.driver, shadow_xpath="/html/body/onboard-v2", wait_time=3)

        # "Connect wallet" кнопка от Scroll Alpha Testnet
        self.automizer.click_button_by_xpath("/html/body/div/div/div[1]/div[1]/div[2]/dl/div[2]/div[2]/dd/ul/li/div[2]/a")
        # "Metamask" кнопка
        shadow_dom.click_button_by_css(
            "section > div > div > div > div > div > div > div > div.scroll-container.svelte-1qwmck3 > div > div > div > div.wallet-button-container.svelte-1vlog3j > button > div")
        # Переключение на появившееся окно подтверждения
        self.automizer.switch_to_new_window()
        # "Next" кнопка
        self.automizer.click_button_by_xpath("/html/body/div[1]/div/div[2]/div/div[3]/div[2]/button[2]")
        # "Connect"" кнопка
        self.automizer.click_button_by_xpath("/html/body/div[1]/div/div[2]/div/div[2]/div[2]/div[2]/footer/button[2]")
        # Перключение обратно на исходное окно
        self.automizer.switch_to_prev_window()

    def transfer_goerli_to_alphatest(self, value: float):
        self.driver.get("https://scroll.io/alpha/bridge")
        self.driver.refresh()

        # Получить количество токенов
        e = float(self.automizer.get_element_by_xpath("/html/body/div/div[1]/div[1]/div[3]/div/div[1]/div[2]/div[2]/h6").text.split(' ')[1])
        # Ввести 99.4% от максимального значения
        self.automizer.input_by_id(':r0:', str(e * (1 - 0.6 / 100)))
        # "Send ETH to Scroll Alpha Test" кнопка
        self.automizer.click_button_by_id(":r2:")
        # Переключиться на всплывающее окно
        self.automizer.switch_to_new_window()
        # "Confirm" кнопка
        self.automizer.click_button_by_xpath("/html/body/div[1]/div/div[2]/div/div[3]/div[3]/footer/button[2]")
        # Переключиться на предыдущее окно
        self.automizer.switch_to_prev_window()
