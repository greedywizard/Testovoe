from abc import ABC, abstractmethod
from typing import final


class ControlPointResult(ABC):
    def __init__(self):
        self.next_point_id = None
        self.data = None


class ControlPoint(ABC):
    def __init__(self, base_id, restore_id):
        self.__rId = restore_id
        self.__bId = base_id

    @final
    def Restore(self, data) -> ControlPointResult:
        result = ControlPointResult()
        result.next_point_id = self.__rId
        result.data = self._restore(data)
        return result

    @final
    def Base(self, data) -> ControlPointResult:
        result = ControlPointResult()
        result.next_point_id = self.__bId
        result.data = self._base(data)
        return result

    @abstractmethod
    def _restore(self, data):
        pass

    @abstractmethod
    def _base(self, data):
        pass
