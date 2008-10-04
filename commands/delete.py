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
        episodes = self.store.find(Episode, Episode.show_id == show.id)

        if not show or not episodes:
            print "No se encuentra el programa %s" % self.options.show
        else:
            episodes.remove()
            self.store.remove(show)
            self.store.commit()

