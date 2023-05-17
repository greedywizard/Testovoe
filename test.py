from abc import ABC, abstractmethod
import typing


class Test(ABC):
    @typing.final
    def Exec(self):
        print("exec")
        return self._run()

    @abstractmethod
    def _run(self):
        pass


class T(Test):
    def _run(self):
        print("run")
        return self


T().Exec()