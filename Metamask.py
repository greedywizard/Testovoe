import time
from selenium.webdriver import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from Automizer import Automizer


class Metamask:
    def __init__(self, driver: WebDriver):
        self.driver: WebDriver = driver
        self.wait = WebDriverWait(driver, 10)
        self.automizer = Automizer(driver, wait_time=15)

    def open_wallet(self, seed_phrase: str) -> None:
        self.driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
        self.driver.refresh()
        # "Import wallet" кнопка
        self.automizer.click_button_by_xpath('/html/body/div[1]/div/div[2]/div/div/div/ul/li[2]/button')
        # "I agree" кнопка
        self.automizer.click_button_by_xpath('/html/body/div[1]/div/div[2]/div/div/div/div/button[1]')

        # Ввод seed фразы
        seed_arr = seed_phrase.split(' ')
        input_element = self.automizer.get_element_by_id('import-srp__srp-word-0')
        input_element.send_keys(seed_arr.pop(0))

        for i in seed_arr:
            input_element.send_keys(Keys.TAB, Keys.TAB)
            input_element = self.driver.switch_to.active_element
            input_element.send_keys(i)

        # "Condirm" кнопка
        self.automizer.click_button_by_xpath('/html/body/div[1]/div/div[2]/div/div/div/div[4]/div/button')
        # Ввод пароля
        password: str = '12345678'
        input_element = self.driver.switch_to.active_element
        input_element.send_keys(password)
        input_element.send_keys(Keys.TAB)
        input_element = self.driver.switch_to.active_element
        input_element.send_keys(password)
        input_element.send_keys(Keys.TAB)
        # Чекбокс
        check_box = self.driver.switch_to.active_element
        check_box.click()
        check_box.send_keys(Keys.TAB, Keys.TAB)
        # "Import" кнопка
        button = self.driver.switch_to.active_element
        button.click()

        time.sleep(3)
        # "Got it" кнопка
        self.automizer.click_button_by_xpath('/html/body/div[1]/div/div[2]/div/div/div/div[2]/button')
        # "Next"
        self.automizer.click_button_by_xpath('/html/body/div[1]/div/div[2]/div/div/div/div[2]/button')
        # "Done"
        self.automizer.click_button_by_xpath('/html/body/div[1]/div/div[2]/div/div/div/div[2]/button')

    def setup_wallet(self) -> None:
        # Открыть настройки
        self.driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#settings/advanced')
        self.driver.refresh()
        # Переключить чекбокс "Show test networks"
        self.automizer.click_button_by_xpath('/html/body/div[1]/div/div[3]/div/div[2]/div[2]/div[2]/div[7]/div[2]/div/label/div[1]')
        # Закрыть настройки
        self.automizer.click_button_by_xpath('/html/body/div[1]/div/div[3]/div/div[1]/div[1]/div[2]')

    def add_test_networks(self):
        self.driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#settings/networks')
        self.driver.refresh()
        self.automizer.click_button_by_xpath('/html/body/div[1]/div/div[3]/div/div[2]/div[2]/div/div[1]/div/button')
        self.automizer.click_button_by_xpath('/html/body/div[1]/div/div[3]/div/div[2]/div[2]/div/div[3]')

        # добавить сеть
        # Network name
        input_element = self.driver.switch_to.active_element
        input_element.send_keys('Scroll Alpha Testnet')
        # New RPC URL
        input_element.send_keys(Keys.TAB)
        input_element = self.driver.switch_to.active_element
        input_element.send_keys('https://alpha-rpc.scroll.io/l2')
        # Chain ID
        input_element.send_keys(Keys.TAB, Keys.TAB)
        input_element = self.driver.switch_to.active_element
        input_element.send_keys('534353')
        # Currency symbol
        input_element.send_keys(Keys.TAB)
        input_element = self.driver.switch_to.active_element
        input_element.send_keys('ETH')
        # Currency symbol
        input_element.send_keys(Keys.TAB)
        input_element = self.driver.switch_to.active_element
        input_element.send_keys('https://blockscout.scroll.io')

        self.automizer.click_button_by_xpath('/html/body/div[1]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[3]/button[2]')
        self.automizer.click_button_by_xpath('/html/body/div[2]/div/div/section/div/div/button[1]')

    def check_balance(self) -> float:
        self.driver.get("chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html")

        # Открыть свиписок сетей
        self.automizer.click_button_by_xpath('/html/body/div[1]/div/div[1]/div/div[2]/div/div', as_mouse=False)
        # Выбрать сеть goerli
        self.automizer.click_button_by_xpath('/html/body/div[1]/div/div[2]/div/div[2]/li[.//span[text()="Goerli test network"]]', as_mouse=False)
        # Получить количество монет
        e: WebElement = self.automizer.get_element_by_xpath('/html/body/div[1]/div/div[3]/div/div/div/div[3]/div/div[./div[2]/button/h2/span[text()="GoerliETH"]]')
        time.sleep(5)
        v = float(e.find_element(By.CLASS_NAME, 'asset-list-item__token-value').text)

        if v == 0.0:
            return 0.0
        else:
            return v

    def clear_account(self):
        self.driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#settings/advanced')
        self.driver.refresh()
        self.automizer.click_button_by_xpath('/html/body/div[1]/div/div[3]/div/div[2]/div[2]/div[2]/div[3]/div[2]/div/button')
        self.automizer.click_button_by_xpath('/html/body/div[1]/div/span/div[1]/div/div/div[2]/button[2]')


