from typing import List

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import Automizer.Scenario
from Automizer.Logger import Logger
from Scenarios import *


def mapper2(x: DeployContract.Result) -> ValidateContract.Data:
    data = ValidateContract.Data()
    data.address = x.address
    data.compile_version = x.compile_version
    return data


def mapper3(x: CreateToken.Result) -> DeployToken.Data:
    data = DeployToken.Data()
    data.name = x.name
    data.code = x.code
    return data


def mapper4(x: DeployToken.Result) -> AddToken.Data:
    data = AddToken.Data()
    data.address = x.address
    return data


def main():
    seed_phrase: str = 'milk craft duck galaxy occur copy rich drastic also wise hair project'

    Logger.Configure(file_name=f'{seed_phrase}.log')

    options = webdriver.ChromeOptions()
    options.add_extension('./Extentions/metamask.crx')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    driver: WebDriver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    wait: WebDriverWait = WebDriverWait(driver, 5)

    wait.until(EC.new_window_is_opened(driver.window_handles))
    all_window_handles = driver.window_handles
    for handle in all_window_handles[1:]:
        driver.switch_to.window(handle)
        driver.close()
    driver.switch_to.window(all_window_handles[0])

    data1 = OpenMetamaskWallet.Data()
    data1.seed = seed_phrase
    OpenMetamaskWallet(driver, wait, data1).Run()
    SetupMetamaskWallet(driver, wait).Run()
    ConnectScroll(driver, wait).Run()
    # try:
    #     TransferGoerliToAlphaTestnet(driver, wait).Run()
    # except ValueError:
    #     Logger.Info("There is no Goerli balance")
    #     print('clear account')
    # WaitTransferGoerliToAlpha(driver, wait).Run()
    ConnectUniswap(driver, wait).Run()
    # SwapEthToWeth(driver, wait).Run()
    # SwapWethToUsdc(driver, wait).Run()
    # AddLiquid(driver, wait).Run()
    # SwapUsdcToEth(driver, wait).Run()
    data2 = DeployContract(driver, wait).Run(mapper2)
    ValidateContract(driver, wait, data2).Run()
    data3 = CreateToken(driver, wait).Run(mapper3)
    data4 = DeployToken(driver, wait, data3).Run(mapper4)
    AddToken(driver, wait, data4).Run()
    SwapToScrollAlpha(driver, wait).Run()
    CreateSecondAccount(driver, wait).Run()
    # SendBetweenAccounts(driver, wait).Run()

    input()
    driver.quit()


if __name__ == "__main__":
    main()
