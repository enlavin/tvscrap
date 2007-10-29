from storm.locals import *
import urllib
#import hachoir_metadata
from BeautifulSoup import BeautifulSoup
import re
from eztvefnet import Scrapper
from optparse import OptionParser

# ideas:
# + tvscrap.py --register-show="Show" --regexp="rx" [--min-size=xx] [--max-size=xx]
# + tvscrap.py --set variable --value xxx
# + tvscrap.py --get variable
# + tvscrap.py --dump-config
# + tvscrap.py --list-shows
# + tvscrap.py --list-episodes SHOW

def define_cmdline_options():
    parser = OptionParser()
    parser.add_option("-l","--list-shows", dest="listshows", action="store_true", help="")
    parser.add_option("-e","--list-episodes", dest="listepisodes", help="", metavar="SHOW")
    parser.add_option("-r","--register-show", dest="show", help="", metavar="SHOW")
    parser.add_option("-x","--regexp", dest="regexp", help="", metavar="RX")
    parser.add_option("-g","--get", dest="getvar", help="", metavar="VARIABLE")
    parser.add_option("-s","--set", dest="setvar", help="", metavar="VARIABLE")
    parser.add_option("-v","--value", dest="value", help="", metavar="VALUE")
    parser.add_option("-d","--dump-config", dest="dump", action="store_true", help="", metavar="DUMP")
    parser.add_option("-m","--min-size", dest="minsize", help="", metavar="MINSIZE")
    parser.add_option("-n","--max-size", dest="maxsize", help="", metavar="MAXSIZE")
    return parser

if __name__ == '__main__':
    #s = Scrapper()
    #res = s()
    #print res

    parser = define_cmdline_options()
    (options, args) = parser.parse_args()
    print options
    print args


