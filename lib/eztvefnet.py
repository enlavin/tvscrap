# -*- coding: utf-8 -*-
"""
eztvefnet.py

Navega por la web de eztv.it y extrae un listado de capitulos
de series con los enlaces a los ficheros .torrent que sirven
para descargarlos.
"""
# GNU General Public Licence (GPL)
# 
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA  02111-1307  USA
import re
import urllib
import BeautifulSoup
import func

class Scrapper(object):
    """ WebScrapper for eztv.it """
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


