import re
import urllib
from BeautifulSoup import BeautifulSoup

class Scrapper(object):
    def __call__(self):
        return self._parse_frontpage()

    def _parse_episode(self, tr):
        data = {}

        tds = tr.findAll('td')
        a = tds[1].findAll('a')[0]
        data['name'] = a.findAll('font')[0].contents[0]
        data['url_torrent'] = [a.get('href')]
        data['url_torrent'] += [re.sub('/tor/', '/get/', link.get('href')) for link in tds[2].findAll('a')]
        data['size'] = int(tds[4].contents[0])

        return data

    def _parse_frontpage(self):
        #url = urllib.urlopen("http://eztvefnet.org/frontpage.php")
        #html = url.read()
        html = file("frontpage-wed.php.html","rt").read()
        soup = BeautifulSoup(html)
        capitulos = soup.findAll('tr', attrs={'class': 'forum_header_border'})

        result = []
        for tr in capitulos:
            result.append(self._parse_episode(tr))

        return result


