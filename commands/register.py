import sys
from base import BaseCommand
from optparse import OptionParser

class Command(BaseCommand):
    def create_parser(self):
        # -r "Show" -x "rx" [-m xx] [-n xx]
        parser = OptionParser()
        parser.add_option("-r", "--register-show", dest="show",
                help="show name", metavar="SHOW")
        parser.add_option("-x", "--regexp", dest="regexp",
                help="regular expression", metavar="RX")
        parser.add_option("-m", "--min-size", dest="minsize", type="float",
                help="min size in Mb", metavar="MINSIZE")
        parser.add_option("-n", "--max-size", dest="maxsize", type="float",
                help="max size in Mb", metavar="MAXSIZE")

        self.parser = parser
        return parser

    def run(self, options):
        pass

