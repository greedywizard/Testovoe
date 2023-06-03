from abc import ABC, abstractmethod
from typing import final


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
    def Restore(self, data) -> ControlPointResult:
        result = self._restore(data)
        return self._base(result)

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
    def _base(self, data):
        pass
