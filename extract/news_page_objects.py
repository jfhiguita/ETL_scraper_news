import requests
import lxml.html as html

from common import config

class NewsPage:
    #configuracion 
    def __init__(self, financial_site_uid, url):
        self._config = config()['financial_sites'][financial_site_uid]
        self._queries = self._config['queries']
        self._parsed = None
        self._url = url

        self._visit(url)

    #obtener informacion del documento que acabamos de parsear segun el query
    def _select(self, query_string):
        return self._parsed.xpath(query_string)

    #visitar la pagina
    def _visit(self, url):
        response = requests.get(url)
        response.raise_for_status()
        home = response.content.decode('UTF-8')
        self._parsed = html.fromstring(home)


class HomePage(NewsPage):

    def __init__(self, financial_site_uid, url):
        super().__init__(financial_site_uid, url)

    @property
    def article_links(self):
        link_list = []
        for link in self._select(self._queries['homepage_article_links']):
            if link:
                link_list.append(link)

        return set(link for link in link_list)


class ArticlePage(NewsPage):

    def __init__(self, financial_site_uid, url):
        super().__init__(financial_site_uid, url)

    @property
    def body(self):
        result = self._select(self._queries['article_body'])
        return result if len(result) else ''

    @property
    def title(self):
        result = self._select(self._queries['article_title'])
        return result[0] if len(result) else ''

    @property
    def summary(self):
        result = self._select(self._queries['article_summary'])
        return result[0] if len(result) else ''

    @property
    def url(self):
        result = self._url
        return result if len(result) else ''

