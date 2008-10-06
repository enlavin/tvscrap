import sys
from base import BaseCommand
from optparse import OptionParser
from db import Show, Episode

class Command(BaseCommand):
    """Muestra los capitulos pendientes de descargar"""
    def create_parser(self):
        #
        parser = OptionParser()
        self.parser = parser
        return parser

    def check_args(self, args):
        (options, _) = self.parser.parse_args(args)
        return True

    def run(self):
        episodes = self.store.find(Episode, Episode.queued == False)
        if episodes.count() <= 0:
            print "No episodes pending"
            return

        for episode in episodes:
            print "%s|%s|%s|%3.1f" % \
                    (episode.name, episode.filename, episode.torrent, episode.size)


