from typing import Type

from Automizer.Logger import Logger
from Automizer.ControlPoint import ControlPoint, ControlPointRestoreData
from Scenarios import *
from db import PipelineOptions


class Point1(ControlPoint):
    def __init__(self, driver, wait, static_data: Type[PipelineOptions], next_point=None, restore_point=None):
        super().__init__(next_point, restore_point)
        self.__driver = driver
        self.__wait = wait
        self.__static_data = static_data

    def _restore(self, data):
        pass

    def _base(self, process_data):
        data = OpenMetamaskWallet.Data()
        data.seed = self.__static_data.seed_phrase
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

    def _base(self, process_data):
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

    def _base(self, process_data):
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

    def _base(self, process_data):
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

    def _base(self, process_data):
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

    def _base(self, process_data: ValidateContract.Data):
        ValidateContract(self.__driver, self.__wait, process_data).Run()
        res3 = CreateToken(self.__driver, self.__wait).Run()
        data3 = DeployToken.Data()
        data3.name = res3.name
        data3.code = res3.code
        return DeployToken(self.__driver, self.__wait, data3).Run()


class Point7(ControlPoint):
    class RestoreData:
        def __init__(self):
            self.token = None
            self.seed_phrase = None

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

    def _base(self, process_data: AddToken.Data):
        AddToken(self.__driver, self.__wait, process_data).Run()
        SwapToScrollAlpha(self.__driver, self.__wait).Run()
        CreateSecondAccount(self.__driver, self.__wait).Run()
        SendBetweenAccounts(self.__driver, self.__wait).Run()


class Point8(ControlPoint):
    class RestoreData(ControlPointRestoreData):
        def __init__(self):
            self.seed_phrase = None

    class StaticData:
        def __init__(self):
            self.discord_login = None
            self.discord_pass = None
            self.twitter_login = None
            self.twitter_pass = None

    def __init__(self, driver, wait, data: Type[PipelineOptions], next_point=None, restore_point=None):
        super().__init__(next_point, restore_point)
        self.__driver = driver
        self.__wait = wait
        self.__static_data = data

    def _restore(self, data: str):
        rd = Point8.RestoreData().FromJson(data)
        mm = OpenMetamaskWallet.Data()
        mm.seed = rd.seed_phrase
        OpenMetamaskWallet(self.__driver, self.__wait, mm).Run()
        SetupMetamaskWallet(self.__driver, self.__wait).Run()
        ConnectScroll(self.__driver, self.__wait).Run()
        ConnectUniswap(self.__driver, self.__wait).Run()

    def _base(self, process_data):
        s = Subscribe.Data()
        s.discord_login = self.__static_data.discord_login
        s.discord_pass = self.__static_data.discord_pass
        s.twitter_login = self.__static_data.twitter_login
        s.twitter_pass = self.__static_data.twitter_pass

        Subscribe(self.__driver, self.__wait, s).Run()


class Mapper1(ControlPoint):
    def __init__(self, driver, wait, next_point=None, restore_point=None):
        super().__init__(next_point, restore_point)
        self.__driver = driver
        self.__wait = wait

    def _restore(self, data: OpenMetamaskWallet.Data):
        return

    def _base(self, process_data: DeployContract.Result):
        result = ValidateContract.Data()
        result.address = process_data.address
        result.compile_version = process_data.compile_version
        return result


class Mapper2(ControlPoint):
    def __init__(self, driver, wait, next_point=None, restore_point=None):
        super().__init__(next_point, restore_point)
        self.__driver = driver
        self.__wait = wait

    def _restore(self, data: OpenMetamaskWallet.Data):
        return

    def _base(self, process_data: DeployToken.Result):
        result = AddToken.Data()
        result.address = process_data.address
        return result
