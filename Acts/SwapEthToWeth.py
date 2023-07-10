import random
import time
from typing import Type

from selenium.webdriver.common.by import By

import Scenarios
from Automizer import Actions
from Automizer.Act import Act
from Automizer.Enums import WindowActions
from Automizer.Logger import Logger
import URLs
from Objects import DObject
from db import PipelineOptions


class SwapEthToWeth(Act[Type[PipelineOptions], DObject]):
    def __init__(self, next_act: str = None):
        super().__init__()
        self._next_act = next_act

    def _restore(self, data):
        Scenarios.OpenMetamaskWallet(self.Env, self._static_data.seed_phrase)
        Scenarios.SetupMetamaskWallet(self.Env)
        Scenarios.ConnectScroll(self.Env)
        Scenarios.ConnectUniswap(self.Env)

    def _base(self, dyna_data):
        Logger.Info("SwapEthToWeth()")

        Actions.OpenUrl(self.Env, URLs.Uniswap_Swap)

        Scenarios.UniswapUseAlpha(self.Env)

        # Выбор
        Actions.Click(self.Env, By.XPATH, "/html/body/div[1]/div/div[2]/div[5]/main/div[3]/div[1]/div/div/div/div[1]/button")
        Actions.Input(self.Env, By.ID, "token-search-input", "Ether")
        Actions.Click(self.Env, By.XPATH, "//div[text()='Wrapped Ether']")

        try:
            # I understand
            Actions.Click(self.Env, By.XPATH, "/html/body/reach-portal[2]/div[3]/div/div/div/div/div/button[1]")
        except:
            pass

        value = Actions.GetElement(self.Env, By.XPATH, '//*[@id="swap-currency-input"]/div/div[2]/div/div[2]/div').Element.text.split(' ')[1]

        val = self._generate_half_random(float(value))

        time.sleep(1)
        Actions.Input(self.Env, By.XPATH, "/html/body/div[1]/div/div[2]/div[5]/main/div[2]/div[1]/div/div/div[1]/input",
                      str(val))

        Actions.Click(self.Env, By.XPATH, "/html/body/div[1]/div/div[2]/div[5]/main/div[3]/div[2]/button", window_action=WindowActions.Open, as_script=True)
        Actions.Click(self.Env, By.XPATH, "//button[text()='Confirm']", window_action=WindowActions.WaitClose)
        Actions.WaitElementVisible(self.Env, By.XPATH, "//p[contains(text(), 'Pending')]")
        Actions.WaitElementVisible(self.Env, By.XPATH, "//p[contains(text(), 'Pending')]", is_visible=False)

    @staticmethod
    def _generate_half_random(target_number):
        pointer = pow(10, str(round(target_number, 8)).split('.')[1].__len__())
        lower_bound = int(target_number * 0.4 * pointer)  # 40% от искомого числа
        upper_bound = int(target_number * 0.6 * pointer)  # 60% от искомого числ

        random_number = random.randint(lower_bound, upper_bound)
        return random_number / pointer

