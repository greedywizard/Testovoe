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
        self.wait: WebDriverWait = WebDriverWait(self.driver, 5)
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

        mm_data = OpenMetamaskWallet.Data()
        mm_data.seed = self.__data.seed_phrase

        graph = {
            "Point 1": Point1(self.driver, self.wait, base_id="Point 2"),
            "Point 2": Point2(self.driver, self.wait, base_id="Point 3", restore_id="Point 2"),
            "Point 3": Point3(self.driver, self.wait, base_id="Point 4", restore_id="Point 3"),
            "Point 4": Point4(self.driver, self.wait, base_id="Point 5", restore_id="Point 4"),
            "Point 5": Point5(self.driver, self.wait, base_id="Mapper 1", restore_id="Point 5"),
            "Point 6": Point6(self.driver, self.wait, base_id="Mapper 2"),
            "Point 7": Point7(self.driver, self.wait),
            "Mapper 1": Mapper1(self.driver, self.wait, base_id="Point 6"),
            "Mapper 2": Mapper1(self.driver, self.wait, base_id="Point 7"),
        }

        DATA = mm_data
        POINT = "Point 5"
        while True:
            result: ControlPointResult
            if self.__is_restore:
                result = graph[POINT].Restore(DATA)
                self.__is_restore = False
            else:
                result = graph[POINT].Base(DATA)

            POINT = result.next_point_id
            DATA = result.data

            if not POINT:
                break

        input()
        self.driver.quit()
