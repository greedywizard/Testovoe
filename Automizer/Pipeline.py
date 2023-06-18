import json
from typing import Dict, Type, Generic, Callable
from Automizer.Act import Act
from Automizer.ExecEnvironment import ExecEnvironment
from Automizer.GenericCollection import D, S


class Pipeline(Generic[S, D]):
    def __init__(self, driver, wait, static_data: S):
        self._env: ExecEnvironment = ExecEnvironment(driver, wait)
        self._static_data: S = static_data
        self._graph: Dict[str, Act[S, D]] = {}
        self._first_act: str = None
        self.complete: Callable[[D], None] = None
        self.update: Callable[[S], None] = None

    def Run(self, dyna_data_type: Type[D]) -> S:
        if self._static_data.restore_data:
            DATA: D = dyna_data_type().FromJson(self._static_data.restore_data)
        else:
            DATA: D = dyna_data_type()

        restore: bool = False
        if self._static_data.restore_point:
            POINT: str = self._static_data.restore_point
            restore: bool = True
        else:
            POINT: str = self._first_act

        while True:
            if restore:
                result = self._graph[POINT].Restore(DATA)
                restore = False
            else:
                result = self._graph[POINT].Base(DATA)

            DATA = result.data
            POINT = result.next_act

            self._static_data.restore_data = json.dumps(DATA.__dict__)

            if not POINT:
                break

            self._static_data.restore_point = POINT
            if self.update:
                self.update(self._static_data)

        if self.complete:
            self.complete(DATA)

        return self._static_data

    def __iadd__(self, act: Act[S, D]):
        act.Env = self._env
        act.Data = self._static_data

        if not self._first_act:
            self._first_act = act.__class__.__name__

        self._graph[act.__class__.__name__] = act
        return self

    @property
    def FirstAct(self) -> str:
        return self._first_act
