import sys
from base import BaseCommand
from optparse import OptionParser
from db import Show

class Command(BaseCommand):
    """Muestra las series registradas"""
    def create_parser(self):
        # 
        parser = OptionParser()
        self.parser = parser
        return parser

    def check_args(self, args):
        (options, _) = self.parser.parse_args(args)
        return True
        
    def run(self):
        shows = self.store.find(Show).order_by(Show.name)
        for show in shows:
            print "'%s' '%s' (min: %3.1f Mb, max: %3.1f Mb)" % \
                    (show.name, show.regexp_filter,
                            show.min_size, show.max_size)


