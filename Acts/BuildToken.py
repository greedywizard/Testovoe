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
import Automizer.Actions as Actions
import URLs
from Objects import DObject
from db import PipelineOptions


class BuildToken(Act[Type[PipelineOptions], DObject]):
    def __init__(self, next_act: str = None):
        super().__init__()
        self._next_act = next_act
        self.__deployTokenTuple = namedtuple('__deployTokenTuple', ['symbols', 'code'])

    def _restore(self, data):
        Scenarios.OpenMetamaskWallet(self.Env, self._static_data.seed_phrase)
        Scenarios.SetupMetamaskWallet(self.Env)
        Scenarios.ConnectScroll(self.Env)
        Scenarios.ConnectUniswap(self.Env)

    def _base(self, dyna_data):
        res = self.__create_token()
        dyna_data.new_token = self.__deploy_token(res.symbols, res.code)

    def __create_token(self):
        Logger.Info("CreateToken()")

        Actions.OpenUrl(self.Env, URLs.OpenZeppelin_Wizard)

        Actions.AcceptAlert(self.Env)

        iframe = Actions.GetElement(self.Env, By.XPATH, "//oz-wizard/iframe").Element
        self.Env.Driver.switch_to.frame(iframe)
        # "Mintable"
        Actions.Click(self.Env, By.XPATH, "/html/body/div/div[2]/div[1]/div[1]/section[2]/div/label[1]/input")
        # очистить поле
        Actions.GetElement(self.Env, By.XPATH, "/html/body/div/div[2]/div[1]/div[1]/section[1]/div/label[2]/input").Element.clear()
        # 3 рандомные буквы
        random_letter = ''.join(random.choices(string.ascii_uppercase, k=3))
        symbols = random_letter
        Actions.Input(self.Env, By.XPATH, "/html/body/div/div[2]/div[1]/div[1]/section[1]/div/label[2]/input", random_letter)
        # много денях
        Actions.Input(self.Env, By.XPATH, "/html/body/div/div[2]/div[1]/div[1]/section[1]/label/input", str(21242))
        # Получить код контракта
        code = Actions.GetElement(self.Env, By.XPATH, "/html/body/div/div[2]/div[2]/pre/code").Element.text
        self.Env.Driver.switch_to.default_content()

        return self.__deployTokenTuple(symbols=symbols, code=code)

    def __deploy_token(self, symbols, code) -> str:
        Logger.Info("DeployToken()")

        Actions.OpenUrl(self.Env, URLs.Remix)

        time.sleep(1)

        if Actions.ExistElement(self.Env, By.XPATH, "//button[@data-id='matomoModal-modal-footer-ok-react']"):
            Actions.Click(self.Env, By.XPATH, "//button[@data-id='matomoModal-modal-footer-ok-react']")

        while True:
            Logger.Info("Try create new file...")
            try:
                # "New file"
                Actions.Click(self.Env, By.XPATH, "//button[text()='New File']")
                break
            except:
                self.Env.Driver.refresh()
                Actions.AcceptAlert(self.Env)

        # Ввод имени файла
        Actions.Click(self.Env, By.ID, "createNewFile")
        action_chain = ActionChains(self.Env.Driver)
        action_chain.send_keys(f"{symbols}.sol").perform()
        action_chain.send_keys(Keys.ENTER).perform()
        # Открыть файл для редактирования
        Actions.Click(self.Env, By.XPATH, f"//span[text()='{symbols}.sol']")
        # Установка каретки в редактор
        Actions.Click(self.Env, By.XPATH, "/html/body/div[1]/div[1]/div[5]/div[1]/div[2]/div/div/section/div/div/div[1]/div[2]/div[1]/div[4]")

        # Ввод кода
        code_arr = code.split('{')
        for i in range(code_arr.__len__()):
            if i != 0:
                action_chain.send_keys('{')
                action_chain.send_keys(Keys.DELETE).perform()
            action_chain.send_keys(code_arr[i]).perform()

        # Открыть компилятор
        Actions.Click(self.Env, By.ID, "verticalIconsKindsolidity")
        # "Compile"
        Actions.Click(self.Env, By.ID, "compileBtn")

        while True:
            Logger.Info("Compiling...")
            try:
                Actions.GetElement(self.Env, By.CLASS_NAME, "text-success")
                break
            except:
                pass

        # Открыть деплой
        Actions.Click(self.Env, By.ID, "verticalIconsKindudapp")
        # Открыть список enviroment
        Actions.Click(self.Env, By.XPATH, "/html/body/div[1]/div[1]/div[2]/section/div/div/div[6]/div/div[1]/div/div[1]/div[1]/div/div/button")
        # Выбрать inject metamsk
        Actions.Click(self.Env, By.XPATH, "//a/span[text()='Injected Provider - MetaMask']")

        while True:
            Logger.Info("Connecting wallet")
            if self._isRestore:
                Actions.Click(self.Env, By.XPATH, "//button[.//div[text()='Deploy']]", window_action=WindowActions.Open)
                Actions.Click(self.Env, By.XPATH, "//button[text()='Next']")
                Actions.Click(self.Env, By.XPATH, "//button[text()='Connect']", window_action=WindowActions.WaitClose)
                break
            else:
                break

        if Actions.ExistElement(self.Env, By.XPATH, "//button[@data-id='udappNotify-modal-footer-ok-react']"):
            Actions.Click(self.Env, By.XPATH, "//button[@data-id='udappNotify-modal-footer-ok-react']")

        while True:
            Logger.Info("Try start deploy...")
            try:
                Actions.Click(self.Env, By.XPATH, "//button[.//div[text()='Deploy']]", window_action=WindowActions.Open)
                Actions.Click(self.Env, By.XPATH, "//button[text()='Confirm']", window_action=WindowActions.WaitClose)
                break
            except:
                pass

        address: str = None
        while True:
            Logger.Info("Deploying...")
            try:
                element = Actions.GetElement(self.Env, By.XPATH,
                                             "/html/body/div[1]/div[1]/div[2]/section/div/div/div[6]/div/div[1]/div/div[4]/div[2]/div/div[1]/div/div[2]/a/i")
                address = element.Element.get_attribute("content")
                break
            except:
                pass

        return address
