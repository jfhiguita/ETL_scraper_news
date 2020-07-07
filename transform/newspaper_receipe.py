import argparse
import hashlib
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
    dataframe = _fill_missing_titles(dataframe)
    dataframe = _fill_missing_summary(dataframe)
    dataframe = _generate_uids_for_rows(dataframe)
    dataframe = _clean_body(dataframe)
    dataframe = _remove_duplicate_entries(dataframe, 'title')
    dataframe = _drop_rows_with_missing_values(dataframe)
    _save_data(dataframe, filename)

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


def _fill_missing_titles(dataframe):
    logger.info('Filling missing titles')
    missing_titles_mask = dataframe['title'].isna()

    missing_titles = (dataframe[missing_titles_mask]['url']
                        .str.extract(r'(?P<missing_titles>[^/]+)$')
                        .applymap(lambda title: title.split('-'))
                        .applymap(lambda title_word_list: ' '.join(title_word_list))
                        )
    dataframe.loc[missing_titles_mask, 'title'] = missing_titles.loc[:, 'missing_titles']

    return dataframe


def _fill_missing_summary(dataframe):
    logger.info('Filling missing summary')
    missing_summary_mask = dataframe['summary'].isna()

    missing_summary = 'Lea:'
    dataframe.loc[missing_summary_mask, 'summary'] = missing_summary

    return dataframe


def _generate_uids_for_rows(dataframe):
    logger.info('Generating uids for each row')
    uids = (dataframe
            .apply(lambda row: hashlib.md5(bytes(row['url'].encode())), axis=1)
            .apply(lambda hash_object: hash_object.hexdigest())
            )
    dataframe['uid'] = uids

    return dataframe.set_index('uid')


def _clean_body(dataframe):
    logger.info('Cleaning body for each row')
    striped_body = (dataframe
                    .apply(lambda row: row['body'], axis=1)
                    .apply(lambda letters: list(map(lambda letter: letter.replace('\n', ''), letters)))
                    .apply(lambda letters: list(map(lambda letter: letter.replace('\r', ''), letters)))
                    .apply(lambda letters: list(map(lambda letter: letter.replace("'", ""), letters)))
                    .apply(lambda letters: list(map(lambda letter: letter.replace('[', ''), letters)))
                    .apply(lambda letters: list(map(lambda letter: letter.replace(']', ''), letters)))
                    .apply(lambda letters: list(map(lambda letter: letter.replace(',', ''), letters)))
                    .apply(lambda letters: ''.join(letters))
                    )

    dataframe['body'] = striped_body

    return dataframe


def _remove_duplicate_entries(dataframe, column_name):
    logger.info('Removing duplicate entries')
    dataframe.drop_duplicates(subset=[column_name], keep='last', inplace=True)

    return dataframe


def _drop_rows_with_missing_values(dataframe):
    logger.info('Dropping rows with missing values')

    return dataframe.dropna()


def _save_data(dataframe, filename):
    clean_filename = f'clean_{filename}'
    logger.info(f'Saving data at location: {clean_filename}')
    dataframe.to_csv(clean_filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('filename',
                        help='The path to the dry data',
                        type=str)

    args = parser.parse_args()
    dataframe = main(args.filename)
    print(dataframe)
