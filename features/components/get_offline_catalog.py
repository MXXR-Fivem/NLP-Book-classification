import os.path

import requests


def get_offline_catalogue() -> None:
    """
    Get offline catalogue csv file, and download it if doesn't exist

    ## Parameters
        None

    ## Returns
        File path
    """

    file_path = './data/pg_catalog.csv'

    if not os.path.exists(file_path):
        response = requests.get('https://www.gutenberg.org/cache/epub/feeds/pg_catalog.csv')

        with open(file_path, 'w+', encoding='utf8') as file:
            file.write(response.text)

    return file_path
