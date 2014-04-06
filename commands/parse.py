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
from optparse import OptionParser
import sys

from db import Show
from lib.base import BaseCommand
from lib.episodes import get_episode_number, InvalidEpisodeName


class Command(BaseCommand):
    """Parses a file name and return normalized data"""

    def create_parser(self):
        # -f filname [-s|-e]
        parser = OptionParser()

        parser.set_defaults(minsize=0, maxsize=0)

        parser.add_option('-f', '--filename', dest='filename',
                help='file name', metavar='FILENAME')
        parser.add_option('-s', '--show', action='store_true', default=False, dest='show',
                help='output the canonical show name', metavar='SHOW')
        parser.add_option('-e', '--episode', action='store_true', default=False, dest='episode',
                help='output the season/episode', metavar='EPISODE')

        return parser

    def check_args(self, args):
        (self.options, _) = self.parser.parse_args(args)
        self.filename = getattr(self.options, 'filename')
        self.print_show = getattr(self.options, 'show')
        self.print_episode = getattr(self.options, 'episode')

        # xor
        return self.filename and (self.print_show ^ self.print_episode)

    def run(self):
        shows = self.store.find(Show).order_by(Show.name)
        for show in shows:
            # Use a different regexp because filenames are similar, but not
            # always the same as the string used in the feed
            if show.match(self.filename, relax=True):
                if self.print_show:
                    print(show.name)
                elif self.print_episode:
                    try:
                        print(get_episode_number(self.filename))
                    except InvalidEpisodeName:
                        pass
                else:
                    pass
