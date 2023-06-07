import json
import time
from typing import Type

import requests
from selenium.webdriver.common.by import By

import Scenarios
from Automizer.Act import Act
from Automizer.Logger import Logger
from Automizer.ExecEnvironment import ExecEnvironment
import Automizer.Actions as Actions
import URLs
from DynaData import DynaData
from db import PipelineOptions


class WaitTransferGoerliToAlpha(Act):
    def __init__(self, driver, wait, data: Type[PipelineOptions], next_point=None, restore_point=None):
        super().__init__(next_point, restore_point)
        self.__driver = driver
        self.__wait = wait
        self.__static_data = data
        self.s = ExecEnvironment(self.__driver, self.__wait)

    def _restore(self, data: DynaData):
        Scenarios.OpenMetamaskWallet(self.s, self.__static_data.seed_phrase)
        Scenarios.SetupMetamaskWallet(self.s)
        Scenarios.ConnectScroll(self.s)
        Scenarios.ConnectUniswap(self.s)

    def _base(self, dyna_data: DynaData):
        wallet_address = dyna_data.Metamask.wallet_address
        Logger.Info("WaitTransferGoerliToAlpha()")
        Actions.OpenUrl(self.s, URLs.Scroll_Bridge)

        while True:
            Logger.Info("Waiting success transfer...")
            try:
                response = requests.get(f'https://alpha-api.scroll.io/bridgehistory/api/txs?address={wallet_address}&offset=0&limit=1')
                a = json.loads(response.text)["data"]["result"][0]
                if "finalizeTx" in a:
                    break
                time.sleep(30)
            except:
                pass

        return
