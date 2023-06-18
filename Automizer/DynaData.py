import json
from abc import ABC
from typing import final


class DynaData(ABC):
    @final
    def FromJson(self, json_string: str):
        json_dict = json.loads(json_string)
        for i in vars(self):
            self.__setattr__(i, json_dict[i])
        return self
