from selenium.webdriver import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Metamask:
    timeout = 10

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def click_button(self, xpath: str) -> None:
        button: WebElement = WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(
            (By.XPATH, xpath)))
        button.click()

    def get_element(self, xpath: str) -> WebElement:
        return WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located(
            (By.XPATH, xpath)))

    def open_wallet(self, seed_phrase: str) -> None:
        self.click_button('/html/body/div[1]/div/div[2]/div/div/div/ul/li[2]/button')
        self.click_button('/html/body/div[1]/div/div[2]/div/div/div/div/button[1]')

        seed_arr = seed_phrase.split(' ')

        input_element = WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(
            (By.ID, 'import-srp__srp-word-0')))

        input_element.send_keys(seed_arr.pop(0))

        for i in seed_arr:
            input_element.send_keys(Keys.TAB, Keys.TAB)
            input_element = self.driver.switch_to.active_element
            input_element.send_keys(i)

        self.click_button('/html/body/div[1]/div/div[2]/div/div/div/div[4]/div/button')

        password: str = '12345678'
        input_element = self.driver.switch_to.active_element
        input_element.send_keys(password)
        input_element.send_keys(Keys.TAB)
        input_element = self.driver.switch_to.active_element
        input_element.send_keys(password)
        input_element.send_keys(Keys.TAB)
        check_box = self.driver.switch_to.active_element
        check_box.click()
        check_box.send_keys(Keys.TAB, Keys.TAB)
        button = self.driver.switch_to.active_element
        button.click()

        self.click_button('/html/body/div[1]/div/div[2]/div/div/div/div[2]/button')
        self.click_button('/html/body/div[1]/div/div[2]/div/div/div/div[2]/button')
        self.click_button('/html/body/div[1]/div/div[2]/div/div/div/div[2]/button')
        self.click_button('/html/body/div[2]/div/div/section/div[2]/div/button')

    def setup_wallet(self) -> None:
        # Открыть настройки
        self.driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#settings/advanced')
        # Переключить чекбокс "Show test networks"
        self.click_button('/html/body/div[1]/div/div[3]/div/div[2]/div[2]/div[2]/div[7]/div[2]/div/label/div[1]')
        # Закрыть настройки
        self.click_button('/html/body/div[1]/div/div[3]/div/div[1]/div[1]/div[2]')

    def add_test_networks(self):
        self.driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#settings/networks')

        self.click_button('/html/body/div[1]/div/div[3]/div/div[2]/div[2]/div/div[1]/div/button')
        self.click_button('/html/body/div[1]/div/div[3]/div/div[2]/div[2]/div/div[3]')

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

        self.click_button('/html/body/div[1]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[3]/button[2]')
        self.click_button('/html/body/div[2]/div/div/section/div/div/button[1]')
        self.click_button('/html/body/div[1]/div/div[1]/div/div[2]/div/div')

    def run(self) -> None:
        # переключится на сеть гоерли
        self.click_button('/html/body/div[1]/div/div[2]/div/div[2]/li[.//span[text()="Goerli test network"]]')

        e: WebElement = self.get_element('/html/body/div[1]/div/div[3]/div/div/div/div[3]/div/div'
                                         '[./div[2]/button/h2/span[text()="GoerliETH"]]')

        print(float(e.find_element(By.CLASS_NAME, 'asset-list-item__token-value').text) != 0.0)

        # Чекнуть есть ли баланс, если нет сбросить ак и выйти?
        if float(e.find_element(By.CLASS_NAME, 'asset-list-item__token-value').text) == 0.0:
            self.driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#settings/advanced')
            self.click_button('/html/body/div[1]/div/div[3]/div/div[2]/div[2]/div[2]/div[3]/div[2]/div/button')
            self.click_button('/html/body/div[1]/div/span/div[1]/div/div/div[2]/button[2]')
            return



