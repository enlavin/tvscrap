from storm.locals import *
import urllib
#import hachoir_metadata
from BeautifulSoup import BeautifulSoup
import re
from eztvefnet import Scrapper

# ideas:
# + tvscrap.py --register-show="Show" --regexp="rx" --min-size=xx --max-size=xx
# tvscrap.ini
# [torrents]
# dir=/home/migue/download/torrents
#

if __name__ == '__main__':
    s = Scrapper()
    res = s()
    print res

