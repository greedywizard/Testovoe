import time
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By

from Automizer.Enums import WindowActions
from Automizer.Logger import Logger
from Automizer.Scenario import Scenario, ScenarioResult
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
import Automizer.Actions as Actions
import URLs


class DeployToken(Scenario):
    def __init__(self,
                 driver: WebDriver,
                 wait: WebDriverWait):
        super().__init__(driver, wait)

    def Exec(self, args=None):
        Logger.Info("CreateToken()")
        result: ScenarioResult = ScenarioResult()

        Actions.OpenUrl(self, URLs.Remix)

        time.sleep(1)

        while True:
            Logger.Info("Try create new file...")
            try:
                # "New file"
                Actions.Click(self, By.XPATH, "//button[text()='New File']")
                break
            except:
                self.Driver.refresh()
                Actions.AcceptAlert(self)

        # Ввод имени файла
        Actions.Click(self, By.ID, "createNewFile")
        action_chain = ActionChains(self.Driver)
        action_chain.send_keys(f"{args['name']}.sol").perform()
        action_chain.send_keys(Keys.ENTER).perform()
        # Открыть файл для редактирования
        Actions.Click(self, By.XPATH, f"//span[text()='{args['name']}.sol']")
        # Установка каретки в редактор
        Actions.Click(self, By.XPATH, "/html/body/div[1]/div[1]/div[5]/div[1]/div[2]/div/div/section/div/div/div[1]/div[2]/div[1]/div[4]")

        # Ввод кода
        code_arr = args['code'].split('{')
        for i in range(code_arr.__len__()):
            if i != 0:
                action_chain.send_keys('{')
                action_chain.send_keys(Keys.DELETE).perform()
            action_chain.send_keys(code_arr[i]).perform()

        # Открыть компилятор
        Actions.Click(self, By.ID, "verticalIconsKindsolidity")
        # "Compile"
        Actions.Click(self, By.ID, "compileBtn")

        while True:
            Logger.Info("Compiling...")
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
        Actions.Click(self, By.XPATH, "//a/span[text()='Injected Provider - MetaMask']")

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
                element = Actions.GetElement(self, By.XPATH,
                    "/html/body/div[1]/div[1]/div[2]/section/div/div/div[6]/div/div[1]/div/div[4]/div[2]/div/div[1]/div/div[2]/a/i")
                result.ResultData["address"] = element.Element.get_attribute("content")
                break
            except:
                pass

        return result
