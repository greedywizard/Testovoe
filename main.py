import time

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from Openzeppelin import Openzeppelin
from Remix import Remix
from ScrollIo import ScrollIo
from Metamask import Metamask
from Uniswap import Uniswap
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


seed_phrase: str = 'milk craft duck galaxy occur copy rich drastic also wise hair project'

options = webdriver.ChromeOptions()
options.add_extension('./Extentions/metamask.crx')
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")

driver: WebDriver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

WebDriverWait(driver, 5).until(EC.new_window_is_opened(driver.window_handles))
current_window = driver.current_window_handle
all_window_handles = driver.window_handles
for handle in all_window_handles[1:]:
    driver.switch_to.window(handle)
    driver.close()
driver.switch_to.window(all_window_handles[0])

mm: Metamask = Metamask(driver)
sio: ScrollIo = ScrollIo(driver)
us: Uniswap = Uniswap(driver)
rem: Remix = Remix(driver)
oz: Openzeppelin = Openzeppelin(driver)

# Начало
mm.open_wallet(seed_phrase)
mm.setup_wallet()
sio.connect_metamask()
mm.add_test_networks()
goerli_balance = mm.check_balance()
print("goerli_balance:", goerli_balance)
if goerli_balance == 0.0:
    mm.clear_account()
else:
    # sio.transfer_goerli_to_alphatest(goerli_balance/10)
    # Ожидаем транзакцию
    # time.sleep(15*60)
    # us.connect_wallet()
    # balance = us.swap_eth_to_weth()
    # us.swap_weth_to_usdc()
    # us.add_liquid()
    # us.swap_usdc_to_eth()
    # deploy = rem.deploy_contract()
    # sio.validate_contract(deploy[0], deploy[1])
    # o = oz.create_contract()
    # a = rem.deploy_token(o[0], o[1])
    # mm.add_token(a)
    # mm.swap_to_sat()
    # mm.create_sencond_account()
    # mm.send_to_2_account_and_revert()
    pass

driver.quit()
