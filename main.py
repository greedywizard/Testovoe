import concurrent.futures as cf
import os
import configparser
import sys
from typing import Type, List
import db
from Automizer.Logger import Logger
from Pipeline import Pipeline


def worker(pipe: Type[db.PipelineOptions]) -> Type[db.PipelineOptions]:
    Logger.Configure(file_name='main')
    Logger.Info(f'Wallet "{pipe.seed_phrase}" starting...')
    return Pipeline(pipe).Start()


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
                        Logger.Info(f'Wallet "{r.seed_phrase}" complete success!')
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
