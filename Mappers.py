from Acts import BuildToken, PlayWithTokenInMetamask
from Automizer.Act import Act


class Mapper(Act):
    def __init__(self, next_point=None, restore_point=None):
        super().__init__(next_point, restore_point)

    def _restore(self, data):
        pass

    def _base(self, dyna_data: BuildToken.Result) -> PlayWithTokenInMetamask.Data:
        result = PlayWithTokenInMetamask.Data()
        result.address = dyna_data.address
        return result
