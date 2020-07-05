import argparse
import logging
logging.basicConfig(level=logging.INFO)
from urllib.parse import urlparse

import pandas as pd

logger = logging.getLogger(__name__)


def main(filename):
    logger.info('Starting cleaning process')

    dataframe = _read_data(filename)
    newspaper_uid = _extract_newspaper_uid(filename)
    dataframe = _add_newspaper_uid_column(dataframe, newspaper_uid)
    dataframe = _extract_host(dataframe)

    return dataframe


def _read_data(filename):
    logger.info(f'Reading file {filename}')

    return pd.read_csv(filename)


def _extract_newspaper_uid(filename):
    logger.info('Extracting newspaper uid')
    newspaper_uid = filename.split('_')[0]

    logger.info(f'Newspaper uid detected: {newspaper_uid}')
    return newspaper_uid


def _add_newspaper_uid_column(dataframe, newspaper_uid):
    logger.info(f'Filling newspaper_uid column with {newspaper_uid}')
    dataframe['newspaper_uid'] = newspaper_uid

    return dataframe


def _extract_host(dataframe):
    logger.info('Extracting host from urls')
    dataframe['host'] = dataframe['url'].apply(lambda url: urlparse(url).netloc)

    return dataframe


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('filename',
                        help='The path to the dry data',
                        type=str)

    args = parser.parse_args()
    dataframe = main(args.filename)
    print(dataframe)
    