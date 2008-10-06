# -*- coding: utf-8 -*-
import sys
from base import BaseCommand
from optparse import OptionParser
from db import Show, Episode

class Command(BaseCommand):
    """Muestra los capitulos registrados de una serie"""
    def create_parser(self):
        # 
        parser = OptionParser()
        parser.add_option("-s", "--show", dest="show",
                help="show list of downloaded episodes", metavar="SHOW")
        self.parser = parser
        return parser

    def check_args(self, args):
        (self.options, _) = self.parser.parse_args(args)
        return getattr(self.options, "show")
        
    def run(self):
        print "list_episodes(%s)" % self.options.show
        for epi in self.store.find(Episode,
                Episode.show_id == Show.id,
                Show.name == unicode(self.options.show)
                ).order_by(Show.name):
            print "%s|%s|%s|%3.1f" % \
                    (epi.name, epi.filename, epi.torrent, epi.size)

