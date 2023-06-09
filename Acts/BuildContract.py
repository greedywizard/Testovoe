import time
from collections import namedtuple
from typing import Type

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import Scenarios
from Automizer.Act import Act
from Automizer.Enums import WindowActions
from Automizer.Logger import Logger
import Automizer.Actions as Actions
import URLs
from Objects import DObject
from db import PipelineOptions


class BuildContract(Act[Type[PipelineOptions], DObject]):
    def __init__(self, next_act: str = None):
        super().__init__()
        self._next_act = next_act
        self.__deployContractTuple = namedtuple('__deployContractTuple', ['address', 'compile_version'])

    def _restore(self, dyna_data):
        Scenarios.OpenMetamaskWallet(self.Env, self._static_data.seed_phrase)
        Scenarios.SetupMetamaskWallet(self.Env)
        Scenarios.ConnectScroll(self.Env)
        Scenarios.ConnectUniswap(self.Env)

    def _base(self, dyna_data):
        res = self.__deploy_contract()
        self.__validate_contract(res.address, res.compile_version)

    def __deploy_contract(self):
        Logger.Info("DeployContract()")

        Actions.OpenUrl(self.Env, URLs.Remix)

        compile_version: str
        # Ожидание анимаций
        time.sleep(1)

        # "Accept"
        if Actions.ExistElement(self.Env, By.XPATH, "//button[@data-id='matomoModal-modal-footer-ok-react']"):
            Actions.Click(self.Env, By.XPATH, "//button[@data-id='matomoModal-modal-footer-ok-react']")

        while True:
            Logger.Info("Waiting github button...")
            try:
                # "Github"
                Actions.Click(self.Env, By.XPATH, "//button[text()='GitHub']")
                break
            except:
                self.Env.Driver.refresh()
                Actions.AcceptAlert(self.Env)

        # Ожидание анимаций
        time.sleep(2)

        # Без этого не работает ввод? ВТФ?
        Actions.Click(self.Env, By.ID, "inputPrompt_text")
        # Ввод ссылки контракта
        Actions.Input(self.Env, By.ID, "inputPrompt_text", "https://github.com/scroll-tech/scroll-contract-deploy-demo/blob/main/contracts/Lock.sol")
        # "Import"
        Actions.Click(self.Env, By.XPATH, "//button[text()='Import']")
        try:
            # Выбрать файл
            Actions.Click(self.Env, By.XPATH, "//span[text()='Lock.sol']")
        except:
            # Развернуть папки
            Actions.Click(self.Env, By.XPATH, "//span[text()='github']")
            Actions.Click(self.Env, By.XPATH, "//span[text()='scroll-tech']")
            Actions.Click(self.Env, By.XPATH, "//span[text()='scroll-contract-deploy-demo']")
            Actions.Click(self.Env, By.XPATH, "//span[text()='contracts']")
            # Выбрать файл
            Actions.Click(self.Env, By.XPATH, "//span[text()='Lock.sol']")

        # Открыть компилятор
        Actions.Click(self.Env, By.ID, "verticalIconsKindsolidity")
        compile_version = Actions.GetElement(self.Env, By.ID, "versionSelector").Element.text.split('soljson-')[1].split('.js')[0]
        # "Compile"
        Actions.Click(self.Env, By.ID, "compileBtn")

        while True:
            Logger.Info("Compile contract...")
            try:
                Actions.GetElement(self.Env, By.CLASS_NAME, "text-success")
                break
            except:
                return

        # Открыть деплой
        Actions.Click(self.Env, By.ID, "verticalIconsKindudapp")
        # Открыть список enviroment
        Actions.Click(self.Env, By.XPATH, "/html/body/div[1]/div[1]/div[2]/section/div/div/div[6]/div/div[1]/div/div[1]/div[1]/div/div/button")
        # Выбрать inject metamsk
        Actions.Click(self.Env, By.XPATH, "//a/span[text()='Injected Provider - MetaMask']", window_action=WindowActions.Open)
        # "Next"
        Actions.Click(self.Env, By.XPATH, "//button[text()='Next']")
        # "Connect"
        Actions.Click(self.Env, By.XPATH, "//button[text()='Connect']", window_action=WindowActions.WaitClose)
        # Количество которое будем лочить
        Actions.Input(self.Env, By.ID, "value", str(1))
        # Выбрать gwei
        Actions.Input(self.Env, By.ID, "unit", "gwei")
        # Время лока
        Actions.Input(self.Env, By.XPATH, "/html/body/div[1]/div[1]/div[2]/section/div/div/div[6]/div/div[1]/div/div[2]/div[3]/div[1]/div/div[1]/div[1]/input",
                      str(1696118400))

        while True:
            Logger.Info("Try start deploy...")
            try:
                Actions.Click(self.Env, By.XPATH, "//button[.//div[text()='Deploy']]", window_action=WindowActions.Open)
                Actions.Click(self.Env, By.XPATH, "//button[text()='Confirm']", window_action=WindowActions.WaitClose)
                break
            except:
                pass

        while True:
            Logger.Info("Deploying...")
            try:
                res = Actions.GetElement(self.Env, By.XPATH, "/html/body/div[1]/div[1]/div[2]/section/div/div/div[6]/div/div[1]/div/div[4]/div[2]/div/div[1]/div/div[2]/a/i")
                address = res.Element.get_attribute("content")
                break
            except:
                pass

        return self.__deployContractTuple(address=address, compile_version=compile_version)

    def __validate_contract(self, address, compile_version):
        Logger.Info("ValidateContract()")

        res = Actions.OpenUrl(self.Env, f"https://blockscout.scroll.io/address/{address}/verify-via-flattened-code/new", in_new_window=True)

        Actions.AcceptAlert(self.Env)

        while True:
            selector: Select = Select(Actions.GetElement(self.Env, By.ID, "smart_contract_compiler_version").Element)
            if selector.options.__len__() == 0:
                self.Env.Driver.refresh()
            else:
                break

        try:
            Actions.Selector(self.Env, By.ID, "smart_contract_compiler_version", compile_version)
        except NoSuchElementException:
            pass

        # Выбор компилятора

        time.sleep(3)
        # "Publish"
        Actions.Click(self.Env, By.XPATH, "//button[text()='Verify & publish']")
        while True:
            Logger.Info("Publishing...")
            if Actions.WaitElementVisible(self.Env, By.ID, "loading", is_visible=False):
                break
            else:
                self.Env.Driver.refresh()

        Actions.CloseWindow(self.Env)
        self.Env.Active_Window = res.Old_Window
