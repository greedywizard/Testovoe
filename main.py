import os
import sys
from typing import Type

from selenium import webdriver

import db
from Pipeline import Pipeline


def main():
    pipe_options: list[Type[db.PipelineOptions]] = db.GetAll()

    options = webdriver.ChromeOptions()
    options.add_extension('./Extentions/metamask.crx')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    for i in pipe_options:
        db.UpdateRecord(Pipeline(options, i).Start())


if __name__ == "__main__":
    if not os.path.exists("data.db"):
        db.CreateTable()
        sys.exit()

    main()
