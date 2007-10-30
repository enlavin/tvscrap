from storm.locals import *
import urllib
#import hachoir_metadata
from BeautifulSoup import BeautifulSoup
import re
from eztvefnet import Scrapper
from optparse import OptionParser

from config import *

# ideas:
# + tvscrap.py --register-show="Show" --regexp="rx" [--min-size=xx] [--max-size=xx]
# + tvscrap.py --set variable --value xxx
# + tvscrap.py --get variable
# + tvscrap.py --dump-config
# + tvscrap.py --list-shows
# + tvscrap.py --list-episodes SHOW

def define_cmdline_options():
    parser = OptionParser()
    parser.add_option("-l","--list-shows", dest="listshows", action="store_true", help="show list of registered shows")
    parser.add_option("-e","--list-episodes", dest="listepisodes", help="show list of downloaded episodes", metavar="SHOW")
    parser.add_option("-r","--register-show", dest="show", help="show name", metavar="SHOW")
    parser.add_option("-x","--regexp", dest="regexp", help="regular expression", metavar="RX")
    parser.add_option("-g","--get", dest="getvar", help="", metavar="VARIABLE")
    parser.add_option("-s","--set", dest="setvar", help="", metavar="VARIABLE")
    parser.add_option("-v","--value", dest="value", help="", metavar="VALUE")
    parser.add_option("-d","--dump-config", dest="dump", action="store_true", help="", metavar="DUMP")
    parser.add_option("-m","--min-size", dest="minsize", type="float", help="min size in Mb", metavar="MINSIZE")
    parser.add_option("-n","--max-size", dest="maxsize", type="float", help="max size in Mb", metavar="MAXSIZE")
    return parser

def list_shows():
    print "list_shows()"

def list_episodes(showname):
    print "list_episodes(%s)" % showname

def register_show(showname, regexp, minsize=0, maxsize=0):
    print "register_show(%s, %s, %3.1f, %3.1f)" % (showname, regexp, minsize, maxsize)

def getvar(varname):
    print "getvar(%s)" % varname

def setvar(varname, value):
    print "setvar(%s,%s)" % (varname, value)

def dump_config():
    print "dump_config()"

def download_torrents():
    print "download_torrents()"

def check_args(options, args):
    # Dependencias
    check_args = True
    if options.show and not options.regexp:
        check_args = False
    return check_args

def main():
    
    parser = define_cmdline_options()
    (options, args) = parser.parse_args()

    if not check_args(options, args):
        parser.print_help()
        exit(1)
        
    if options.listshows:
        list_shows()
    elif options.listepisodes:
        list_episodes(options.listepisodes)
    elif options.show and options.regexp:
        register_show(options.show, options.regexp, options.minsize, options.maxsize)
    elif options.getvar:
        getvar(options.getvar)
    elif options.setvar and options.value:
        setvar(options.setvar, options.value)
    elif options.dump:
        dump_config()
    else:
        download_torrents()

if __name__ == '__main__':
    main()

