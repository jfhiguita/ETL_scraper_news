import argparse
import datetime
import csv
import logging
logging.basicConfig(level=logging.INFO)
import re

from requests.exceptions import HTTPError
from urllib3.exceptions import MaxRetryError

import news_page_objects as news
from common import config


logger = logging.getLogger(__name__)
is_well_formed_link = re.compile(r'^https?://.+/.+$')
is_root_path = re.compile(r'^/.+$')


def _financial_scrapper(financial_site_uid):
    host = config()['financial_sites'][financial_site_uid]['url']

    logging.info(f'Beginning scraper for {host}')
    logging.info('Finding links in homepage...')
    homepage = news.HomePage(financial_site_uid, host)

    articles = []
    for link in homepage.article_links:
        article = _fetch_article(financial_site_uid, host, link)

        if article:
            logger.info('Article fetched!!!')
            articles.append(article)
            break

    _save_articles(financial_site_uid, articles)


def _save_articles(financial_site_uid, articles):
    now = datetime.datetime.now().strftime('%Y_%m_%d')
    out_file_name = f'{financial_site_uid}_{now}_articles.csv'
    csv_headers = list(filter(lambda property: not property.startswith('_'), dir(articles[0])))

    with open(out_file_name, mode='w+') as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers)

        for article in articles:
            row = [str(getattr(article, prop)) for prop in csv_headers]
            writer.writerow(row)


def _fetch_article(financial_site_uid, host, link):
    logger.info(f'Start fetching article at {link}')

    article = None
    try:
        article = news.ArticlePage(financial_site_uid, _build_link(host, link))

    except (HTTPError, MaxRetryError) as e:
        logger.warning('Error while fetching the article', exc_info=False)

    if article and not article.body:
        logger.warning('Invalid article. There is no body')
        return None

    return article


def _build_link(host, link):
    if is_well_formed_link.match(link):
        return link
    elif is_root_path.match(link):
        return f'{host}{link}'
    else:
        return f'{host}/{link}'



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

