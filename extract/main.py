import argparse
import logging
logging.basicConfig(level=logging.INFO)

import financial_page_objects as financial
from common import config


logger = logging.getLogger(__name__)


def _financial_scrapper(financial_site_uid):
    host = config()['financial_sites'][financial_site_uid]['url']

    logging.info(f'Beginning scraper for {host}')



if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    financial_site_choice = list(config()['financial_sites'].keys())
    parser.add_argument('financial_site',
                        help='The financial news site that you want to scrape',
                        type=str,
                        choices=financial_site_choice)

    args = parser.parse_args()
    #iniciamos nuestro scrapper
    _financial_scrapper(args.financial_site)

