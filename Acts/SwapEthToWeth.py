import random
import time
from typing import Type

from selenium.webdriver.common.by import By

import Scenarios
from Automizer import Actions
from Automizer.Act import Act
from Automizer.Enums import WindowActions
from Automizer.Logger import Logger
from Automizer.ExecEnvironment import ExecEnvironment
import Automizer.Actions as Actions
import URLs
from db import PipelineOptions


class SwapEthToWeth(Act):
    def __init__(self, driver, wait, data: Type[PipelineOptions], next_point=None, restore_point=None):
        super().__init__(next_point, restore_point)
        self.__driver = driver
        self.__wait = wait
        self.__static_data = data
        self.s = ExecEnvironment(self.__driver, self.__wait)

    def _restore(self, data):
        Scenarios.OpenMetamaskWallet(self.s, self.__static_data.seed_phrase)
        Scenarios.SetupMetamaskWallet(self.s)
        Scenarios.ConnectScroll(self.s)
        Scenarios.ConnectUniswap(self.s)

    def _base(self, dyna_data):
        Logger.Info("SwapEthToWeth()")

        Actions.OpenUrl(self.s, URLs.Uniswap_Swap)

        # Переключение на scroll Alpha
        size = self.s.Driver.get_window_size()
        width = size['width']
        if width < 640:
            Actions.Click(self.s, By.XPATH, "/html/body/div[1]/div/div[1]/nav/div/div[1]/div[2]/div/button")
        else:
            Actions.Click(self.s, By.XPATH, "/html/body/div[1]/div/div[1]/nav/div/div[3]/div/div[3]/div/button")

        res = Actions.Click(self.s, By.XPATH, "//button[.//div[text()='Scroll Alpha']]", as_script=True, window_action=WindowActions.Open)
        if res.Prev_Window != res.New_Window:
            Actions.Click(self.s, By.XPATH, "//button[text()='Switch network']", window_action=WindowActions.WaitClose)

        # Выбор
        Actions.Click(self.s, By.XPATH, "/html/body/div[1]/div/div[2]/div[5]/main/div[3]/div[1]/div/div/div/div[1]/button")
        Actions.Input(self.s, By.ID, "token-search-input", "Ether")
        Actions.Click(self.s, By.XPATH, "//div[text()='Wrapped Ether']")

        try:
            # I understand
            Actions.Click(self.s, By.XPATH, "/html/body/reach-portal[2]/div[3]/div/div/div/div/div/button[1]")
        except:
            pass

        value = Actions.GetElement(self.s, By.XPATH, '//*[@id="swap-currency-input"]/div/div[2]/div/div[2]/div').Element.text.split(' ')[1]

        val = self._generate_half_random(float(value))

        time.sleep(1)
        Actions.Input(self.s, By.XPATH, "/html/body/div[1]/div/div[2]/div[5]/main/div[2]/div[1]/div/div/div[1]/input",
                      str(val))
        # "Warp"
        Actions.Click(self.s, By.XPATH, "/html/body/div[1]/div/div[2]/div[5]/main/div[3]/div[2]/button", window_action=WindowActions.Open)
        # "Confirm"
        Actions.Click(self.s, By.XPATH, "//button[text()='Confirm']", window_action=WindowActions.WaitClose)

        Actions.GetElement(self.s, By.XPATH, "//button[text()='Insufficient ETH balance']")

    @staticmethod
    def _generate_half_random(target_number):
        pointer = pow(10, str(round(target_number, 8)).split('.')[1].__len__())
        lower_bound = int(target_number * 0.4 * pointer)  # 40% от искомого числа
        upper_bound = int(target_number * 0.6 * pointer)  # 60% от искомого числ

        random_number = random.randint(lower_bound, upper_bound)
        return random_number / pointer

