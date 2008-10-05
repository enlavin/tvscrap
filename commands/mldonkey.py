import sys
from base import BaseCommand
from optparse import OptionParser
from telnetlib import Telnet

class Command(BaseCommand):
    def create_parser(self):
        parser = OptionParser(usage="mldonkey")
        self.parser = parser

        parser.set_defaults(host='localhost', port=4000, user="admin", passwd="")
        parser.add_option("-h", "--host", dest="host",
                help="hostname", metavar="HOST")
        parser.add_option("-p", "--port", dest="port", type="integer",
                help="port", metavar="PORT")
        parser.add_option("-u", "--user", dest="user",
                help="user", metavar="USER")
        parser.add_option("-w", "--password", dest="passwd",
                help="password", metavar="PASSWORD")
        return parser

    def check_args(self, args):
        (self.options, _) = self.parser.parse_args(args)
        return True

    def _send_command(self, torrent_file):
        telnet = Telnet()
        telnet.open(self.options.hostname, self.options.port)
        telnet.read_until(">")
        telnet.write("auth %s %s\n" % (self.options.user, self.options.passwd))
        telnet.read_until(">")
        telnet.write("dllink %s\n" % torrent_file)
        telnet.read_until(">")
        telnet.write("quit\n")
        telnet.read_all()

    def run(self):
        episodes = self.store.find(Episode, Episode.queued == False)
        if not episodes:
            return

        for episode in episodes:
            print "Downloading %s" % episode.torrent
            self._send_command(episode.filename)
            episode.queued = True
            self.store.commit()

