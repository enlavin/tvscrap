import re
import urllib
from BeautifulSoup import BeautifulSoup
import func

class Scrapper(object):
    def __call__(self, url=None, file=None):
        self.url = url
        self.file = file
        return self._parse_frontpage()
    __call__ = func.retry_n(__call__, 3)

    def _parse_episode(self, tr):
        data = {}

        tds = tr.findAll('td')
        a = tds[1].findAll('a')[0]
        data['name'] = unicode(a.findAll('font')[0].contents[0])
        data['url_torrent'] = [unicode(a.get('href'))]
        data['url_torrent'] += [unicode(re.sub('/tor/', '/get/', link.get('href'))) for link in tds[2].findAll('a')]
        data['size'] = float(tds[4].contents[0])

        return data

    def _parse_frontpage(self):
        if self.file:
            try:
                f = file(self.file, "rt")
                html = f.read()
            finally:
                f.close()
        else:
            if not self.url:
                self.url = "http://eztv.it/frontpage.php"
            url = urllib.urlopen(self.url)
            html = url.read()
        soup = BeautifulSoup(html)
        capitulos = soup.findAll('tr', attrs={'class': 'forum_header_border'})

        result = []
        for tr in capitulos:
            try:
                result.append(self._parse_episode(tr))
            except:
                pass

        return result


