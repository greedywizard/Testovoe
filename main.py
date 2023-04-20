import time
from metamask import Metamask
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_extension('./Extentions/metamask.crx')

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

input()

driver.quit()