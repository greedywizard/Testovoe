import time

from selenium.common import NoAlertPresentException
from selenium.webdriver import Keys, ActionChains
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
        self.__automizer.click_button_by_xpath("//button[text()='Accept']")

        while True:
            try:
                # "Github"
                self.__automizer.click_button_by_xpath("//button[text()='GitHub']")
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
        self.__automizer.click_button_by_xpath("//button[text()='Import']")
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

        while True:
            try:
                self.__automizer.get_element_by_class_name("text-success")
                break
            except:
                pass


        # Открыть деплой
        self.__automizer.click_button_by_id("verticalIconsKindudapp")
        # Открыть список enviroment
        self.__automizer.click_button_by_xpath("/html/body/div[1]/div[1]/div[2]/section/div/div/div[6]/div/div[1]/div/div[1]/div[1]/div/div/button")
        # Выбрать inject metamsk
        self.__automizer.click_button_by_xpath("//a/span[text()='Injected Provider - MetaMask']")
        # Переключаемся на всплывающее окно
        self.__automizer.switch_to_new_window()
        # "Next"
        self.__automizer.click_button_by_xpath("//button[text()='Next']")
        # "Connect"
        self.__automizer.click_button_by_xpath("//button[text()='Connect']")
        # Переключение на основное окно
        self.__automizer.switch_to_prev_window()
        # Количество которое будем лочить
        self.__automizer.input_by_id("value", str(1))
        # Выбрать gwei
        self.__automizer.select_by_id("unit", "gwei")
        # Время лока
        self.__automizer.input_by_xpath("/html/body/div[1]/div[1]/div[2]/section/div/div/div[6]/div/div[1]/div/div[2]/div[3]/div[1]/div/div[1]/div[1]/input",
                                        str(1696118400))

        while True:
            try:
                # "Deploy"
                self.__automizer.click_button_by_xpath("//button[.//div[text()='Deploy']]")
                # Переключаемся на всплывающее окно
                self.__automizer.switch_to_new_window()
                # "Confirm"
                self.__automizer.click_button_by_xpath("//button[text()='Confirm']")
                # Переключение на основное окно
                self.__automizer.switch_to_prev_window()
                break
            except:
                pass


        # Получаем адресс токена
        address: str
        while True:
            try:
                element = self.__automizer.get_element_by_xpath("/html/body/div[1]/div[1]/div[2]/section/div/div/div[6]/div/div[1]/div/div[4]/div[2]/div/div[1]/div/div[2]/a/i")
                address = element.get_attribute("content")
                break
            except:
                pass

        return compile_version, address

    def deploy_token(self, code: str, name: str) -> str:
        self.__driver.get("https://remix.ethereum.org/")
        # Ожидание анимаций
        time.sleep(1)

        while True:
            try:
                # "New file"
                self.__automizer.click_button_by_xpath("//button[text()='New File']")
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

        # Ввод имени файла
        self.__automizer.click_button_by_id("createNewFile")
        action = ActionChains(self.__driver)
        action.send_keys(f"{name}.sol").perform()
        action.send_keys(Keys.ENTER).perform()
        # Открыть файл для редактирования
        self.__automizer.click_button_by_xpath(f"//span[text()='{name}.sol']")
        # Установка каретки в редактор
        self.__automizer.click_button_by_xpath("/html/body/div[1]/div[1]/div[5]/div[1]/div[2]/div/div/section/div/div/div[1]/div[2]/div[1]/div[4]")

        # Ввод кода
        code_arr = code.split('{')
        for i in range(code_arr.__len__()):
            if i != 0:
                action.send_keys('{')
                action.send_keys(Keys.DELETE).perform()
            action.send_keys(code_arr[i]).perform()

        # Открыть компилятор
        self.__automizer.click_button_by_id("verticalIconsKindsolidity")
        # "Compile"
        self.__automizer.click_button_by_id("compileBtn")

        while True:
            try:
                self.__automizer.get_element_by_class_name("text-success")
                break
            except:
                pass

        # Открыть деплой
        self.__automizer.click_button_by_id("verticalIconsKindudapp")
        # Открыть список enviroment
        self.__automizer.click_button_by_xpath("/html/body/div[1]/div[1]/div[2]/section/div/div/div[6]/div/div[1]/div/div[1]/div[1]/div/div/button")
        # Выбрать inject metamsk
        self.__automizer.click_button_by_xpath("//a/span[text()='Injected Provider - MetaMask']")

        while True:
            try:
                # "Deploy"
                self.__automizer.click_button_by_xpath("//button[.//div[text()='Deploy']]")
                # Переключаемся на всплывающее окно
                self.__automizer.switch_to_new_window()
                # "Confirm"
                self.__automizer.click_button_by_xpath("//button[text()='Confirm']")
                # Переключение на основное окно
                self.__automizer.switch_to_prev_window()
                break
            except:
                pass

        address: str
        while True:
            try:
                element = self.__automizer.get_element_by_xpath(
                    "/html/body/div[1]/div[1]/div[2]/section/div/div/div[6]/div/div[1]/div/div[4]/div[2]/div/div[1]/div/div[2]/a/i")
                address = element.get_attribute("content")
                break
            except:
                pass

        return address