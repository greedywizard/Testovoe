from typing import Type
import Scenarios
from Automizer.Act import Act
from Automizer.Logger import Logger
from Automizer.ExecEnvironment import ExecEnvironment
from DynaData import DynaData
from db import PipelineOptions


class ConnectMetamask(Act):
    class Data:
        wallet_address: str = None

    def __init__(self, driver, wait, data: Type[PipelineOptions], next_point=None, restore_point=None):
        super().__init__(next_point, restore_point)
        self.__driver = driver
        self.__wait = wait
        self.__static_data = data
        self.s = ExecEnvironment(self.__driver, self.__wait)

    def _restore(self, data):
        pass

    def _base(self, dyna_data: DynaData):
        Logger.Info("ConnectMetamask()")

        dyna_data.Metamask.wallet_address = Scenarios.OpenMetamaskWallet(self.s, self.__static_data.seed_phrase)
        Scenarios.SetupMetamaskWallet(self.s)
        Scenarios.ConnectScroll(self.s)
        Scenarios.ConnectUniswap(self.s)
        Scenarios.ConnectGuild(self.s)



