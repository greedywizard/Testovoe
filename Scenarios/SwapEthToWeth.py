import random
from selenium.webdriver.common.by import By
from Automizer.Enums import WindowActions
from Automizer.Logger import Logger
from Automizer.Scenario import Scenario
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
import Automizer.Actions as Actions
import URLs


class SwapEthToWeth(Scenario):
    def __init__(self,
                 driver: WebDriver,
                 wait: WebDriverWait):
        super().__init__(driver, wait)

    def _exec(self):
        Logger.Info("SwapEthToWeth()")

        Actions.OpenUrl(self, URLs.Uniswap_Swap)

        # Список токенов на которые переводить
        Actions.Click(self, By.XPATH, "/html/body/div[1]/div/div[2]/div[5]/main/div[3]/div[1]/div/div/div/div[1]/button")
        # Выбрать токен WETH
        Actions.Click(self, By.XPATH, '/html/body/reach-portal[2]/div[3]/div/div/div/div/div[3]/div[1]/div/div/div[./div[2]/div[text()="WETH"]]')
        # "I understand"
        Actions.Click(self, By.XPATH, "/html/body/reach-portal[2]/div[3]/div/div/div/div/div/button[1]")

        value = Actions.GetElement(self, By.XPATH, '//*[@id="swap-currency-input"]/div/div[2]/div/div[2]/div').Element.text.split(' ')[1]

        # Рандомная половина
        val = self._generate_half_random(float(value))
        # Ввод количества
        Actions.Input(self, By.XPATH, "/html/body/div[1]/div/div[2]/div[5]/main/div[2]/div[1]/div/div/div[1]/input",
                      str(val))
        # "Warp"
        res = Actions.Click(self, By.XPATH, "/html/body/div[1]/div/div[2]/div[5]/main/div[3]/div[2]/button", window_action=WindowActions.Open)
        # Переключение на всплвающее окно
        self.Active_Window = res.New_Window
        # "Confirm"
        Actions.Click(self, By.XPATH, "//button[text()='Confirm']", window_action=WindowActions.WaitClose)
        # Переключение на исходное окно
        self.Active_Window = res.Old_Window

    @staticmethod
    def _generate_half_random(target_number):
        pointer = pow(10, str(round(target_number, 8)).split('.')[1].__len__())
        lower_bound = int(target_number * 0.4 * pointer)  # 40% от искомого числа
        upper_bound = int(target_number * 0.6 * pointer)  # 60% от искомого числ

        random_number = random.randint(lower_bound, upper_bound)
        return random_number / pointer
