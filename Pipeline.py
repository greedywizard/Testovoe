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
from db import PipelineOptions
import Mappers as mp


class Pipeline:
    def __init__(self, options: webdriver.ChromeOptions, pipe_options: Type[PipelineOptions]):
        self.driver: WebDriver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        self.wait: WebDriverWait = WebDriverWait(self.driver, 20)
        self.__opt = pipe_options

    def Start(self) -> Type[PipelineOptions]:
        Logger.Configure(file_path="logs/", file_name=f'{self.__opt.seed_phrase}.log')

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
            WaitTransferGoerliToAlpha.__name__: TransferGoerliToAlphaTestnet(self.driver, self.wait, self.__opt, next_point=SwapEthToWeth.__name__),
            SwapEthToWeth.__name__: SwapEthToWeth(self.driver, self.wait, self.__opt, next_point=SwapWethToUsdc.__name__),
            SwapWethToUsdc.__name__: SwapWethToUsdc(self.driver, self.wait, self.__opt, next_point=AddLiquid.__name__),
            AddLiquid.__name__: AddLiquid(self.driver, self.wait, self.__opt, next_point=SwapUsdcToEth.__name__),
            SwapUsdcToEth.__name__: SwapUsdcToEth(self.driver, self.wait, self.__opt, next_point=BuildContract.__name__),
            BuildContract.__name__: BuildContract(self.driver, self.wait, self.__opt, next_point=BuildToken.__name__),
            BuildToken.__name__: BuildToken(self.driver, self.wait, self.__opt, next_point=mp.Mapper.__name__),
            mp.Mapper.__name__: mp.Mapper(next_point=PlayWithTokenInMetamask.__name__),
            PlayWithTokenInMetamask.__name__: PlayWithTokenInMetamask(self.driver, self.wait, self.__opt, next_point=Subscribe.__name__),
            Subscribe.__name__: Subscribe(self.driver, self.wait, self.__opt)
        }

        if self.__opt.restore_data:
            DATA = self.__opt.restore_data
        else:
            DATA = None

        if self.__opt.restore_point:
            POINT = self.__opt.restore_point
        else:
            POINT = ""

        while True:
            try:
                if self.__opt.is_restore:
                    result = graph[POINT].Restore(DATA)
                    self.__opt.is_restore = False
                else:
                    result = graph[POINT].Base(DATA)
            except:
                self.__opt.is_restore = True
                db.UpdateRecord(self.__opt)
                break

            DATA = result.data
            POINT = result.next_point

            if not POINT:
                break

            self.__opt.restore_data = json.dumps(DATA.__dict__)
            self.__opt.restore_point = POINT
            db.UpdateRecord(self.__opt)

        Logger.Info("Profit!")
        self.driver.quit()

        self.__opt.is_complete = True
        self.__opt.is_restore = False
        self.__opt.restore_data = None
        self.__opt.restore_point = None
        return self.__opt
