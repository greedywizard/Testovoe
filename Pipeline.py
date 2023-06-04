import json
from typing import List

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import Automizer.Scenario
from Automizer.Logger import Logger
from Automizer.ControlPoint import ControlPoint, ControlPointResult
from ControlPoints import *
from Scenarios import *


class PipelineOptions:
    def __init__(self, seed, dl, dp, tl, tp, rp, rd):
        self.seed_phrase = seed
        self.discord_login = dl
        self.discord_pass = dp
        self.twitter_login = tl
        self.twitter_pass = tp
        self.restore_point = rp
        self.restore_data = rd


class Pipeline:
    def __init__(self, options: webdriver.ChromeOptions, is_restore: bool, pipe_options: PipelineOptions):
        self.driver: WebDriver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        self.wait: WebDriverWait = WebDriverWait(self.driver, 10)
        self.__is_restore = is_restore
        self.__opt = pipe_options

    def Start(self):
        Logger.Configure(file_name=f'{self.__opt.seed_phrase}.log')

        self.wait.until(EC.new_window_is_opened(self.driver.window_handles))
        all_window_handles = self.driver.window_handles
        for handle in all_window_handles[1:]:
            self.driver.switch_to.window(handle)
            self.driver.close()
        self.driver.switch_to.window(all_window_handles[0])

        data_p1 = Point1.StaticData()
        data_p1.seed_phrase = self.__opt.seed_phrase

        data_p8 = Point8.StaticData()
        data_p8.discord_login = self.__opt.discord_login
        data_p8.discord_pass = self.__opt.discord_pass
        data_p8.twitter_login = self.__opt.twitter_login
        data_p8.twitter_pass = self.__opt.twitter_pass

        graph = {
            "Point 1": Point1(self.driver, self.wait, data_p1, next_point="Point 2"),
            "Point 2": Point2(self.driver, self.wait, next_point="Point 3"),
            "Point 3": Point3(self.driver, self.wait, next_point="Point 4"),
            "Point 4": Point4(self.driver, self.wait, next_point="Point 5"),
            "Point 5": Point5(self.driver, self.wait, next_point="Mapper 1"),
            "Point 6": Point6(self.driver, self.wait, next_point="Mapper 2"),
            "Point 7": Point7(self.driver, self.wait, next_point="Point 8"),
            "Point 8": Point8(self.driver, self.wait, data_p8),
            "Mapper 1": Mapper1(self.driver, self.wait, next_point="Point 6"),
            "Mapper 2": Mapper1(self.driver, self.wait, next_point="Point 7"),
        }

        # RESTORE_DATA = Point8.RestoreData()
        # RESTORE_DATA.seed_phrase = self.__opt.seed_phrase
        # RESTORE_DATA.token = "0xb03ac08CDB198EC41Ff90C1FBC709D5468da20eB"

        if self.__opt.restore_data:
            DATA = self.__opt.restore_data
        else:
            DATA = None

        POINT = self.__opt.restore_point

        while True:
            result: ControlPointResult
            if self.__is_restore:
                result = graph[POINT].Restore(DATA)
                self.__is_restore = False
            else:
                result = graph[POINT].Base(DATA)

            DATA = result.data
            POINT = result.next_point

            if not POINT:
                break

        Logger.Info("Profit!")
        input()
        self.driver.quit()
