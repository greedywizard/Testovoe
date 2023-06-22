from typing import Type

from selenium.webdriver.common.by import By
import Scenarios
from Automizer.Act import Act
from Automizer.Enums import WindowActions
from Automizer.Logger import Logger
import Automizer.Actions as Actions
import URLs
from Objects import DObject
from db import PipelineOptions


class AddLiquidEthUSDC(Act[Type[PipelineOptions], DObject]):
    def __init__(self, next_act: str = None):
        super().__init__()
        self._next_act = next_act

    def _restore(self, data):
        Scenarios.OpenMetamaskWallet(self.Env, self._static_data.seed_phrase)
        Scenarios.SetupMetamaskWallet(self.Env)
        Scenarios.ConnectScroll(self.Env)
        Scenarios.ConnectUniswap(self.Env)

    def _base(self, dyna_data):
        Logger.Info("AddLiquid()")

        Actions.OpenUrl(self.Env, URLs.Uniswap_ETH_Liquid)
        self.Env.Driver.refresh()

        Actions.Click(self.Env, By.XPATH, "/html/body/div[1]/div/div[2]/div[4]/main/div[2]/div/div[1]/div/div[2]/div[1]/div/div/button")
        Actions.Input(self.Env, By.ID, "token-search-input", "Ether")
        Actions.Click(self.Env, By.XPATH, "//div[text()='Ether']")
        Actions.Click(self.Env, By.XPATH, "/html/body/div[1]/div/div[2]/div[4]/main/div[2]/div/div[1]/div/div[2]/div[3]/div/div/button")
        Actions.Input(self.Env, By.ID, "token-search-input", "0xA0D71B9877f44C744546D649147E3F1e70a93760")
        Actions.Click(self.Env, By.XPATH, "//div[text()='USD Coin']")

        try:
            # I understand
            Actions.Click(self.Env, By.XPATH, "/html/body/reach-portal[2]/div[3]/div/div/div/div/div/button[1]")
        except:
            pass

        # 0.5%
        Actions.Click(self.Env, By.XPATH, '/html/body/div[1]/div/div[2]/div[4]/main/div[2]/div/div[1]/div/div[3]/div/div[2]/button[1]')
        # Full range
        Actions.Click(self.Env, By.XPATH, '/html/body/div[1]/div/div[2]/div[4]/main/div[2]/div/div[4]/div[2]/div/div/div/div[2]/button')
        # I  understand
        Actions.Click(self.Env, By.XPATH, '/html/body/div[1]/div/div[2]/div[4]/main/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[3]/button')

        balance = Actions.GetElement(self.Env, By.XPATH, "/html/body/div[1]/div/div[2]/div[4]/main/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[2]/div", is_visible=False)\
            .Element.text.split(' ')[1]

        Actions.Input(self.Env, By.XPATH, "/html/body/div[1]/div/div[2]/div[4]/main/div[2]/div/div[2]/div/div/div[2]/div/div[1]/input", str(float(balance) * 0.70)[0:6])

        try:
            Actions.Click(self.Env, By.XPATH, "//button[text()='Approve USDC']", is_visible=False, as_script=True, window_action=WindowActions.Open)
            Actions.Click(self.Env, By.XPATH, "//button[text()='Max']")
            Actions.Click(self.Env, By.XPATH, "//button[@data-testid='page-container-footer-next']")
            Actions.Click(self.Env, By.XPATH, "//button[@data-testid='page-container-footer-next']", window_action=WindowActions.WaitClose)
        except:
            pass

        if Actions.ExistElement(self.Env, By.XPATH, "/html/body/div[1]/div/div[2]/div[4]/main/div[2]/div/div[3]/div/button"):
            Actions.Click(self.Env, By.XPATH, "/html/body/div[1]/div/div[2]/div[4]/main/div[2]/div/div[3]/div/button", is_visible=False, as_script=True)

        if Actions.ExistElement(self.Env, By.XPATH, "/html/body/div[1]/div/div[2]/div[4]/main/div[2]/div/div[4]/div[3]/div/button"):
            Actions.Click(self.Env, By.XPATH, "/html/body/div[1]/div/div[2]/div[4]/main/div[2]/div/div[4]/div[3]/div/button", is_visible=False, as_script=True)

        # Add
        Actions.Click(self.Env, By.XPATH, "/html/body/reach-portal[2]/div[3]/div/div/div/div/div[2]/button", window_action=WindowActions.Open)
        Actions.Click(self.Env, By.XPATH, "//button[@data-testid='page-container-footer-next']", window_action=WindowActions.WaitClose)

        while True:
            Logger.Info("Wait success")
            e = Actions.GetElement(self.Env, By.XPATH, "//div[text()='Success']").Element
            if e:
                break

        Actions.Click(self.Env, By.XPATH, "/html/body/reach-portal[2]/div[3]/div/div/div/div/div/div[3]/button")
