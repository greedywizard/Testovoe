import time
from collections import namedtuple
from typing import Type

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

import Scenarios
from Automizer.Act import Act
from Automizer.Enums import WindowActions
from Automizer.Logger import Logger
from Automizer.ExecEnvironment import ExecEnvironment
import Automizer.Actions as Actions
import URLs
from db import PipelineOptions


class BuildContract(Act):
    def __init__(self, driver, wait, data: Type[PipelineOptions], next_point=None, restore_point=None):
        super().__init__(next_point, restore_point)
        self.__driver = driver
        self.__wait = wait
        self.__static_data = data
        self.s = ExecEnvironment(self.__driver, self.__wait)

        self.__deployContractTuple = namedtuple('__deployContractTuple', ['address', 'compile_version'])

    def _restore(self, data):
        Scenarios.OpenMetamaskWallet(self.s, self.__static_data.seed_phrase)
        Scenarios.SetupMetamaskWallet(self.s)
        Scenarios.ConnectScroll(self.s)
        Scenarios.ConnectUniswap(self.s)

    def _base(self, dyna_data):
        res = self.__deploy_contract()
        self.__validate_contract(res.address, res.compile_version)

    def __deploy_contract(self):
        Logger.Info("DeployContract()")

        Actions.OpenUrl(self.s, URLs.Remix)

        compile_version: str
        # Ожидание анимаций
        time.sleep(1)

        # "Accept"
        Actions.Click(self.s, By.XPATH, "//button[text()='Accept']")

        while True:
            Logger.Info("Waiting github button...")
            try:
                # "Github"
                Actions.Click(self.s, By.XPATH, "//button[text()='GitHub']")
                break
            except:
                self.s.Driver.refresh()
                Actions.AcceptAlert(self.s)

        # Ожидание анимаций
        time.sleep(2)

        # Без этого не работает ввод? ВТФ?
        Actions.Click(self.s, By.ID, "inputPrompt_text")
        # Ввод ссылки контракта
        Actions.Input(self.s, By.ID, "inputPrompt_text", "https://github.com/scroll-tech/scroll-contract-deploy-demo/blob/main/contracts/Lock.sol")
        # "Import"
        Actions.Click(self.s, By.XPATH, "//button[text()='Import']")
        try:
            # Выбрать файл
            Actions.Click(self.s, By.XPATH, "//span[text()='Lock.sol']")
        except:
            # Развернуть папки
            Actions.Click(self.s, By.XPATH, "//span[text()='github']")
            Actions.Click(self.s, By.XPATH, "//span[text()='scroll-tech']")
            Actions.Click(self.s, By.XPATH, "//span[text()='scroll-contract-deploy-demo']")
            Actions.Click(self.s, By.XPATH, "//span[text()='contracts']")
            # Выбрать файл
            Actions.Click(self.s, By.XPATH, "//span[text()='Lock.sol']")

        # Открыть компилятор
        Actions.Click(self.s, By.ID, "verticalIconsKindsolidity")
        compile_version = Actions.GetElement(self.s, By.ID, "versionSelector").Element.text.split('soljson-')[1].split('.js')[0]
        # "Compile"
        Actions.Click(self.s, By.ID, "compileBtn")

        while True:
            Logger.Info("Compile contract...")
            try:
                Actions.GetElement(self.s, By.CLASS_NAME, "text-success")
                break
            except:
                return

        # Открыть деплой
        Actions.Click(self.s, By.ID, "verticalIconsKindudapp")
        # Открыть список enviroment
        Actions.Click(self.s, By.XPATH, "/html/body/div[1]/div[1]/div[2]/section/div/div/div[6]/div/div[1]/div/div[1]/div[1]/div/div/button")
        # Выбрать inject metamsk
        Actions.Click(self.s, By.XPATH, "//a/span[text()='Injected Provider - MetaMask']", window_action=WindowActions.Open)
        # "Next"
        Actions.Click(self.s, By.XPATH, "//button[text()='Next']")
        # "Connect"
        Actions.Click(self.s, By.XPATH, "//button[text()='Connect']", window_action=WindowActions.WaitClose)
        # Количество которое будем лочить
        Actions.Input(self.s, By.ID, "value", str(1))
        # Выбрать gwei
        Actions.Input(self.s, By.ID, "unit", "gwei")
        # Время лока
        Actions.Input(self.s, By.XPATH, "/html/body/div[1]/div[1]/div[2]/section/div/div/div[6]/div/div[1]/div/div[2]/div[3]/div[1]/div/div[1]/div[1]/input",
                      str(1696118400))

        while True:
            Logger.Info("Try start deploy...")
            try:
                Actions.Click(self.s, By.XPATH, "//button[.//div[text()='Deploy']]", window_action=WindowActions.Open)
                Actions.Click(self.s, By.XPATH, "//button[text()='Confirm']", window_action=WindowActions.WaitClose)
                break
            except:
                pass

        while True:
            Logger.Info("Deploying...")
            try:
                res = Actions.GetElement(self.s, By.XPATH, "/html/body/div[1]/div[1]/div[2]/section/div/div/div[6]/div/div[1]/div/div[4]/div[2]/div/div[1]/div/div[2]/a/i")
                address = res.Element.get_attribute("content")
                break
            except:
                pass

        return self.__deployContractTuple(address=address, compile_version=compile_version)

    def __validate_contract(self, address, compile_version):
        Logger.Info("ValidateContract()")

        res = Actions.OpenUrl(self.s, f"https://blockscout.scroll.io/address/{address}/verify-via-flattened-code/new", in_new_window=True)

        Actions.AcceptAlert(self.s)

        try:
            Actions.Selector(self.s, By.ID, "smart_contract_compiler_version", compile_version)
        except NoSuchElementException:
            pass
        # Выбор компилятора

        time.sleep(3)
        # "Publish"
        Actions.Click(self.s, By.XPATH, "//button[text()='Verify & publish']")
        while True:
            Logger.Info("Publishing...")
            try:
                # self.Driver.refresh()
                Actions.WaitElementVisible(self.s, By.ID, "loading", hide=True)
                break
            except:
                pass

        self.s.Active_Window = res.Old_Window
        self.s.Driver.close()
