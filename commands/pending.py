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
from lib.base import BaseCommand
from optparse import OptionParser


class Command(BaseCommand):
    """shows the episodes not yet queued"""
    def create_parser(self):
        parser = OptionParser()
        self.parser = parser
        return parser

    def check_args(self, args):
        (options, _) = self.parser.parse_args(args)
        return True

    def run(self):
        episodes = list(self.store.episodes_not_queued())
        if len(episodes) <= 0:
            print("No episodes pending")
            return

        for episode in episodes:
            print("{}|{}|{}|{:3.1f}".format(
                episode.name, episode.filename, episode.torrent, episode.size))


