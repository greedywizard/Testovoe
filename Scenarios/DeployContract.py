import time
from selenium.common import NoAlertPresentException
from selenium.webdriver.common.by import By
from Automizer.Scenario import Scenario, ScenarioResult
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
import Automizer.Actions as Actions
import URLs


class DeployContract(Scenario):
    def __init__(self,
                 driver: WebDriver,
                 wait: WebDriverWait):
        super().__init__(driver, wait)

    def Exec(self, args=None):
        result: ScenarioResult = ScenarioResult()

        Actions.OpenUrl(self, URLs.Remix)

        compile_version: str
        # Ожидание анимаций
        time.sleep(1)

        # "Accept"
        Actions.Click(self, By.XPATH, "//button[text()='Accept']")

        while True:
            try:
                # "Github"
                Actions.Click(self, By.XPATH, "//button[text()='GitHub']")
                break
            except:
                self.Driver.refresh()
                try:
                    Actions.AcceptAlert(self)
                except NoAlertPresentException:
                    pass

        # Ожидание анимаций
        time.sleep(2)

        # Без этого не работает ввод? ВТФ?
        Actions.Click(self, By.ID, "inputPrompt_text")
        # Ввод ссылки контракта
        Actions.Input(self, By.ID, "inputPrompt_text", "https://github.com/scroll-tech/scroll-contract-deploy-demo/blob/main/contracts/Lock.sol")
        # "Import"
        Actions.Click(self, By.XPATH, "//button[text()='Import']")
        try:
            # Выбрать файл
            Actions.Click(self, By.XPATH, "//span[text()='Lock.sol']")
        except:
            # Развернуть папки
            Actions.Click(self, By.XPATH, "//span[text()='github']")
            Actions.Click(self, By.XPATH, "//span[text()='scroll-tech']")
            Actions.Click(self, By.XPATH, "//span[text()='scroll-contract-deploy-demo']")
            Actions.Click(self, By.XPATH, "//span[text()='contracts']")
            # Выбрать файл
            Actions.Click(self, By.XPATH, "//span[text()='Lock.sol']")

        # Открыть компилятор
        Actions.Click(self, By.ID, "verticalIconsKindsolidity")
        result.ResultData["compile_version"] = Actions.GetElement(self, By.ID, "versionSelector").Element.text.split('soljson-')[1].split('.js')[0]
        # "Compile"
        Actions.Click(self, By.ID, "compileBtn")

        while True:
            try:
                Actions.GetElement(self, By.CLASS_NAME, "text-success")
                break
            except:
                pass

        # Открыть деплой
        Actions.Click(self, By.ID, "verticalIconsKindudapp")
        # Открыть список enviroment
        Actions.Click(self, By.XPATH, "/html/body/div[1]/div[1]/div[2]/section/div/div/div[6]/div/div[1]/div/div[1]/div[1]/div/div/button")
        # Выбрать inject metamsk
        res = Actions.Click(self, By.XPATH, "//a/span[text()='Injected Provider - MetaMask']")
        # Переключаемся на всплывающее окно
        self.Active_Window = res.New_Window
        # "Next"
        Actions.Click(self, By.XPATH, "//button[text()='Next']")
        # "Connect"
        Actions.Click(self, By.XPATH, "//button[text()='Connect']")
        # Переключение на основное окно
        self.Active_Window = res.Old_Window
        # Количество которое будем лочить
        Actions.Input(self, By.ID, "value", str(1))
        # Выбрать gwei
        Actions.Input(self, By.ID, "unit", "gwei")
        # Время лока
        Actions.Input(self, By.XPATH, "/html/body/div[1]/div[1]/div[2]/section/div/div/div[6]/div/div[1]/div/div[2]/div[3]/div[1]/div/div[1]/div[1]/input",
                                        str(1696118400))

        while True:
            try:
                # "Deploy"
                res = Actions.Click(self, By.XPATH, "//button[.//div[text()='Deploy']]")
                # Переключаемся на всплывающее окно
                self.Active_Window = res.New_Window
                # "Confirm"
                Actions.Click(self, By.XPATH, "//button[text()='Confirm']")
                # Переключение на основное окно
                self.Active_Window = res.Old_Window
                break
            except:
                pass

        while True:
            try:
                res = Actions.GetElement(self, By.XPATH, "/html/body/div[1]/div[1]/div[2]/section/div/div/div[6]/div/div[1]/div/div[4]/div[2]/div/div[1]/div/div[2]/a/i")
                result.ResultData["address"] = res.Element.get_attribute("content")
                break
            except:
                pass

        return result
