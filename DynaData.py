import json
from typing import final

from Acts import *


class DynaData:
    def __init__(self):
        self.wallet_address: str = None
        self.new_token: str = None

    @final
    def FromJson(self, json_string: str):
        json_dict = json.loads(json_string)
        for i in vars(self):
            self.__setattr__(i, json_dict[i])
        return self
