import sys
from base import BaseCommand
from optparse import OptionParser

class Command(BaseCommand):
    def create_parser(self):
        return OptionParser(usage="help")

    def check_args(self, args):
        (options, _) = self.parser.parse_args(args)
        return True

    def run(self):
        print """
tvscrap help
    Show this help
tvscrap register -r <show> -x <rx> [-m xx] [-n xx]
    Register a new show in DB
tvscrap shows
    Show list
tvscrap episodes <show>
    Episode list for a show
tvscrap delete -s <show> [-e <episode>]
    Delete an episode from DB
tvscrap eztv [-f file|-u url]
    Download torrents from eztv
tvscrap mldonkey [-h host] [-p port] [-u username] [-w password]
    Queue torrents in mldonkey
        """
