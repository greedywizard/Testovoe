import json
import time
from datetime import datetime, timedelta
from typing import Type

import requests

import Scenarios
from Automizer.Act import Act
from Automizer.Logger import Logger
from Objects import DObject
from db import PipelineOptions


class WaitTransferGoerliToAlpha(Act[Type[PipelineOptions], DObject]):
    def __init__(self, next_act: str = None):
        super().__init__()
        self._next_act = next_act

    def _restore(self, dyna_data):
        Scenarios.OpenMetamaskWallet(self.Env, self._static_data.seed_phrase)
        Scenarios.SetupMetamaskWallet(self.Env)
        Scenarios.ConnectScroll(self.Env)
        Scenarios.ConnectUniswap(self.Env, use_scroll=False)

    def _base(self, dyna_data: DObject):
        Logger.Info("WaitTransferGoerliToAlpha()")

        delta_m = 15
        minDate = datetime.utcnow() - timedelta(minutes=delta_m)
        start_date = datetime.utcnow()
        while True:
            Logger.Info("Waiting success transfer...")
            if datetime.utcnow() - timedelta(minutes=delta_m) > start_date:
                Logger.Info("Transfer is too long. Break")
                break
            try:
                response = requests.get(f'https://alpha-api.scroll.io/bridgehistory/api/txs?address={dyna_data.wallet_address}&offset=0&limit=1')
                a = json.loads(response.text)["data"]["result"][0]
                date_string = a["blockTimestamp"].replace("Z", "")
                t = datetime.fromisoformat(date_string)
                if "finalizeTx" in a and minDate < t:
                    break
                time.sleep(30)
            except:
                pass
