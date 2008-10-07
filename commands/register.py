# -*- coding: utf-8 -*-
import sys
from base import BaseCommand
from optparse import OptionParser
from db import Show

class Command(BaseCommand):
    """Registra una nueva serie en la BD"""

    def create_parser(self):
        # -r "Show" -x "rx" [-m xx] [-n xx]
        parser = OptionParser()
        
        parser.set_defaults(minsize=0, maxsize=0)

        parser.add_option("-s", "--show", dest="show",
                help="show name", metavar="SHOW")
        parser.add_option("-x", "--regexp", dest="regexp",
                help="regular expression", metavar="RX")
        parser.add_option("-m", "--min-size", dest="minsize", type="float",
                help="min size in Mb", metavar="MINSIZE")
        parser.add_option("-n", "--max-size", dest="maxsize", type="float",
                help="max size in Mb", metavar="MAXSIZE")

        return parser

    def check_args(self, args):
        (self.options, _) = self.parser.parse_args(args)
        args_present = getattr(self.options,'regexp') and getattr(self.options, 'show')
        minmax_ok = getattr(self.options, 'minsize') <= getattr(self.options, 'maxsize')
        return args_present and minmax_ok
        
    def run(self):
        show = self.store.find(Show, Show.name == unicode(self.options.show)).one()
        if not show:
            show = Show()

        show.name = unicode(self.options.show)
        show.regexp_filter = unicode(self.options.regexp)
        show.min_size = self.options.minsize
        show.max_size = self.options.maxsize
        self.store.add(show)
        self.store.commit()
        print "%s registrado con exito" % self.options.show


