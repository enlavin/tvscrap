# -*- coding: utf-8 -*-
"""
eztvefnet.py

scraps the web https://eztv.* to extract a list of episodes and
their torrent links.
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
import requests
import bs4
from lib import func


class Scrapper(object):
    """ web scrapper for https://eztv.* """
    def __init__(self):
        self.url = self.file = None

    def __call__(self, url=None, file=None):
        self.url = url
        self.file = file
        return self._parse_frontpage()
    __call__ = func.retry_n(__call__, 3)

    def _get_size(self, title):
        rx = re.compile("\(([\d\.]+)\s+(MB|GB)\)")
        try:
            size, units = rx.findall(title)[0]
            size = float(size)
            if units == "GB":
                size = size * 1000
            return size
        except:
            return 0

    def _parse_episode(self, trow):
        """ Extract the name and torrent links for an episode """
        data = {}

        tds = trow.findAll('td')
        link = tds[1].findAll('a')[0]
        data['name'] = link.contents[0]
        data["size"] = self._get_size(link.get("title"))
        data['url_torrent'] = []
        data['url_torrent'] += \
            [re.sub('/tor/', '/get/', url.get('href'))
                for url in tds[2].findAll('a') if url.get('href')]

        return data

    def _parse_frontpage(self):
        """ Analiza la página principal de eztv y saca los
        capitulos para descargar """
        if self.file:
            try:
                fhtml = open(self.file, "rt")
                html = fhtml.read()
            finally:
                fhtml.close()
        else:
            if not self.url:
                self.url = "https://eztv.ch/"
            resp = requests.get(self.url, timeout=60, verify=False)
            if resp.status_code != 200:
                return
            html = resp.text
        soup = bs4.BeautifulSoup(html)
        capitulos = soup.findAll('tr', attrs={'class': 'forum_header_border'})

        for trow in capitulos:
            try:
                yield self._parse_episode(trow)
            except:
                pass
