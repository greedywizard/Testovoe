from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Scenarios import *

seed_phrase: str = 'milk craft duck galaxy occur copy rich drastic also wise hair project'

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
# Добавить ликвидность
# SwapUsdcToEth(driver, wait).Exec()
# res = DeployContract(driver, wait).Exec()
# ValidateContract().Exec(res.ResultData)

# Начало
#     us.add_liquid()
#     o = oz.create_contract()
#     a = rem.deploy_token(o[0], o[1])
#     mm.add_token(a)
#     mm.swap_to_sat()
#     mm.create_sencond_account()
#     mm.send_to_2_account_and_revert()
#     pass

input()
driver.quit()
