from typing import Generic, Type

import Scenarios
from Automizer.Act import Act
from Automizer.Logger import Logger
from Objects import DObject
from db import PipelineOptions


class ConnectMetamask(Act[Type[PipelineOptions], DObject]):
    def __init__(self, next_act: str):
        super().__init__()
        self._next_act = next_act

    def _restore(self, data):
        pass

    def _base(self, dyna_data):
        Logger.Info("ConnectMetamask()")

        dyna_data.wallet_address = Scenarios.OpenMetamaskWallet(self.Env, self._static_data.seed_phrase)
        Scenarios.SetupMetamaskWallet(self.Env)
        Scenarios.ConnectScroll(self.Env)
        Scenarios.ConnectUniswap(self.Env, use_scroll=False)
