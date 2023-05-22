from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Scenarios import *

seed_phrase: str = ''

options = webdriver.ChromeOptions()
options.add_extension('./Extentions/metamask.crx')
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")

driver: WebDriver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
wait: WebDriverWait = WebDriverWait(driver, 5)

wait.until(EC.new_window_is_opened(driver.window_handles))
current_window = driver.current_window_handle
all_window_handles = driver.window_handles
for handle in all_window_handles[1:]:
    driver.switch_to.window(handle)
    driver.close()
driver.switch_to.window(all_window_handles[0])

OpenMetamaskWallet(driver, wait).Exec({"seed": seed_phrase})
SetupMetamaskWallet(driver, wait).Exec()
ConnectScroll(driver, wait).Exec()
try:
    TransferGoerliToAlphaTestnet(driver, wait).Exec()
except ValueError:
    print('clear account')
ConnectUniswap(driver, wait).Exec()
# SwapEthToWeth(driver, wait).Exec()
# SwapWethToUsdc(driver, wait).Exec()
# AddLiquid(driver, wait)
# SwapUsdcToEth(driver, wait).Exec()
# res = DeployContract(driver, wait).Exec()
# ValidateContract().Exec(res.ResultData)
res = CreateToken(driver, wait).Exec()
res = DeployToken(driver, wait).Exec(res)
AddToken(driver, wait).Exec(res)
SwapToScrollAlpha(driver, wait).Exec()
CreateSecondAccount(driver, wait).Exec()
SendBetweenAccounts(driver, wait).Exec()


input()
driver.quit()
