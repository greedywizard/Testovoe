import logging
import os
from typing import Type


class Logger:
    _instance = None
    _logger: logging.Logger = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Logger, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    @classmethod
    def Configure(cls, file_path: str = None, file_name: str = 'debug', file_ext: str = '.log'):
        cls()

        if file_path and not os.path.exists(file_path):
            os.makedirs(file_path)

        if file_path:
            _file_path: str = os.path.join(file_path, f'{file_name}{file_ext}')
        else:
            _file_path: str = f'{file_name}{file_ext}'

        if file_name in logging.Logger.manager.loggerDict:
            logging.Logger.manager.loggerDict.pop(file_name)
        logger = logging.getLogger(file_name)
        logger.setLevel(logging.INFO)

        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler(_file_path)

        c_handler.setFormatter(logging.Formatter('%(levelname)s @ %(asctime)s - %(name)s: %(message)s'))
        f_handler.setFormatter(logging.Formatter('%(levelname)s @ %(asctime)s: %(message)s'))

        logger.addHandler(c_handler)
        logger.addHandler(f_handler)

        cls._logger = logger

    @classmethod
    def Warring(cls, message: str):
        cls._logger.warning(message)

    @classmethod
    def Error(cls, message: str):
        cls._logger.error(message)

    @classmethod
    def Info(cls, message: str):
        cls._logger.info(message)

    @classmethod
    def Exception(cls, exception: Exception):
        cls._logger.exception(exception)

