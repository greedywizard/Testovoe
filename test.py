import random

from selenium.webdriver import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver


# options = webdriver.ChromeOptions()
# options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--no-sandbox")
#
# driver: WebDriver = webdriver.Chrome(options=options)
#
# driver.get("https://scroll.io/alpha/bridge")
#
# button: WebElement = WebDriverWait(driver, 3).until(EC.visibility_of_element_located(
#         (By.XPATH, "/html/body/div/div/div[1]/div[1]/button")))
# button.click()
#
# shadow_host = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.XPATH, "/html/body/onboard-v2")))
#
# shadow_root = driver.execute_script('return arguments[0].shadowRoot', shadow_host)
# element_inside_shadow_dom = shadow_root.find_element(By.CSS_SELECTOR, "section > div > div > div > div > div > div > div > div.button-container.absolute.svelte-1qwmck3 > div")
#
# print("inner", element_inside_shadow_dom)
#
# element_inside_shadow_dom.click()
# input()
#
# driver.quit()


result = generate_half_random(target_number)
print(result)