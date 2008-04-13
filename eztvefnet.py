# -*- coding: utf-8 -*-
"""
eztvefnet.py

Navega por la web de eztv.it y extrae un listado de capitulos
de series con los enlaces a los ficheros .torrent que sirven
para descargarlos.
"""
import re
import urllib
import BeautifulSoup
import func

class Scrapper(object):
    """ WebScrapper para eztv.it """
    def __init__(self):
        self.url = self.file = None

    def __call__(self, url=None, file=None):
        self.url = url
        self.file = file
        return self._parse_frontpage()
    __call__ = func.retry_n(__call__, 3)

    def _parse_episode(self, trow):
        """ Extrae el nombre y los enlaces torrent para un episodio """
        data = {}

        tds = trow.findAll('td')
        link = tds[1].findAll('a')[0]
        data['name'] = unicode(link.findAll('font')[0].contents[0])
        data['url_torrent'] = [unicode(link.get('href'))]
        data['url_torrent'] += \
            [unicode(re.sub('/tor/', '/get/', link.get('href')))
                for link in tds[2].findAll('a')]
        data['size'] = float(tds[4].contents[0])

        return data

    def _parse_frontpage(self):
        """ Analiza la página principal de eztv y saca los
        capitulos para descargar """
        if self.file:
            try:
                fhtml = file(self.file, "rt")
                html = fhtml.read()
            finally:
                fhtml.close()
        else:
            if not self.url:
                self.url = "http://eztv.it/frontpage.php"
            url = urllib.urlopen(self.url)
            html = url.read()
        soup = BeautifulSoup.BeautifulSoup(html)
        capitulos = soup.findAll('tr', attrs={'class': 'forum_header_border'})

        result = []
        for trow in capitulos:
            try:
                result.append(self._parse_episode(trow))
            except:
                pass

        return result


