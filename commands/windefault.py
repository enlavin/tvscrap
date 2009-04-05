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
from telnetlib import Telnet
from lib.base import BaseCommand
from optparse import OptionParser
from db import Episode, Show
from lib.torrent_downloader import TorrentCommand
import urllib2

if sys.platform != 'win32':
    class Command(TorrentCommand):
        def create_parser(self):
            parser = OptionParser(usage="windefault")
            self.parser = parser

            parser.set_defaults()
            return parser

        def check_args(self, args):
            print "Only works in Windows OS"
            return False
else:
    class Command(TorrentCommand):
        def create_parser(self):
            parser = OptionParser(usage="windefault")
            self.parser = parser

            parser.set_defaults()
            return parser

        def check_args(self, args):
            (self.options, _) = self.parser.parse_args(args)
            return True

        def _send_command(self, torrent):
            # todo: descarga el .torrent en un fichero temporal
            try:
                u = urllib2.urlopen(torrent)
                torrent_data = u.read()
            except HTTPError:
                raise TorrentURLException

            #TODO: check if the result is torrent or html
            tempname = tempfile.mktemp(suffix='.torrent')
            try:
                fout = file(tempname, "wb+")
                fout.write(torrent_data)
            finally:
                fout.close()

            import win32api
            win32api.ShellExecute(0, "open", tempname, None, ".", 0)
            # don't delete torrent file

