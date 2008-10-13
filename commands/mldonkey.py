# -*- coding: utf-8 -*-
import sys
from telnetlib import Telnet
from base import BaseCommand
from optparse import OptionParser
from db import Episode, Show
from torrent_downloader import TorrentCommand, TorrentAuthException, TorrentURLException

class Command(TorrentCommand):
    def create_parser(self):
        parser = OptionParser(usage="mldonkey")
        self.parser = parser

        parser.add_option("-m", "--host", dest="host",
                help="hostname", metavar="HOST")
        parser.add_option("-p", "--port", dest="port", type="int",
                help="port", metavar="PORT")
        parser.add_option("-u", "--user", dest="user",
                help="user", metavar="USER")
        parser.add_option("-w", "--password", dest="passwd",
                help="password", metavar="PASSWORD")

        parser.set_defaults()
        return parser

    def check_args(self, args):
        (self.options, _) = self.parser.parse_args(args)

        self.username = self._best_value(self.options.user, "mldonkey.username", "admin")
        self.passwd = self._best_value(self.options.passwd, "mldonkey.password", "")
        self.host = self._best_value(self.options.host, "mldonkey.host", "localhost")
        self.port = self._best_value(self.options.port, "mldonkey.port", 4000)

        return True

    def _send_command(self, torrent):
        telnet = Telnet()
        telnet.open(self.host, int(self.port))
        try:
            telnet.read_until(">")
            telnet.write("auth %s %s\n" % (str(self.username), str(self.passwd)))
            telnet.read_until(">")
            telnet.write("dllink %s\n" % str(torrent))
            telnet.write("quit\n")
            session = telnet.read_all()
            #print session
            if "Bad login" in session:
                raise TorrentAuthException
            elif "exception" in session:
                raise TorrentURLException

        finally:
            telnet.close()

