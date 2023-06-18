import random
from collections import namedtuple
from typing import Type

from selenium.webdriver.common.by import By

import Scenarios
from Automizer.Act import Act
from Automizer.Logger import Logger
import Automizer.Actions as Actions
import URLs
from Objects import DObject
from db import PipelineOptions


class PlayWithTokenInMetamask(Act[Type[PipelineOptions], DObject]):
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
        self.__add_token(dyna_data.new_token)
        self.__swap_to_scrollAlpha()
        self.__create_second_account()
        self.__send_between_accounts("Account 1", "scroll2")
        self.__send_between_accounts("scroll2", "Account 1", lambda x: x/2)
        Actions.OpenUrl(self.Env, URLs.Metamask_Home)
        Actions.Click(self.Env, By.XPATH, "//button[@data-testid='account-menu-icon']", as_script=True)
        Actions.Click(self.Env, By.XPATH, f"//button[.//div[3]/div[text()='Account 1']]", as_script=True)

    def __add_token(self, address):
        Logger.Info("AddToken()")

        Actions.OpenUrl(self.Env, URLs.Metamask_ImportToken)

        Actions.AcceptAlert(self.Env)

        Actions.Input(self.Env, By.ID, "custom-address", address)

        while True:
            Logger.Info("Importing token...")
            try:
                Actions.WaitAttributeChanged(self.Env, By.ID, "custom-symbol", "value", "")
                break
            except:
                pass

        Actions.Click(self.Env, By.XPATH, "//button[text()='Add custom token']", as_script=True)
        Actions.Click(self.Env, By.XPATH, "//button[text()='Import tokens']", as_script=True)

    def __swap_to_scrollAlpha(self):
        Logger.Info("SwapToScrollAlpha()")

        Actions.OpenUrl(self.Env, URLs.Metamask_Home)

        # Открыть свиписок сетей
        Actions.Click(self.Env, By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div/div', as_script=True)
        # Выбрать сеть goerli
        Actions.Click(self.Env, By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/li[.//span[contains(text(), "Scroll Alpha")]]', as_script=True)

    def __create_second_account(self):
        Logger.Info("CreateSecondAccount()")

        Actions.OpenUrl(self.Env, URLs.Metamask_NewAccount)
        Actions.Input(self.Env, By.XPATH, "/html/body/div[1]/div/div[3]/div/div/div[2]/input", "scroll2")
        Actions.Click(self.Env, By.XPATH, "//button[text()='Create']")
        Actions.GetElement(self.Env, By.XPATH, "//div[text()='scroll2']", is_visible=False)

    def __send_between_accounts(self, account_from, account_to, rand=None):
        Logger.Info("SendBetweenAccounts()")
        Actions.OpenUrl(self.Env, URLs.Metamask_Home)

        Actions.Click(self.Env, By.XPATH, "//button[@data-testid='account-menu-icon']", as_script=True)
        #
        Actions.Click(self.Env, By.XPATH, f"//button[.//div[3]/div[text()='{account_from}']]", as_script=True)

        Actions.Click(self.Env, By.XPATH, "//button[@data-testid='eth-overview-send']", as_script=True)
        # Открыть список аккаунтов
        Actions.Click(self.Env, By.XPATH, "//a[text()='Transfer between my accounts']", as_script=True)
        # Выбрать 2 аккаунт
        Actions.Click(self.Env, By.XPATH, f"//div[text()='{account_to}']", as_script=True)
        #
        max_value = float(Actions.GetElement(self.Env, By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[3]/div/div[1]/div[2]/div/div/div/div[2]/div[2]/div/span[2]').Element.text)

        if rand:
            rand_value = rand(max_value)
        else:
            if max_value >= 0.0015:
                rand_value = random.randint(5, 15) / 10000
            else:
                rand_value = max_value

        # Ввести значения
        Actions.Input(self.Env, By.XPATH, "/html/body/div[1]/div/div[3]/div/div[3]/div/div[2]/div[2]/div[1]/div/div/div[1]/input", str(rand_value))

        Actions.Click(self.Env, By.XPATH, "//button[@data-testid='page-container-footer-next']", as_script=True)
        Actions.Click(self.Env, By.XPATH, "//button[@data-testid='page-container-footer-next']", as_script=True)

        while True:
            Logger.Info(f"Pending ({account_from} -> {account_to})...")
            try:
                Actions.Click(self.Env, By.XPATH, "/html/body/div[1]/div/div[3]/div/div/div/div[3]/div/div/div/div/div[1]", is_visible=False, is_clickable=False, as_script=True)
                if Actions.GetElement(self.Env, By.XPATH, "/html/body/div[2]/div/div/section/div[2]/div/div[2]/div[1]/div[2]/div", is_visible=False).Element.text == "Confirmed":
                    break
            except:
                pass
