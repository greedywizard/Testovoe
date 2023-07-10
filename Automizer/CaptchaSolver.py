from datetime import time
from typing import re

import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from Automizer import Actions
from Automizer.ExecEnvironment import ExecEnvironment
from Automizer.Logger import Logger


class CapthcaSolver:
    def __init__(self, key):
        self.key = key

    def solve_hcaptcha_token(self, Env: ExecEnvironment, iframe: WebElement):
        Env.Driver.switch_to.frame(iframe)
        del Env.Driver.requests
        Actions.Click(Env, By.ID, "checkbox")
        Env.Driver.switch_to.default_content()

        url = iframe.get_attribute("src")
        regex = r'sitekey=([^&]*)'
        sitekey = re.search(regex, url).group(1)

        API = 'https://api.nopecha.com/token'

        job_id = requests.post(API, json={
            'type': 'hcaptcha',
            'sitekey': sitekey,
            'url': 'https://discord.com',
            'key': self.key,
        }).json()['data']

        while True:
            res = requests.get(f'{API}?key={self.key}&id={job_id}').json()
            if 'data' in res:
                res = res['data']
                break
            Logger.Info("Try complete")
            time.sleep(5)


        Env.Driver.execute_script(f"document.querySelector('[name=\"h-captcha-response\"]').innerHTML='{res}'")
        Env.Driver.execute_script(f"document.querySelector('[name=\"g-recaptcha-response\"]').innerHTML='{res}'")
