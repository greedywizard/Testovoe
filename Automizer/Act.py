import json
from abc import ABC, abstractmethod
from typing import final, Generic

from Automizer.DynaData import DynaData
from Automizer.ExecEnvironment import ExecEnvironment
from Automizer.GenericCollection import S, D


class ActResult:
    def __init__(self):
        self.next_act: str = None
        self.data: DynaData = None


class Act(ABC, Generic[S, D]):
    def __init__(self):
        self._static_data: S = None
        self._next_act = None
        self._env: ExecEnvironment = None
        self._isRestore: bool = False

    @property
    def Env(self) -> ExecEnvironment:
        return self._env

    @Env.setter
    def Env(self, value: ExecEnvironment):
        self._env = value

    @property
    def Data(self) -> D:
        return self._static_data

    @Data.setter
    def Data(self, value: D):
        self._static_data = value

    @final
    def Restore(self, dyna_data: DynaData) -> ActResult:
        self._isRestore = True
        self._restore(dyna_data)
        return self.Base(dyna_data)

    @final
    def Base(self, dyna_data: DynaData) -> ActResult:
        result = ActResult()
        self._base(dyna_data)
        result.next_act = self._next_act
        result.data = dyna_data
        return result

    @abstractmethod
    def _restore(self, dyna_data: D):
        pass

    @abstractmethod
    def _base(self, dyna_data: D):
        pass
