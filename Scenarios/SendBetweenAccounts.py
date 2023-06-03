import random
import time
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By

from Automizer.Logger import Logger
from Automizer.Scenario import Scenario
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
import Automizer.Actions as Actions
import URLs


class SendBetweenAccounts(Scenario):
    def __init__(self,
                 driver: WebDriver,
                 wait: WebDriverWait):
        super().__init__(driver, wait)

    def _exec(self):
        Logger.Info("SendBetweenAccounts()")
        Actions.OpenUrl(self, URLs.Metamask_Home)

        Actions.Click(self, By.XPATH, "//button[@data-testid='account-menu-icon']", as_script=True)
        #
        Actions.Click(self, By.XPATH, "//button[.//div[3]/div[text()='Account 1']]", as_script=True)

        Actions.Click(self, By.XPATH, "//button[@data-testid='eth-overview-send']", as_script=True)
        # Открыть список аккаунтов
        Actions.Click(self, By.XPATH, "//a[text()='Transfer between my accounts']", as_script=True)
        # Выбрать 2 аккаунт
        Actions.Click(self, By.XPATH, "//div[text()='scroll2']", as_script=True)
        #
        max_value = float(Actions.GetElement(self, By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[3]/div/div[1]/div[2]/div/div/div/div[2]/div[2]/div/span[2]').Element.text)

        if max_value >= 0.0015:
            rand_value = random.randint(5, 15) / 10000
        else:
            rand_value = max_value

        # Ввести значения
        Actions.Input(self, By.XPATH, "/html/body/div[1]/div/div[3]/div/div[3]/div/div[2]/div[2]/div[1]/div/div/div[1]/input", str(rand_value))

        Actions.Click(self, By.XPATH, "//button[@data-testid='page-container-footer-next']", as_script=True)
        Actions.Click(self, By.XPATH, "//button[@data-testid='page-container-footer-next']", as_script=True)

        while True:
            Logger.Info("Pending (Account 1 -> scroll2)...")
            try:
                Actions.Click(self, By.XPATH, "/html/body/div[1]/div/div[3]/div/div/div/div[3]/div/div/div/div/div[1]", as_script=True)
                if Actions.GetElement(self, By.XPATH, "/html/body/div[2]/div/div/section/div[2]/div/div[2]/div[1]/div[2]/div").Element.text == "Confirmed":
                    break
            except:
                pass

        # Выбрать 2 аккаунт
        Actions.Click(self, By.XPATH, "//button[@data-testid='account-menu-icon']", as_script=True)
        # Выбрать scroll2
        Actions.Click(self, By.XPATH, "//button/div[3]/div[text()='scroll2']", as_script=True)

        Actions.OpenUrl(self, URLs.Metamask_Send)

        # Открыть список аккаунтов
        Actions.Click(self, By.XPATH, "/html/body/div[1]/div/div[3]/div/div[3]/div/div/a", as_script=True)
        # Выбрать 2 аккаунт
        Actions.Click(self, By.XPATH, "//div[text()='Account 1']", as_script=True)

        Actions.Input(self, By.XPATH, "/html/body/div[1]/div/div[3]/div/div[3]/div/div[2]/div[2]/div[1]/div/div/div[1]/input", str(rand_value / 2))

        Actions.Click(self, By.XPATH, "//button[@data-testid='page-container-footer-next']", as_script=True)
        Actions.Click(self, By.XPATH, "//button[@data-testid='page-container-footer-next']", as_script=True)

        while True:
            Logger.Info("Pending (scroll2 -> Account 1)...")
            try:
                Actions.Click(self, By.XPATH, "/html/body/div[1]/div/div[3]/div/div/div/div[3]/div/div/div/div/div[1]", as_script=True)
                if Actions.GetElement(self, By.XPATH, "/html/body/div[2]/div/div/section/div[2]/div/div[2]/div[1]/div[2]/div").Element.text == "Confirmed":
                    break
            except:
                pass
