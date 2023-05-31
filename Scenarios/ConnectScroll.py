from selenium.webdriver.common.by import By
from Automizer.Enums import WindowActions
from Automizer.Logger import Logger
from Automizer.Scenario import Scenario
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
import Automizer.Actions as Actions
import URLs


class ConnectScroll(Scenario):
    def __init__(self,
                 driver: WebDriver,
                 wait: WebDriverWait):
        super().__init__(driver, wait)

    def _exec(self):
        Logger.Info("ConnectScroll()")

        Actions.OpenUrl(self, url=URLs.Scroll_Alpha)

        Actions.Click(self, By.XPATH, "/html/body/div/div/div[2]/div[1]/div[2]/dl/div[2]/div[2]/dd/ul/li/div[2]/a")

        result_sr = Actions.GetShadowRoot(self, By.XPATH, "/html/body/onboard-v2")
        r: Actions.Click = Actions.Click(self,
                                         By.CSS_SELECTOR,
                                         "section > div > div > div > div > div > div > div > div.scroll-container.svelte-1qwmck3 >"
                                         " div > div > div > div.wallet-button-container.svelte-1vlog3j > button > div",
                                         shadow_root=result_sr.Element,
                                         window_action=WindowActions.Open)

        self.Active_Window = r.New_Window

        Actions.Click(self, By.XPATH, "//button[text()='Next']")
        Actions.Click(self, By.XPATH, "//button[text()='Connect']", window_action=WindowActions.WaitClose)

        self.Active_Window = r.Old_Window
