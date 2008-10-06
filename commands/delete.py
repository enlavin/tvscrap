# -*- coding: utf-8 -*-
import sys
from base import BaseCommand
from optparse import OptionParser
from db import Show, Episode

class Command(BaseCommand):
    """Borra una serie y todos sus capitulos"""

    def create_parser(self):
        # 
        parser = OptionParser()
        parser.add_option("-s", "--show", dest="show",
                help="show name", metavar="SHOW")
        parser.add_option("-e", "--episode", dest="episode",
                help="episode name SxxEyy or SxEE", metavar="EPISODE")
        self.parser = parser
        return parser

    def check_args(self, args):
        (self.options, _) = self.parser.parse_args(args)
        return getattr(self.options, "show") or 
            (getattr(self.options, "show") and getattr(self.options, "episode"))
        
    def run(self):
        show = self.store.find(Show, Show.name == unicode(self.options.show)).one()
        if not show:
            print "No se encuentra el programa %s" % self.options.show
            return

        # borra un episodio
        if self.options.episode:
            episode = self.store.find(Episode,
                Episode.name == unicode(episodename),
                Show.name == unicode(showname),
                Episode.show_id == Show.id).one()
            self.store.remove(episode)
        else:
            # borra el show y sus episodios
            episodes = self.store.find(Episode, Episode.show_id == show.id)
            episodes.remove()
            self.store.remove(show)
        self.store.commit()

