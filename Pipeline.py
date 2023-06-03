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


class PipelineData:
    seed_phrase: str = None


class Pipeline:
    def __init__(self, options: webdriver.ChromeOptions, is_restore: bool, data: PipelineData):
        self.driver: WebDriver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        self.wait: WebDriverWait = WebDriverWait(self.driver, 10)
        self.__is_restore = is_restore
        self.__data = data

    def Start(self):
        Logger.Configure(file_name=f'{self.__data.seed_phrase}.log')

        self.wait.until(EC.new_window_is_opened(self.driver.window_handles))
        all_window_handles = self.driver.window_handles
        for handle in all_window_handles[1:]:
            self.driver.switch_to.window(handle)
            self.driver.close()
        self.driver.switch_to.window(all_window_handles[0])

        graph = {
            "Point 1": Point1(self.driver, self.wait, next_point="Point 2"),
            "Point 2": Point2(self.driver, self.wait, next_point="Point 3"),
            "Point 3": Point3(self.driver, self.wait, next_point="Point 4"),
            "Point 4": Point4(self.driver, self.wait, next_point="Point 5"),
            "Point 5": Point5(self.driver, self.wait, next_point="Mapper 1"),
            "Point 6": Point6(self.driver, self.wait, next_point="Mapper 2"),
            "Point 7": Point7(self.driver, self.wait),
            "Mapper 1": Mapper1(self.driver, self.wait, next_point="Point 6"),
            "Mapper 2": Mapper1(self.driver, self.wait, next_point="Point 7"),
        }

        RESTORE_DATA = Point7.RestoreData()
        RESTORE_DATA.seed_phrase = self.__data.seed_phrase
        RESTORE_DATA.token = "0xb03ac08CDB198EC41Ff90C1FBC709D5468da20eB"

        DATA = None
        POINT = "Point 7"
        while True:
            result: ControlPointResult
            if self.__is_restore:
                result = graph[POINT].Restore(RESTORE_DATA)
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
