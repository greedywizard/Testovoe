from Automizer.DynaData import DynaData


class DObject(DynaData):
    def __init__(self):
        self.wallet_address: str = None
        self.new_token: str = None
