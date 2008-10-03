import sys
from base import BaseCommand
from optparse import OptionParser

class Command(BaseCommand):
    def create_parser(self):
        # [-m url|-f file]
        parser = OptionParser()
        parser.add_option("-u", "--force-url", dest="url",
                help="", metavar="URL")
        parser.add_option("-f", "--force-file", dest="file",
                help="", metavar="FILE")

        self.parser = parser
        return parser

    def run(self, options):
        pass


