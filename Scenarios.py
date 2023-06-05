from selenium.webdriver.common.by import By
import URLs
from Automizer.Enums import WindowActions
from Automizer.ExecEnvironment import ExecEnvironment
import Automizer.Actions as Actions
from Automizer.Logger import Logger


def OpenMetamaskWallet(scenario: ExecEnvironment, seed: str):
    Logger.Info("OpenMetamaskWallet()")

    Actions.OpenUrl(scenario, url=URLs.Metamask_Home)

    while True:
        try:
            Logger.Info("Try import wallet...")
            Actions.Click(scenario, By.ID, "onboarding__terms-checkbox")
            Actions.Click(scenario, By.XPATH, "//button[@data-testid='onboarding-import-wallet']")
            break
        except:
            scenario.Driver.refresh()

    Actions.Click(scenario, By.XPATH, "//button[@data-testid='metametrics-i-agree']")

    seed_arr = seed.split(' ')
    for i in range(seed_arr.__len__()):
        Actions.Input(scenario, By.ID, f"import-srp__srp-word-{i}", seed_arr[i])

    Actions.Click(scenario, By.XPATH, "//button[@data-testid='import-srp-confirm']")

    password: str = '12345678'
    Actions.Input(scenario, By.XPATH, "//input[@data-testid='create-password-new']", password)
    Actions.Input(scenario, By.XPATH, "//input[@data-testid='create-password-confirm']", password)
    Actions.Click(scenario, By.XPATH, "//input[@data-testid='create-password-terms']")
    Actions.Click(scenario, By.XPATH, "//button[@data-testid='create-password-import']")

    while True:
        try:
            Logger.Info("Try complete import...")
            # "Got it"
            Actions.Click(scenario, By.XPATH, "//button[@data-testid='onboarding-complete-done']")
            break
        except:
            pass

    Actions.Click(scenario, By.XPATH, "//button[@data-testid='pin-extension-next']")
    Actions.Click(scenario, By.XPATH, "//button[@data-testid='pin-extension-done']")


def SetupMetamaskWallet(scenario: ExecEnvironment):
    Logger.Info("SetupMetamaskWallet()")

    Actions.OpenUrl(scenario, url=URLs.Metamask_Settings_Advance)

    Actions.Click(scenario, By.XPATH, "/html/body/div[1]/div/div[3]/div/div[2]/div[2]/div[2]/div[5]/div[2]/div/label/div[1]/div[1]/div[2]")
    Actions.Click(scenario, By.XPATH, "/html/body/div[1]/div/div[3]/div/div[1]/div[1]/div[2]")
    Actions.Click(scenario, By.XPATH, "//div[@data-testid='network-display']", as_script=True)
    Actions.Click(scenario, By.XPATH, "//li[.//span[text()='Goerli test network']]", as_script=True)


def ConnectScroll(scenario: ExecEnvironment):
    Logger.Info("ConnectScroll()")

    Actions.OpenUrl(scenario, url=URLs.Scroll_Alpha)

    Actions.Click(scenario, By.XPATH, "/html/body/div/div/div[2]/div[1]/div[2]/dl/div[2]/div[2]/dd/ul/li/div[2]/a")

    result_sr = Actions.GetShadowRoot(scenario, By.XPATH, "/html/body/onboard-v2")
    r: Actions.Click = Actions.Click(scenario,
                                     By.CSS_SELECTOR,
                                     "section > div > div > div > div > div > div > div > div.scroll-container.svelte-1qwmck3 >"
                                     " div > div > div > div.wallet-button-container.svelte-1vlog3j > button > div",
                                     shadow_root=result_sr.Element,
                                     window_action=WindowActions.Open)

    Actions.Click(scenario, By.XPATH, "//button[text()='Next']")
    Actions.Click(scenario, By.XPATH, "//button[text()='Connect']", window_action=WindowActions.WaitClose)


def ConnectUniswap(scenario: ExecEnvironment):
    Logger.Info("ConnectUniswap()")

    Actions.OpenUrl(scenario, URLs.Uniswap_Swap)

    Actions.Click(scenario, By.XPATH, "//button[text()='Connect']")
    res = Actions.Click(scenario, By.ID, "metamask", window_action=WindowActions.Open)
    scenario.Active_Window = res.New_Window
    Actions.Click(scenario, By.XPATH, "//button[text()='Next']")
    Actions.Click(scenario, By.XPATH, "//button[text()='Connect']", window_action=WindowActions.WaitClose)
    scenario.Active_Window = res.Old_Window
    Actions.Click(scenario, By.XPATH, "/html/body/div[1]/div/div[1]/nav/div/div[3]/div/div[3]/div/button")
    res = Actions.Click(scenario, By.XPATH, "//button[.//div[text()='Scroll Alpha']]", window_action=WindowActions.Open)
    scenario.Active_Window = res.New_Window
    Actions.Click(scenario, By.XPATH, "//button[text()='Approve']")
    Actions.Click(scenario, By.XPATH, "//button[text()='Switch network']", window_action=WindowActions.WaitClose)
    scenario.Active_Window = res.Old_Window
