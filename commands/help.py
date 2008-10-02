import sys
from base import BaseCommand

class Command(BaseCommand):
    def run(self, options):
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
        sys.exit(1)
