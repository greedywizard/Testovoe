import time
from metamask import Metamask
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver

options = webdriver.ChromeOptions()
options.add_extension('./Extentions/metamask.crx')
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")

driver: WebDriver = webdriver.Chrome(options=options)
driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')

current_window = driver.current_window_handle

all_window_handles = driver.window_handles

for handle in all_window_handles[1:]:
    driver.switch_to.window(handle)
    driver.close()

driver.switch_to.window(all_window_handles[0])

seed_phrase: str = 'milk craft duck galaxy occur copy rich drastic also wise hair project'

mm: Metamask = Metamask(driver)

mm.open_wallet(seed_phrase)
mm.setup_wallet()
mm.add_test_networks()
mm.run()

input()

driver.quit()