import time

from selenium.webdriver.common.by import By
import URLs
from Automizer.Enums import WindowActions
from Automizer.ExecEnvironment import ExecEnvironment
import Automizer.Actions as Actions
from Automizer.Logger import Logger


def OpenMetamaskWallet(env: ExecEnvironment, seed: str):
    time.sleep(3)
    Logger.Info("OpenMetamaskWallet()")

    Actions.OpenUrl(env, url=URLs.Metamask_Home)

    while True:
        try:
            Logger.Info("Try import wallet...")
            Actions.Click(env, By.ID, "onboarding__terms-checkbox")
            Actions.Click(env, By.XPATH, "//button[@data-testid='onboarding-import-wallet']")
            break
        except:
            env.Driver.refresh()

    Actions.Click(env, By.XPATH, "//button[@data-testid='metametrics-i-agree']")

    seed_arr = seed.split(' ')
    for i in range(seed_arr.__len__()):
        Actions.Input(env, By.ID, f"import-srp__srp-word-{i}", seed_arr[i])

    Actions.Click(env, By.XPATH, "//button[@data-testid='import-srp-confirm']")

    password: str = '12345678'
    Actions.Input(env, By.XPATH, "//input[@data-testid='create-password-new']", password)
    Actions.Input(env, By.XPATH, "//input[@data-testid='create-password-confirm']", password)
    Actions.Click(env, By.XPATH, "//input[@data-testid='create-password-terms']")
    Actions.Click(env, By.XPATH, "//button[@data-testid='create-password-import']")

    while True:
        try:
            Logger.Info("Try complete import...")
            # "Got it"
            Actions.Click(env, By.XPATH, "//button[@data-testid='onboarding-complete-done']")
            break
        except:
            pass

    Actions.Click(env, By.XPATH, "//button[@data-testid='pin-extension-next']")
    Actions.Click(env, By.XPATH, "//button[@data-testid='pin-extension-done']")

    Actions.Click(env, By.XPATH, "/html/body/div[1]/div/div[3]/div/div/div/div[1]/span/button/span", as_script=True)
    Actions.Click(env, By.XPATH, "//button[@data-testid='account-options-menu__account-details']", as_script=True)
    wallet_address = Actions.GetElement(env, By.XPATH, "/html/body/div[1]/div/span/div[1]/div/div/div/div[3]/div[2]/div/div/div").Element.text
    Actions.Click(env, By.XPATH, "/html/body/div[1]/div/span/div[1]/div/div/div/button[1]", as_script=True)
    return wallet_address


def SetupMetamaskWallet(env: ExecEnvironment):
    Logger.Info("SetupMetamaskWallet()")

    Actions.OpenUrl(env, url=URLs.Metamask_Settings_Advance)

    Actions.Click(env, By.XPATH, "/html/body/div[1]/div/div[3]/div/div[2]/div[2]/div[2]/div[5]/div[2]/div/label/div[1]/div[1]/div[2]", as_script=True)
    Actions.Click(env, By.XPATH, "/html/body/div[1]/div/div[3]/div/div[1]/div[1]/div[2]", as_script=True)
    Actions.Click(env, By.XPATH, "//div[@data-testid='network-display']", as_script=True)
    Actions.Click(env, By.XPATH, "//li[.//span[text()='Goerli test network']]", as_script=True)


def  ConnectScroll(env: ExecEnvironment):
    Logger.Info("ConnectScroll()")

    Actions.OpenUrl(env, url=URLs.Scroll_Alpha)

    Actions.Click(env, By.XPATH, "/html/body/div/div/div[2]/div[1]/div[2]/dl/div[2]/div[2]/dd/ul/li/div[2]/a")

    result_sr = Actions.GetShadowRoot(env, By.XPATH, "/html/body/onboard-v2")
    Actions.Click(env,
                  By.CSS_SELECTOR,
                  "section > div > div > div > div > div > div > div > div.scroll-container.svelte-1qwmck3 >"
                  " div > div > div > div.wallet-button-container.svelte-1vlog3j > button > div",
                  shadow_root=result_sr.Element,
                  window_action=WindowActions.Open)

    Actions.Click(env, By.XPATH, "//button[text()='Next']")
    Actions.Click(env, By.XPATH, "//button[text()='Connect']", window_action=WindowActions.WaitClose)


def UniswapUseAlpha(env: ExecEnvironment):
    if Actions.ExistElement(env, By.XPATH, "/html/body/div[1]/div/div[1]/nav/div/div[1]/div[2]/div/button"):
        Actions.Click(env, By.XPATH, "/html/body/div[1]/div/div[1]/nav/div/div[1]/div[2]/div/button")
    if Actions.ExistElement(env, By.XPATH, "/html/body/div[1]/div/div[1]/nav/div/div[3]/div/div[3]/div/button"):
        Actions.Click(env, By.XPATH, "/html/body/div[1]/div/div[1]/nav/div/div[3]/div/div[3]/div/button")

    res = Actions.Click(env, By.XPATH, "//button[.//div[text()='Scroll Alpha']]", as_script=True, window_action=WindowActions.Open)
    if res.Prev_Window != res.New_Window:
        if Actions.ExistElement(env, By.XPATH, "//button[text()='Approve']"):
            Actions.Click(env, By.XPATH, "//button[text()='Approve']")
        Actions.Click(env, By.XPATH, "//button[text()='Switch network']", window_action=WindowActions.WaitClose)


def ConnectUniswap(env: ExecEnvironment, useScroll: bool = True):
    Logger.Info("ConnectUniswap()")

    Actions.OpenUrl(env, URLs.Uniswap_Swap)

    Actions.Click(env, By.XPATH, "/html/body/div[1]/div/div[1]/nav/div/div[3]/div/span/div/button[1]")
    Actions.Click(env, By.ID, "metamask", window_action=WindowActions.Open)
    Actions.Click(env, By.XPATH, "//button[text()='Next']")
    Actions.Click(env, By.XPATH, "//button[text()='Connect']", window_action=WindowActions.WaitClose)
    Actions.WaitElementVisible(env, By.XPATH, "//div[text()='Waiting to connect']", hide=True)

    if useScroll:
        UniswapUseAlpha(env)


def ConnectGuild(env: ExecEnvironment):
    Actions.OpenUrl(env, URLs.Guild)

    Actions.Click(env, By.XPATH, "//span[text()='Connect to a wallet']")
    Actions.Click(env, By.XPATH, "//span[text()='MetaMask']", window_action=WindowActions.Open)
    Actions.Click(env, By.XPATH, "//button[text()='Next']")
    Actions.Click(env, By.XPATH, "//button[text()='Connect']", window_action=WindowActions.WaitClose)
    Actions.Click(env, By.XPATH, "//span[text()='Verify account']", window_action=WindowActions.Open)
    Actions.Click(env, By.XPATH, "//button[@data-testid='page-container-footer-next']", window_action=WindowActions.WaitClose)
