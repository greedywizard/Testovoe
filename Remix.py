import time

from selenium.common import NoAlertPresentException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from Automizer import Automizer

class Remix:
    def __init__(self, driver: WebDriver):
        self.__driver: WebDriver = driver
        self.__wait = WebDriverWait(driver, 10)
        self.__automizer = Automizer(driver, wait_time=15)

    def deploy_contract(self) -> (str, str):
        self.__driver.get("https://remix.ethereum.org/")

        compile_version: str
        # Ожидание анимаций
        time.sleep(1)

        # "Accept"
        self.__automizer.click_button_by_xpath("/html/body/div[1]/div[3]/div/div/div[3]/button[1]")

        while True:
            try:
                # "Github"
                self.__automizer.click_button_by_xpath("/html/body/div[1]/div[1]/div[5]/div[1]/div[3]/div/div/div/div/div/div/div/div[1]/div[4]/div[2]/button[1]")
                break
            except:
                self.__driver.refresh()
                try:
                    # Проверьте наличие модального диалога и примите его, если он есть
                    alert = self.__driver.switch_to.alert
                    alert.accept()
                except NoAlertPresentException:
                    # Продолжить, если нет модального диалога
                    pass

        # Ожидание анимаций
        time.sleep(2)

        # Без этого не работает ввод? ВТФ?
        self.__automizer.click_button_by_id("inputPrompt_text")
        # Ввод ссылки контракта
        self.__automizer.input_by_id("inputPrompt_text", "https://github.com/scroll-tech/scroll-contract-deploy-demo/blob/main/contracts/Lock.sol")
        # "Import"
        self.__automizer.click_button_by_xpath("/html/body/div[1]/div[1]/div[5]/div[1]/div[3]/div/div/div/div/div/div/div/div[1]/div[2]/div/div/div[3]/button")
        try:
            # Выбрать файл
            self.__automizer.click_button_by_xpath("//span[text()='Lock.sol']")
        except:
            # Развернуть папки
            self.__automizer.click_button_by_xpath("//span[text()='github']")
            self.__automizer.click_button_by_xpath("//span[text()='scroll-tech']")
            self.__automizer.click_button_by_xpath("//span[text()='scroll-contract-deploy-demo']")
            self.__automizer.click_button_by_xpath("//span[text()='contracts']")
            # Выбрать файл
            self.__automizer.click_button_by_xpath("//span[text()='Lock.sol']")

        # Открыть компилятор
        self.__automizer.click_button_by_id("verticalIconsKindsolidity")
        compile_version = self.__automizer.get_element_by_id("versionSelector").text.split('soljson-')[1].split('.js')[0]
        # "Compile"
        self.__automizer.click_button_by_id("compileBtn")
        # Открыть деплой
        self.__automizer.click_button_by_id("verticalIconsKindudapp")
        # Открыть список enviroment
        self.__automizer.click_button_by_xpath("/html/body/div[1]/div[1]/div[2]/section/div/div/div[6]/div/div[1]/div/div[1]/div[1]/div/div/button")
        # Выбрать inject metamsk
        self.__automizer.click_button_by_xpath("//a/span[text()='Injected Provider - MetaMask']")
        # Переключаемся на всплывающее окно
        self.__automizer.switch_to_new_window()
        # "Next"
        self.__automizer.click_button_by_xpath("/html/body/div[1]/div/div[2]/div/div[3]/div[2]/button[2]")
        # "Connect"
        self.__automizer.click_button_by_xpath("/html/body/div[1]/div/div[2]/div/div[2]/div[2]/div[2]/footer/button[2]")
        # Переключение на основное окно
        self.__automizer.switch_to_prev_window()
        # Количество которое будем лочить
        self.__automizer.input_by_id("value", str(1))
        # Выбрать gwei
        self.__automizer.select_by_id("unit", "gwei")
        # Время лока
        self.__automizer.input_by_xpath("/html/body/div[1]/div[1]/div[2]/section/div/div/div[6]/div/div[1]/div/div[2]/div[3]/div[1]/div/div[1]/div[1]/input",
                                        str(1696118400))
        self.__automizer.click_button_by_xpath("/html/body/div[1]/div[1]/div[2]/section/div/div/div[6]/div/div[1]/div/div[2]/div[3]/div[1]/div/div[1]/div[1]/button")
        # Переключаемся на всплывающее окно
        self.__automizer.switch_to_new_window()
        # "Confirm"
        self.__automizer.click_button_by_xpath("//button[text()='Confirm']")
        # Переключение на основное окно
        self.__automizer.switch_to_prev_window()
        #
        address: str
        while True:
            try:
                element = self.__automizer.get_element_by_xpath("/html/body/div[1]/div[1]/div[2]/section/div/div/div[6]/div/div[1]/div/div[4]/div[2]/div/div[1]/div/div[2]/a/i")
                address = element.get_attribute("content")
                break
            except:
                pass

        return compile_version, address

    def deploy_token(self, code: str, name: str):
        self.__driver.get("https://remix.ethereum.org/")
        # Ожидание анимаций
        time.sleep(1)

        # "Accept"
        self.__automizer.click_button_by_xpath("/html/body/div[1]/div[3]/div/div/div[3]/button[1]")

        while True:
            try:
                # "New file"
                self.__automizer.click_button_by_xpath("/html/body/div[1]/div[1]/div[5]/div[1]/div[3]/div/div/div/div/div/div/div/div[1]/div[4]/div[1]/button[1]")
                break
            except:
                self.__driver.refresh()
                try:
                    # Проверьте наличие модального диалога и примите его, если он есть
                    alert = self.__driver.switch_to.alert
                    alert.accept()
                except NoAlertPresentException:
                    # Продолжить, если нет модального диалога
                    pass

        self.__automizer.click_button_by_id("createNewFile")
        input_element = self.__driver.switch_to.active_element
        input_element.send_keys(f"{name}.sol")
