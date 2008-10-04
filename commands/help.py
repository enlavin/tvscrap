import sys
from base import BaseCommand
from optparse import OptionParser

class Command(BaseCommand):
    def create_parser(self):
        return OptionParser()

    def check_args(self, args):
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
tvscrap delete <show> <episode>
    Delete an episode from DB
tvscrap eztv [-f file|-u url]
    Enqueue torrents from eztv
        """
