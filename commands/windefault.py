# -*- coding: utf-8 -*-
import sys
from telnetlib import Telnet
from base import BaseCommand
from optparse import OptionParser
from db import Episode, Show
from torrent_downloader import TorrentCommand
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

