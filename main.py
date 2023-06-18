import concurrent.futures as cf
import os
import configparser
import sys
from typing import Type, List

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import db
from Acts import *

from Automizer.Logger import Logger
from Automizer.Pipeline import Pipeline
from Exceptions import NoGoerliBalanceException
from Objects import DObject


def worker(pipe: Type[db.PipelineOptions]) -> Type[db.PipelineOptions]:
    Logger.Configure(file_name='main')
    Logger.Info(f'Wallet "{pipe.seed_phrase}" starting...')
    # Создаем драйвер
    Logger.Configure(file_path="walletlogs/", file_name=f'{pipe.seed_phrase}')
    options = webdriver.ChromeOptions()
    options.add_extension('./Extentions/metamask.crx')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    driver: WebDriver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.set_window_size(800, 800)
    driver.implicitly_wait(1)
    wait: WebDriverWait = WebDriverWait(driver, 20)
    # Закрыть окно метамаска
    wait.until(EC.new_window_is_opened(driver.window_handles))
    all_window_handles = driver.window_handles
    for handle in all_window_handles[1:]:
        driver.switch_to.window(handle)
        driver.close()
    driver.switch_to.window(all_window_handles[0])
    # Создать пайплайн
    P = Pipeline[Type[db.PipelineOptions], DObject](driver, wait, pipe)
    # Заполнить пайплайн
    P += ConnectMetamask(TransferGoerliToAlphaTestnet.__name__)
    P += TransferGoerliToAlphaTestnet(WaitTransferGoerliToAlpha.__name__)
    P += WaitTransferGoerliToAlpha(SwapEthToWeth.__name__)
    P += SwapEthToWeth(SwapWethToUsdc.__name__)
    P += SwapWethToUsdc(AddLiquidEthUSDC.__name__)
    P += AddLiquidEthUSDC(RemoveLiquidEthUSDC.__name__)
    P += RemoveLiquidEthUSDC(SwapUsdcToEth.__name__)
    P += SwapUsdcToEth(BuildContract.__name__)
    P += BuildContract(BuildToken.__name__)
    P += BuildToken(PlayWithTokenInMetamask.__name__)
    P += PlayWithTokenInMetamask(SubscribeDiscord.__name__)
    P += SubscribeDiscord(SubscribeTwitter.__name__)
    P += SubscribeTwitter()

    P.update = lambda p: db.UpdateRecord(p)

    try:
        P.Run(DObject)
        pipe.restore_data = None
        pipe.restore_point = None
        pipe.is_complete = True
        pipe.status = "Success"
        db.UpdateRecord(pipe)
    except NoGoerliBalanceException:
        pipe.restore_data = None
        pipe.restore_point = None
        pipe.is_complete = True
        pipe.status = 'No Goerli balance'
        db.UpdateRecord(pipe)
    except Exception as e:
        Logger.Exception(e)
        Logger.Error("End task with error")
    finally:
        driver.quit()

    return pipe


def main():
    cfg = configparser.ConfigParser()
    cfg.read('config.ini')
    max_process_count = int(cfg['WORKERS']['max_count'])
    timeout = int(cfg['WORKERS']['timeout'])

    pipe_options: List[Type[db.PipelineOptions]] = db.GetAll()

    with cf.ProcessPoolExecutor(max_workers=max_process_count) as executor:
        futures: {cf.Future} = {executor.submit(worker, i) for i in pipe_options}

        while futures:
            done, not_done = cf.wait(futures, return_when=cf.FIRST_COMPLETED, timeout=timeout)

            if done:
                for future in done:
                    futures.remove(future)
                    r: Type[db.PipelineOptions] = future.result()
                    if r.is_complete:
                        Logger.Info(f'Wallet "{r.seed_phrase}" complete with status: {r.status}!')
                    else:
                        futures.add(executor.submit(worker, r))
                        Logger.Info(f'Wallet "{r.seed_phrase}" complete with error! Restarting...')

            if not_done:
                for future in not_done:
                    futures.remove(future)
                    r: Type[db.PipelineOptions] = future.result()
                    Logger.Error(f'Fatal error {r.seed_phrase}. Drop without restart.')


if __name__ == "__main__":
    Logger.Configure(file_name='main')
    if not os.path.exists("data.db"):
        db.CreateTable()
        sys.exit()

    if not os.path.exists("config.ini"):
        config = configparser.ConfigParser()
        config['WORKERS'] = {
            'max_count': '1',
            'timeout': '1200'
        }

        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    main()
