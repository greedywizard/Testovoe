from abc import ABC, abstractmethod
import Automizer.Actions


Actions.click_button_by_xpath()

class Scenario(ABC):
    def __init__(self):
        self._ss = None

    @property
    @abstractmethod
    def level(self):
        pass



class A(Scenario):
    @property
    def level(self):
        return 1


def test(v: Scenario):
    print(v.level)

var = A()

test(A())
