from selenium.webdriver.common.by import By
from Automizer.Scenario import Scenario, ScenarioResult
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
import Automizer.Actions as Actions
import URLs


class TransferGoerliToAlphaTestnet(Scenario):
    def __init__(self,
                 driver: WebDriver,
                 wait: WebDriverWait):
        super().__init__(driver, wait)

    def Exec(self, args=None):
        result: ScenarioResult = ScenarioResult()

        Actions.OpenUrl(self, URLs.Scroll_Bridge)

        res = Actions.GetElement(self, By.XPATH, "//div[1]//h6[contains(text(), 'Balance')]")
        balance = float(res.Element.text.split(' ')[1])/100

        if balance == 0.0:
            raise ValueError

        Actions.Input(self, By.ID, ":r0:", str(balance))
        res = Actions.Click(self, By.ID, ":r2:", is_opening_window=True)
        self.Active_Window = res.New_Window
        Actions.Click(self, By.XPATH, "//button[@data-testid='page-container-footer-next']")
        self.Active_Window = res.Old_Window

        while True:
            try:
                print("wait success")
                Actions.GetElement(self, By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[2]/div/table/tbody/tr[1]/td[1]/div/div[1]/span[text()='Success']")
                Actions.GetElement(self, By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[2]/div/table/tbody/tr[1]/td[1]/div/div[2]/span[text()='Success']")
                break
            except:
                pass

        return result
