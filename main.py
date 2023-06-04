import csv

from selenium import webdriver
from Pipeline import Pipeline, PipelineOptions


def main():
    pipe_options = []
    with open('accounts.csv', 'r') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            user = PipelineOptions(row['Seed'],
                                   row['DiscordLogin'],
                                   row['DiscordPass'],
                                   row['TwitterLogin'],
                                   row['TwitterPass'],
                                   row['RestorePoint'],
                                   row['RestoreData'])
            pipe_options.append(user)

    options = webdriver.ChromeOptions()
    options.add_extension('./Extentions/metamask.crx')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    Pipeline(options, True, pipe_options[0]).Start()


if __name__ == "__main__":
    main()
