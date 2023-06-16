import json
from typing import Type

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import db
from Automizer.Logger import Logger
from Acts import *
from DynaData import DynaData
from db import PipelineOptions


class Pipeline:
    def __init__(self, pipe_options: Type[PipelineOptions]):
        Logger.Configure(file_path="walletlogs/", file_name=f'{pipe_options.seed_phrase}')
        options = webdriver.ChromeOptions()
        options.add_extension('./Extentions/metamask.crx')
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        self.driver: WebDriver = webdriver.Edge(service=ChromeService(ChromeDriverManager().install()), options=options)
        self.driver.set_window_size(800, 800)
        self.driver.implicitly_wait(1)
        self.wait: WebDriverWait = WebDriverWait(self.driver, 20)
        self.__opt = pipe_options

    def Start(self) -> Type[PipelineOptions]:
        self.wait.until(EC.new_window_is_opened(self.driver.window_handles))
        all_window_handles = self.driver.window_handles
        for handle in all_window_handles[1:]:
            self.driver.switch_to.window(handle)
            self.driver.close()
        self.driver.switch_to.window(all_window_handles[0])

        # Граф взаимодействия
        graph = {
            "": ConnectMetamask(self.driver, self.wait, self.__opt, next_point=TransferGoerliToAlphaTestnet.__name__),
            TransferGoerliToAlphaTestnet.__name__: TransferGoerliToAlphaTestnet(self.driver, self.wait, self.__opt, next_point=WaitTransferGoerliToAlpha.__name__),
            WaitTransferGoerliToAlpha.__name__: WaitTransferGoerliToAlpha(self.driver, self.wait, self.__opt, next_point=SwapEthToWeth.__name__),
            SwapEthToWeth.__name__: SwapEthToWeth(self.driver, self.wait, self.__opt, next_point=SwapWethToUsdc.__name__),  # uniswap
            SwapWethToUsdc.__name__: SwapWethToUsdc(self.driver, self.wait, self.__opt, next_point=AddLiquidEthUSDC.__name__),  # uniswap
            AddLiquidEthUSDC.__name__: AddLiquidEthUSDC(self.driver, self.wait, self.__opt, next_point=RemoveLiquidEthUSDC.__name__),  # uniswap
            RemoveLiquidEthUSDC.__name__: RemoveLiquidEthUSDC(self.driver, self.wait, self.__opt, next_point=SwapUsdcToEth.__name__),  # uniswap
            SwapUsdcToEth.__name__: SwapUsdcToEth(self.driver, self.wait, self.__opt, next_point=BuildContract.__name__),  # uniswap
            BuildContract.__name__: BuildContract(self.driver, self.wait, self.__opt, next_point=BuildToken.__name__),  # remix
            BuildToken.__name__: BuildToken(self.driver, self.wait, self.__opt, next_point=PlayWithTokenInMetamask.__name__),
            PlayWithTokenInMetamask.__name__: PlayWithTokenInMetamask(self.driver, self.wait, self.__opt, next_point=SubscribeDiscord.__name__),
            SubscribeDiscord.__name__: SubscribeDiscord(self.driver, self.wait, self.__opt, next_point=SubscribeTwitter.__name__),
            SubscribeTwitter.__name__: SubscribeTwitter(self.driver, self.wait, self.__opt)
        }

        if self.__opt.restore_data:
            DATA = DynaData().FromJson(self.__opt.restore_data)
        else:
            DATA = DynaData()

        restore: bool = False
        if self.__opt.restore_point:
            POINT = self.__opt.restore_point
            restore: bool = True
        else:
            POINT = ""

        try:
            while True:
                if restore:
                    result = graph[POINT].Restore(DATA)
                    restore = False
                else:
                    result = graph[POINT].Base(DATA)

                DATA = result.data
                POINT = result.next_point

                if not POINT:
                    break

                self.__opt.restore_data = json.dumps(DATA.__dict__)

                self.__opt.restore_point = POINT
                db.UpdateRecord(self.__opt)

            Logger.Info("Profit!")
            self.__opt.is_complete = True
            self.__opt.restore_data = None
            self.__opt.restore_point = None

            db.UpdateRecord(self.__opt)

        except Exception as e:
            Logger.Exception(e)
            Logger.Error("End task with error")

        finally:
            self.driver.quit()
            return self.__opt
