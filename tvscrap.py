from storm.locals import *
import urllib
#import hachoir_metadata
from BeautifulSoup import BeautifulSoup
import re

def parse_capitulo_eztvefnet(tr):
    data = {}

    tds = tr.findAll('td')
    a = tds[1].findAll('a')[0]
    data['name'] = a.findAll('font')[0].contents[0]
    data['url_torrent'] = [a.get('href')]
    data['url_torrent'] += [re.sub('/tor/', '/get/', link.get('href')) for link in tds[2].findAll('a')]
    data['size'] = int(tds[4].contents[0])

    return data

def parse_eztvefnet_frontpage():
    url = urllib.urlopen("http://eztvefnet.org/frontpage.php")
    #html = file("frontpage.php.html","rt").read()
    html = url.read()
    soup = BeautifulSoup(html)
    capitulos = soup.findAll('tr', attrs={'class': 'forum_header_border'})

    result = []
    for tr in capitulos:
        result.append(parse_capitulo_eztvefnet(tr))

    return result

