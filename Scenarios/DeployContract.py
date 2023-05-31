import time
from selenium.common import NoAlertPresentException
from selenium.webdriver.common.by import By

from Automizer.Enums import WindowActions
from Automizer.Logger import Logger
from Automizer.Scenario import Scenario
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
import Automizer.Actions as Actions
import URLs


class DeployContract(Scenario):
    class Result:
        def __init__(self):
            self.compile_version = None
            self.address = None

    def __init__(self,
                 driver: WebDriver,
                 wait: WebDriverWait):
        super().__init__(driver, wait)

    def _exec(self):
        Logger.Info("DeployContract()")
        result = self.Result()

        Actions.OpenUrl(self, URLs.Remix)

        compile_version: str
        # Ожидание анимаций
        time.sleep(1)

        # "Accept"
        Actions.Click(self, By.XPATH, "//button[text()='Accept']")

        while True:
            Logger.Info("Waiting github button...")
            try:
                # "Github"
                Actions.Click(self, By.XPATH, "//button[text()='GitHub']")
                break
            except:
                self.Driver.refresh()
                Actions.AcceptAlert(self)

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
        result.compile_version = Actions.GetElement(self, By.ID, "versionSelector").Element.text.split('soljson-')[1].split('.js')[0]
        # "Compile"
        Actions.Click(self, By.ID, "compileBtn")

        while True:
            Logger.Info("Compile contract...")
            try:
                Actions.GetElement(self, By.CLASS_NAME, "text-success")
                break
            except:
                return result

        # Открыть деплой
        Actions.Click(self, By.ID, "verticalIconsKindudapp")
        # Открыть список enviroment
        Actions.Click(self, By.XPATH, "/html/body/div[1]/div[1]/div[2]/section/div/div/div[6]/div/div[1]/div/div[1]/div[1]/div/div/button")
        # Выбрать inject metamsk
        res = Actions.Click(self, By.XPATH, "//a/span[text()='Injected Provider - MetaMask']", window_action=WindowActions.Open)
        # Переключаемся на всплывающее окно
        self.Active_Window = res.New_Window
        # "Next"
        Actions.Click(self, By.XPATH, "//button[text()='Next']")
        # "Connect"
        Actions.Click(self, By.XPATH, "//button[text()='Connect']", window_action=WindowActions.WaitClose)
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
            Logger.Info("Try start deploy...")
            try:
                # "Deploy"
                res = Actions.Click(self, By.XPATH, "//button[.//div[text()='Deploy']]", window_action=WindowActions.Open)
                # Переключаемся на всплывающее окно
                self.Active_Window = res.New_Window
                # "Confirm"
                Actions.Click(self, By.XPATH, "//button[text()='Confirm']", window_action=WindowActions.WaitClose)
                # Переключение на основное окно
                self.Active_Window = res.Old_Window
                break
            except:
                pass

        while True:
            Logger.Info("Deploying...")
            try:
                res = Actions.GetElement(self, By.XPATH, "/html/body/div[1]/div[1]/div[2]/section/div/div/div[6]/div/div[1]/div/div[4]/div[2]/div/div[1]/div/div[2]/a/i")
                result.address = res.Element.get_attribute("content")
                break
            except:
                pass

        return result
