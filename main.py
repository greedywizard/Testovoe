from selenium import webdriver
from Pipeline import Pipeline, PipelineOptions


def main():
    seed_phrase: str = 'milk craft duck galaxy occur copy rich drastic also wise hair project'

    options = webdriver.ChromeOptions()
    options.add_extension('./Extentions/metamask.crx')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    data = PipelineOptions()
    data.seed_phrase = seed_phrase

    Pipeline(options, True, data).Start()


if __name__ == "__main__":
    main()
