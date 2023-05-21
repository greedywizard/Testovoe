from selenium.webdriver.common.by import By
from Automizer.Scenario import Scenario, ScenarioResult
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
import Automizer.Actions as Actions
import URLs


class ConnectUniswap(Scenario):
    def __init__(self,
                 driver: WebDriver,
                 wait: WebDriverWait):
        super().__init__(driver, wait)

    def Exec(self, args=None):
        result: ScenarioResult = ScenarioResult()

        Actions.OpenUrl(self, URLs.Uniswap_Swap)

        Actions.Click(self, By.XPATH, "//button[text()='Connect']")
        res = Actions.Click(self, By.ID, "metamask", is_opening_window=True)
        self.Active_Window = res.New_Window
        Actions.Click(self, By.XPATH, "//button[text()='Next']")
        Actions.Click(self, By.XPATH, "//button[text()='Connect']")
        self.Active_Window = res.Old_Window
        Actions.Click(self, By.XPATH, "/html/body/div[1]/div/div[1]/nav/div/div[3]/div/div[3]/div/button")
        res = Actions.Click(self, By.XPATH, "//button[.//div[text()='Scroll Alpha']]", is_opening_window=True)
        self.Active_Window = res.New_Window
        Actions.Click(self, By.XPATH, "//button[text()='Approve']")
        Actions.Click(self, By.XPATH, "//button[text()='Switch network']")
        self.Active_Window = res.Old_Window

        return result
