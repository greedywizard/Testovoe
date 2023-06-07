import json
from abc import ABC, abstractmethod
from typing import final


class ActResult(ABC):
    def __init__(self):
        self.restore_point = None
        self.next_point = None
        self.data = None


class Act(ABC):
    def __init__(self, next_point, restore_point):
        self.__rId = restore_point
        self.__bId = next_point

    @final
    def Restore(self, data: str) -> ActResult:
        """
        Подготавливает скрипт для продолжения с контрольной точки
        :param data: JSON строка с данными для восстановления
        :return:Данные для последующего вызова основного тела контрольной точки
        """
        res = self._restore(data)
        if res:
            return self.Base(res)
        else:
            return self.Base(data)

    @final
    def Base(self, data) -> ActResult:
        result = ActResult()
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
    def _base(self, dyna_data):
        pass
