import random
import string
import time
from collections import namedtuple
from typing import Type

from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By

import Scenarios
from Automizer.Act import Act
from Automizer.Enums import WindowActions
from Automizer.Logger import Logger
from Automizer.ExecEnvironment import ExecEnvironment
import Automizer.Actions as Actions
import URLs
from db import PipelineOptions


class BuildToken(Act):
    class Result:
        address: str = None

    def __init__(self, driver, wait, data: Type[PipelineOptions], next_point=None, restore_point=None):
        super().__init__(next_point, restore_point)
        self.__driver = driver
        self.__wait = wait
        self.__static_data = data
        self.s = ExecEnvironment(self.__driver, self.__wait)

        self.__deployTokenTuple = namedtuple('__deployTokenTuple', ['symbols', 'code'])

    def _restore(self, data):
        Scenarios.OpenMetamaskWallet(self.s, self.__static_data.seed_phrase)
        Scenarios.SetupMetamaskWallet(self.s)
        Scenarios.ConnectScroll(self.s)
        Scenarios.ConnectUniswap(self.s)

    def _base(self, dyna_data):
        res = self.__create_token()
        return self.__deploy_token(res.symbols, res.code)

    def __create_token(self):
        Logger.Info("CreateToken()")

        Actions.OpenUrl(self.s, URLs.OpenZeppelin_Wizard)

        Actions.AcceptAlert(self.s)

        iframe = Actions.GetElement(self.s, By.XPATH, "//oz-wizard/iframe").Element
        self.s.Driver.switch_to.frame(iframe)
        # "Mintable"
        Actions.Click(self.s, By.XPATH, "/html/body/div/div[2]/div[1]/div[1]/section[2]/div/label[1]/input")
        # очистить поле
        Actions.GetElement(self.s, By.XPATH, "/html/body/div/div[2]/div[1]/div[1]/section[1]/div/label[2]/input").Element.clear()
        # 3 рандомные буквы
        random_letter = ''.join(random.choices(string.ascii_uppercase, k=3))
        symbols = random_letter
        Actions.Input(self.s, By.XPATH, "/html/body/div/div[2]/div[1]/div[1]/section[1]/div/label[2]/input", random_letter)
        # много денях
        Actions.Input(self.s, By.XPATH, "/html/body/div/div[2]/div[1]/div[1]/section[1]/label/input", str(2124221))
        # Получить код контракта
        code = Actions.GetElement(self.s, By.XPATH, "/html/body/div/div[2]/div[2]/pre/code").Element.text
        self.s.Driver.switch_to.default_content()

        return self.__deployTokenTuple(symbols=symbols, code=code)

    def __deploy_token(self, symbols, code):
        Logger.Info("DeployToken()")

        Actions.OpenUrl(self.s, URLs.Remix)

        time.sleep(1)

        while True:
            Logger.Info("Try create new file...")
            try:
                # "New file"
                Actions.Click(self.s, By.XPATH, "//button[text()='New File']")
                break
            except:
                self.s.Driver.refresh()
                Actions.AcceptAlert(self.s)

        # Ввод имени файла
        Actions.Click(self.s, By.ID, "createNewFile")
        action_chain = ActionChains(self.s.Driver)
        action_chain.send_keys(f"{symbols}.sol").perform()
        action_chain.send_keys(Keys.ENTER).perform()
        # Открыть файл для редактирования
        Actions.Click(self.s, By.XPATH, f"//span[text()='{symbols}.sol']")
        # Установка каретки в редактор
        Actions.Click(self.s, By.XPATH, "/html/body/div[1]/div[1]/div[5]/div[1]/div[2]/div/div/section/div/div/div[1]/div[2]/div[1]/div[4]")

        # Ввод кода
        code_arr = code.split('{')
        for i in range(code_arr.__len__()):
            if i != 0:
                action_chain.send_keys('{')
                action_chain.send_keys(Keys.DELETE).perform()
            action_chain.send_keys(code_arr[i]).perform()

        # Открыть компилятор
        Actions.Click(self.s, By.ID, "verticalIconsKindsolidity")
        # "Compile"
        Actions.Click(self.s, By.ID, "compileBtn")

        while True:
            Logger.Info("Compiling...")
            try:
                Actions.GetElement(self.s, By.CLASS_NAME, "text-success")
                break
            except:
                pass

        # Открыть деплой
        Actions.Click(self.s, By.ID, "verticalIconsKindudapp")
        # Открыть список enviroment
        Actions.Click(self.s, By.XPATH, "/html/body/div[1]/div[1]/div[2]/section/div/div/div[6]/div/div[1]/div/div[1]/div[1]/div/div/button")
        # Выбрать inject metamsk
        Actions.Click(self.s, By.XPATH, "//a/span[text()='Injected Provider - MetaMask']")

        while True:
            Logger.Info("Try start deploy...")
            try:
                # "Deploy"
                res = Actions.Click(self.s, By.XPATH, "//button[.//div[text()='Deploy']]", window_action=WindowActions.Open)
                # Переключаемся на всплывающее окно
                self.s.Active_Window = res.New_Window
                # "Confirm"
                Actions.Click(self.s, By.XPATH, "//button[text()='Confirm']", window_action=WindowActions.WaitClose)
                # Переключение на основное окно
                self.s.Active_Window = res.Old_Window
                break
            except:
                pass

        result = self.Result()
        while True:
            Logger.Info("Deploying...")
            try:
                element = Actions.GetElement(self.s, By.XPATH,
                                             "/html/body/div[1]/div[1]/div[2]/section/div/div/div[6]/div/div[1]/div/div[4]/div[2]/div/div[1]/div/div[2]/a/i")
                result.address = element.Element.get_attribute("content")
                break
            except:
                pass

        return result