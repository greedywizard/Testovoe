import json
from abc import ABC, abstractmethod
from typing import final


class ControlPointRestoreData(ABC):
    @final
    def FromJson(self, json_string: str):
        json_dict = json.loads(json_string)
        for i in vars(self):
            self.__setattr__(i, json_dict[i])
        return self


class ControlPointResult(ABC):
    def __init__(self):
        self.restore_point = None
        self.next_point = None
        self.data = None


class ControlPoint(ABC):
    def __init__(self, next_point, restore_point):
        self.__rId = restore_point
        self.__bId = next_point

    @final
    def Restore(self, data: str) -> ControlPointResult:
        """
        Подготавливает скрипт для продолжения с контрольной точки
        :param data: JSON строка с данными для восстановления
        :return:Данные для последующего вызова основного тела контрольной точки
        """
        res = self._restore(data)
        return self.Base(res)

    @final
    def Base(self, data) -> ControlPointResult:
        result = ControlPointResult()
        result.next_point = self.__bId
        if self.__rId:
            result.restore_point = self.__rId
        else:
            result.restore_point = self.__bId
        result.data = self._base(data)
        return result

    @abstractmethod
    def _restore(self, data):
        pass

    @abstractmethod
    def _base(self, process_data):
        pass
