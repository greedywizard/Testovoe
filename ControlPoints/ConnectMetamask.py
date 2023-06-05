from typing import Type
import Scenarios
from Automizer.ControlPoint import ControlPoint
from Automizer.Logger import Logger
from Automizer.Scenario import Scenario
from db import PipelineOptions


class ConnectMetamask(ControlPoint):
    def __init__(self, driver, wait, data: Type[PipelineOptions],next_point=None, restore_point=None):
        super().__init__(next_point, restore_point)
        self.__driver = driver
        self.__wait = wait
        self.__static_data = data
        self.s = Scenario(self.__driver, self.__wait)

    def _restore(self, data):
        pass

    def _base(self, process_data):
        Logger.Info("ConnectMetamask()")

        Scenarios.OpenMetamaskWallet(self.s, self.__static_data.seed_phrase)
        Scenarios.SetupMetamaskWallet(self.s)
        Scenarios.ConnectScroll(self.s)
        Scenarios.ConnectUniswap(self.s)


