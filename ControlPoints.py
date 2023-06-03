from Automizer.Logger import Logger
from Automizer.ControlPoint import ControlPoint, ControlPointResult
from Scenarios import *


class Point1(ControlPoint):
    def __init__(self, driver, wait, next_point=None, restore_point=None):
        super().__init__(next_point, restore_point)
        self.__driver = driver
        self.__wait = wait

    def _restore(self, data):
        pass

    def _base(self, data: OpenMetamaskWallet.Data):
        OpenMetamaskWallet(self.__driver, self.__wait, data).Run()
        SetupMetamaskWallet(self.__driver, self.__wait).Run()
        ConnectScroll(self.__driver, self.__wait).Run()
        try:
            TransferGoerliToAlphaTestnet(self.__driver, self.__wait).Run()
        except ValueError:
            Logger.Info("There is no Goerli balance")
            print('clear account')
        return


class Point2(ControlPoint):
    def __init__(self, driver, wait, next_point=None, restore_point=None):
        super().__init__(next_point, restore_point)
        self.__driver = driver
        self.__wait = wait

    def _restore(self, data: OpenMetamaskWallet.Data):
        OpenMetamaskWallet(self.__driver, self.__wait, data).Run()
        SetupMetamaskWallet(self.__driver, self.__wait).Run()
        ConnectScroll(self.__driver, self.__wait).Run()
        return

    def _base(self, data):
        WaitTransferGoerliToAlpha(self.__driver, self.__wait).Run()
        return


class Point3(ControlPoint):
    def __init__(self, driver, wait, next_point=None, restore_point=None):
        super().__init__(next_point, restore_point)
        self.__driver = driver
        self.__wait = wait

    def _restore(self, data: OpenMetamaskWallet.Data):
        OpenMetamaskWallet(self.__driver, self.__wait, data).Run()
        SetupMetamaskWallet(self.__driver, self.__wait).Run()
        ConnectScroll(self.__driver, self.__wait).Run()
        return

    def _base(self, data):
        ConnectUniswap(self.__driver, self.__driver).Run()
        return


class Point4(ControlPoint):
    def __init__(self, driver, wait, next_point=None, restore_point=None):
        super().__init__(next_point, restore_point)
        self.__driver = driver
        self.__wait = wait

    def _restore(self, data: OpenMetamaskWallet.Data):
        OpenMetamaskWallet(self.__driver, self.__wait, data).Run()
        SetupMetamaskWallet(self.__driver, self.__wait).Run()
        ConnectScroll(self.__driver, self.__wait).Run()
        ConnectUniswap(self.__driver, self.__wait).Run()
        return

    def _base(self, data):
        SwapEthToWeth(self.__driver, self.__wait).Run()
        SwapWethToUsdc(self.__driver, self.__wait).Run()
        AddLiquid(self.__driver, self.__wait).Run()
        SwapUsdcToEth(self.__driver, self.__wait).Run()
        return


class Point5(ControlPoint):
    def __init__(self, driver, wait, next_point=None, restore_point=None):
        super().__init__(next_point, restore_point)
        self.__driver = driver
        self.__wait = wait

    def _restore(self, data: OpenMetamaskWallet.Data):
        OpenMetamaskWallet(self.__driver, self.__wait, data).Run()
        SetupMetamaskWallet(self.__driver, self.__wait).Run()
        ConnectScroll(self.__driver, self.__wait).Run()
        ConnectUniswap(self.__driver, self.__wait).Run()
        return

    def _base(self, data):
        return DeployContract(self.__driver, self.__wait).Run()


class Point6(ControlPoint):
    def __init__(self, driver, wait, next_point=None, restore_point=None):
        super().__init__(next_point, restore_point)
        self.__driver = driver
        self.__wait = wait

    def _restore(self, data: OpenMetamaskWallet.Data):
        OpenMetamaskWallet(self.__driver, self.__wait, data).Run()
        SetupMetamaskWallet(self.__driver, self.__wait).Run()
        ConnectScroll(self.__driver, self.__wait).Run()
        ConnectUniswap(self.__driver, self.__wait).Run()
        return

    def _base(self, data: ValidateContract.Data):
        ValidateContract(self.__driver, self.__wait, data).Run()
        res3 = CreateToken(self.__driver, self.__wait).Run()
        data3 = DeployToken.Data()
        data3.name = res3.name
        data3.code = res3.code
        return DeployToken(self.__driver, self.__wait, data3).Run()


class Point7(ControlPoint):
    class RestoreData:
        token = None
        seed_phrase = None

    def __init__(self, driver, wait, next_point=None, restore_point=None):
        super().__init__(next_point, restore_point)
        self.__driver = driver
        self.__wait = wait

    def _restore(self, data: RestoreData):
        mm = OpenMetamaskWallet.Data()
        mm.seed = data.seed_phrase
        OpenMetamaskWallet(self.__driver, self.__wait, mm).Run()
        SetupMetamaskWallet(self.__driver, self.__wait).Run()
        ConnectScroll(self.__driver, self.__wait).Run()
        ConnectUniswap(self.__driver, self.__wait).Run()
        result = AddToken.Data()
        result.address = data.token
        return result

    def _base(self, data: AddToken.Data):
        AddToken(self.__driver, self.__wait, data).Run()
        SwapToScrollAlpha(self.__driver, self.__wait).Run()
        CreateSecondAccount(self.__driver, self.__wait).Run()
        SendBetweenAccounts(self.__driver, self.__wait).Run()


class Mapper1(ControlPoint):
    def __init__(self, driver, wait, next_point=None, restore_point=None):
        super().__init__(next_point, restore_point)
        self.__driver = driver
        self.__wait = wait

    def _restore(self, data: OpenMetamaskWallet.Data):
        return

    def _base(self, data: DeployContract.Result):
        result = ValidateContract.Data()
        result.address = data.address
        result.compile_version = data.compile_version
        return result


class Mapper2(ControlPoint):
    def __init__(self, driver, wait, next_point=None, restore_point=None):
        super().__init__(next_point, restore_point)
        self.__driver = driver
        self.__wait = wait

    def _restore(self, data: OpenMetamaskWallet.Data):
        return

    def _base(self, data: DeployToken.Result):
        result = AddToken.Data()
        result.address = data.address
        return result