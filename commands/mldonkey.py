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
from telnetlib import Telnet
import socket
from optparse import OptionParser
from lib.torrent_downloader import TorrentCommand, TorrentAuthException,\
    TorrentURLException, TorrentServerConnectException


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
        try:
            telnet.open(self.host, int(self.port))
        except socket.error:
            raise TorrentServerConnectException

        try:
            telnet.read_until(">")
            telnet.write("auth %s %s\n" % (str(self.username), str(self.passwd)))
            telnet.read_until(">")
            telnet.write("dllink %s\n" % str(torrent))
            telnet.write("quit\n")
            session = telnet.read_all()
            if "Bad login" in session:
                raise TorrentAuthException
            elif "exception" in session:
                raise TorrentURLException
        finally:
            telnet.close()

