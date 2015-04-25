# -*- coding: utf-8 -*-
# GNU General Public Licence (GPL)
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA  02111-1307  USA
import sys
try:
    import transmissionrpc
except ImportError:
    print "TransmissionRPC support not installed. Try easy_install transmissionrpc."
    sys.exit(1)

from optparse import OptionParser
import urllib2

from lib.torrent_downloader import TorrentCommand, TorrentAuthException,\
    TorrentURLException, TorrentServerConnectException


class Command(TorrentCommand):
    def create_parser(self):
        parser = OptionParser(usage="transmission")
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

        self.username = self._best_value(self.options.user, "transmission.username", "")
        self.passwd = self._best_value(self.options.passwd, "transmission.password", "")
        self.host = self._best_value(self.options.host, "transmission.host", "localhost")
        self.port = self._best_value(self.options.port, "transmission.port", 9091)

        return True

    def _send_command(self, torrent):
        args = {"address": str(self.host), "port": int(self.port)}
        if self.username:
            args["user"] = str(self.username)
            args["password"] = str(self.passwd)
        client = transmissionrpc.Client(**args)

        try:
            client.add_uri(uri=torrent)
        except transmissionrpc.TransmissionError, e:
            ml = e.message.lower()
            if "http error" in ml:
                raise TorrentAuthException(), None, sys.exc_info()[2]
            elif "corrupt" in ml:
                raise TorrentURLException(), None, sys.exc_info()[2]
            elif "file does not exist" in ml:
                raise TorrentURLException(), None, sys.exc_info()[2]
            elif "duplicate" in ml:
                print("warning: duplicate torrent")
            else:
                raise TorrentServerConnectException(), None, sys.exc_info()[2]
        except urllib2.URLError:
                raise TorrentServerConnectException(), None, sys.exc_info()[2]
