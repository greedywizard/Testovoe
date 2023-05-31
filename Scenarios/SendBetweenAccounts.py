import random
import time
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
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

        Actions.OpenUrl(self, URLs.Metamask_Home)

        Actions.Click(self, By.XPATH,"//button[@data-testid='account-menu-icon']", as_script=True)
        #
        Actions.Click(self, By.XPATH, "/html/body/div[1]/div/div[3]/div[4]/div/button[1]", as_script=True)

        Actions.Click(self, By.XPATH, "//button[.//span[text()='Send']]", as_script=True)
        # Открыть список аккаунтов
        Actions.Click(self, By.XPATH, "//a[text()='Transfer between my accounts']", as_script=True)
        # Выбрать 2 аккаунт
        Actions.Click(self, By.XPATH, "//div[text()='scroll2']", as_script=True)
        #
        max_value = float(Actions.GetElement(self, By.CLASS_NAME, "currency-display-component__text").Element.text)
        rand_value = 0.0

        if max_value >= 0.0015:
            rand_value = random.randint(5, 15) / 10000
        else:
            rand_value = max_value

        # Ввести значения
        Actions.Input(self, By.XPATH, "/html/body/div[1]/div/div[3]/div/div[3]/div/div[2]/div[2]/div[1]/div/div/div[1]/input", str(rand_value))

        while True:
            try:
                #  "Next"
                Actions.Click(self, By.XPATH, "/html/body/div[1]/div/div[3]/div/div[4]/footer/button[2]", as_script=True)
                #  "Confirm"
                Actions.Click(self, By.XPATH, "/html/body/div[1]/div/div[3]/div/div[3]/div[3]/footer/button[2]", as_script=True)
                break
            except Exception as e:
                print(e)
                pass

        while True:
            try:
                # Открыть информацию о
                Actions.Click(self, By.XPATH, "/html/body/div[1]/div/div[3]/div/div/div/div[3]/div/div/div/div/div[1]", as_script=True)
                if Actions.GetElement(self, By.XPATH, "/html/body/div[2]/div/div/section/div[2]/div/div[2]/div[1]/div[2]/div").Element.text == "Confirmed":
                    break
                Actions.Click(self, By.XPATH, "/html/body/div[2]/div/div/section/div[1]/div/button", as_script=True)
            except:
                pass

        # Выбрать 2 аккаунт
        Actions.Click(self, By.XPATH, "/html/body/div[1]/div/div[1]/div/div[2]/button/div", as_script=True)
        # Выбрать scroll2
        Actions.Click(self, By.XPATH, "//button/div[3]/div[text()='scroll2']", as_script=True)

        Actions.OpenUrl(self, URLs.Metamask_Send)

        # Открыть список аккаунтов
        Actions.Click(self, By.XPATH, "/html/body/div[1]/div/div[3]/div/div[3]/div/div/a", as_script=True)
        # Выбрать 2 аккаунт
        Actions.Click(self, By.XPATH, "//div[.//div[2]/div[text()='Account 1']]", as_script=True)

        while True:
            try:
                # Ввести значения
                Actions.Input(self, By.XPATH, "/html/body/div[1]/div/div[3]/div/div[3]/div/div[2]/div[2]/div[1]/div/div/div[1]/input", str(rand_value / 2))
                #  "Next"
                Actions.Click(self, By.XPATH, "//button[text()='Next']", as_script=True)
                #  "Confirm"
                Actions.Click(self, By.XPATH, "//button[text()='Confirm']", as_script=True)
                break
            except:
                pass

        while True:
            try:
                Actions.Click(self, By.XPATH, "/html/body/div[1]/div/div[3]/div/div/div/div[3]/div/div/div/div/div[1]", as_script=True)
                if Actions.GetElement(self, By.XPATH, "/html/body/div[2]/div/div/section/div[2]/div/div[2]/div[1]/div[2]/div").Element.text == "Confirmed":
                    break
                Actions.Click(self, By.XPATH, "/html/body/div[2]/div/div/section/div[1]/div/button", as_script=True)
            except:
                pass
