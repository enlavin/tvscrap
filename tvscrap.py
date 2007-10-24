from storm.locals import *
import urllib
#import hachoir_metadata
from BeautifulSoup import BeautifulSoup
import re
from eztvefnet import Scrapper

if __name__ == '__main__':
    s = Scrapper()
    res = s()
    print res

