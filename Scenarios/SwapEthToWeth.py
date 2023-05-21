from random import random
from selenium.webdriver.common.by import By
from Automizer.Scenario import Scenario, ScenarioResult
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
import Automizer.Actions as Actions
import URLs


class SwapEthToWeth(Scenario):
    def __init__(self,
                 driver: WebDriver,
                 wait: WebDriverWait):
        super().__init__(driver, wait)

    def Exec(self, args=None):
        result: ScenarioResult = ScenarioResult()

        Actions.OpenUrl(self, URLs.Uniswap_Swap)

        # Список токенов на которые переводить
        Actions.Click(self, By.XPATH, "/html/body/div[1]/div/div[2]/div[5]/main/div[3]/div[1]/div/div/div/div[1]/button")
        # Выбрать токен WETH
        Actions.Click(self, By.XPATH, '/html/body/reach-portal[2]/div[3]/div/div/div/div/div[3]/div[1]/div/div/div[./div[2]/div[text()="WETH"]]')
        # "I understand"
        Actions.Click(self, By.XPATH, "/html/body/reach-portal[2]/div[3]/div/div/div/div/div/button[1]")
        # Рандомная половина
        val = self._generate_half_random(args['value'])
        # Ввод количества
        Actions.Click(self, By.XPATH, "/html/body/div[1]/div/div[2]/div[5]/main/div[2]/div[1]/div/div/div[1]/input",
                      str(val))
        # "Warp"
        res = Actions.Click(self, By.XPATH, "/html/body/div[1]/div/div[2]/div[5]/main/div[3]/div[2]/button", is_opening_window=True)
        # Переключение на всплвающее окно
        self.Active_Window = res.New_Window
        # "Confirm"
        Actions.Click(self, By.XPATH, "//button[text()='Confirm']")
        # Переключение на исходное окно
        self.Active_Window = res.Old_Window

        result.ResultData["value"] = val

        return result

    @staticmethod
    def _generate_half_random(target_number):
        pointer = 100
        lower_bound = int(target_number * 0.4 * pointer)  # 40% от искомого числа
        upper_bound = int(target_number * 0.6 * pointer)  # 60% от искомого числа

        random_number = random.randint(lower_bound, upper_bound)
        return random_number / pointer
